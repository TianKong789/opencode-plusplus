from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationConfig(BaseSettings):
    """Top-level application configuration.

    Environment variables:
        APP_NAME, APP_ENV, APP_DEBUG, APP_LOG_LEVEL
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    name: str = "opencode-plusplus"
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
