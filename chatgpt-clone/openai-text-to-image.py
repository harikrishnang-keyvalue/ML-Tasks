from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()


def get_openai_image_response(prompt: str):
    try:

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                        organization=os.environ["OPENAI_ORGANIZATION_ID"])

        response = client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            n=1,
            quality="standard",
            size="1024x1024",
            style="natural",
        )

        image_url = response.data[0]

        return image_url
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None


prompt = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: Generate an image where two stacked boxes of light snacks are placed to the left of two stacked boxes containing sandwiches. The boxes of light snacks are transparent and show compartments with items like fries and sliced fruits. The sandwich boxes are also transparent and contain sandwiches with lettuce, tomato, and meat."
image_url = get_openai_image_response(prompt)
print(image_url)
