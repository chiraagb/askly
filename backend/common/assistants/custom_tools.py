from langchain.agents import tool
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from pydantic.v1 import BaseModel, Field
from .prompts import money_complaint_prompt
from typing import Optional, Type
from langchain_core.tools import BaseTool
import os

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


@tool
def get_temperature(country: str) -> str:
    """
    This function takes country as argument and returns the temperature of that country.
    """
    return "2f"


class delegate_work_to_legal_document_drafter_input(BaseModel):
    work_description: str = Field(
        description="""This field takes the description of work that legal document drafter agent should do. 
                                                  It includes the type of document that needs to drafted and some decription of the document that user provides"""
    )


@tool(args_schema=delegate_work_to_legal_document_drafter_input)
def delegate_work_to_legal_document_drafter(work_description):
    """
    This function is used to delegate drafting of legal document work to legal document drafter agent.
    """
    return {"work_description": work_description}


class draft_legal_document_input(BaseModel):
    legal_document: str = Field(
        description="This field is the created legal document in perfect markdown."
    )


@tool(args_schema=draft_legal_document_input)
def draft_legal_document(legal_document):
    """
    This function is used to create legal documents with perfect markdown.
    """
    return {"legal_document": legal_document}


class draft_money_complaint_related_legal_document_input(BaseModel):
    money_complaint_document: str = Field(
        description="This field is the created money complaint document from the user info in perfect markdown."
    )


class draft_money_complaint_related_legal_document(BaseTool):
    name = "draft_money_complaint_related_legal_document"
    description = f"""
                  This function is used to create a money related legal document from the info from the user in the below format with perfect markdown:

                  {money_complaint_prompt}
                  """
    args_schema: Type[BaseModel] = draft_money_complaint_related_legal_document_input

    def _run(
        self,
        money_complaint_document: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:

        return {"money_complaint_document": money_complaint_document}


class draft_money_complaint_related_legal_document_input2(BaseModel):
    document_context: str = Field(
        description="This field used to give context of the document from users info"
    )


class draft_money_complaint_related_legal_document2(BaseTool):
    name = "draft_money_complaint_related_legal_document"
    description = f"""
                  This function is used to create a money related legal document from the info from the user.

                  
                  """
    args_schema: Type[BaseModel] = draft_money_complaint_related_legal_document_input2

    def _run(
        self,
        document_context: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

        result = llm.invoke(
            f"""
        Below is the users context about the document.
                            
        {document_context}

        You need to create a money complaint document in the below format and respond with only perfect markdown and dont cover it ``` symbols and repond with perfect markdown
        {money_complaint_prompt}
        """
        )

        return result.content


@tool
def claude_summarize_pdf(pdf_file_path):
    """
    hello pull
    """
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load()

    llm = ChatAnthropic(
        temperature=0,
        anthropic_api_key="",
        model_name="claude-3-opus-20240229",
    )
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


def claude_summarize_pdf2(pdf_file_path):
    # Define prompt
    prompt_template = """Write an Elaborate summary of the legal document in perfect markdown of below:
    "{text}"
    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatAnthropic(
        temperature=0,
        anthropic_api_key="",
        model_name="claude-3-opus-20240229",
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load()

    return stuff_chain.run(docs)


def format_docs(docs):
    context = """

            """
    for doc in docs:
        format = f"""
                    
BOOK - {doc.metadata["source"]}
PAGE_CONTENT:

page - {doc.page_content}

                """
        context += format

    return context


@tool
def get_indian_constituion_law_info(law: str) -> str:
    """
    This function takes a the law that you want to get info on from official constituion of india.

    Use Condition:
        - Use this function only when you need law info from constitution of india.

    Output:
        - This function uses similarity search to query vector database on the law that you need to query.

    """

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = Qdrant(
        client=QdrantClient(
            "https://e8c12a55-0f19-4100-b2b2-0dd693d8b721.us-east4-0.gcp.cloud.qdrant.io:6333",
            prefer_grpc=True,
            api_key="8FxFIJv8AKNsdoW1h1iqdjSqaDdR-MBs1sm262zmRQthrLgA-hLP6A",
        ),
        collection_name="constitution",
        embeddings=embeddings,
    )

    retriver = vectorstore.as_retriever()

    result = retriver.invoke(law)

    return format_docs(result)


class get_california_laws_info_input(BaseModel):
    law: str = Field(
        description="This field takes the queries on which similarity search is performed on the california laws"
    )


class get_california_laws_info(BaseTool):
    name = "get_california_laws_info"
    description = """
        This function takes the law that you want to get info on from official laws of california.

        Use Condition:
            - Use this function only when you need law info about california

        Output:
            - This function uses similarity search to query vector database on the law that you need to query.

        """
    args_schema: Type[BaseModel] = get_california_laws_info_input

    def _run(
        self, law: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        vectorstore = Qdrant(
            client=QdrantClient(
                os.getenv("QDRANT_CLOUD"),
                prefer_grpc=True,
                api_key=os.getenv("QDRANT_API_KEY"),
            ),
            collection_name="california-laws",
            embeddings=embeddings,
        )

        retriver = vectorstore.as_retriever(search_kwargs={"k": 5})

        result = retriver.invoke(law)

        return format_docs(result)


if __name__ == "__main__":
    print("hello")
    print(
        get_california_laws_info().run(
            tool_input={"law": "California Family Rights Act"}
        )
    )
    # print(get_california_laws_info(law = "familiy laws in california"))
