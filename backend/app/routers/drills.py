"""
Drills Router

Responsibility: Handles drill-related endpoints.
Includes fetching drills, submitting responses, and getting feedback.

Routes delegate to grading and scheduling services.
"""

from fastapi import APIRouter

from app.schemas.drill import DrillResponse, SubmitDrillRequest, SubmitDrillResponse

router = APIRouter()


@router.get("/today", response_model=DrillResponse)
async def get_todays_drill():
    """
    Get the next drill scheduled for today.

    TODO: Inject CurrentUserId dependency
    TODO: Call scheduling service to get next drill
    TODO: Return drill or null if daily quota met
    """
    # TODO: Implement
    return {"drill": None, "remaining_count": 0, "completed_today": 0}


@router.get("/{drill_id}", response_model=DrillResponse)
async def get_drill(drill_id: str):
    """
    Get a specific drill by ID.

    TODO: Fetch drill from database
    TODO: Check if user has access to this drill
    """
    # TODO: Implement
    return {"drill": None, "remaining_count": 0, "completed_today": 0}


@router.post("/submit", response_model=SubmitDrillResponse)
async def submit_drill_response(request: SubmitDrillRequest):
    """
    Submit a response to a drill for grading.

    TODO: Inject CurrentUserId dependency
    TODO: Validate drill exists and user has access
    TODO: Call grading service to evaluate response
    TODO: Update mastery score
    TODO: Calculate next review date
    TODO: Save attempt to database
    """
    # TODO: Implement
    return {
        "attempt_id": "",
        "feedback": {
            "scores": [],
            "total_score": 0,
            "max_score": 0,
            "justification": "Not implemented",
            "improvement": "Not implemented",
        },
        "new_mastery_score": 0,
        "next_review_due_at": "",
    }
