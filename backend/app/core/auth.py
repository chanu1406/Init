"""
Authentication Dependencies

Responsibility: Validate JWT tokens from Supabase and extract user information.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from supabase import Client

from app.core.config import settings
from app.core.supabase import get_supabase_client


# Security scheme for extracting Bearer token from header
security = HTTPBearer()


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Client, Depends(get_supabase_client)],
) -> str:
    """
    Dependency to extract and validate the current user's ID from JWT.
    
    Args:
        credentials: Bearer token from Authorization header
        db: Supabase client for user validation
        
    Returns:
        User ID (UUID string)
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    try:
        # For Supabase JWTs, we can decode without verification first
        # to get the user_id, then verify via Supabase's get_user method
        # This is safer than trying to verify ES256 signatures ourselves
        unverified = jwt.decode(
            token,
            options={"verify_signature": False},
        )
        
        user_id = unverified.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )
        
        # Verify the token is valid by calling Supabase
        try:
            db.auth.get_user(token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        
        return user_id
        
    except HTTPException:
        raise
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
        )


# Type alias for injecting current user ID
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
