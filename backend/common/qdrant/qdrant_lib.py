from langchain.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders.pdf import PyPDFLoader

from qdrant_client import QdrantClient
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from django.conf import settings
import os

QDRANT_URL = os.getenv("QDRANT_CLOUD")


class QdrantHelper:
    def __init__(
        self, collection, client=None, embeddings=None, vectorstore=None, llm=None
    ):
        self.client = client
        self.collection = collection
        self.embeddings = embeddings
        self.vectorstore = vectorstore
        self.llm = llm

        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

        if self.client is None:
            self.client = QdrantClient(prefer_grpc=True, api_key=QDRANT_URL)

        if self.llm is None:
            self.llm = OpenAI(temperature=0)

    def _initialize_client(self):
        client = QdrantClient(QDRANT_URL, api_key=os.getenv("QDRANT_API_KEY"))
        return client

    def convert_to_docs(self, loader):
        docs = loader.load_and_split()
        return docs

    def create_db(self, loader, documents=None):
        if documents is None:
            documents = docs = self.convert_to_docs(loader)

        vectorstore = Qdrant.from_documents(
            documents,
            self.embeddings,
            url=QDRANT_URL,
            prefer_grpc=True,
            api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=self.collection,
        )
        self.vectorstore = vectorstore
        return self.vectorstore
