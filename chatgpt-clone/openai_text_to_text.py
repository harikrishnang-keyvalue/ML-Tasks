from openai import OpenAI
from typing import Optional
import dotenv
import json
import os

dotenv.load_dotenv()


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
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content

        if content is not None:
            return json.loads(content)

        return content
    except Exception as e:
        print(f"Error getting response from the AI model: {e}")
        return None
