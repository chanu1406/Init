"""
Drill Models

Responsibility: Pydantic models for drill-related database entities.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DrillType(str, Enum):
    """Types of drills supported by the system."""

    QUIZ = "quiz"
    EXPLAIN = "explain"
    DEBUG = "debug"


class RubricCriterion(BaseModel):
    """A single criterion in a grading rubric."""

    name: str
    description: str
    max_score: int = Field(ge=1, le=10)


class DrillRubric(BaseModel):
    """Complete rubric for grading a drill."""

    criteria: list[RubricCriterion]
    expected_key_points: list[str]
    common_mistakes: list[str] = []
    followup_questions: list[str] = []
    model_answer_outline: list[str] = []


class Drill(BaseModel):
    """
    Drill entity model.
    Represents an atomic learning action.
    """

    id: str
    unit_id: str
    slug: str
    drill_type: DrillType
    prompt_markdown: str
    rubric: DrillRubric
    difficulty: int = Field(ge=1, le=5)
    estimated_minutes: int = Field(ge=1)
    concept_tags: list[str] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DrillSummary(BaseModel):
    """
    Lightweight drill model for list views.
    """

    id: str
    slug: str
    drill_type: DrillType
    difficulty: int
    estimated_minutes: int
    concept_tags: list[str] = []


class UserDrillProgress(BaseModel):
    """
    Tracks a user's progress on a specific drill.
    """

    id: str
    user_id: str
    drill_id: str
    mastery_score: int = Field(ge=0, le=5)
    attempt_count: int = 0
    last_attempt_at: datetime | None = None
    next_review_due_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DrillAttempt(BaseModel):
    """
    Record of a single drill attempt.
    """

    id: str
    user_id: str
    drill_id: str
    user_response: str
    ai_feedback: dict[str, Any]
    score: int | None = None
    max_score: int | None = None
    created_at: datetime


# ============================================================================
# API Request/Response Models
# ============================================================================


class DrillAttemptRequest(BaseModel):
    """Request model for submitting a drill attempt."""

    user_response: str = Field(
        min_length=10,
        description="The user's submitted answer to the drill"
    )


class DrillAttemptResponse(BaseModel):
    """Response model for drill attempt submission."""

    attempt_id: str
    drill_id: str
    total_score: int
    max_score: int
    feedback: str
    strengths: list[str]
    improvements: list[str]
    follow_up_question: str | None = None
    mastery_score: int = Field(ge=0, le=5, description="Updated mastery level")
    created_at: datetime
