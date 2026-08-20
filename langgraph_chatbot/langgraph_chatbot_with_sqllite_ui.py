import streamlit as st
from backend_with_sqllite import workflow,retrive_all_thread_id
import uuid
import os
from langchain_core.messages import HumanMessage,AIMessage
os.environ["LANGSMITH_PROJECT"]="LangGraph Chatbot"
st.title("Agent Chatbot")
def uuid_generator():
    return str(uuid.uuid4())
def resert_chat():
    st.session_state.messages = []
    st.session_state.thread_id = uuid_generator()
    add_thread(st.session_state.thread_id)
def add_thread(thread_id):
    if thread_id not in st.session_state.thread_id_list:
        st.session_state.thread_id_list.append(thread_id)
def load_con(thread_id):
     config = {"configurable": {"thread_id": thread_id}}
     state = workflow.get_state(config)
     return state.values.get("messages", [])
# from langgraph.graph.message import HumanMessage, AIMessag

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = uuid_generator()
if "thread_id_list" not in st.session_state:
    st.session_state.thread_id_list=retrive_all_thread_id()
for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.write(messages["content"])
add_thread(st.session_state.thread_id)

st.sidebar.title("Chats")
st.sidebar.button("New Chat",type="primary",width=100,on_click=resert_chat)
for thread_id in st.session_state.thread_id_list:
    if st.sidebar.button(f"Chat {thread_id}",key=thread_id):
        st.session_state.thread_id=thread_id
        history = load_con(thread_id)
        temp_messages=[]
        for msg in history:
            if isinstance(msg,HumanMessage):
                role="user"
            elif  isinstance(msg,AIMessage):  
                role="assistant"
            else:
                continue
            temp_messages.append({"role": role, "content": msg.content})
        st.session_state.messages=temp_messages 
        st.rerun()


CONFIG={'configurable':{"thread_id":st.session_state.thread_id},"metadata":{"thread_id":st.session_state.thread_id},"run_name":f"chat_{st.session_state.thread_id}"}

user_input = st.chat_input("Type your message here...")


if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    response=workflow.stream({"messages":[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages') 
    with st.chat_message("assistant"):
        ai_message=st.write_stream(messages.content for messages ,metadata in workflow.stream({"messages":[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages'))
        st.session_state.messages.append({"role": "assistant", "content": ai_message})