import json
import shutil

from enum import Enum

from openai_text_to_text import get_openai_response
from prompts import QUESTION_VARIANTS_GENERATION_PROMPT


class QuestionTypes(Enum):
    SHORT_ANSWER = "Short Answer"
    LONG_ANSWER = "Long Answer"
    MCQ = "MCQ"


def get_question_variants(
    question_id: str,
    question: str,
    question_type=QuestionTypes,
    question_images: list[str] = [],
    subject: str = "",
    difficulty: str = "",
    total_variants: int = 1,
):
    """
    Generate question variants based on the original question.
    :param question: The original question to generate variants for.
    :param question_id: The ID of the original question.
    :param question_type: The type of the original question. (MCQ, Short Answer, Long Answer)
    :param subject: The subject of the original question.
    :param difficulty: The difficulty level of the original question.
    :param total_variants: The desired number of question variants.
    :return: A dictionary containing the question ID, the generated variants, and any errors.
    """

    model = "gpt-4o"

    if not question:
        raise ValueError("Question cannot be empty.")

    try:
        variant_prompt = QUESTION_VARIANTS_GENERATION_PROMPT

        prompt = variant_prompt.format(
            question=question,
            question_images=question_images,
            subject=subject,
            question_type=question_type,
            difficulty=difficulty,
            total_variants=total_variants,
        )

        response = get_openai_response(
            prompt=prompt,
            model=model,
        )

        print(response)

        if response is None:
            raise ValueError("No response from AI model.")

        return response

    except (KeyError, IndexError) as e:
        error_message = f"Error parsing AI response: {str(e)}"
    except ValueError as e:
        error_message = f"Error: {str(e)}"
    except Exception as e:
        error_message = f"Error: {str(e)}"

    print(f"Question ID: {question_id} {error_message}")
    return []


variants = get_question_variants(
    question_id="1",
    question_type=QuestionTypes.SHORT_ANSWER,
    subject="Mathematics",
    difficulty="AO1",
    question="In a survey about favorite sports, 25% chose soccer and 35% chose basketball. What percentage chose other sports?",
    question_images=["https://www.imghippo.com/i/CWZBQ1727352365.png"],
    total_variants=3,
)
# write the variants to a file
with open("variants.json", "w") as f:
    f.write(json.dumps(variants))

for variant in variants.get("variants", []):
    diagrams = variant.get("diagrams", [])
    if diagrams:
        for diagram in diagrams:
            exec(diagram)
            # upload to s3 and get the url

    # delete the tmp folder even if there are files in it
    # shutil.rmtree("tmp")
