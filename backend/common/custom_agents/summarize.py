from langchain.document_loaders.pdf import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


def summarize_pdf(pdf_file_path, custom_prompt=""):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)

    return summary


def claude_summarize_pdf(pdf_file_path):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load()

    llm = ChatAnthropic(
        temperature=0, anthropic_api_key="", model_name="claude-3-opus-20240229"
    )
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


# chat = ChatAnthropic(temperature=0, anthropic_api_key="YOUR_API_KEY", model_name="claude-3-opus-20240229")

print(claude_summarize_pdf("legal.pdf"))
