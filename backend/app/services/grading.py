"""
Grading Service

Responsibility: Handles drill response grading logic.
Coordinates between rubric evaluation and OpenAI scoring.
"""

from typing import Any
from app.services.openai_client import OpenAIClient


class GradingService:
    """
    Service for grading user responses to drills.

    Grading flow:
    1. Receive user response and drill rubric
    2. Call OpenAI to evaluate against rubric criteria
    3. Calculate total score and mastery impact
    4. Generate improvement suggestions
    5. Return structured feedback
    """

    def __init__(self, openai_client: OpenAIClient):
        """Initialize grading service with dependencies."""
        self.openai_client = openai_client

    async def grade_drill_response(
        self,
        drill_id: str,
        prompt: str,
        rubric: dict[str, Any],
        user_response: str,
        drill_type: str,
    ) -> dict[str, Any]:
        """
        Grade a user's response to a drill.

        Args:
            drill_id: The drill being answered
            prompt: The drill prompt text
            rubric: The grading rubric
            user_response: The user's submitted answer
            drill_type: Type of drill (explain, debug, quiz)

        Returns:
            Structured feedback with scores and suggestions
        """
        # Call OpenAI to evaluate the response
        ai_feedback = await self.openai_client.grade_response(
            prompt=prompt,
            rubric=rubric,
            user_response=user_response,
            drill_type=drill_type,
        )

        # Return structured feedback
        return {
            "drill_id": drill_id,
            "criterion_scores": ai_feedback.get("criterion_scores", {}),
            "total_score": ai_feedback.get("total_score", 0),
            "max_score": ai_feedback.get("max_score", 0),
            "feedback": ai_feedback.get("feedback", ""),
            "strengths": ai_feedback.get("strengths", []),
            "improvements": ai_feedback.get("improvements", []),
            "follow_up_question": ai_feedback.get("follow_up_question"),
        }

    def calculate_mastery_delta(
        self,
        current_mastery: int,
        score_percentage: float,
    ) -> int:
        """
        Calculate how mastery score should change based on performance.

        Mastery levels:
        0: unseen
        1: exposed (seen the concept)
        2: basic recall (can recall basics)
        3: clear explanation (can explain clearly)
        4: applied understanding (can apply to problems)
        5: confident and consistent (mastery)

        Args:
            current_mastery: Current mastery level (0-5)
            score_percentage: Percentage score on this attempt (0-1)

        Returns:
            New mastery score (0-5)
        """
        # Performance thresholds
        EXCELLENT = 0.85  # 85%+
        GOOD = 0.70       # 70%+
        ADEQUATE = 0.50   # 50%+

        # First exposure - set to level 1
        if current_mastery == 0:
            return 1

        # Strong performance - increase mastery
        if score_percentage >= EXCELLENT:
            return min(current_mastery + 1, 5)
        
        # Good performance - maintain or slight increase
        elif score_percentage >= GOOD:
            if current_mastery < 3:
                return current_mastery + 1
            return current_mastery
        
        # Adequate performance - maintain current level
        elif score_percentage >= ADEQUATE:
            return current_mastery
        
        # Poor performance - decrease mastery (but never below 1)
        else:
            return max(current_mastery - 1, 1)
