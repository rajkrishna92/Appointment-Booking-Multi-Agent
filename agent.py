from typing import Literal, List, Any
import sqlite3
from langchain_core.tools import tool
from typing_extensions import TypedDict, Annotated
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from prompt.prompt import system_prompt
from utils.llm import LLMModel
from utils.helper import pretty_print_message, pre_model_hook
from toolkit.tools import *

from langgraph.types import Command
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph_supervisor import create_supervisor

sqlite_conn = sqlite3.connect("data/checkpoint.db", check_same_thread= False)
memory= SqliteSaver(sqlite_conn)

llm_model = LLMModel()


booking_agent = create_react_agent(
    model=llm_model.get_model(),
    tools=[set_appointment,cancel_appointment,reschedule_appointment],
    prompt="You are specialized agent to set, cancel or reschedule appointment based on the query. You have access to the tool.\n Make sure to ask user politely if you need any further information to execute the tool.\n For your information, Always consider current year is 2025.",
    name="booking_agent",
)

information_agent = create_react_agent(
    model=llm_model.get_model(),
    tools=[check_availability ,check_availability_by_specialization],
    prompt="You are specialized agent to provide information related to availability or any FAQs based on the query. You have access to the tool.\n Make sure to ask user politely if you need any further information to execute the tool.\n For your information, Always consider current year is 2025.",
    name="information_agent",
)

supervisor = create_supervisor(
    model=llm_model.get_model(),
    agents=[information_agent, booking_agent],
    prompt=system_prompt,
    pre_model_hook=pre_model_hook,
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile(checkpointer=memory)


if __name__ == "__main__":
    state = {'messages': HumanMessage(content='what is my name?')}
    config={"configurable":{"thread_id":'raj@xyz'}}
    result = supervisor.invoke(state, config=config)
    for m in result['messages']:
        m.pretty_print()
    print(result["messages"][-1].content)