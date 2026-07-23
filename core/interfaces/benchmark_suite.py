from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.benchmark import Benchmark


@runtime_checkable
class BenchmarkSuitePort(Protocol):
    """Retrieves benchmarks associated with a skill."""

    def get_for_skill(self, skill_id: str) -> tuple[Benchmark, ...]:
        """Retrieve all benchmarks associated with a skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            An immutable tuple of the skill's benchmarks.
        """
