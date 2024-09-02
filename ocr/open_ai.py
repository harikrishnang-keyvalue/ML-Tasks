from openai import OpenAI
import base64
import requests
import dotenv
import os

dotenv.load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                organization=os.environ["OPENAI_ORGANIZATION_ID"])
prompt = """You are an expert at performing OCR on handwritten text.
        **Task:** Optical Character Recognition and LaTex Conversion
        **Input:** An image containing handwritten homework in the subject {subject}.
        **Subject Specifics:**
                * **Math:** May include geometric shapes, symbols, English language steps, and mathematical formulas.
                * **Science:** May include diagrams, chemical formulas, and scientific terms.
                * **English:** May include grammar, punctuation, and sentence structure.
        **Output:** A complete LaTex document containing the extracted expression from the handwritten homework. The output should strictly 
        start with \documentclass article and end with \end document.
        **Rules:**
                * You must represent the input content as it is. Do not correct any errors in the handwriting.
                * If the handwriting is unclear, return the error message "Error: Image is unclear".
                * If the input image is not a handwritten homework, return the error message "Error: Image is not of a handwritten homework".
"""
image1 = requests.get(
    "https://storage.cloud.google.com/vertexai-test-subtle-chimera-424908-r4/test_1.JPEG"
)
image2 = requests.get(
    "https://storage.cloud.google.com/vertexai-test-subtle-chimera-424908-r4/test_2.JPEG"
)
image1 = encode_image("test_1.JPEG")
image2 = encode_image("test_2.JPEG")
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt.format(subject="Math"),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image1}"},
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image2}"},
                },
            ],
        },
    ],
    model="gpt-4o",
)
# print(response.headers.get("X-My-Header"))

completion = response.choices[
    0
].message.content  # get the object that `chat.completions.create()` would have returned
print(completion)
