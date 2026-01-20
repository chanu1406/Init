"""
Scheduler Service

Implements spaced repetition logic and drill selection for daily practice.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from supabase import Client


def calculate_next_review(
    mastery_score: int,
    current_date: Optional[datetime] = None
) -> datetime:
    """
    Calculate when a drill should be reviewed next based on mastery score.
    
    Uses spaced repetition intervals:
    - Mastery 5 (mastered): 30 days
    - Mastery 4 (strong): 14 days  
    - Mastery 3 (good): 7 days
    - Mastery 2 (okay): 3 days
    - Mastery 0-1 (struggling): 1 day
    
    Args:
        mastery_score: Current mastery level (0-5)
        current_date: Reference date (defaults to now)
        
    Returns:
        datetime: When the drill should be reviewed next
        
    Raises:
        ValueError: If mastery_score is not in range 0-5
    """
    if not 0 <= mastery_score <= 5:
        raise ValueError(f"Mastery score must be 0-5, got {mastery_score}")
    
    if current_date is None:
        current_date = datetime.now(timezone.utc)
    
    # Spaced repetition intervals based on mastery
    intervals = {
        5: timedelta(days=30),  # Mastered - rare review
        4: timedelta(days=14),  # Strong - bi-weekly
        3: timedelta(days=7),   # Good - weekly
        2: timedelta(days=3),   # Okay - frequent
        1: timedelta(days=1),   # Struggling - daily
        0: timedelta(days=1),   # No understanding - daily
    }
    
    interval = intervals[mastery_score]
    next_review = current_date + interval
    
    return next_review


def get_daily_drills(
    user_id: str,
    db: Client,
    limit: int = 3,
    current_date: Optional[datetime] = None
) -> List[Dict[str, Any]]:
    """
    Select drills for today's practice based on spaced repetition.
    
    Priority order:
    1. Overdue reviews (next_review_due_at < now)
    2. Low mastery drills (mastery 0-2)
    3. New drills (never attempted)
    
    Args:
        user_id: User's UUID
        db: Supabase client
        limit: Maximum number of drills to return (default 3)
        current_date: Reference date (defaults to now)
        
    Returns:
        List of drill objects with metadata:
        - id, slug, drill_type, prompt_markdown, rubric
        - mastery_score (if attempted)
        - reason (why selected: "overdue", "low_mastery", "new")
    """
    if current_date is None:
        current_date = datetime.now(timezone.utc)
    
    selected_drills = []
    
    # 1. Get overdue reviews (highest priority)
    overdue_response = (
        db.table("user_drill_progress")
        .select("drill_id, mastery_score, last_attempt_at, next_review_due_at")
        .eq("user_id", user_id)
        .lt("next_review_due_at", current_date.isoformat())
        .order("mastery_score", desc=False)  # Lowest mastery first
        .limit(limit)
        .execute()
    )
    
    overdue_drill_ids = [row["drill_id"] for row in overdue_response.data]
    
    if overdue_drill_ids:
        # Fetch full drill details
        drills_response = (
            db.table("drills")
            .select("*")
            .in_("id", overdue_drill_ids)
            .execute()
        )
        
        # Add metadata
        for drill in drills_response.data:
            progress_data = next(
                (p for p in overdue_response.data if p["drill_id"] == drill["id"]),
                None
            )
            drill["mastery_score"] = progress_data["mastery_score"]
            drill["last_attempt_at"] = progress_data["last_attempt_at"]
            drill["next_review_due_at"] = progress_data["next_review_due_at"]
            drill["reason"] = "overdue"
            selected_drills.append(drill)
    
    # 2. If we need more, get low mastery drills (not already overdue)
    if len(selected_drills) < limit:
        remaining = limit - len(selected_drills)
        
        low_mastery_response = (
            db.table("user_drill_progress")
            .select("drill_id, mastery_score, last_attempt_at")
            .eq("user_id", user_id)
            .lte("mastery_score", 2)
            .gte("next_review_due_at", current_date.isoformat())  # Not overdue
            .order("mastery_score", desc=False)
            .limit(remaining)
            .execute()
        )
        
        low_mastery_drill_ids = [row["drill_id"] for row in low_mastery_response.data]
        
        if low_mastery_drill_ids:
            drills_response = (
                db.table("drills")
                .select("*")
                .in_("id", low_mastery_drill_ids)
                .execute()
            )
            
            for drill in drills_response.data:
                progress_data = next(
                    (p for p in low_mastery_response.data if p["drill_id"] == drill["id"]),
                    None
                )
                drill["mastery_score"] = progress_data["mastery_score"]
                drill["last_attempt_at"] = progress_data["last_attempt_at"]
                drill["reason"] = "low_mastery"
                selected_drills.append(drill)
    
    # 3. Fill remaining slots with new drills
    if len(selected_drills) < limit:
        remaining = limit - len(selected_drills)
        
        # Get all drill IDs user has attempted
        attempted_response = (
            db.table("user_drill_progress")
            .select("drill_id")
            .eq("user_id", user_id)
            .execute()
        )
        
        attempted_drill_ids = [row["drill_id"] for row in attempted_response.data]
        
        # Get new drills (not attempted)
        new_drills_query = db.table("drills").select("*").order("created_at", desc=False)
        
        if attempted_drill_ids:
            new_drills_query = new_drills_query.not_.in_("id", attempted_drill_ids)
        
        new_drills_response = new_drills_query.limit(remaining).execute()
        
        for drill in new_drills_response.data:
            drill["mastery_score"] = None
            drill["last_attempt_at"] = None
            drill["reason"] = "new"
            selected_drills.append(drill)
    
    return selected_drills
