from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Setting class holding all global settings used throughout the app."""

    # Common settings
    app_env: str

    # Database settings
    database_url: str

    class Config:
        """Configuration for settings.

        env_file specifies location to environment file from which setting values are fetched.
        """

        env_file = Path(__file__).resolve().parent / ".env"


@lru_cache
def get_settings() -> Settings:
    """Getter for settings.

    Decorator @lru_cache is used to load settings from the file only once.
    """

    return Settings()
