from openai import OpenAI
import base64
import dotenv
import os

dotenv.load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                organization=os.environ["OPENAI_ORGANIZATION_ID"])
prompt = """Consider yourself as a mathematics teacher of 6th grade. Can you give 15 MCQ questions which carries 1 mark each, 15 short 
    answer questions having  2 mark each and 15 long answer questions which carries 4 mark each on the topic Mean, Median, and Mode. For MCQ questions 
    list 4 options. Also solve the questions and give answers for all of the questions including MCQ, Short Answer and Long Answer. The answers 
    should not be in fractions."""
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
    ],
    model="gpt-4o",
)
# print(response.headers.get("X-My-Header"))

completion = response.choices[
    0
].message.content  # get the object that `chat.completions.create()` would have returned
print(completion)
