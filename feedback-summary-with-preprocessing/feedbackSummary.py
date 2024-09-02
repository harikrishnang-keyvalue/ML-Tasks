from openai_utils import get_openai_structured_response
from models import StudentIndividualHomeworkReport
from prompts import STUDENT_INDIVIDUAL_HOMEWORK_ANALYSIS_GENERATION_PROMPT


def get_student_individual_assignment_analysis(
    unique_id: str,
    topics: list[str],
    skills: list[str],
    marks: int,
    maximum_marks: int,
    feedbacks: list[str],
    error_types: dict[str, str],
) -> dict:

    try:

        if not topics or not skills or not maximum_marks or not error_types:
            print(f"{unique_id} Invalid input.")
            raise ValueError("Invalid input.")

        model = "gpt-4o-2024-08-06"

        analysis_prompt = STUDENT_INDIVIDUAL_HOMEWORK_ANALYSIS_GENERATION_PROMPT

        prompt = analysis_prompt.format(
            topics=topics,
            skills=skills,
            marks=marks,
            maximum_marks=maximum_marks,
            feedbacks=feedbacks,
            error_types=error_types
        )

        print(prompt)

        response = get_openai_structured_response(
            prompt=prompt,
            model=model,
            response_format=StudentIndividualHomeworkReport,
        )

        print(response)

        if response is None:
            raise ValueError("No response from AI model.")

        assignment_summary = response.get("assignment_summary")
        assignment_errors = response.get("assignment_errors")
        strengths = response.get("strengths")
        weaknesses = response.get("weaknesses")

        print(
            f"""Student Individual Homework Analysis for {unique_id}:
            Assignment Summary: {assignment_summary}
            Strengths: {strengths}
            Weaknesses: {weaknesses}
            Assignment Errors: {assignment_errors}""")

        common_errors = []
        common_errors = [{
            "type": error['error_type'],
            "percentageValue": (error['value'] * 100)/len(feedbacks) if len(feedbacks) > 0 else 0,
        } for error in assignment_errors]

        print(
            f"""Student Individual Homework Analysis for {unique_id}: 
            Assignment Summary: {assignment_summary}
            Strengths: {strengths}
            Weaknesses: {weaknesses}
            Common Errors: {common_errors}""")
        return {"assignmentSummary": assignment_summary, "commonErrorTypes": common_errors, "strengths": strengths, "weaknesses": weaknesses, "error": ""}

    except ValueError as e:
        error_message = f"Error: {str(e)}"
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"

    print(f"{unique_id} {error_message}")
    return {"assignmentSummary": "", "commonErrorTypes": "", "strengths": "", "weaknesses": "", "error": error_message}


get_student_individual_assignment_analysis(
    "1-1",
    [
        "Mean, Median, and Mode"
    ],
    [
        "Mean, Median, and Mode"
    ],
    12, 14,
    [
        "Thank you for your effort. The denominator is the number below the line in a fraction. In this case, the correct answer is 8. Review the definition of 'denominator' and try again. Keep up the good work and don't give up"
    ],
    {
        "Conceptual": "The student had trouble understanding the concept.",
        "Calculation": "The student made a calculation error.",
        "Measurement": "The student missed including units in their answer.",
        "Explanation": "The student did not provide the steps or explanation."
    }
)
