import dotenv
import os
import re
import json
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
        tools=[{"type": "code_interpreter"}]
    )
    return created_assistant


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


def setup_openai_assistant(client: OpenAI):
    math_assistant_metadata = {
        "instructions": """
        You are a helpful english assistant who can generate question variants.
        **TASK**:
            - Your task is to generate a brief text similar to the example question, and use the generated brief text to make an image of compare and contrast table.
        **STEPS**:
            - Generate a brief text for the variant question similar to the given input.
            - Generate a compare and contrast table with 2 rows for which the student will chose using checkboxes, and generate a python code to generate image corresponding to that table. The image should be 600x200 pixels, HD quality, easy to read, with a white background, and the text should be black, the font style should be simple, and the font size should be 30.
            - Run the Python code to create the image and save it to OpenAI files.
            - Return the file ID of the generated image and the brief text.
        **RULES**:
            - You should neither return the same text as the given input nor return the text with the exact same meaning of the given input.
            - You can be creative and generate a text that is in similar structure to the question given in the input.
                - Example: If the input question is about apples and oranges, you can generate something with cars and bikes.
        **INPUT**:
            Sample input be will be:
            {
                "question": brief text of the example question,
                "image_url": image url of the example question
            }
        **OUTPUT**:
            - The TextContentBlock output should be a JSON object in the following structure:
            ```json
            {
                "output": {
                    "question": "Generated question text",
                    "file_id": "file_id_of_generated_image"
                }
            }
            ```
        **EXAMPLE**:
            - Example for python code getting generated:
                from PIL import Image, ImageDraw, ImageFont

                def create_image_with_table():
                    # Image size and background
                    img = Image.new('RGB', (600, 200), color=(255, 255, 255))
                    draw = ImageDraw.Draw(img)
                    
                    # Load a font (ensure you have a font file like Arial.ttf in the same directory or specify a path)
                    try:
                        font = ImageFont.truetype("arial.ttf", 20)
                    except IOError:
                        font = ImageFont.load_default()
                    
                    # Table title
                    draw.text((20, 20), "Compare and Contrast: Rabbit vs Squirrel", font=font, fill=(0, 0, 0))
                    
                    # Draw the table headers
                    draw.text((50, 60), "Characteristic", font=font, fill=(0, 0, 0))
                    draw.text((250, 60), "Rabbit", font=font, fill=(0, 0, 0))
                    draw.text((400, 60), "Squirrel", font=font, fill=(0, 0, 0))
                    
                    # Draw the rows with checkboxes
                    draw.text((50, 100), "Lives in trees", font=font, fill=(0, 0, 0))
                    draw.text((50, 140), "Hops on the ground", font=font, fill=(0, 0, 0))
                    
                    # Draw checkboxes (just simple rectangles for now)
                    draw.rectangle([250, 100, 270, 120], outline="black")
                    draw.rectangle([400, 100, 420, 120], outline="black")
                    draw.rectangle([250, 140, 270, 160], outline="black")
                    draw.rectangle([400, 140, 420, 160], outline="black")
                    
                    # Save the image
                    img.save("compare_and_contrast_table.png")

                create_image_with_table()
        """,
        "model": "gpt-4o",
        "name": "English Assistant"
    }
    return create_assistant(client, math_assistant_metadata)


def send_question(client: OpenAI, thread_id: str):
    message = {
        "role": "user",
        "content": """{
            "question": "Pumpkins are often thought of as vegetables, but they are actually fruits, like apples. Pumpkins are as popular as apples when it comes to making delicious pies. However, for a quick snack, an apple is a better choice, because you can eat an apple's skin.",
            "image_url": "https://imgtr.ee/image/hKeMsX"
        }"""
    }
    return create_message(client, thread_id, message)


def handle_run_completion(client: OpenAI, thread_id: str, run):
    while run.status != 'completed':
        print(f"\nRun completed: {run}")
        run = retrieve_run(client, run.id, thread_id)
    return run


def extract_content(client: OpenAI, thread_id: str):
    thread_messages = list_messages(client, thread_id)
    print(f"\nThread messages: {thread_messages.data[0].content}")
    content = thread_messages.data[0].content

    for item in content:
        print(f"\nContent item: {item}")
        if item.type == "text":
            output = item.text.value
            print(f"\nOutput: {output}")
            json_pattern = r'```json\n(.*?)\n```'
            json_match = re.search(json_pattern, output, re.DOTALL)
            match_object = json_match.group(1) if json_match else None
            json_object = json.loads(match_object)
            question = json_object["output"]["question"]

            for annotation in item.text.annotations:
                if annotation.type == "file_path":
                    image_path = annotation.file_path.file_id
                    print(f"\nImage path: {image_path}")
                    image_content = client.files.content(image_path)
                    with open(image_path + ".png", "wb") as f:
                        f.write(image_content.content)
                    return {"question": question, "image_path": image_path + ".png"}


def main():
    client = get_openai_client()

    math_assistant = setup_openai_assistant(client)
    print(f"Created assistant: {math_assistant}")

    thread = create_thread(client)
    print(f"Created thread: {thread}")

    send_question(client, thread.id)

    created_run = create_thread_run(client, thread.id, math_assistant.id)
    print(f"Created run: {created_run}")

    run = handle_run_completion(client, thread.id, created_run)
    print(f"Run completed: {run}")

    output = extract_content(client, thread.id)
    print(output)
    return output


output = main()
print(output)
