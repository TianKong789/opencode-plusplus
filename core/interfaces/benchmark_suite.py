from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.benchmark import Benchmark


class BenchmarkSuitePort(ABC):
    """Retrieves benchmarks associated with a skill."""

    @abstractmethod
    def get_for_skill(self, skill_id: str) -> tuple[Benchmark, ...]:
        """Retrieve all benchmarks associated with a skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            An immutable tuple of the skill's benchmarks.
        """
