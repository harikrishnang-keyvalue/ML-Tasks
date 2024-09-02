from openai_utils import get_openai_response
from typing import List
from dataclasses import dataclass


@dataclass
class StudentFeedbackInput:
    topics: str
    skills: str
    marks: int
    maximum_marks: int


STUDENT_ALL_HOMEWORKS_FEEDBACK_GENERATION_PROMPT = """
        You are a teacher's assistant who is an expert at generating feedback of students based on their performance.
        **Task:** Generate Student Feedback
        **Inputs:**
                * Input: {input}
                * The input is a list of JSON objects in which each object contains the following keys:
                        * "topics": The topics of the assignment.
                        * "skills": A list of skills.
                        * "marks": The marks obtained by the student.
                        * "maximumMarks": The maximum marks that can be obtained.
        **Output:**
                * Return the result in a valid JSON format, without markdown, with the following structure:
                "feedback": A summarized, encouraging, constructive feedback for the student's report card in not more than 5 sentences.
        **Rules:**
                * The feedback summary should be concise, encouraging and highlight the student's strengths and weaknesses.
                * The feedback should be based on the given list of inputs which contain the student's performance in different topics and skills.
                * The feedback must be accurate. Do not hallucinate or make up data.
"""


def get_student_feedback(
    unique_id: str,
    input: List[StudentFeedbackInput],
) -> dict:
    """
    Generate summarized analysis of students based on their performance.
    :param unique_id: The unique ID for the analysis.
    :param input: A list of dictionaries containing the student's performance data.
    :return: A dictionary containing the feedback summary, or an error message.
    """

    if not input:
        print(f"{unique_id} Invalid input.")
        return {"summary": "", "strengths": "", "weaknesses": "", "error": "Invalid input."}

    model = "gpt-4o"

    analysis_prompt = STUDENT_ALL_HOMEWORKS_FEEDBACK_GENERATION_PROMPT

    try:
        prompt = analysis_prompt.format(
            input=input
        )

        response = get_openai_response(
            prompt=prompt,
            model=model
        )

        if response is None:
            print(
                f"{unique_id} Error generating student analysis: No response from AI model.")
            return {"feedback": "", "error": "No response from AI model."}

        feedback = response.get("feedback")

        print(
            f"""Student Analysis for {unique_id}: 
            Feedback: {feedback}""")
        return {"feedback": feedback, "error": ""}

    except (KeyError, IndexError) as e:
        error_message = f"Error parsing AI response: {str(e)}"
    except Exception as e:
        error_message = f"Error: {str(e)}"
    print(f"{unique_id} {error_message}")
    return {"feedback": "", "error": error_message}


get_student_feedback("1-1", [
    {
        "topics": "Mean, Median, and Mode",
        "skills": "Mean, Median, and Mode",
        "marks": 0,
        "maximum_marks": 4
    },
    {
        "topics": "Numbers",
        "skills": "Subtraction",
        "marks": 4,
        "maximum_marks": 4
    },
    {
        "topics": "Numbers",
        "skills": "Addition",
        "marks": 4,
        "maximum_marks": 4
    },
    {
        "topics": "Numbers",
        "skills": "Multiplication",
        "marks": 2,
        "maximum_marks": 4
    },
    {
        "topics": "Numbers",
        "skills": "Division",
        "marks": 2,
        "maximum_marks": 4
    }
])
