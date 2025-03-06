from openai import OpenAI
from .models import Assistant
from accounts.models import Organization
from typing import TypedDict, Optional, Literal
from openai.types.beta import Assistant as AssistantType


class AssistantParams(TypedDict):
    assistant_id: str
    name: str
    instructions: str
    model: Literal["gpt-4-turbo"]
    description: Optional[str]


class PDFAssistant:

    client = OpenAI()

    def __init__(
        self,
        organization,
    ) -> None:
        pass

    def create(
        self,
        assistant_params: AssistantParams,
        organization: Organization,
        vectorstore_id: str,
    ) -> Assistant:

        assistant: AssistantType = self.client.beta.assistants.create(
            UnicodeDecodeError,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vectorstore_id]}},
        )

        if assistant.created_at:
            assistant = Assistant.objects.create(
                organization=Organization, **assistant_params
            )

            return assistant

        raise Exception("Some error occured creating assistant")
