import os
import base64
import dotenv
import json
import google.generativeai as genai

dotenv.load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def detect_document():
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    prompt = """You are a teacher assistant who evaluates and grades homeworks given to school students.
        **Task:** Automated Homework Evaluation and Grading
        **Inputs:**
                * Subject of the homework: {subject}
                * Question: {question}
                * Answer: The final answer submitted by the student: {answer}
                * Evaluation Criteria (Optional): A set of rules or guidelines for awarding marks: {evaluation_criteria}
                * Worksheet (Optional): LaTex representation of the student's handwritten homework, detailing the steps taken to reach the answer: {worksheet}
                * Maximum Marks: The maximum marks that can be awarded for the question: {maximum_marks}
        **Instructions:**
                * Perform arithmetic calculations as necessary to verify the correctness of the student's answer.
                * Evaluate the student's answer based on the correctness and completeness of their response.
        **Output:**
                * Return the result in a valid JSON format, without markdown, with the following structure:
                "final_grade": The final grade awarded to the student based on their answer, and steps in the worksheet, if provided. (Eg: "3")
                "marks_breakdown": A detailed breakdown of the marks awarded for each evaluation criteria.
                "feedback": Constructive, motivational feedback for the student based on the evaluation.
        **Grading Rules:**
                * If evaluation criteria are not provided, award 1 marks for the correctness of the answer, and the rest of the marks for the correct method/steps.
                * If the worksheet is not provided, evaluate the answer based on the following criteria:
                        * Award 2 marks if the answer is correct and has the required units.
                        * Award 1 marks if the answer is correct but the required units are missing.
                        * Award zero marks if the answer is incorrect.
                        * When awarding partial marks, specify that the answer is correct but the units are missing.
                * Awarded marks must be in whole numbers.
                * Feedback should be constructive, motivating, and provide guidance on how to improve the answer.
"""
    final_prompt = prompt.format(
        subject="Mathematics",
        question="Calculate the area of the circle with radius 10cm.",
        answer="314.16 sq.cm.",
        evaluation_criteria=None,
        worksheet=None,
        maximum_marks="3",
    )

    response = model.generate_content(
        contents=[
            final_prompt,
        ]
    )
    print(json.loads(response.candidates[0].content.parts[0].text))


detect_document()
