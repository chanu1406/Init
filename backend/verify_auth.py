#!/usr/bin/env python3
"""Verify that the authenticated drill attempt was stored correctly."""

from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

db = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

# Check the latest drill attempt
attempt = db.table('drill_attempts').select('*').eq('id', '06b08530-5d2e-4744-9e57-0ece752a1851').execute()

if attempt.data:
    data = attempt.data[0]
    print('✅ Drill Attempt Verification:')
    print(f'   Attempt ID: {data["id"]}')
    print(f'   User ID: {data["user_id"]}')
    print(f'   Expected: 8a6902a2-29e3-4e0a-a6d3-f6088a186e58')
    print(f'   Match: {data["user_id"] == "8a6902a2-29e3-4e0a-a6d3-f6088a186e58"}')
    print(f'   Score: {data["ai_feedback"]["total_score"]}/{data["ai_feedback"]["max_score"]}')
    print()
    
    # Check user drill progress
    progress = db.table('user_drill_progress').select('*').eq('user_id', data["user_id"]).eq('drill_id', data["drill_id"]).execute()
    if progress.data:
        prog = progress.data[0]
        print('✅ User Progress Updated:')
        print(f'   Mastery Score: {prog["mastery_score"]}')
        print(f'   Last Attempt: {prog["last_attempt_at"]}')
        print(f'   Next Review: {prog["next_review_due_at"]}')
else:
    print('❌ Attempt not found')
