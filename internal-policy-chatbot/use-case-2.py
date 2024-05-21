"""
2. Use Case: Streamlining Internal Policy Inquiries with a Chat Application

Scenario:  Employees frequently have questions about company policies and procedures. Traditionally, they might need to search through a company intranet, HR portal, or even email HR directly. This process can be time-consuming and inefficient, especially for simple questions.
Solution: Integrate a knowledge base chatbot functionality within the company's existing chat application.
"""

# pip install langchain (version = 0.1.20)

import dotenv
import json
import streamlit as st
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
documents_directory = "docs/"

st.title("Internal Policy Chatbot")

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def generate_response(input: str, config: dict):
    loader = PyPDFDirectoryLoader(documents_directory, extract_images=True)
    pages = loader.load_and_split()
    system_message = """
    Answer the user's questions based on the below context. 
    If the context doesn't contain any relevant information to the question, just say "I don't know":

    <context>
    {context}
    </context>
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message,
            ),
            MessagesPlaceholder(variable_name="messages"),
            HumanMessage(content=input),
        ]
    )
    chat = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo-1106")
    stuff_chain = create_stuff_documents_chain(chat, prompt)
    with_message_history = RunnableWithMessageHistory(
        stuff_chain,
        get_session_history,
        input_messages_key="messages",
    )
    response = with_message_history.invoke(
        {
            "messages": get_session_history(
                config["configurable"]["session_id"]
            ).messages,
            "context": pages,
        },
        config=config,
    )
    print(response)
    return response


if prompt := st.chat_input("Say something"):
    store_file = open("store.json", "r")
    try:
        chat_history = json.loads(store_file.read())
    except json.decoder.JSONDecodeError:
        chat_history = {}
    config = {"configurable": {"session_id": "abc123"}}
    for session_id, messages in chat_history.items():
        store[session_id] = ChatMessageHistory()
        for message in messages:
            if message["role"] == "assistant":
              store[session_id].add_message(AIMessage(content=message["content"]))
            elif message["role"] == "user":
              store[session_id].add_message(HumanMessage(content=message["content"]))
    store_file.close()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(prompt, config)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    store_file = open("store.json", "w")
    store_file.write(json.dumps({"abc123": st.session_state.messages}))
    store_file.close()
