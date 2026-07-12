from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkspaceConfig(BaseSettings):
    """Workspace isolation configuration.

    Environment variables:
        WORKSPACE_ROOT, WORKSPACE_MAX_CONCURRENT, WORKSPACE_CLEANUP_ON_EXIT
    """

    model_config = SettingsConfigDict(
        env_prefix="WORKSPACE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    root: str = ".workspaces"
    max_concurrent: int = 4
    cleanup_on_exit: bool = True
