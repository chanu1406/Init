"""
Test Script: Drill Grading Flow

Tests the drill attempt submission without relying on OpenAI quota.
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


async def test_grading_flow():
    """Test the complete grading flow with mock AI feedback."""
    
    # Initialize Supabase client
    db = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Get a test drill
    drills = db.table("drills").select("*").limit(1).execute()
    if not drills.data:
        print("❌ No drills found in database")
        return
    
    drill = drills.data[0]
    drill_id = drill["id"]
    
    print(f"✓ Found drill: {drill['slug']}")
    print(f"  Type: {drill['drill_type']}")
    print(f"  Prompt: {drill['prompt_markdown'][:100]}...")
    
    # Mock user response
    user_response = "This is a test response explaining the concept clearly with examples."
    user_id = "00000000-0000-0000-0000-000000000000"
    
    # Mock AI feedback (simulating what OpenAI would return)
    mock_feedback = {
        "criterion_scores": {"accuracy": 2, "completeness": 2, "clarity": 1},
        "total_score": 5,
        "max_score": 5,
        "feedback": "Good explanation with clear reasoning. Consider adding more specific examples.",
        "strengths": ["Clear explanation", "Correct terminology"],
        "improvements": ["Add specific examples", "Mention edge cases"],
        "follow_up_question": "Can you explain what happens under high load?"
    }
    
    # Store the attempt
    attempt_data = {
        "user_id": user_id,
        "drill_id": drill_id,
        "user_response": user_response,
        "ai_feedback": mock_feedback,
        "score": mock_feedback["total_score"],
        "max_score": mock_feedback["max_score"],
    }
    
    attempt_response = db.table("drill_attempts").insert(attempt_data).execute()
    attempt_id = attempt_response.data[0]["id"]
    
    print(f"\n✓ Stored drill attempt: {attempt_id}")
    print(f"  Score: {mock_feedback['total_score']}/{mock_feedback['max_score']}")
    
    # Check/update progress
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
        print(f"\n✓ Current mastery: {current_mastery}")
    else:
        print(f"\n✓ First attempt at this drill")
    
    # Calculate new mastery (using simple logic)
    score_percentage = mock_feedback["total_score"] / mock_feedback["max_score"]
    if score_percentage >= 0.85:
        new_mastery = min(current_mastery + 1, 5)
    elif score_percentage >= 0.70:
        new_mastery = current_mastery if current_mastery >= 3 else current_mastery + 1
    else:
        new_mastery = max(current_mastery, 1)
    
    print(f"  Score percentage: {score_percentage:.0%}")
    print(f"  New mastery: {new_mastery}")
    
    # Update progress
    now = datetime.now(timezone.utc)
    progress_data = {
        "user_id": user_id,
        "drill_id": drill_id,
        "mastery_score": new_mastery,
        "last_attempt_at": now.isoformat(),
        "next_review_due_at": now.isoformat(),
    }
    
    if progress_response.data:
        db.table("user_drill_progress").update(progress_data).eq("id", progress_response.data[0]["id"]).execute()
        print(f"\n✓ Updated progress record")
    else:
        db.table("user_drill_progress").insert(progress_data).execute()
        print(f"\n✓ Created new progress record")
    
    # Verify the data was stored
    verify_attempt = db.table("drill_attempts").select("*").eq("id", attempt_id).execute()
    verify_progress = (
        db.table("user_drill_progress")
        .select("*")
        .eq("user_id", user_id)
        .eq("drill_id", drill_id)
        .execute()
    )
    
    print(f"\n{'='*60}")
    print("DATABASE VERIFICATION")
    print(f"{'='*60}")
    print(f"\nAttempt stored: {len(verify_attempt.data) == 1}")
    print(f"Progress updated: {len(verify_progress.data) == 1}")
    if verify_progress.data:
        print(f"Final mastery: {verify_progress.data[0]['mastery_score']}")
    
    print(f"\n{'='*60}")
    print("✅ GRADING FLOW TEST COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(test_grading_flow())
