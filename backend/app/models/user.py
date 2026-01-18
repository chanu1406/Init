"""
User Models

Responsibility: Pydantic models for user-related database entities.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    User entity model.
    Note: Auth is handled by Supabase; this is for profile data.
    """

    id: str
    email: EmailStr
    created_at: datetime


class UserPreferences(BaseModel):
    """
    User preferences stored in the database.
    TODO: Define preference schema
    """

    user_id: str
    daily_drill_count: int = 3
    notifications_enabled: bool = True
    preferred_time: str | None = None  # e.g., "09:00"
