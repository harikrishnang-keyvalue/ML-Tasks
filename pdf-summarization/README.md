### 1. Use Case: Auto-generating Contract Summaries with CLM
Scenario:  The sales team finalizes a contract with a new client.  This contract, like most others, is lengthy and full of legal jargon. Traditionally, someone from the legal department would need to spend time manually summarizing the key terms for various stakeholders across the organization. This process can be slow and inefficient.

Solution: Utilize the contract lifecycle management (CLM) platform's built-in contract summary functionality. The CLM system can automatically extract key information from the uploaded contract, such as:
- Parties involved
- Contract type (e.g., NDA, Service Agreement)
- Key dates (e.g., start date, termination date)
- Financial terms (e.g., payment schedule, pricing)
- Important clauses (e.g., confidentiality, intellectual property)
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
