from openai import OpenAI
from pydantic import BaseModel

from typing import Optional

import dotenv
import json
import os

dotenv.load_dotenv()


def get_openai_response(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    image_url: Optional[str] = None,
    image_urls: Optional[list[str]] = None,
    encoded_image: Optional[str] = None,
    is_json_response: bool = True,
):
    """
    Get the response from the OpenAI API.
    :param prompt: The prompt to send to the API.
    :param image_url: (Optional) The URL of the image to be sent to the model.
    :param image_urls: (Optional) The list of URLs of the images to be sent to the model.
    :param encoded_image: (Optional) The base64 encoded image to be sent to the model.
    :param is_json_response: Whether the response should be parsed as JSON.
    :param logger: The logger instance.
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

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"} if is_json_response else {
                "type": "text"}
        )

        content = response.choices[0].message.content

        if content is not None and is_json_response:
            return json.loads(content)

        return content
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None


def get_openai_structured_response(
    prompt: str,
    model: str = "gpt-4o-2024-08-06",
    response_format: BaseModel = BaseModel,
    image_url: Optional[str] = None,
    image_urls: Optional[list[str]] = None,
    encoded_image: Optional[str] = None,
):
    """
    Get the response from the OpenAI API.
    :param prompt: The prompt to send to the API.
    :param image_url: (Optional) The URL of the image to be sent to the model.
    :param image_urls: (Optional) The list of URLs of the images to be sent to the model.
    :param encoded_image: (Optional) The base64 encoded image to be sent to the model.
    :param is_json_response: Whether the response should be parsed as JSON.
    :param logger: The logger instance.
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
            response_format=response_format,
        )

        content = response.choices[0].message.parsed

        print(content)

        return content
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None
