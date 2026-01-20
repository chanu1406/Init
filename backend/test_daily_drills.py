#!/usr/bin/env python3
"""Test the get_daily_drills function with real user data."""

import sys
sys.path.insert(0, '/Users/chanuollala/Documents/Init/backend')

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client
from app.services.scheduler import get_daily_drills

load_dotenv()

def test_get_daily_drills():
    """Test drill selection with our test user."""
    
    # Our test user
    user_id = "8a6902a2-29e3-4e0a-a6d3-f6088a186e58"
    
    # Connect to Supabase
    db = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_SERVICE_KEY')
    )
    
    print("Testing get_daily_drills function...")
    print(f"User ID: {user_id}\n")
    
    # Check user's current progress
    progress = db.table("user_drill_progress").select("*").eq("user_id", user_id).execute()
    
    print(f"User has attempted {len(progress.data)} drills:")
    for p in progress.data:
        print(f"  - Drill {p['drill_id'][:8]}... | Mastery: {p['mastery_score']} | Next review: {p.get('next_review_due_at', 'Not set')}")
    
    print("\n" + "="*60)
    print("Getting today's drills (limit=3)...")
    print("="*60 + "\n")
    
    # Get today's drills
    drills = get_daily_drills(user_id, db, limit=3)
    
    print(f"Selected {len(drills)} drills:\n")
    
    for i, drill in enumerate(drills, 1):
        print(f"{i}. {drill['slug']}")
        print(f"   Reason: {drill['reason']}")
        print(f"   Type: {drill['drill_type']}")
        print(f"   Mastery: {drill.get('mastery_score', 'New')}")
        if drill.get('last_attempt_at'):
            print(f"   Last attempt: {drill['last_attempt_at']}")
        if drill.get('next_review_due_at'):
            print(f"   Next review: {drill['next_review_due_at']}")
        print(f"   Prompt: {drill['prompt_markdown'][:80]}...")
        print()
    
    # Verify selection logic
    print("="*60)
    print("Verification:")
    print("="*60)
    
    reasons = [d['reason'] for d in drills]
    print(f"✓ Drill selection reasons: {reasons}")
    
    if 'overdue' in reasons:
        print("✓ Prioritized overdue reviews")
    if 'low_mastery' in reasons:
        print("✓ Included low mastery drills")
    if 'new' in reasons:
        print("✓ Included new content")
    
    print(f"\n✅ Successfully selected {len(drills)} drills for practice")

if __name__ == "__main__":
    test_get_daily_drills()
