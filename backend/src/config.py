"""
Configuration management for the backend application.

This module loads environment variables and provides typed configuration
objects for different parts of the application.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Qdrant Configuration
    qdrant_api_key: str
    qdrant_url: str

    # Gemini Configuration
    gemini_api_key: str

    # Database Configuration (Bonus)
    neon_database_url: str = ""
    database_url: str = ""

    # Authentication (Bonus)
    auth_secret_key: str = ""
    better_auth_secret: str = ""  # User provided name

    # Application Configuration
    environment: str = "development"
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    rate_limit_per_minute: int = 100

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

    @property
    def get_secret_key(self) -> str:
        """Return the available secret key."""
        return self.auth_secret_key or self.better_auth_secret or "default_insecure_secret_key"

    @property
    def get_database_url(self) -> str:
        """Return the available database URL."""
        return self.neon_database_url or self.database_url

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
