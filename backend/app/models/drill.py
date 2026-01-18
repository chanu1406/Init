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
    max_score: int = Field(ge=1, le=5)


class DrillRubric(BaseModel):
    """Complete rubric for grading a drill."""

    criteria: list[RubricCriterion]
    expected_key_points: list[str]
    common_mistakes: list[str]


class Drill(BaseModel):
    """
    Drill entity model.
    Represents an atomic learning action.
    """

    id: str
    unit_id: str
    drill_type: DrillType
    prompt_markdown: str
    rubric: DrillRubric
    difficulty: int = Field(ge=1, le=5)
    estimated_minutes: int = Field(ge=1)
    concept_tags: list[str] = []


class UserDrillProgress(BaseModel):
    """
    Tracks a user's progress on a specific drill.
    """

    id: str
    user_id: str
    drill_id: str
    mastery_score: int = Field(ge=0, le=5)
    last_attempt_at: datetime
    next_review_due_at: datetime


class DrillAttempt(BaseModel):
    """
    Record of a single drill attempt.
    """

    id: str
    user_id: str
    drill_id: str
    user_response: str
    ai_feedback: dict[str, Any]
    created_at: datetime
