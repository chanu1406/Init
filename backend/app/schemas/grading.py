"""
Grading Schemas

Responsibility: Schemas for grading-related data structures.
"""

from pydantic import BaseModel


class GradingRequest(BaseModel):
    """Internal request to grade a response (not an API schema)."""

    drill_id: str
    prompt: str
    rubric: dict
    user_response: str


class GradingResult(BaseModel):
    """Result of grading a drill response."""

    scores: list[dict]
    total_score: int
    max_score: int
    justification: str
    improvement_suggestion: str
    follow_up_question: str | None = None
    mastery_delta: int
