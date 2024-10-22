import os
import json

from typing import Optional
import anthropic
from anthropic.types import ContentBlock


def get_claude_ai_response(
    prompt: str,
    model: str = "claude-3-5-sonnet-20240620",
    image_urls: Optional[list[str]] = None,
):
    """
    Get the response from the Claude AI API.
    :param prompt: The prompt to send to the API.
    :param logger: The logger instance.
    :param model: The model to use for generating the response.
    :param image_urls: (Optional) The list of URLs of the images to be sent to the model.
    :return The response from the Google AI API.
    """
    try:
        client = anthropic.Anthropic(
            api_key=os.environ["CLAUDE_API_KEY"],
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please provide your response based on the system prompt."
                    }
                ]
            }
        ]

        if image_urls:
            for image in image_urls:
                messages[0]["content"].append({
                    "type": "image",
                    "source": {
                        "type": "base64" if image.startswith("data:image") else "url",
                        "data": image
                    }
                })

        message = client.messages.create(
            temperature=0.2,
            system=prompt,
            messages=messages,
            model=model,
        )

        text_block = next(
            (block for block in message.content if isinstance(block, ContentBlock)), None)
        if text_block:
            json_string = text_block.text
            return json.loads(json_string)
        else:
            print("No text content found in the response")
            return None
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None
