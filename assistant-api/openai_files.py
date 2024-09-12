import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()


def get_openai_client():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                    organization=os.environ["OPENAI_ORGANIZATION_ID"])
    return client


client = get_openai_client()
image_content = client.files.content("file-ShhqAY34Rq01GsufmORJUPqa")
with open("output.png", "wb") as f:
    f.write(image_content.content)
print(image_content)
