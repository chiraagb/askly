from celery import shared_task, current_task
from langchain.document_loaders import PyPDFLoader
from common.qdrant.qdrant_lib import QdrantHelper
import os
import traceback
from openai import OpenAI, AsyncOpenAI
from chat.models import Assistant, AssitantVectorStore, Session, Thread, AssistantFile
from config.settings import DEFAULT_OPENAI_MODEL
import shutil


PDF_STATUS_STARTED = "STARTING"
PDF_STATUS_LOADING = "LOADING"
PDF_STATUS_ANALYZING = "ANALYZING"
PDF_STATUS_SUMMARIZING = "SUMMARIZING"
PDF_STATUS_FAILED = "FAILED"
PDF_STATUS_SUCCESS = "SUCCESS"



client = OpenAI()



@shared_task
def updated_upload_pdf(pdf_path, pdf_name, organization_id, user_id, assistant_file_id, local_folder):
    try:

        current_task.update_state(state=PDF_STATUS_LOADING)

        vectorestore: AssitantVectorStore = (
            AssitantVectorStore.objects.create_with_openai_vectorstore(
                name=pdf_name, pdf_path=pdf_path, organization_id=organization_id
            )
        )

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Any question regarding this pdf should be answered from the pdf",
                }
            ],
            tool_resources={
                "file_search": {"vector_store_ids": [vectorestore.vector_store_id]}
            },
        )
        current_task.update_state(state=PDF_STATUS_ANALYZING)

        assistant_file = AssistantFile.objects.get(id=assistant_file_id)
        assistant_file.vectorstore = vectorestore
        assistant_file.save()

        session = Session.objects.create(
            user_id=user_id, name=pdf_name, vectorstore=vectorestore
        )
        thread = Thread.objects.create(session=session, thread_id=thread.id)

        return {"session_id": session.id , "file":assistant_file.file.url}

    except Exception as e:
        print(e)
        print(traceback.print_exc())
        current_task.update_state(
            state=PDF_STATUS_FAILED, meta={"error_message": str(e)}
        )
        return PDF_STATUS_FAILED
    
    finally:
        if os.path.exists(local_folder):
            shutil.rmtree(local_folder)


@shared_task
def upload_pdf(pdf_path, pdf_name, organization_id):
    try:

        current_task.update_state(state=PDF_STATUS_LOADING)

        org_assistant = Assistant.objects.filter(organization_id=organization_id).last()

        vectorestore = AssitantVectorStore.objects.create_with_openai_vectorstore(
            name=pdf_name, pdf_path=pdf_path, organization_id=organization_id
        )

        if not org_assistant:

            org_assistant: Assistant = Assistant.objects.create_with_assistant(
                name=f"Assistant-{organization_id}",
                model=DEFAULT_OPENAI_MODEL,
                instructions=""" 
                    You are Pdf Retriver, enhanced with the capability to retrieve information directly from User PDF document. 
                    Your task is to assist users by extracting precise information from these documents using a Retriever-Augmented Generation (RAG) approach.
                    When a user asks a question, you first identify relevant PDFs , retrieve key excerpts that pertain to the query, and 
                    then synthesize this information into a coherent and informative response. 
                    Your goal is to provide accurate, detailed answers based on the content of the PDF, effectively bridging the gap between vast data repositories and user needs.
                """,
                organization_id=organization_id,
            )

        else:

            existing_vectorstore = AssitantVectorStore.objects.filter(
                assistant=org_assistant
            ).delete()

            org_assistant.update_with_assistant(
                assistant_id=org_assistant.assistant_id, vectorstore=vectorestore
            )

    except Exception as e:
        print(e)
        print(traceback.print_exc())
        current_task.update_state(
            state=PDF_STATUS_FAILED, meta={"error_message": str(e)}
        )
        return PDF_STATUS_FAILED
    
    
