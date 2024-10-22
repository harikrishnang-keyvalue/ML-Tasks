from openai import OpenAI
from typing import Optional, TypeVar, Type
import dotenv
import json
import os

dotenv.load_dotenv()

T = TypeVar("T")


def get_openai_response(
        prompt: str,
        model: str = "gpt-4o",
        image_urls: Optional[list[str]] = None,
):
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                        organization=os.environ["OPENAI_ORGANIZATION_ID"])

        messages = [
            {"role": "system", "content": prompt}
        ]

        if image_urls:
            for url in image_urls:
                messages.append({
                    "role": "user",
                    "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                            "url": url
                                    }
                                }
                                ]
                })

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if content is not None:
            return json.loads(content)

        return content
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None


def get_openai_structured_response(
    prompt: str,
    response_format: Type[T],
    model: str = "gpt-4o-2024-08-06",
    image_url: Optional[str] = None,
    image_urls: Optional[list[str]] = None,
    encoded_image: Optional[str] = None,
) -> T:
    """
    Get the structured response from the OpenAI API.
    :param prompt: The prompt to send to the API.
    :param image_url: (Optional) The URL of the image to be sent to the model.
    :param image_urls: (Optional) The list of URLs of the images to be sent to the model.
    :param encoded_image: (Optional) The base64 encoded image to be sent to the model.
    :param logger: The logger instance.
    :param response_format: The format of the structured response.
    :return The response from the OpenAI API.
    """
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                        organization=os.environ["OPENAI_ORGANIZATION_ID"])

        messages = [
            {"role": "system", "content": prompt}
        ]

        if encoded_image or image_url:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}" if encoded_image else image_url
                        }
                    }
                ]
            })

        if image_urls:
            for url in image_urls:
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ]
                })

        response = client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format
        )

        content = response.choices[0].message.parsed

        return content
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None
