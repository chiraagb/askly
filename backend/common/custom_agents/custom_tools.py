from langchain.agents import tool
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


def claude_summarize_pdf(pdf_file_path):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load()

    llm = ChatAnthropic(
        temperature=0, anthropic_api_key="", model_name="claude-3-opus-20240229"
    )
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


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
        client=QdrantClient("", prefer_grpc=True, api_key=""),
        collection_name="constitution",
        embeddings=embeddings,
    )

    retriver = vectorstore.as_retriever()

    result = retriver.invoke(law)

    return format_docs(result)


if __name__ == "__main__":
    print(get_indian_constituion_law_info("right to freedom"))
