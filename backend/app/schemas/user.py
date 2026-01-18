"""
User Schemas

Responsibility: Request and response schemas for user endpoints.
"""

from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    """Public user profile information."""

    id: str
    email: EmailStr


class UserPreferencesUpdate(BaseModel):
    """Request to update user preferences."""

    daily_drill_count: int | None = None
    notifications_enabled: bool | None = None
    preferred_time: str | None = None
