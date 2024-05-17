
'''
1. Use Case: Auto-generating Contract Summaries with CLM

Scenario:  The sales team finalizes a contract with a new client.  This contract, like most others, is lengthy and full of legal jargon. Traditionally, someone from the legal department would need to spend time manually summarizing the key terms for various stakeholders across the organization. This process can be slow and inefficient.

Solution: Utilize the contract lifecycle management (CLM) platform's built-in contract summary functionality. The CLM system can automatically extract key information from the uploaded contract, such as:
Parties involved
Contract type (e.g., NDA, Service Agreement)
Key dates (e.g., start date, termination date)
Financial terms (e.g., payment schedule, pricing)
Important clauses (e.g., confidentiality, intellectual property)
1.b) Do it for an image based PDF (try OCR)
1.c) Do summary of the given format
‘’’
This is a {contract type} between {party 1} and {party 2}, which is effective from {start date/effective date}.

Below is a summary of key terms of the contract.

Purpose: {content}
Confidentiality: {content}
Term and Termination: {content}
Representation and Warranty: {content}
Ownership: {content}

In addition, below are details that you may find useful
{may contain any other important points not mentioned above}
‘’’
Values in {} have to be fetched from open-ai
'''

# pip install langchain (version = 0.1.20)

import os
import dotenv
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

dotenv.load_dotenv()

repeat_flag = True

while repeat_flag:
  document = input("Enter the document name: ")
  file_name, file_extension = os.path.splitext('./' + document)

  loader = PyPDFLoader(document, extract_images=True)
  pages = loader.load_and_split()

  prompt_template = """Write a summary exactly in the following format keeping in mind the values in <> have to be fetched from the text provided to summarize:
  This is a <contract type> between <party 1> and <party 2>, which is effective from <start date/effective date>.

  Below is a summary of key terms of the contract.

  Purpose: <purpose of the contract>
  Confidentiality: <confidentiality of the contract>
  Term and Termination: <term and termination of contract>
  Representation and Warranty: <representation and warranty of contract>
  Ownership: <ownership of contract>

  In addition, below are details that you may find useful: <additional information>

  The text to be summarized is: {text}."""
  prompt = PromptTemplate.from_template(prompt_template)

  llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
  llm_chain = LLMChain(llm=llm, prompt=prompt)
  stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
  llm_output = stuff_chain.invoke(pages)
  file_to_write = open(file_name + ".txt", 'w')
  file_to_write.write(llm_output['output_text'])
  file_to_write.close()
  continue_or_not = input("Do you want to continue summarizing another file? (yes/no): ")
  if continue_or_not.lower() == 'no':
    repeat_flag = False
  else:
    repeat_flag = True
