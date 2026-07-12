from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class MemoryConfig(BaseSettings):
    """Experience and skill storage configuration.

    Environment variables:
        MEMORY_BACKEND, MEMORY_PATH, MEMORY_MAX_ENTRIES
    """

    model_config = SettingsConfigDict(
        env_prefix="MEMORY_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    backend: str = "local"
    path: str = ".memory"
    max_entries: int = 10000
