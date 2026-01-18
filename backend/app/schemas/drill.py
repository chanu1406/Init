"""
Drill Schemas

Responsibility: Request and response schemas for drill endpoints.
"""

from typing import Any

from pydantic import BaseModel

from app.models.drill import Drill


class DrillResponse(BaseModel):
    """Response for getting a drill."""

    drill: Drill | None
    remaining_count: int
    completed_today: int


class SubmitDrillRequest(BaseModel):
    """Request to submit a drill response for grading."""

    drill_id: str
    response: str


class CriterionScore(BaseModel):
    """Score for a single rubric criterion."""

    criterion: str
    score: int
    max_score: int
    feedback: str


class AIFeedback(BaseModel):
    """Structured AI feedback on a drill response."""

    scores: list[CriterionScore]
    total_score: int
    max_score: int
    justification: str
    improvement: str
    follow_up_question: str | None = None


class SubmitDrillResponse(BaseModel):
    """Response after submitting a drill for grading."""

    attempt_id: str
    feedback: AIFeedback
    new_mastery_score: int
    next_review_due_at: str
