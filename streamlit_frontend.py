import streamlit as st
from chatbot import app, State
from langchain_core.messages import AIMessage, HumanMessage


st.set_page_config(layout='wide', page_title='AI HR Assistant', page_icon='🧑‍💼')

if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Здравствуйте! Чем могу быть полезен?")]

left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. Buttons for chat - Clear Button

with left_col:
    if st.button('Очистить чат'):
        st.session_state.message_history = []


# 2. Chat history and input
with main_col:
    user_input = st.chat_input("Печатайте...")

    if user_input:
        st.session_state.message_history.append(HumanMessage(content=user_input))
        config = {"configurable": {"thread_id": "1"}}
        response = app.invoke(State(question=user_input), config)
        st.session_state.message_history.append(AIMessage(content=response['answer']))

    for i in range(1, len(st.session_state.message_history) + 1):
        this_message = st.session_state.message_history[-i]
        if isinstance(this_message, AIMessage):
            message_box = st.chat_message('assistant')
        elif isinstance(this_message, HumanMessage):
            message_box = st.chat_message('user')
        message_box.markdown(this_message.content)

