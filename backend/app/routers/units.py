"""
Units Router

Responsibility: Handles unit-specific endpoints, primarily drill access.
"""

from fastapi import APIRouter, HTTPException, status

from app.models.drill import Drill, DrillSummary

# TODO: Replace with actual Supabase client from dependencies
from supabase import create_client
from app.core.config import settings

router = APIRouter()


def get_supabase():
    """Get Supabase client. TODO: Move to dependency injection."""
    return create_client(settings.supabase_url, settings.supabase_service_key)


@router.get("/{unit_id}/drills", response_model=list[DrillSummary])
async def list_unit_drills(unit_id: str):
    """
    List all drills in a unit.

    Returns drill summaries (without full prompt/rubric) for browsing.
    """
    client = get_supabase()

    # Verify unit exists
    unit_response = client.table("units").select("id").eq("id", unit_id).execute()

    if not unit_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unit '{unit_id}' not found",
        )

    # Get drills
    drills_response = (
        client.table("drills")
        .select("id, slug, drill_type, difficulty, estimated_minutes, concept_tags")
        .eq("unit_id", unit_id)
        .order("slug")
        .execute()
    )

    return [DrillSummary(**drill) for drill in drills_response.data]


@router.get("/{unit_id}/drills/{drill_slug}", response_model=Drill)
async def get_drill(unit_id: str, drill_slug: str):
    """
    Get a specific drill by unit ID and drill slug.

    Returns full drill details including prompt and rubric.
    """
    client = get_supabase()

    response = (
        client.table("drills")
        .select("*")
        .eq("unit_id", unit_id)
        .eq("slug", drill_slug)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Drill '{drill_slug}' not found in unit '{unit_id}'",
        )

    return Drill(**response.data[0])
