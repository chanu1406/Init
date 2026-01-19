"""
AI Client Service

Responsibility: Wraps AI API interactions (currently using Google Gemini).
All AI calls should go through this service.

IMPORTANT: Frontend should NEVER call AI APIs directly.
"""

import json
from typing import Any
import google.generativeai as genai
from app.core.config import settings


class OpenAIClient:
    """
    Wrapper for AI API interactions.
    Currently using Google Gemini for grading.
    """

    def __init__(self):
        """Initialize the Gemini client with API key from settings."""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.ai_model)

    async def grade_response(
        self,
        prompt: str,
        rubric: dict[str, Any],
        user_response: str,
        drill_type: str,
    ) -> dict[str, Any]:
        """
        Grade a user's response to a drill using the provided rubric.

        Args:
            prompt: The original drill prompt
            rubric: The grading rubric with criteria
            user_response: The user's submitted response
            drill_type: Type of drill (explain, debug, quiz)

        Returns:
            Grading result with scores and feedback

        Raises:
            Exception: If AI API call fails
        """
        system_prompt = self._build_system_prompt(drill_type)
        user_prompt = self._build_user_prompt(prompt, rubric, user_response)

        try:
            # Combine system and user prompts for Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Call Gemini API
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,  # Lower temperature for consistent grading
                    response_mime_type="application/json",
                ),
            )

            # Parse the JSON response
            result = json.loads(response.text)
            return result

        except Exception as e:
            # Log error and re-raise for handling at service layer
            print(f"AI API error: {e}")
            raise

    def _build_system_prompt(self, drill_type: str) -> str:
        """Build the system prompt for the grading model."""
        base = """You are an expert systems engineer evaluating CS student responses.

Your role:
- Grade responses against explicit rubrics
- Focus on correctness, completeness, and clarity
- Provide actionable, specific feedback
- Identify strengths before improvements
- Be encouraging but honest

Grading philosophy:
- Correctness: Is the explanation technically accurate?
- Completeness: Did they cover the key concepts?
- Clarity: Can a peer understand their explanation?
- Terminology: Do they use correct technical terms?

Always return valid JSON with this structure:
{
  "criterion_scores": {"criterion_name": score_int, ...},
  "total_score": sum_of_scores_int,
  "max_score": max_possible_int,
  "feedback": "detailed feedback string",
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["improvement 1", "improvement 2"],
  "follow_up_question": "optional clarifying question or null"
}"""

        if drill_type == "explain":
            return base + """

For explain drills:
- Look for clear mental models, not memorized definitions
- Reward examples and analogies
- Flag conceptual misunderstandings immediately"""
        elif drill_type == "debug":
            return base + """

For debug drills:
- Evaluate the reasoning process, not just the answer
- Look for systematic thinking and elimination
- Reward mentioning tools or debugging approaches"""
        else:
            return base

    def _build_user_prompt(
        self, prompt: str, rubric: dict[str, Any], user_response: str
    ) -> str:
        """Build the user prompt containing the response to grade."""
        criteria_text = "\n".join(
            f"- {c['name']}: {c['description']} (max {c['max_score']} points)"
            for c in rubric.get("criteria", [])
        )

        key_points = "\n".join(
            f"- {point}" for point in rubric.get("expected_key_points", [])
        )

        common_mistakes = "\n".join(
            f"- {mistake}" for mistake in rubric.get("common_mistakes", [])
        )

        return f"""DRILL PROMPT:
{prompt}

STUDENT RESPONSE:
{user_response}

GRADING CRITERIA:
{criteria_text}

EXPECTED KEY POINTS:
{key_points}

COMMON MISTAKES TO WATCH FOR:
{common_mistakes}

Please evaluate this response and return your assessment as JSON."""
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
