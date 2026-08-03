import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage
# from langgraph.graph.message import HumanMessage, AIMessage
thread_id="2"
CONFIG={'configurable':{"thread_id":thread_id}}
if "messages" not in st.session_state:

    st.session_state.messages = []
for messages in st.session_state.messages:
    with st.chat_message(messages["role"]):
        st.write(messages["content"])


user_input = st.chat_input("Type your message here...")


if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    response=workflow.stream({"messages":[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages') 
    with st.chat_message("ai"):

        ai_message=st.write_stream(messages.content for messages ,metadata in workflow.stream({"messages":[HumanMessage(content=user_input)]},config=CONFIG,stream_mode='messages'))
        st.session_state.messages.append({"role": "user", "content": ai_message})