from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
import asyncio
from django.contrib.auth import get_user_model
from openai import OpenAI, AsyncOpenAI
from accounts.models import User as UserModel
from common.assistants.assistant import AIAssistant
from .models import SessionChatHistory, Session, Assistant, AssitantVectorStore, AssistantFile
import asyncio
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI, AsyncOpenAI
import os
from common.prompts.bid_summary import bid_summary_prompt


User = get_user_model()


class ChatAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_active = True

    async def connect(self):
        self.user = self.scope["user"]
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]


        print(self.session_id, os.getenv("OPENAI_API_KEY"))

        if self.user.is_authenticated and self.session_id:
            try:
                self.client = AsyncOpenAI()

                self.session = await database_sync_to_async(Session.objects.get)(
                    user=self.user, id=self.session_id
                )

                self.thread_id = await self.get_thread_id(self.session)

                print(os.getenv("PDF_ASSISTANT_ID"), "thread id")

                self.assistant = AIAssistant(
                    assistant_id=os.environ["PDF_ASSISTANT_ID"],
                    thread_id=self.thread_id,
                )

            except Exception as e:
                print(e)
                await self.close()
            else:
                await self.accept()
        else:
            await self.close(401)

    @database_sync_to_async
    def get_thread_id(self, session):
        return session.thread.thread_id

    @database_sync_to_async
    def get_pdf_source(self, session):
        assistant_file = AssistantFile.objects.filter(vectorstore = session.vectorstore).last()
        return assistant_file.file.name

    async def receive_json(self, content, **kwargs):
        if "stop_response" in content and content["stop_response"] == "stop":
            print("called stopping")
            # Send a stop message to itself via the channel layer
            await self.channel_layer.send(self.channel_name, {"type": "stop_streaming"})
            return
        
        elif "command" in content and content["command"] == "summarize":
            await self.channel_layer.send(self.channel_name, {"type": "summarize"})
            return 

        elif content["client_message"] == "/summarize":
            self.stream_active = True
            # await self.channel_layer.send(self.channel_name, {"type": "summarize", "command": "/summarize"})
            asyncio.create_task(self.summarize())
            return 

        else:
            self.stream_active = True
            asyncio.create_task(self.handle_stream(content["client_message"]))

    async def send_stream(self, generator):
        response_chat = ""
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_event_loop()

        try:
            while self.stream_active:
                response = await loop.run_in_executor(executor, next, generator, None)
                if response is None:
                    break
                else:
                    await self.send_json({"response": response, "is_complete": False})
                    
                    response_chat += response

            await self.send_json({"is_complete": True,"response":""})

        finally:
            executor.shutdown()
            await database_sync_to_async(SessionChatHistory.objects.create)(
                session=self.session, is_user_message=False, message=response_chat
            )


    async def handle_stream(self, client_message):
        await database_sync_to_async(SessionChatHistory.objects.create)(
            session=self.session, is_user_message=True, message=client_message
        )
        response_chat = ""
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_event_loop()

        generator = self.assistant.run_and_stream(client_message)

        

        try:
            while self.stream_active:
                response = await loop.run_in_executor(executor, next, generator, None)
                if response is None:
                    break
                else:
                    await self.send_json({"response": response, "is_complete": False})
                    
                    response_chat += response

            # pdf_source = await self.get_pdf_source(self.session)

            await self.send_json({"is_complete": True,"response":""})

        finally:
            executor.shutdown()
            await database_sync_to_async(SessionChatHistory.objects.create)(
                session=self.session, is_user_message=False, message=response_chat
            )

    async def stop_streaming(self, event):
        print("stoping..")
        try:

            await self.client.beta.threads.runs.cancel(
                run_id=self.assistant.run, thread_id=self.assistant.thread_id
            )

        except Exception as e:
            print(e)

        self.stream_active = False

    async def summarize(self):
        try:
            await database_sync_to_async(SessionChatHistory.objects.create)(
            session=self.session, is_user_message=True, message="/summarize"
            )
            print("here")
            client_message = f"""
            {bid_summary_prompt}
            """
            generator = self.assistant.run_and_stream(client_message)
            
            await self.send_stream(generator)

        except Exception as e:
            print(e)

    async def disconnect(self, code):
        print("Disconnected with code:", code)
        self.stream_active = False
        await self.close()


class ChatSyncJsonWebsocketConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.user: UserModel = self.scope["user"]
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]

        print(self.session_id, self.user.is_authenticated)

        if self.user.is_authenticated and self.session_id:
            try:

                self.session = Session.objects.get(user=self.user, id=self.session_id)
                self.assistant = AIAssistant(
                    assistant_id="asst_yiI6vJ98ycu8I6tsP7C2DhXz",
                    thread_id=self.session.thread_id,
                )

            except Exception as e:
                print("here")
                self.close()
            self.accept()
        else:
            print("here2")
            self.close(401)

    def receive_json(self, content, **kwargs):
        print("message recieved from client")
        print(content)
        client_message = content["client_message"]

        SessionChatHistory.objects.create(
            session=self.session, is_user_message=True, message=client_message
        )

        reponse_chat = """
        """
        for i in self.assistant.run_and_stream(client_message):
            print(i)
            self.send_json({"response": i})
            reponse_chat += i

        SessionChatHistory.objects.create(
            session=self.session, is_user_message=False, message=reponse_chat
        )

    async def disconnect(self, code):
        print("disconnected", code)

    async def get_user(self):
        user_model = get_user_model()
        return await database_sync_to_async(get_user_model().objects.first)()
