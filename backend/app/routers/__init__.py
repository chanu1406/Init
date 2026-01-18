"""
Routers module

Contains all API route handlers.
Route handlers should be thin and delegate to services.
"""

from app.routers import auth, drills, health

__all__ = ["auth", "drills", "health"]
