"""
Content Schema Validation Models

Responsibility: Pydantic models for validating content JSON files.
Used by the seeding script to ensure content integrity before database sync.
"""

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class DrillType(str, Enum):
    """Types of drills supported by the system."""

    QUIZ = "quiz"
    EXPLAIN = "explain"
    DEBUG = "debug"


class RubricCriterion(BaseModel):
    """A single criterion in a grading rubric."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    max_score: int = Field(..., ge=1, le=10)


class DrillRubric(BaseModel):
    """Complete rubric for grading a drill."""

    criteria: list[RubricCriterion] = Field(..., min_length=1)
    expected_key_points: list[str] = Field(..., min_length=1)
    common_mistakes: list[str] = Field(default_factory=list)
    followup_questions: list[str] = Field(default_factory=list)
    model_answer_outline: list[str] = Field(default_factory=list)


class TrackContent(BaseModel):
    """Schema for track.json files."""

    slug: str = Field(..., pattern=r"^[a-z0-9-]+$", min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)


class UnitContent(BaseModel):
    """Schema for unit JSON files."""

    track_slug: str = Field(..., pattern=r"^[a-z0-9-]+$")
    order_index: int = Field(..., ge=0)
    title: str = Field(..., min_length=1, max_length=200)
    summary_markdown: str = Field(default="")


class DrillContent(BaseModel):
    """Schema for drill JSON files."""

    slug: str = Field(..., pattern=r"^[a-z0-9-]+$", min_length=1, max_length=100)
    unit_order_index: int = Field(..., ge=0)
    drill_type: DrillType
    prompt_markdown: str = Field(..., min_length=10)
    difficulty: int = Field(..., ge=1, le=5)
    estimated_minutes: int = Field(..., ge=1, le=60)
    concept_tags: list[str] = Field(..., min_length=1)
    rubric: DrillRubric

    @field_validator("concept_tags")
    @classmethod
    def validate_concept_tags(cls, v: list[str]) -> list[str]:
        """Ensure concept tags are lowercase and hyphenated."""
        validated = []
        for tag in v:
            # Normalize tag
            normalized = tag.lower().strip()
            if not normalized:
                raise ValueError("Empty concept tag")
            validated.append(normalized)
        return validated


# Type aliases for clarity
Slug = Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
