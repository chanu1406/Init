"""
Authentication Router

Responsibility: Handles authentication-related endpoints.
Supabase handles primary auth (signup/login), this provides server-side utilities.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from supabase import Client

from app.core.supabase import get_supabase_client
from app.core.auth import CurrentUserId


router = APIRouter()


class SignupRequest(BaseModel):
    """Request model for user signup."""
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response model for auth operations."""
    access_token: str
    refresh_token: str
    user_id: str
    email: str


@router.post("/signup", response_model=AuthResponse)
async def signup(
    request: SignupRequest,
    db: Client = Depends(get_supabase_client),
):
    """
    Register a new user with email and password.
    
    Uses Supabase Auth for user management.
    Note: If email confirmation is enabled, user must verify email before logging in.
    """
    try:
        response = db.auth.sign_up({
            "email": request.email,
            "password": request.password,
        })
        
        if not response.user:
            raise Exception("Signup failed - no user returned")
        
        # If email confirmation is required, session will be None
        if not response.session:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_201_CREATED,
                detail="User created. Please check your email to confirm your account."
            )
        
        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id,
            email=response.user.email,
        )
    except HTTPException:
        raise
    except Exception as e:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {str(e)}"
        )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    db: Client = Depends(get_supabase_client),
):
    """
    Login with email and password.
    
    Returns JWT access token for API authentication.
    """
    try:
        response = db.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })
        
        if not response.user:
            raise Exception("Login failed")
        
        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id,
            email=response.user.email,
        )
    except Exception as e:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me")
async def get_current_user(user_id: CurrentUserId):
    """
    Get the current authenticated user's profile.
    
    Requires valid JWT token in Authorization header.
    """
    return {
        "user_id": user_id,
        "authenticated": True,
    }


@router.post("/verify")
async def verify_token(user_id: CurrentUserId):
    """
    Verify a JWT token is valid.
    
    Returns user_id if token is valid, otherwise returns 401.
    """
    return {
        "valid": True,
        "user_id": user_id,
    }