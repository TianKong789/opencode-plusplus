from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class GitConfig(BaseSettings):
    """Git integration configuration.

    Environment variables:
        GIT_DEFAULT_BRANCH, GIT_AUTO_COMMIT, GIT_AUTHOR_NAME,
        GIT_AUTHOR_EMAIL
    """

    model_config = SettingsConfigDict(
        env_prefix="GIT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    default_branch: str = "main"
    auto_commit: bool = False
    author_name: str = "opencode++"
    author_email: str = "bot@opencode.dev"
