from enum import Enum
from pydantic import BaseModel


class QuestionType(str, Enum):
    mcq = "MCQ"
    short_answer = "Short Answer"
    long_answer = "Long Answer"


class AssignmentError(BaseModel):
    error_type: str
    value: int


class QuestionTypePerformance(BaseModel):
    type: QuestionType
    total_marks: int
    marks_sum: int


class StudentIndividualHomeworkReport(BaseModel):
    assignment_summary: str
    strengths: list[str]
    weaknesses: list[str]
    assignment_errors: list[AssignmentError]
