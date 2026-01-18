"""
Health Check Router

Responsibility: Provides health check endpoints for monitoring.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    Returns OK if the service is running.
    """
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    TODO: Verify database connectivity
    TODO: Verify OpenAI API connectivity
    """
    # TODO: Add actual readiness checks
    return {
        "status": "ok",
        "checks": {
            "database": "ok",  # TODO: Actually check
            "openai": "ok",  # TODO: Actually check
        },
    }
