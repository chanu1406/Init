"""
OpenAI Client Service

Responsibility: Wraps OpenAI API interactions.
All AI calls should go through this service.

IMPORTANT: Frontend should NEVER call OpenAI directly.
"""

from app.core.config import settings


class OpenAIClient:
    """
    Wrapper for OpenAI API interactions.

    TODO: Initialize OpenAI client with API key
    TODO: Add retry logic for API failures
    TODO: Add response caching where appropriate
    """

    def __init__(self):
        """
        Initialize the OpenAI client.
        TODO: Set up actual OpenAI client instance
        """
        self.model = settings.openai_model
        # TODO: self.client = OpenAI(api_key=settings.openai_api_key)

    async def grade_response(
        self,
        prompt: str,
        rubric: dict,
        user_response: str,
    ) -> dict:
        """
        Grade a user's response to a drill using the provided rubric.

        Args:
            prompt: The original drill prompt
            rubric: The grading rubric with criteria
            user_response: The user's submitted response

        Returns:
            Grading result with scores and feedback

        TODO: Implement actual OpenAI API call
        TODO: Parse and validate response structure
        TODO: Handle API errors gracefully
        """
        # TODO: Implement
        raise NotImplementedError("OpenAI grading not implemented")

    async def generate_follow_up(
        self,
        prompt: str,
        user_response: str,
        feedback: dict,
    ) -> str | None:
        """
        Generate an optional follow-up question based on the response.

        TODO: Implement follow-up generation
        """
        # TODO: Implement
        return None
