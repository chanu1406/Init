#!/usr/bin/env python3
"""Test scheduler integration with drill submission."""

import sys
sys.path.insert(0, '/Users/chanuollala/Documents/Init/backend')

import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Load token
with open('/tmp/login_response.json') as f:
    token = json.load(f)['access_token']

# Use a drill ID we know exists (from database query)
drill_id = "39638fa2-8181-4188-9784-061e5590250f"  # debug-fork-return-value (new drill)

print(f'Testing drill submission with scheduler integration...')
print(f'Drill: debug-fork-return-value\n')

# Submit a good response (should get high mastery)
response = requests.post(
    f'http://localhost:8000/drills/{drill_id}/attempts',
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    json={
        'user_response': 'The fork() system call returns twice: once in parent with child PID, once in child with 0. You check the return value to determine which process you are in. The parent receives the child PID so it can wait() for the child to complete.'
    }
)

result = response.json()
print(f'✅ Drill submitted successfully')
if 'total_score' in result:
    print(f'   Score: {result["total_score"]}/{result["max_score"]}')
    print(f'   Mastery: {result["mastery_score"]}')
else:
    print(f'   Response: {result}')
print()

# Now verify the next_review_due_at was calculated
db = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))

progress = db.table('user_drill_progress').select('*').eq('drill_id', drill_id).eq('user_id', '8a6902a2-29e3-4e0a-a6d3-f6088a186e58').execute()

if progress.data:
    p = progress.data[0]
    mastery = p['mastery_score']
    last_attempt = datetime.fromisoformat(p['last_attempt_at'].replace('Z', '+00:00'))
    next_review = datetime.fromisoformat(p['next_review_due_at'].replace('Z', '+00:00'))
    days_until_review = (next_review - last_attempt).days
    
    # Expected days based on mastery
    expected_days = {5: 30, 4: 14, 3: 7, 2: 3, 1: 1, 0: 1}
    expected = expected_days[mastery]
    
    print('✅ Next review date verification:')
    print(f'   Mastery score: {mastery}')
    print(f'   Last attempt: {last_attempt.strftime("%Y-%m-%d %H:%M")}')
    print(f'   Next review: {next_review.strftime("%Y-%m-%d %H:%M")}')
    print(f'   Days until review: {days_until_review}')
    print(f'   Expected: {expected} days')
    match = "✅ PASS" if days_until_review == expected else "❌ FAIL"
    print(f'   Result: {match}')
else:
    print('❌ Progress record not found')
