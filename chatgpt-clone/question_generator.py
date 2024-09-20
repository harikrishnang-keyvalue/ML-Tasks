import json
import time

from openai_text_to_text import get_openai_response
from prompts import QUESTION_GENERATOR_PROMPT

prompt = QUESTION_GENERATOR_PROMPT

question_generator_input = {
    "class": "3",
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
