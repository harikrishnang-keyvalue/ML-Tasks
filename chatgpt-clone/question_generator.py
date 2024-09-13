import json
from openai_text_to_text import get_openai_response
from prompts import QUESTION_GENERATOR_PROMPT


prompt = QUESTION_GENERATOR_PROMPT

question_generator_input = {
    "class": "3",
    "topic": "Percentage",
    "skills": ["Finding a percentage of a quantity",
               "Express a part of a whole as a percentage",
               "Express fractions and decimals as percentages",
               "Express percentages as fractions and decimals",
               "Solve problems involving discount",
               "Solve problems involving GST",
               "Solve problems involving annual interest",
               "Finding a percentage part of a whole"],
    "difficulties": ["A01", "A02", "A03"],
    "question_types": ["MCQ", "Short Answer", "Long Answer"],
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
print(response)
