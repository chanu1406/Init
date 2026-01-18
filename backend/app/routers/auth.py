"""
Authentication Router

Responsibility: Handles authentication-related endpoints.
Note: Primary auth is handled by Supabase client-side.
This router handles server-side auth utilities.

TODO: Add token verification endpoint
TODO: Add user profile endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_current_user():
    """
    Get the current authenticated user's profile.
    TODO: Implement with CurrentUserId dependency
    TODO: Fetch user profile from database
    """
    # TODO: Implement
    return {"message": "Not implemented"}


@router.post("/verify")
async def verify_token():
    """
    Verify a Supabase JWT token.
    TODO: Implement token verification
    """
    # TODO: Implement
    return {"valid": False, "message": "Not implemented"}
