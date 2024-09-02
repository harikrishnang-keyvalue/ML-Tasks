import os
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import ChatVertexAI
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader

pages = []
images = ["test_1.JPEG", "test_2.JPEG"]
for image in images:
    loader = UnstructuredFileLoader(image)
    pages.append(loader.load_and_split())

prompt_template = """Consider you are an image detection expert, and you are looking for mathematical solutions in the images.
Output the mathematical solutions along with other descriptions in the image exactly in latex code.

The content to be summarized is: {content}."""
prompt = PromptTemplate.from_template(prompt_template)

llm = ChatVertexAI(temperature=0, model_name="gemini-1.5-flash")
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(
    llm_chain=llm_chain, document_variable_name="content"
)
llm_output = stuff_chain.invoke(pages)
print(llm_output["output_text"])
