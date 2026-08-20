import os
import time
import sqlite3
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import Annotated, TypedDict,Literal,List
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
import finnhub
from langchain_core.tools import tool


load_dotenv()
llm=ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
)
search=DuckDuckGoSearchRun()
@tool
def calculator(num1:int,num2:int,operation:str)->float:
    """Tool for performing basic arithmetic operations."""
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    else:
        raise ValueError(f"Unsupported operation: {operation}")
@tool
def get_stock_price(stock_name:str)->dict:
    """Tool for fetching the current stock price of a given stock symbol."""
    load_dotenv()
    finnhub_client = finnhub.Client(api_key=os.getenv("FINHUB_API_KEY"))
    result=finnhub_client.quote(stock_name)
    return result
tools=[search,calculator,get_stock_price]
tools_node=ToolNode(tools)
llm_binded=llm.bind_tools(tools)
class ChatBotState(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]
graph=StateGraph(ChatBotState)

def chat_bot(state:ChatBotState)->ChatBotState:
    messages=state["messages"]
    response=llm_binded.invoke(messages)
    return {'messages':[response]}
graph.add_node("ChatBot", chat_bot)

graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "ChatBot")

graph.add_conditional_edges(
    "ChatBot",
    tools_condition
)
graph.add_edge("tools", "ChatBot")
conn=sqlite3.connect("chatdb.db",check_same_thread=False)
chackpointer=SqliteSaver(conn=conn)
workflow=graph.compile(checkpointer=chackpointer)
all_id=set()
def retrive_all_thread_id():
    for chackpointers in  chackpointer.list(None):
        all_id.add(chackpointers.config["configurable"]["thread_id"])
    return list(all_id)

