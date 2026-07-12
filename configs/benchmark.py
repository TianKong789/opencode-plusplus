from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class BenchmarkConfig(BaseSettings):
    """Benchmark runner configuration.

    Environment variables:
        BENCHMARK_TIMEOUT_MS, BENCHMARK_MAX_RETRIES, BENCHMARK_PARALLEL
    """

    model_config = SettingsConfigDict(
        env_prefix="BENCHMARK_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    timeout_ms: float = 30000.0
    max_retries: int = 3
    parallel: bool = False
