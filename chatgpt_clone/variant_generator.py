import json
import shutil
from pydantic import BaseModel
from typing import Optional

from enum import Enum

from chatgpt_clone.openai_text_to_text import get_openai_structured_response
from chatgpt_clone.prompts import QUESTION_VARIANTS_GENERATION_PROMPT, QUESTION_VARIANT_REPLACEMENT_INPUT_PROMPT


class AnswerInfo(BaseModel):
    answer: str
    is_correct: bool


class QuestionVariant(BaseModel):
    question_number: int
    question: str
    answers: list[AnswerInfo]
    diagrams: Optional[list[str]]


class Variants(BaseModel):
    variants: list[QuestionVariant]


class QuestionTypes(Enum):
    SHORT_ANSWER = "Short Answer"
    LONG_ANSWER = "Long Answer"
    MCQ = "MCQ"


class VariantGenerationFlowTypes(Enum):
    VARIANT_GENERATION = "VARIANTS_GENERATION"
    REPLACEMENT_GENERATION = "REPLACEMENT_GENERATION"


def get_question_variants(
    event_type: str,
    question_id: str,
    question: str,
    question_type=QuestionTypes,
    question_images: list[str] = [],
    subject: str = "",
    topic: str = "",
    skills: list[str] = [],
    difficulty: str = "",
    total_variants: int = 1,
    rejected_variant: Optional[str] = None,
    rejection_reason: Optional[str] = None,
) -> Variants:
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

    if not question:
        raise ValueError("Question cannot be empty.")

    try:
        if event_type == VariantGenerationFlowTypes.REPLACEMENT_GENERATION:
            prompt = QUESTION_VARIANT_REPLACEMENT_INPUT_PROMPT.format(
                subject=subject,
                topic=topic,
                skills=skills,
                question_type=question_type,
                difficulty=difficulty,
                question=question,
                question_images=question_images,
                rejected_variant=rejected_variant,
                rejection_reason=rejection_reason,
            )
        else:
            prompt = QUESTION_VARIANTS_GENERATION_PROMPT.format(
                subject=subject,
                question=question,
                question_images=question_images,
                topic=topic,
                skills=skills,
                question_type=question_type,
                difficulty=difficulty,
                total_variants=total_variants,
            )

        response = get_openai_structured_response(
            prompt=prompt,
            response_format=Variants,
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
    return Variants(variants=[])


def generate_variants():
    variants = get_question_variants(
        event_type=VariantGenerationFlowTypes.VARIANT_GENERATION,
        question_id="1",
        question_type=QuestionTypes.SHORT_ANSWER,
        subject="Mathematics",
        topic="Pie Charts",
        skills=["Solve problem using data given in a Pie Chart, involving percentage"],
        difficulty="AO1",
        question="In a survey about favorite sports, 25% chose soccer and 35% chose basketball. What percentage chose other sports?",
        question_images=["https://www.imghippo.com/i/CWZBQ1727352365.png"],
        total_variants=3,
    )

    # write the variants to a file
    with open("variants.json", "w") as f:
        f.write(json.dumps(variants.model_dump_json()))

    for variant in variants.variants:
        diagrams = variant.diagrams
        if diagrams:
            for diagram in diagrams:
                exec(diagram)
        # upload to s3 and get the url

        # delete the tmp folder even if there are files in it
        # shutil.rmtree("tmp")


def generate_replacements():
    variants = get_question_variants(
        event_type=VariantGenerationFlowTypes.REPLACEMENT_GENERATION,
        question_id="1",
        question_type=QuestionTypes.SHORT_ANSWER,
        subject="Mathematics",
        topic="Pie Charts",
        skills=["Solve problem using data given in a Pie Chart, involving percentage"],
        difficulty="AO1",
        question="In a survey about favorite sports, 25% chose soccer and 35% chose basketball. What percentage chose other sports?",
        question_images=["https://www.imghippo.com/i/CWZBQ1727352365.png"],
        rejected_variant="In a survey about favorite sports, 25% chose soccer. What percentage chose basketball?",
        rejection_reason="The question is incomplete.",
    )

    # write the variants to a file
    with open("variants.json", "w") as f:
        f.write(json.dumps(variants.model_dump_json()))

    for variant in variants.variants:
        diagrams = variant.diagrams
        if diagrams:
            for diagram in diagrams:
                exec(diagram)
        # upload to s3 and get the url

        # delete the tmp folder even if there are files in it
        # shutil.rmtree("tmp")


generate_replacements()
