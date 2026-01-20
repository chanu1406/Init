"""
Drills Router

Responsibility: Handles drill-related endpoints.
Includes fetching drills, submitting responses, and getting feedback.

Routes delegate to grading and scheduling services.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from supabase import Client

from app.core.supabase import get_supabase_client
from app.core.auth import CurrentUserId
from app.models.drill import DrillAttemptRequest, DrillAttemptResponse
from app.services.grading import GradingService
from app.services.openai_client import OpenAIClient
from app.services.scheduler import calculate_next_review, get_daily_drills

router = APIRouter()


@router.get("/today")
async def get_todays_drills(
    user_id: CurrentUserId,
    db: Client = Depends(get_supabase_client),
    limit: int = 3,
):
    """
    Get today's personalized drill queue based on spaced repetition.
    
    Returns a mix of:
    - Overdue reviews (highest priority)
    - Low mastery drills (need practice)
    - New drills (gradual introduction)
    
    Args:
        user_id: Authenticated user's ID (from JWT)
        limit: Maximum number of drills to return (default 3)
    
    Returns:
        List of drills with metadata (reason, mastery, last_attempt)
    """
    drills = get_daily_drills(user_id, db, limit=limit)
    
    # Format response for frontend
    return {
        "drills": drills,
        "total_available": len(drills),
        "limit": limit,
        "user_id": user_id,
    }


@router.post("/{drill_id}/attempts", response_model=DrillAttemptResponse)
async def submit_drill_attempt(
    drill_id: str,
    request: DrillAttemptRequest,
    user_id: CurrentUserId,
    db: Client = Depends(get_supabase_client),
):
    """
    Submit a response to a drill for AI grading.

    Flow:
    1. Fetch drill with rubric
    2. Grade response via AI
    3. Store attempt in drill_attempts
    4. Update or create user_drill_progress
    5. Return feedback and new mastery score
    
    Requires: Valid JWT token in Authorization header
    """

    # Fetch the drill
    drill_response = db.table("drills").select("*").eq("id", drill_id).execute()
    
    if not drill_response.data:
        raise HTTPException(status_code=404, detail="Drill not found")
    
    drill = drill_response.data[0]

    # Initialize services
    openai_client = OpenAIClient()
    grading_service = GradingService(openai_client)

    # Grade the response
    feedback = await grading_service.grade_drill_response(
        drill_id=drill_id,
        prompt=drill["prompt_markdown"],
        rubric=drill["rubric"],
        user_response=request.user_response,
        drill_type=drill["drill_type"],
    )

    # Calculate score percentage
    score_percentage = feedback["total_score"] / feedback["max_score"] if feedback["max_score"] > 0 else 0

    # Fetch current mastery or initialize
    progress_response = (
        db.table("user_drill_progress")
        .select("*")
        .eq("user_id", user_id)
        .eq("drill_id", drill_id)
        .execute()
    )

    current_mastery = 0
    if progress_response.data:
        current_mastery = progress_response.data[0]["mastery_score"]

    # Calculate new mastery
    new_mastery = grading_service.calculate_mastery_delta(
        current_mastery=current_mastery,
        score_percentage=score_percentage,
    )

    # Store the attempt
    attempt_data = {
        "user_id": user_id,
        "drill_id": drill_id,
        "user_response": request.user_response,
        "ai_feedback": feedback,
        "score": feedback["total_score"],
        "max_score": feedback["max_score"],
    }
    
    attempt_response = db.table("drill_attempts").insert(attempt_data).execute()
    attempt_id = attempt_response.data[0]["id"]

    # Update or create progress
    now = datetime.now(timezone.utc)
    next_review = calculate_next_review(new_mastery, now)
    
    progress_data = {
        "user_id": user_id,
        "drill_id": drill_id,
        "mastery_score": new_mastery,
        "last_attempt_at": now.isoformat(),
        "next_review_due_at": next_review.isoformat(),
    }

    if progress_response.data:
        # Update existing
        db.table("user_drill_progress").update(progress_data).eq("id", progress_response.data[0]["id"]).execute()
    else:
        # Create new
        db.table("user_drill_progress").insert(progress_data).execute()

    # Return response
    return DrillAttemptResponse(
        attempt_id=attempt_id,
        drill_id=drill_id,
        total_score=feedback["total_score"],
        max_score=feedback["max_score"],
        feedback=feedback["feedback"],
        strengths=feedback["strengths"],
        improvements=feedback["improvements"],
        follow_up_question=feedback.get("follow_up_question"),
        mastery_score=new_mastery,
        created_at=now,
    )
