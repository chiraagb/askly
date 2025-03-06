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
from .custom_tools import get_indian_constituion_law_info
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain


# @tool
# def get_word_length(word: str) -> int:
#     """Returns the length of a word."""
#     return len(word)


# prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "You are very powerful assistant, but don't know current events",
#             ),
#             ("user", "{input}"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# llm_with_tools = llm.bind_tools(tools)

# agent = (
#     {
#         "input": lambda x: x["input"],
#         "agent_scratchpad": lambda x: format_to_openai_tool_messages(
#             x["intermediate_steps"]
#         ),
#     }
#     | prompt
#     | llm_with_tools
#     | OpenAIToolsAgentOutputParser()
# )

# result = agent.invoke({
#     "input":"word count of halley",
#     "intermediate_steps":[(OpenAIToolAgentAction(tool='get_word_length', tool_input={'word': 'halley'}, log="\nInvoking: `get_word_length` with `{'word': 'halley'}`\n\n\n", message_log=[AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_hEoWbCopBIqSxXmpnUNUoj3D', 'function': {'arguments': '{"word":"halley"}', 'name': 'get_word_length'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 16, 'prompt_tokens': 74, 'total_tokens': 90}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': 'fp_3bc1b5746c', 'finish_reason': 'tool_calls', 'logprobs': None})], tool_call_id='call_hEoWbCopBIqSxXmpnUNUoj3D'), "6")]
# })


tools = [get_indian_constituion_law_info]


def summarize_pdf(pdf_file_path, custom_prompt=""):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)

    return summary


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
            function_result = function.run(function_arguments)
            print("function result: ", function_result)

            intermediate_steps.append((result[0], function_result))

        else:
            raise Exception("Unkown result class type", type(result))

        iteration_limit += 1


if __name__ == "__main__":

    # result = ask_lawyser("can you tell me about right to freedom ?", tools=tools)

    # print(result)

    print(summarize_pdf("legal.pdf"))
