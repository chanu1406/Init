"""
Track Models

Responsibility: Pydantic models for track and unit database entities.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Track(BaseModel):
    """
    Track entity model.
    High-level learning path (e.g., systems-foundations).
    """

    id: str
    slug: str
    title: str
    description: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TrackSummary(BaseModel):
    """
    Lightweight track model for list views.
    """

    id: str
    slug: str
    title: str
    description: str


class Unit(BaseModel):
    """
    Unit entity model.
    Ordered section within a track.
    """

    id: str
    track_id: str
    order_index: int = Field(ge=0)
    title: str
    summary_markdown: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UnitSummary(BaseModel):
    """
    Lightweight unit model for list views.
    """

    id: str
    order_index: int
    title: str


class UnitWithDrillCount(BaseModel):
    """
    Unit with drill count for track detail views.
    """

    id: str
    order_index: int
    title: str
    summary_markdown: str
    drill_count: int = 0
