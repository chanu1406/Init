"""
FastAPI Application Entrypoint

Responsibility: Creates and configures the FastAPI application instance.
Registers routers, middleware, and event handlers.

Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, drills, health, tracks, units

# Create FastAPI application
app = FastAPI(
    title="Init API",
    description="Backend API for the Init learning application",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Configure CORS
# TODO: Restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
app.include_router(units.router, prefix="/units", tags=["Units"])
app.include_router(drills.router, prefix="/drills", tags=["Drills"])

# TODO: Add progress router


@app.on_event("startup")
async def startup_event():
    """
    Application startup handler.
    TODO: Initialize database connections, warm up caches, etc.
    """
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown handler.
    TODO: Clean up resources, close connections, etc.
    """
    pass
