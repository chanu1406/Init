#!/usr/bin/env python3
"""Test the calculate_next_review function."""

import sys
sys.path.insert(0, '/Users/chanuollala/Documents/Init/backend')

from datetime import datetime, timezone
from app.services.scheduler import calculate_next_review

def test_calculate_next_review():
    """Test spaced repetition intervals for all mastery scores."""
    
    # Use a fixed date for consistent testing
    test_date = datetime(2026, 1, 20, 12, 0, 0, tzinfo=timezone.utc)
    
    print("Testing calculate_next_review function...\n")
    print(f"Reference date: {test_date.strftime('%Y-%m-%d %H:%M')}\n")
    
    # Test each mastery level
    test_cases = [
        (0, 1, "Struggling - daily practice"),
        (1, 1, "Struggling - daily practice"),
        (2, 3, "Okay - frequent review"),
        (3, 7, "Good - weekly review"),
        (4, 14, "Strong - bi-weekly review"),
        (5, 30, "Mastered - rare review"),
    ]
    
    all_passed = True
    
    for mastery, expected_days, description in test_cases:
        next_review = calculate_next_review(mastery, test_date)
        actual_days = (next_review - test_date).days
        
        status = "✅" if actual_days == expected_days else "❌"
        if actual_days != expected_days:
            all_passed = False
            
        print(f"{status} Mastery {mastery}: {description}")
        print(f"   Expected: +{expected_days} days")
        print(f"   Actual: +{actual_days} days")
        print(f"   Next review: {next_review.strftime('%Y-%m-%d %H:%M')}")
        print()
    
    # Test error handling
    print("Testing error handling...")
    try:
        calculate_next_review(6)  # Invalid mastery score
        print("❌ Should have raised ValueError for mastery > 5")
        all_passed = False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    try:
        calculate_next_review(-1)  # Invalid mastery score
        print("❌ Should have raised ValueError for mastery < 0")
        all_passed = False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*50)

if __name__ == "__main__":
    test_calculate_next_review()
