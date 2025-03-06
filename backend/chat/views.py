from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework import status

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from openai import OpenAI
from openai import NotFoundError

from config.settings import DEFAULT_OPENAI_MODEL
import time
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import Optional, Type

from common.assistants.custom_tools import claude_summarize_pdf2

# from common.assistants.assistants import SnowmanAgent
from accounts.models import Documents, OrganizationFile, Organization
from langchain_core.agents import AgentFinish
from django.http import FileResponse
from md2pdf.core import md2pdf
from accounts.models import User as UserModel
from common.assistants.assistant import AIAssistant
from .models import SessionChatHistory, Session, PdfDetail, Assistant, AssistantFile
from pdf2docx import parse
from django.shortcuts import get_object_or_404
from .serializers import SessionChatsSerailzer, SessionSerializer
from common.tasks import upload_pdf, updated_upload_pdf
from celery.result import AsyncResult
import traceback
from common.tasks import PDF_STATUS_SUCCESS,PDF_STATUS_STARTED
import tempfile
from django.utils.text import slugify
from django.core.files.storage import default_storage
from config.settings import MEDIA_ROOT, DEFAULT_TEMP_UPLOAD_FILE_STORAGE
import random

User = get_user_model()


class TextToPdf(APIView):

    def get(self, request, format=None):
        markdown_content = request.query_params.get("markdown_content")
        print(markdown_content, "mr")
        pdf_file_path = f"test-{request.user.id}.pdf"
        docx_file_path = f"test-{request.user.id}.docx"

        md2pdf(pdf_file_path, markdown_content)
        # Check if the file exists
        if os.path.exists(pdf_file_path):
            # Directly create a FileResponse without using 'with'

            parse(pdf_file_path, docx_file_path)

            response = FileResponse(
                open(docx_file_path, "rb"), content_type="application/vnd.ms-word"
            )
            # Set the content disposition to attachment to force download
            response["Content-Disposition"] = (
                'attachment; filename="your_docx_file.docx"'
            )

        os.remove(pdf_file_path)
        os.remove(docx_file_path)

        return response


class SessionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        session = Session.objects.create(
            user=user, name="some chat", thread_id=AIAssistant.create_thread().id
        )

        return Response({"id": session.id}, status=status.HTTP_200_OK)

    def get(self, request, pk=None, format=None):
        user = request.user
        if pk:
            session = get_object_or_404(Session, id=pk)
            return Response({"name": session.name, "id": session.id})

        user_sessions = Session.objects.filter(user=user).order_by("-updated_at")

        seralizer = SessionSerializer(user_sessions, many=True, context={'request': request})

        return Response(seralizer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        data = request.data
        session = get_object_or_404(Session, id=pk, user=request.user)

        if data.get("name"):
            session.name = data["name"]
            session.save()

        serializer = SessionSerializer(session)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        session = get_object_or_404(Session, id=pk, user=request.user)
        session_id = session.id

        session.delete()

        return Response(
            {"msg": f"session with id {session_id} deleted"}, status=status.HTTP_200_OK
        )


class SessionChatsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id, format=None):
        user = request.user

        session_chats = SessionChatHistory.objects.filter(session_id=session_id).order_by("created_at")

        serializer = SessionChatsSerailzer(session_chats, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Summary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id, format=None):

        session = get_object_or_404(Session, id=session_id)
        chat_history = session.chat_history.all()[:2]
        if len(chat_history) < 2:
            return Response(
                {"msg": "need atleast 2 conversation"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # print(chat_history)
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize below conversation between bot and user and repond with 4-5 words of summary",
                },
                {
                    "role": "user",
                    "content": f"""
                    summarize below conversation:

                    user: {chat_history[0].message}
                    bot: {chat_history[1].message}
                """,
                },
            ],
        )
        session.name = response.choices[0].message.content
        session.save()

        print(response.choices[0].message.content, "response")
        return Response(
            {"msg": response.choices[0].message.content}, status=status.HTTP_200_OK
        )


class PDFUploadStatus(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pdf_key, format=None):
        result = AsyncResult(str(pdf_key))
        print(result.result, result.status)
        if result.status == PDF_STATUS_SUCCESS:
            assitant_file = AssistantFile.objects.filter(id=pdf_key).last()
            session = Session.objects.filter(
                user=request.user, vectorstore=assitant_file.vectorstore
            ).last()
            
            return Response(
                {
                    "msg": result.result,
                    "status": result.status,
                    "session_id": session.id,
                    "file":assitant_file.file.url
                }
            )

        return Response({"msg": result.result, "status": result.status})


class FetchSession(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pdf_key, format=None):

        assitant_file = AssistantFile.objects.filter(id=pdf_key).last()

        session = get_object_or_404(
            Session, user=request.user, vectorstore=assitant_file.vectorstore
        )

        return Response({"session_id": session.id})


class UploadPDFView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def save_user_uploaded_file(uploaded_file, directory='uploads/'):
        """
        Save an uploaded file to a local directory.

        Parameters:
        - uploaded_file: The file uploaded by the user via a form or API.
        - directory: The local directory where the file should be saved.
        """
        # Create the directory if it doesn't exist

        os.makedirs(directory, exist_ok=True)


        # Create a safe filename using slugify and avoid conflicts
        safe_filename = slugify(uploaded_file.name)
        destination_path = os.path.join(directory,random.randint(0,10000), safe_filename)

        # Write the uploaded file data to the local destination
        with open(destination_path, 'wb+') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)

        return destination_path

    def post(self, request, format=None):

        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES["file"]

        if not file.name.endswith(".pdf"):
            return Response(
                {"error": "File format not supported."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            
            random_dir = str(random.randint(0,100000))
            local_folder = os.path.join(DEFAULT_TEMP_UPLOAD_FILE_STORAGE, random_dir)
            os.makedirs(local_folder, exist_ok=True)

            file_path = os.path.join(local_folder,file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            org_file = AssistantFile.objects.create(
                name=file.name, organization=request.user.organization, file=file
            )
            print(org_file.file.url)

            updated_upload_pdf.apply_async(
                args=[
                    file_path,
                    file.name,
                    request.user.organization_id,
                    request.user.id,
                    org_file.id,
                    local_folder
                ],
                task_id=str(org_file.id),
            )
            return Response(
                {"message": "File being processed ...", "pdf_key": org_file.id,"status": PDF_STATUS_STARTED},
                status=status.HTTP_200_OK,
                
            )

        except Exception as e:
            print(traceback.print_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
