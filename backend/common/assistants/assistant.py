from openai.resources.beta import Assistants, Threads
import warnings
from openai import OpenAI
import time
from typing import Optional, List
from openai.types.beta import assistant_update_params, Assistant
from langchain.tools.render import format_tool_to_openai_function
from langchain.tools import tool
import json
from .custom_tools import get_indian_constituion_law_info, get_california_laws_info
import os
import json
import openai
from openai.types.beta.assistant_stream_event import (
    ThreadRunRequiresAction,
    ThreadRunCompleted,
    ThreadMessageDelta,
    ThreadRunFailed,
    ThreadRunCreated,
    
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def retry_on_timout(func):
    def wrapper(*args, max_retries=3, **kwargs):
        tries = 0
        while tries < max_retries:
            try:
                result = func(*args, **kwargs)
                return result
            except openai.APITimeoutError as e:
                tries += 1
                if tries == max_retries:
                    raise Exception(
                        f"Max retries reached {tries}. Last error: {str(e)}"
                    ) from e

    return wrapper


class AssistantHelper:
    """
    This is a Helper class which contains helpful methods to ineract with assistance api.
    This is basically a Wrapper on top of Assistance api for ease of use.
    """

    def __init__(
        self,
        assistant_id: str,
        thread_id: str = None,
        thread: Threads = None,
        assistant: Assistants = None,
    ) -> None:
        self.client = OpenAI()
        self.assistant_id = assistant_id
        self.assistant = assistant
        self.thread_id = thread_id
        self.thread = thread
        self.instructions = None
        self.model = "gpt-4-turbo-preview"

        if self.thread is not None and self.thread_id is None:
            self.thread_id = thread_id

    @staticmethod
    def create_thread(client: OpenAI = None, timeout: int = None) -> Threads:
        """
        This method creates a new Thread object.
        """
        if client is None:
            client = OpenAI()

        thread = client.beta.threads.create(timeout=timeout)
        return thread

    @staticmethod
    def retrieve_thread(thread_id: str, client: OpenAI = None, timeout=None) -> Threads:
        """
        This method retrieves Thread object from a thread id.
        """
        if client is None:
            client = OpenAI()
        thread = client.beta.threads.retrieve(thread_id=thread_id, timeout=timeout)
        return thread

    @staticmethod
    def create_assistant(
        name: str,
        model: str,
        client: OpenAI,
        file_ids: List[str] = None,
        description: str = None,
        instructions: str = None,
        langchain_tools: List[tool] = None,
    ) -> Assistants:
        """
        This method is used to create an assistant.
        """
        warnings.warn(f"creating assistant with model {model}")
        dynamic_args = {}
        if description:
            dynamic_args["description"] = description
        if instructions:
            dynamic_args["instructions"] = instructions

        if langchain_tools:
            dynamic_args["tools"] = [
                {"type": "function", "function": format_tool_to_openai_function(tool)}
                for tool in langchain_tools
            ]

        assistant = client.beta.assistants.create(
            name=name, model=model, **dynamic_args
        )

        return assistant

    @staticmethod
    def update_assistant(
        assistant_id: str, client: OpenAI, langchain_tools: List[tool] = None, **kwargs
    ) -> Assistants:
        """
        This method is used to create an assistant.
        """

        if langchain_tools:
            tools = [
                {"type": "function", "function": format_tool_to_openai_function(tool)}
                for tool in langchain_tools
            ]

        assistant = client.beta.assistants.update(
            assistant_id=assistant_id, tools=tools, **kwargs
        )

        return assistant


    @staticmethod
    def retrieve_assistant(assistant_id: str, client: OpenAI = None) -> Assistants:
        """
        This method is used to retrive an Assistant object from assistant id.
        """
        if client is None:
            client = OpenAI()
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
        return assistant

    def add_message_to_thread(
        self, thread: Threads, user_question: str, client: OpenAI = None
    ):
        """
        This method is used to add messages to a particular thread.
        """
        if client is None:
            client = OpenAI()

        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=user_question, timeout=10
        )
        return message

    def run(self, message: str) -> str:
        """
        This method takes a message and adds it to a thread and then returns the outcome of the message from assistant.
        """
        self.add_message_to_thread(
            thread=self.thread, user_question=message, client=self.client
        )

        run_obj = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )

        max_iterations = 100
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
                time.sleep(0.5)
                iterations += 1

            else:
                iterations += 1
                raise Exception(f"response status {response.status} unkown!")

        raise Exception(f"max iterations reached {max_iterations}")


class AIAssistant(AssistantHelper):
    def __init__(
        self,
        assistant_id: str,
        thread_id: str = None,
        thread: Threads = None,
        assistant: Assistants = None,
    ) -> None:

        super().__init__(assistant_id, thread_id, thread, assistant)

    model = "gpt-4-turbo-preview"
    langchain_tools: List[tool] = [get_california_laws_info()]
    langchain_tools_dict = {tool.name: tool for tool in langchain_tools}
    stream = None
    run = None

    # @classmethod
    # def create_masking_assistant(cls) -> Assistants:
    #     """
    #     This static method uses create_assistant method to create an masking assistant.
    #     """

    #     assistant = cls.create_assistant(
    #         name="masking-assistant",
    #         model=cls.model,
    #         client=OpenAI(api_key=OPENAI_API_KEY),
    #         instructions=service_points_masking_assistant_prompt,
    #         langchain_tools=cls.langchain_tools,
    #     )

    #     return assistant

    @classmethod
    def update_ai_assistant(cls, assistant_id: str) -> Assistants:
        """
        This static method uses update_assistant method to update a masking assistant.
        """

        assistant = cls.update_assistant(
            assistant_id=assistant_id,
            client=OpenAI(api_key=OPENAI_API_KEY),
            langchain_tools=cls.langchain_tools,
        )

        return assistant

    def create_run(self, timeout: int = None):
        run_obj = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            timeout=timeout,
        )
        return run_obj

    def run(self, message: str) -> str:
        """
        This method takes a message and adds it to a thread and then returns the outcome of the message from assistant.
        """
        self.add_message_to_thread(
            thread=self.thread, user_question=message, client=self.client
        )

        run_obj = self.create_run(timeout=10)

        max_iterations = 100
        iterations = 0

        while iterations < max_iterations:
            tool_results = []

            response = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run_obj.id,
                timeout=10,
            )

            if response.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                message_content = messages.data[0].content[0].text.value
                return message_content

            elif response.status == "in_progress" or response.status == "queued":
                time.sleep(0.5)
                iterations += 1

            elif response.status == "requires_action":
                tool_calls = response.required_action.submit_tool_outputs.tool_calls
                for tool in tool_calls:
                    langchain_function = self.langchain_tools_dict[tool.function.name]
                    langchain_func_arguments = json.loads(tool.function.arguments)

                    print(langchain_func_arguments)

                    result = langchain_function.run(langchain_func_arguments)

                    # print(result, "result")

                    tool_results.append(
                        {"tool_call_id": tool.id, "output": json.dumps(result)}
                    )

                self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=run_obj.id,
                    tool_outputs=tool_results,
                )

                # self.client.beta.threads.runs.cancel(
                #     run_id=run_obj.id, thread_id=self.thread_id, timeout=10
                # )
                # return result

            else:
                iterations += 1
                raise Exception(f"response status {response.status} unkown!")

        raise Exception(f"max iterations reached {max_iterations}")

    def run_and_stream(self, message: str) -> str:
        """
        This method takes a message and adds it to a thread and then returns the outcome of the message from assistant.
        """

        self.add_message_to_thread(
            thread=self.thread, user_question=message, client=self.client
        )

        stream = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id, stream=True
        )

        self.stream = stream

        tool_results = []

        def stream_gen(stream):
            for event in stream:
                if isinstance(event, ThreadRunCreated):
                    self.run = event.data.id

                if isinstance(event, ThreadMessageDelta):
                    yield event.data.delta.content[0].text.value

                if isinstance(event, ThreadRunFailed):
                    print(event)
                    raise Exception("api status failed")

                if isinstance(event, ThreadRunRequiresAction):
                    # print(event.data)
                    tool_calls = (
                        event.data.required_action.submit_tool_outputs.tool_calls
                    )
                    # tool_calls = response.required_action.submit_tool_outputs.tool_calls
                    for tool in tool_calls:
                        langchain_function = self.langchain_tools_dict[
                            tool.function.name
                        ]
                        langchain_func_arguments = json.loads(tool.function.arguments)

                        # print(langchain_func_arguments)

                        result = langchain_function.run(langchain_func_arguments)

                        # print(result, "result")

                        tool_results.append(
                            {"tool_call_id": tool.id, "output": json.dumps(result)}
                        )

                    stream = self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=self.thread_id,
                        run_id=event.data.id,
                        tool_outputs=tool_results,
                        stream=True,
                    )

                    for i in stream_gen(stream):
                        yield i

                if isinstance(event, ThreadRunCompleted):
                    messages = self.client.beta.threads.messages.list(thread_id=event.data.thread_id)
                    print(len(messages.data))
                    last_annotation = messages.data[0].content[0].text.annotations
                    if last_annotation:
                        file= self.client.files.retrieve(file_id=last_annotation[0].file_citation.file_id)
                        # print(last_annotation[0].file_citation)
                        yield f"\n\n pdf source {file.filename}"
                    # print(event)

        return stream_gen(stream)

    async def arun_and_stream(self, message: str):
        """
        Asynchronously handles streaming responses from the assistant.

        This method takes a message, sends it to the assistant, and streams back the response.
        """
        # Assume add_message_to_thread is properly adjusted to be asynchronous if needed
        self.add_message_to_thread(
            thread=self.thread, user_question=message, client=self.client
        )

        stream = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id, stream=True
        )

        for event in stream:
            if isinstance(event, ThreadRunCreated):
                print(event)
            if isinstance(event, ThreadMessageDelta):
                yield event.data.delta.content[0].text.value

            elif isinstance(event, ThreadRunFailed):
                raise Exception("Assistant run failed")

            elif isinstance(event, ThreadRunRequiresAction):
                tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
                tool_results = []

                for tool in tool_calls:
                    langchain_function = self.langchain_tools_dict[tool.function.name]
                    langchain_func_arguments = json.loads(tool.function.arguments)
                    result = await langchain_function.run(
                        langchain_func_arguments
                    )  # Assuming this can be awaited
                    tool_results.append(
                        {"tool_call_id": tool.id, "output": json.dumps(result)}
                    )

                # Continue the stream with the results from tools
                additional_stream = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread_id,
                    run_id=event.data.id,
                    tool_outputs=tool_results,
                    stream=True,
                )
                for item in additional_stream:
                    yield item


if __name__ == "__main__":
    print(os.getenv("OPENAI_API_KEY"), "openai aoi key")
    thread = AIAssistant.create_thread()

    assistant = AIAssistant("asst_yiI6vJ98ycu8I6tsP7C2DhXz", thread_id=thread.id)
    for i in assistant.run_and_stream("tell me about labour laws"):
        print(i, end="")

    # re = AIAssistant.update_ai_assistant("asst_yiI6vJ98ycu8I6tsP7C2DhXz")

    # print(result)
