import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from datetime import date

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key
)


st.title("Streamlit AI Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])    

question = st.chat_input("Ask me anything...")

if question:
    # Display and store the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Ask the AI
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            today = date.today().strftime("%B %d, %Y")

            messages = [
                {
                    "role": "system",
                    "content": f"Today's date is {today}. "
                            "When asked for today's date, use this date. "
                            "Do not guess the current date."
                },
                *st.session_state.messages
            ]

            response = llm.invoke(messages)
            # response = llm.invoke(st.session_state.messages)
            st.write(response.content)

    # Store the AI's answer
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })