import json
import time

from openai_text_to_text import get_openai_response
from prompts import MATHS_QUESTION_GENERATOR_PROMPT, ENGLISH_QUESTION_GENERATOR_PROMPT


def maths_question_generator():
    prompt = MATHS_QUESTION_GENERATOR_PROMPT
    question_generator_input = {
        "class": "3",
        "subject": "Mathematics",
        "topic": "Pie Charts",
        "skills": [
            "Solve problem using data given in a Pie Chart, involving fractions",
            "Solve problem using data given in a Pie Chart, involving percentage"
        ],
        "difficulties": [
            "A01",
            "A02",
            "A03"
        ],
        "question_types": [
            "MCQ",
            "Short Answer",
            "Long Answer"
        ],
        "number_of_questions": {
            "mcq": 4,
            "short_answer": 3,
            "long_answer": 3
        },
        "marks": {
            "mcq": 1,
            "short_answer": 2,
            "long_answer": 4,
            "total": 22
        }
    }

    start_time = time.time()
    response = get_openai_response(prompt.format(
        input=json.dumps(question_generator_input)))
    end_time = time.time()
    # print difference of time in seconds
    print(f"Time taken: {end_time - start_time} seconds")
    # save the response to a file
    with open("response.json", "w") as f:
        json.dump(response, f)

    for question in response['questions']:
        diagrams = question.get('diagrams')
        if diagrams:
            for diagram in diagrams:
                if diagram:
                    exec(diagram)


def english_question_generator():
    prompt = ENGLISH_QUESTION_GENERATOR_PROMPT
    question_generator_input = {
        "class": "3",
        "subject": "English",
        "topic": "Multiple-meaning words",
        "skills": [
            "Multiple-meaning words with pictures",
            "Which definition matches the sentence?",
            "Which sentence matches the definition?"
        ],
        "difficulties": [
            "A01",
            "A02",
            "A03"
        ],
        "question_types": [
            "MCQ",
            "Short Answer",
            "Long Answer"
        ],
        "number_of_questions": {
            "mcq": 4,
            "short_answer": 3,
            "long_answer": 3
        },
        "marks": {
            "mcq": 1,
            "short_answer": 2,
            "long_answer": 4,
            "total": 22
        }
    }

    start_time = time.time()
    response = get_openai_response(prompt.format(
        input=json.dumps(question_generator_input)))
    end_time = time.time()
    # print difference of time in seconds
    print(f"Time taken: {end_time - start_time} seconds")
    # save the response to a file
    with open("response.json", "w") as f:
        json.dump(response, f)

    # # Generate images from image_options and question_images using flux models (creative images)
    # for question in response['questions']:
    #     for question_image in response['question_images']:
    #         # generate image from question_image using flux model
    #     for image_option in response['image_options']:
    #         # generate image from image_option using flux model

    # for question in response['questions']:
    #     diagrams = question.get('diagrams')
    #     if diagrams:
    #         for diagram in diagrams:
    #             if diagram:
    #                 exec(diagram)


maths_question_generator()
english_question_generator()
