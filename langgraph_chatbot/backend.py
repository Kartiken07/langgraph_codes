import os
import time
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import Annotated, TypedDict,Literal,List
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
os.environ["LANGSMITH_PROJECT"]="LangGraph Chatbot"
load_dotenv()
llm=ChatGroq(
    model="groq/compound-mini",
    api_key=os.getenv("GROQ_API_KEY"),
)
class ChatBotState(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]

graph=StateGraph(ChatBotState)

def chat_bot(state:ChatBotState)->ChatBotState:
    messages=state["messages"]
    response=llm.invoke(messages)
    return {'messages':[response]}
graph.add_node("ChatNode",chat_bot)
graph.add_edge(START,"ChatNode")
graph.add_edge("ChatNode",END)

chackpointer=InMemorySaver()

workflow=graph.compile(checkpointer=chackpointer)
