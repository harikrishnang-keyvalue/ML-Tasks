import dotenv
import os
import time
from openai import OpenAI

dotenv.load_dotenv()


def get_openai_client():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                    organization=os.environ["OPENAI_ORGANIZATION_ID"])
    return client


def create_assistant(client: OpenAI, assistant: dict):
    created_assistant = client.beta.assistants.create(
        instructions=assistant["instructions"],
        model=assistant["model"],
        name=assistant["name"],
    )
    return created_assistant


def update_assistant(client: OpenAI, assistant_id: str, assistant: dict):
    return client.beta.assistants.update(
        assistant_id=assistant_id,
        instructions=assistant["instructions"]
    )


def retrieve_assistant(client: OpenAI, assistant_id: str):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant


def create_thread(client: OpenAI):
    empty_thread = client.beta.threads.create()
    return empty_thread


def retrieve_thread(client: OpenAI, thread_id: str):
    thread = client.beta.threads.retrieve(thread_id)
    return thread


def update_thread(client: OpenAI, thread_id: str, messages: list):
    updated_thread = client.beta.threads.update(thread_id, messages=messages)
    return updated_thread


def delete_thread(client: OpenAI, thread_id: str):
    deleted_thread = client.beta.threads.delete(thread_id)
    return deleted_thread


def create_message(client: OpenAI, thread_id: str, message: dict):
    created_message = client.beta.threads.messages.create(
        thread_id=thread_id, role=message["role"], content=message["content"])
    return created_message


def delete_message(client: OpenAI, thread_id: str, message_id: str):
    deleted_message = client.beta.threads.messages.delete(
        message_id=message_id,
        thread_id=thread_id
    )
    return deleted_message


def list_messages(client: OpenAI, thread_id: str):
    messages = client.beta.threads.messages.list(thread_id)
    return messages


def retrieve_message(client: OpenAI, thread_id: str, message_id: str):
    message = client.beta.threads.messages.retrieve(
        message_id=message_id, thread_id=thread_id)
    return message


def create_thread_run(client: OpenAI, thread_id: str, assistant_id: str):
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id)
    return run


def retrieve_run(client: OpenAI, run_id: str, thread_id: str):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run


# def main():
#     client = get_openai_client()
#     math_assistant_metadata = {
#         "instructions": "You are a helpful assistant who gets as input the marks of students and calculates the average. Your response should be the average of the marks.",
#         "model": "gpt-4o",
#         "name": "Math Assistant"
#     }
#     math_assistant = create_assistant(client, math_assistant_metadata)
#     print(f"Created assistant: {math_assistant}")

#     thread = create_thread(client)
#     print(f"Created thread: {thread}")

#     message = {
#         "role": "user",
#         "content": "Sam's mark is 40"
#     }
#     created_message = create_message(
#         client, thread_id=thread.id, message=message)
#     print(f"\nCreated message: {created_message}")

#     message = {
#         "role": "user",
#         "content": "Anjana's mark is 50"
#     }

#     created_message = create_message(
#         client, thread_id=thread.id, message=message)
#     print(f"\nCreated message: {created_message}")

#     message = {
#         "role": "user",
#         "content": "Da Vinci's mark is 60"
#     }

#     created_message = create_message(
#         client, thread_id=thread.id, message=message)
#     print(f"\nCreated message: {created_message}")

#     created_run = create_thread_run(client, thread.id, math_assistant.id)
#     print(f"\nCreated run: {created_run}")

#     # Polling for the run status until it is completed
#     while True:
#         run_status = retrieve_run(
#             client, run_id=created_run.id, thread_id=thread.id)
#         if run_status.status == 'completed':
#             print(f"\nRun completed: {run_status}")
#             thread_messages = list_messages(client, thread_id=thread.id)
#             print(f"\nThread messages: {thread_messages.data[0].content}")
#             break
#         else:
#             print(f"\nNot completed. Run status: {run_status.status}")
#         time.sleep(5)  # Wait for 5 seconds before checking again


# if __name__ == "__main__":
#     main()

client = get_openai_client()

# math_assistant_metadata = {
#     "instructions": ASSIGNMENT_CLASS_REPORT_GENERATION_ASSISTANT_PROMPT,
# }
# math_assistant = update_assistant(
#     client=client, assistant_id="asst_g0UoJg5Kpn7sgr5zCuLyOtoC", assistant=math_assistant_metadata)
# print(math_assistant)
