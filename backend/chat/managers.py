from typing import Any
from django.db import models
from openai import OpenAI


class AssistantManager(models.Manager):
    client = OpenAI()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def create_with_assistant(
        self, name, model, instructions, organization, vector_store_id, **kwargs
    ):
        assistant = self.client.beta.assistants.create(
            name=name,
            model=model,
            instructions=instructions,
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        return super().create(
            name, model, instructions, organization, assistant_id=assistant.id, **kwargs
        )


class AssitantVectorstoreManager(models.Manager):
    client = OpenAI()

    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)

    def create_with_openai_vectorstore(self, name, pdf_path, organization_id, **kwargs):
        file_streams = [open(path, "rb") for path in [pdf_path]]
        vector_store = self.client.beta.vector_stores.create(name=name)

        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        return super().create(
            name=name,
            organization_id=organization_id,
            vector_store_id=vector_store.id,
            **kwargs
        )
