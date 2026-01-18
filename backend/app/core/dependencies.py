"""
FastAPI Dependencies

Responsibility: Provides dependency injection for route handlers.
Includes auth verification, database clients, and service instances.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

# TODO: Import Supabase client
# TODO: Import service classes


async def get_current_user_id(
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    """
    Extracts and validates the current user from the Authorization header.

    TODO: Implement JWT verification with Supabase
    TODO: Return actual user ID from token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
        )

    # TODO: Verify JWT token with Supabase
    # TODO: Extract user_id from token claims

    # Placeholder - replace with actual implementation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Auth not implemented",
    )


# Type alias for dependency injection
CurrentUserId = Annotated[str, Depends(get_current_user_id)]


# TODO: Add get_supabase_client dependency
# TODO: Add get_grading_service dependency
# TODO: Add get_scheduling_service dependency
