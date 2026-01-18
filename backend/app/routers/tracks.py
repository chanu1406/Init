"""
Tracks Router

Responsibility: Handles track and unit related endpoints.
Read-only endpoints for browsing learning content.
"""

from fastapi import APIRouter, HTTPException, status

from app.models.track import Track, TrackSummary, Unit, UnitSummary, UnitWithDrillCount
from app.models.drill import Drill, DrillSummary

# TODO: Replace with actual Supabase client from dependencies
from supabase import create_client
from app.core.config import settings

router = APIRouter()


def get_supabase():
    """Get Supabase client. TODO: Move to dependency injection."""
    return create_client(settings.supabase_url, settings.supabase_service_key)


@router.get("", response_model=list[TrackSummary])
async def list_tracks():
    """
    List all available tracks.

    Returns a list of track summaries for browsing.
    """
    client = get_supabase()

    response = client.table("tracks").select("id, slug, title, description").order("title").execute()

    return [TrackSummary(**track) for track in response.data]


@router.get("/{slug}", response_model=Track)
async def get_track(slug: str):
    """
    Get a track by slug.

    Returns full track details.
    """
    client = get_supabase()

    response = client.table("tracks").select("*").eq("slug", slug).execute()

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track '{slug}' not found",
        )

    return Track(**response.data[0])


@router.get("/{slug}/units", response_model=list[UnitWithDrillCount])
async def list_track_units(slug: str):
    """
    List all units in a track.

    Returns units ordered by order_index, with drill counts.
    """
    client = get_supabase()

    # First get the track
    track_response = client.table("tracks").select("id").eq("slug", slug).execute()

    if not track_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track '{slug}' not found",
        )

    track_id = track_response.data[0]["id"]

    # Get units with drill counts
    # Note: Supabase doesn't support count aggregation easily, so we'll do this in two queries
    units_response = (
        client.table("units")
        .select("id, order_index, title, summary_markdown")
        .eq("track_id", track_id)
        .order("order_index")
        .execute()
    )

    # Get drill counts per unit
    drills_response = (
        client.table("drills")
        .select("unit_id")
        .execute()
    )

    # Count drills per unit
    drill_counts: dict[str, int] = {}
    for drill in drills_response.data:
        unit_id = drill["unit_id"]
        drill_counts[unit_id] = drill_counts.get(unit_id, 0) + 1

    # Build response
    units = []
    for unit in units_response.data:
        units.append(
            UnitWithDrillCount(
                id=unit["id"],
                order_index=unit["order_index"],
                title=unit["title"],
                summary_markdown=unit["summary_markdown"],
                drill_count=drill_counts.get(unit["id"], 0),
            )
        )

    return units


@router.get("/{slug}/units/{order_index}", response_model=Unit)
async def get_unit(slug: str, order_index: int):
    """
    Get a specific unit by track slug and order index.
    """
    client = get_supabase()

    # Get track
    track_response = client.table("tracks").select("id").eq("slug", slug).execute()

    if not track_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track '{slug}' not found",
        )

    track_id = track_response.data[0]["id"]

    # Get unit
    unit_response = (
        client.table("units")
        .select("*")
        .eq("track_id", track_id)
        .eq("order_index", order_index)
        .execute()
    )

    if not unit_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unit {order_index} not found in track '{slug}'",
        )

    return Unit(**unit_response.data[0])
