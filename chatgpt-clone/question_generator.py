import json
import matplotlib.pyplot as plt

from openai_text_to_text import get_openai_response
from prompts import QUESTION_GENERATOR_PROMPT

prompt = QUESTION_GENERATOR_PROMPT

question_generator_input = {
    "class": "3",
    "topic": "Circles",
    "skills": [
        "Find area of composite figures made of circles and other shapes", "Given radius, find perimeter of a quadrant or semicircle", "Given number of turns & diameter, find distance travelled", "Given radius, find total area of quadrants or semicircles", "Given side of square, find area of the figure", "Given radius, find shaded area of the figure", "Find area for patterns involving circles and triangles", "Given perimeter, find area of a circle", "Find perimeter of composite figures made of circles and other shapes"
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

response = get_openai_response(prompt.format(
    input=json.dumps(question_generator_input)))

# save the response to a file
with open("response.json", "w") as f:
    json.dump(response, f)

for question in response['questions']:
    diagrams = question.get('diagrams')
    if diagrams:
        for diagram in diagrams:
            if diagram:
                exec(diagram)
