"""
Scheduling Service

Responsibility: Handles drill scheduling and spaced repetition logic.
Determines which drills a user should see and when.
"""

from datetime import datetime


class SchedulingService:
    """
    Service for scheduling drills using spaced repetition.

    Scheduling principles:
    - Prioritize drills with low mastery scores
    - Respect next_review_due_at timestamps
    - Mix new and review drills
    - Cap daily workload based on user preferences
    """

    # Spaced repetition intervals in days
    # Based on simplified SM-2 algorithm
    INTERVALS = [1, 3, 7, 14, 30, 60]

    async def get_next_drill(
        self,
        user_id: str,
        daily_limit: int = 3,
    ) -> dict | None:
        """
        Get the next drill for a user to complete.

        Args:
            user_id: The user's ID
            daily_limit: Maximum drills per day

        Returns:
            Next drill to show, or None if daily quota met

        TODO: Query user_drill_progress for due reviews
        TODO: Prioritize by mastery score (lower = higher priority)
        TODO: Check daily completion count
        TODO: Return drill or None
        """
        # TODO: Implement
        raise NotImplementedError("Scheduling not implemented")

    def calculate_next_review_date(
        self,
        mastery_score: int,
        last_attempt: datetime,
    ) -> datetime:
        """
        Calculate when the next review should be scheduled.

        Args:
            mastery_score: Current mastery level (0-5)
            last_attempt: When the drill was last attempted

        Returns:
            DateTime for next scheduled review

        TODO: Implement spaced repetition interval logic
        """
        # TODO: Use mastery_score to index into INTERVALS
        # TODO: Add interval to last_attempt
        raise NotImplementedError("Next review calculation not implemented")

    async def get_daily_stats(
        self,
        user_id: str,
    ) -> dict:
        """
        Get user's progress stats for today.

        Returns:
            Dict with completed_today, remaining, streak, etc.

        TODO: Implement daily stats query
        """
        # TODO: Implement
        return {
            "completed_today": 0,
            "remaining": 0,
            "current_streak": 0,
        }
