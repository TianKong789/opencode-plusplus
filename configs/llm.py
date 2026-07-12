from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    """LLM provider configuration.

    Environment variables:
        LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, LLM_TEMPERATURE,
        LLM_MAX_TOKENS, LLM_TIMEOUT_SECONDS
    """

    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    provider: str = "openai"
    model: str = "gpt-4o"
    api_key: str = ""
    temperature: float = 0.0
    max_tokens: int = 4096
    timeout_seconds: float = 120.0
