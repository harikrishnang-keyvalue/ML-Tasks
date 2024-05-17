'''
2. Use Case: Streamlining Internal Policy Inquiries with a Chat Application

Scenario:  Employees frequently have questions about company policies and procedures. Traditionally, they might need to search through a company intranet, HR portal, or even email HR directly. This process can be time-consuming and inefficient, especially for simple questions.
Solution: Integrate a knowledge base chatbot functionality within the company's existing chat application.
'''

# pip install langchain (version = 0.1.20)

import streamlit as st
import dotenv
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.memory import ChatMessageHistory

dotenv.load_dotenv()
documents_directory = 'docs/'
internal_policy_chat_message_history = ChatMessageHistory()

st.title("Internal Policy Chatbot")

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

def generate_response(input_text):
  loader = PyPDFDirectoryLoader(documents_directory, extract_images=True)
  pages = loader.load_and_split()

  prompt_template = input_text + " Take into context the documents which are conference policy document and holiday policy document, content: {text}"
  print(prompt_template)
  prompt = PromptTemplate.from_template(prompt_template)
  chat = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo-1106")
  llm_chain = LLMChain(llm=chat, prompt=prompt)
  stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
  llm_output = stuff_chain.invoke(pages)
  return llm_output['output_text']

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})





