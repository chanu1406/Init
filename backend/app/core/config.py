"""
Application Configuration

Responsibility: Loads and validates environment variables.
Uses Pydantic Settings for type-safe configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Environment
    environment: str = "development"
    debug: bool = True

    # Supabase
    supabase_url: str
    supabase_service_key: str
    supabase_anon_key: str

    # AI API
    gemini_api_key: str
    ai_model: str = "gemini-2.0-flash"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


# Global settings instance
# TODO: Add validation that required env vars are set
settings = Settings()
