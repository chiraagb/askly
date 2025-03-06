# help
from openai.resources.beta import Assistants, Threads
import warnings
from openai import OpenAI
import time
from typing import Optional, List
from config.settings import DEFAULT_OPENAI_MODEL
from django.core.cache import cache
from django.contrib.auth import get_user_model
from langchain.tools.render import format_tool_to_openai_function
from .assistant_tools import get_temperature, get_contact_card
from langchain.tools import tool
from openai.types.beta import assistant_update_params, Assistant
from openai.types.beta.threads import MessageContentText
import json


User = get_user_model()


class AssistantHelper:
    def __init__(
        self,
        assistant_id: str,
        thread_id: str = None,
        thread: Threads = None,
        assistant: Assistants = None,
        langchain_tools: List[tool] = None,
    ) -> None:
        self.client = OpenAI()
        self.assistant_id = assistant_id
        self.assistant = assistant
        self.model = DEFAULT_OPENAI_MODEL
        self.thread_id = thread_id
        self.thread = thread
        self.instructions = None
        self.langchain_tools = langchain_tools
        self.tools = None
        self.langchain_tools_dict = None

        # cache
        self.cache = None
        self.cache_time_out = 3600 * 2 * 24

        if self.thread is not None and self.thread_id is None:
            self.thread_id = thread_id

        if self.instructions is None:
            self.instructions = """
                                You are assistant. 
                                """
        if self.langchain_tools:
            self.tools = [
                format_tool_to_openai_function(tool) for tool in langchain_tools
            ]
            self.langchain_tools_dict = {
                tool.name: tool for tool in self.langchain_tools
            }

    @staticmethod
    def update_assistant(
        assistant_id,
        tools: List[assistant_update_params.Tool] = None,
        langchain_tools: List[tool] = None,
        client: OpenAI = OpenAI(),
    ) -> Assistant:
        dynamic_args = {}
        if langchain_tools:
            dynamic_args["tools"] = [
                {"type": "function", "function": format_tool_to_openai_function(tool)}
                for tool in langchain_tools
            ] + [{"type": "code_interpreter"}]
        if tools:
            dynamic_args["tools"] = tools

        assistant = client.beta.assistants.update(
            assistant_id=assistant_id, **dynamic_args
        )
        return assistant

    @staticmethod
    def create_thread(client: OpenAI = None) -> Threads:
        if client is None:
            client = OpenAI()

        thread = client.beta.threads.create()
        return thread

    @staticmethod
    def retrieve_thread(thread_id: str, client: OpenAI = None) -> Threads:
        if client is None:
            client = OpenAI()
        thread = client.beta.threads.retrieve(thread_id=thread_id)
        return thread

    @staticmethod
    def retrieve_clean_messages(
        thread_id: str, client: OpenAI = OpenAI()
    ) -> List[dict]:
        messages_obj = client.beta.threads.messages.list(thread_id=thread_id)
        messages = [
            {"content": obj.content[0].text.value, "role": obj.role}
            for obj in messages_obj.data
        ]
        return messages

    @staticmethod
    def create_assistant(
        model: str,
        client: OpenAI,
        file_ids: List[str] = None,
        description: str = None,
        instructions: str = None,
    ) -> Assistants:
        warnings.warn(f"creating assistant with model {model}")
        dynamic_args = {}
        if description:
            dynamic_args["description"] = description
        if instructions:
            dynamic_args["instructions"] = instructions

        assistant = client.beta.assistants.create(
            client=client, model=model, **dynamic_args
        )

        return assistant

    @staticmethod
    def retrieve_assistant(assistant_id: str, client: OpenAI = None) -> Assistants:
        if client is None:
            client = OpenAI()
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
        return assistant

    @staticmethod
    def retrieve_messages(
        thread_id: str, client: OpenAI = None
    ) -> List[MessageContentText]:
        if client is None:
            client = OpenAI()

        messages = client.beta.threads.messages.list(thread_id=thread_id).data
        return messages

    def set_thread(self) -> Threads:
        try:
            if not self.thread_id and not self.thread:
                self.thread = self.client.beta.threads.create()
                self.thread_id = self.thread.id
            elif not self.thread:
                self.thread = self.retrieve_thread(self.thread_id)

        except Exception as e:
            print(e)
            self.thread = self.client.beta.threads.create()

        return self.thread

    def add_message_to_thread(
        self, thread: Threads, user_question: str, client: OpenAI = None
    ):
        if client is None:
            client = OpenAI()
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=user_question
        )
        return message

    def run(self, message: str) -> str:

        self.add_message_to_thread(
            thread=self.thread, user_question=message, client=self.client
        )

        run_obj = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )

        max_iterations = 200
        iterations = 0

        while iterations < max_iterations:
            response = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run_obj.id
            )
            if response.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                message_content = messages.data[0].content[0].text.value
                return message_content

            elif response.status == "in_progress":
                print("progressing...")
                time.sleep(1)
                iterations += 1

            elif response.status == "requires_action":
                print("requires action..")
                tool_calls = response.required_action.submit_tool_outputs.tool_calls
                tool_results = []
                for tool in tool_calls:
                    langchain_function = self.langchain_tools_dict[tool.function.name]
                    result = langchain_function.run(tool.function.arguments)
                    tool_results.append({"tool_call_id": tool.id, "output": result})

                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=run_obj.id,
                    tool_outputs=tool_results,
                )

                iterations += 1

            else:
                print(f"unknown status {response.status} -> response {response}")
                iterations += 1
                # raise Exception(f"response status {response.status} unkown!")

        raise Exception(f"max iterations reached {max_iterations}")


class SnowmanAgent(AssistantHelper):
    def __init__(
        self,
        assistant_id: str,
        thread_id: str = None,
        thread: Threads = None,
        assistant: Assistants = None,
        langchain_tools: List[tool] = None,
    ) -> None:

        super().__init__(assistant_id, thread_id, thread, assistant, langchain_tools)

        self.json_functions_mapping = None

    @classmethod
    def get_cached_message(cls, message: str, user: User, cache_obj=None):
        try:
            if cache_obj is None:
                cache_obj = cache

            cached_message = cache_obj.get(f"user-{user.id}: {message}")
            return cached_message

        except Exception as e:
            print(e)
            raise Exception("django cache not found")

    @classmethod
    def set_cache_message(
        cls, query: str, ans: str, user: User, time_out=3600 * 24 * 2, cache_obj=None
    ):
        try:
            if cache_obj is None:
                cache_obj = cache

            cache_obj.set(f"user-{user.id}: {query}", ans, timeout=time_out)

        except Exception as e:
            print(e)
            raise Exception("django cache not found")

    def add_message_to_thread(
        self, thread: Threads, user_question: str, client: OpenAI = None
    ):
        if client is None:
            client = OpenAI()
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=user_question
        )
        return message

    def run(self, message: str) -> str:

        self.add_message_to_thread(
            thread=self.thread, user_question=message, client=self.client
        )

        run_obj = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )

        max_iterations = 200
        iterations = 0
        json_results = []

        while iterations < max_iterations:
            response = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run_obj.id
            )
            tool_results = []

            if response.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                message_content = messages.data[0].content[0].text.value
                return {
                    "message_content": message_content,
                    "json_results": json_results,
                }

            elif response.status == "in_progress":
                print("progressing...")
                time.sleep(1)
                iterations += 1

            elif response.status == "requires_action":
                print("requires action..")
                tool_calls = response.required_action.submit_tool_outputs.tool_calls

                for tool in tool_calls:
                    langchain_function = self.langchain_tools_dict[tool.function.name]
                    print(
                        tool.function.arguments,
                        "tool.function.arguments",
                        langchain_function,
                        "function",
                    )
                    arguments = json.loads(tool.function.arguments)

                    result = langchain_function.run(arguments)
                    tool_results.append(
                        {"tool_call_id": tool.id, "output": json.dumps(result)}
                    )

                    if tool.function.name in self.json_functions_mapping:
                        json_results.append(
                            {
                                "function_name": tool.function.name,
                                "json_output": result,
                                "type": self.json_functions_mapping[tool.function.name],
                            }
                        )

                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=run_obj.id,
                    tool_outputs=tool_results,
                )

                iterations += 1

            elif response.status == "failed":
                print("failed ...")
                print(response.failed_at)
                return {
                    "message_content": "Assistant couldn't resolve your query, something went wrong please ask again.",
                    "json_results": json_results,
                    "type": "failed",
                }

            else:
                print(f"unknown status {response.status} -> response {response}")
                iterations += 1
                # raise Exception(f"response status {response.status} unkown!")

        raise Exception(f"max iterations reached {max_iterations}")


# from common.assistants.assistants import AssistantHelper
# assistant = AssistantHelper("asst_xoCkAKENU02dWKbupfAaPHQw")
# from common.assistants.assistant_tools import get_temperature, get_contact_card
# AssistantHelper.update_assistant("asst_xoCkAKENU02dWKbupfAaPHQw",langchain_tools = [get_temperature, get_contact_card])
