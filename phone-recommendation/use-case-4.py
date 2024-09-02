"""
4. Use Case: Choosing the Perfect Phone with a Mobile Chatbot

Scenario:  Choosing a new phone can be overwhelming. With countless models, features, and brands to consider, consumers often struggle to find the right fit for their needs and budget. Researching online can be time-consuming, and technical specifications can be confusing.

Solution: Create a RAG based chatbot. The document with mobile info is AI Learning Case-4 data

User Flow:
User opens that chat application
User asks guidelines
User asks to recommend some phones (recommend the links to the phone in data)
"""

# pip install langchain (version = 0.1.20)

import dotenv
import json
import streamlit as st
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever

dotenv.load_dotenv()
document = "use-case-4.pdf"

st.title("Phone Recommendation Chatbot")

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
    loader = PyPDFLoader(file_path=document, extract_images=True)
    pages = loader.load_and_split()
    vector_db = Chroma.from_documents(documents=pages, embedding=OpenAIEmbeddings())
    system_message = """
    Consider yourself as an expert in finding the right mobile phone for a particular user based on their needs.
    Answer the user's questions based on the below context and give the mobile phone link for purchasing from below context.
    The below context contains information about mobile phones and their specifications. If you are unable to find the information, just say "I don't know":

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
    chat = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=vector_db.as_retriever(),
        llm=chat,
    )
    stuff_chain = StuffDocumentsChain(llm_chain=multi_query_retriever.llm_chain, document_prompt=prompt)
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
