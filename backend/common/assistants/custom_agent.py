from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolAgentAction
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.agents import AgentFinish
from typing import Sequence, List
import json
from .custom_tools import (
    get_indian_constituion_law_info,
    delegate_work_to_legal_document_drafter,
    draft_legal_document,
    draft_money_complaint_related_legal_document,
    draft_money_complaint_related_legal_document2,
)
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
import os


tools = [get_indian_constituion_law_info, delegate_work_to_legal_document_drafter]

legal_document_tools = [
    draft_legal_document,
    draft_money_complaint_related_legal_document2(),
]


def summarize_pdf(pdf_file_path, custom_prompt=""):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)

    return summary


chat_history = []


def ask_lawyser(query, tools=tools):
    intermediate_steps = []
    iterations = 0
    iteration_limit = 10

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are  Indian Ai Lawyer.
                   You always respond with perfect and beautiful markdown.
                   When you answer about law please be elaborate and  include page and book that you have took the information from.
                
                """,
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    while iterations < iteration_limit:
        result = agent.invoke(
            {"input": query, "intermediate_steps": intermediate_steps}
        )

        if isinstance(result, AgentFinish):
            return result

        elif isinstance(result, List) and isinstance(result[0], OpenAIToolAgentAction):
            function_name = result[0].tool
            function_arguments = result[0].tool_input
            function = [func for func in tools if function_name == func.name][0]

            print(result[0].log)

            if function_name == delegate_work_to_legal_document_drafter.name:
                return contract_drafting_agent(function_arguments["work_description"])

            function_result = function.run(function_arguments)
            print("function result: ", function_result)

            intermediate_steps.append((result[0], function_result))

        else:
            raise Exception("Unkown result class type", type(result))

        iteration_limit += 1


def contract_drafting_agent(query, tools=legal_document_tools):
    intermediate_steps = []
    iterations = 0
    iteration_limit = 10

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are Contract Drafter
                   You always respond with perfect and beautiful markdown.
                   
                
                """,
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    while iterations < iteration_limit:
        result = agent.invoke(
            {"input": query, "intermediate_steps": intermediate_steps}
        )

        if isinstance(result, AgentFinish):
            return result

        elif isinstance(result, List) and isinstance(result[0], OpenAIToolAgentAction):
            function_name = result[0].tool
            function_arguments = result[0].tool_input
            function = [func for func in tools if function_name == func.name][0]

            if function_name == draft_legal_document.name:
                return function_arguments["legal_document"]

            if function_name == draft_money_complaint_related_legal_document().name:
                return function.run(function_arguments)

            print(result[0].log)
            function_result = function.run(function_arguments)
            print("function result: ", function_result)

            intermediate_steps.append((result[0], function_result))

        else:
            raise Exception("Unkown result class type", type(result))

        iteration_limit += 1


if __name__ == "__main__":

    # result = ask_lawyser("can you tell me about right to freedom ?", tools=tools)

    # print(result)

    # print(summarize_pdf("legal.pdf"))

    # print(ask_lawyser("give me a template for rent agreement"))
    print(
        contract_drafting_agent(
            "create a money complaint document with my name as avinash and plaintiff as meta company, as they owe me 1k$ for bonus"
        )
    )
