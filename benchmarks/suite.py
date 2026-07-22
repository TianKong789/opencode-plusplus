from __future__ import annotations

from dataclasses import dataclass, field

from core.models.benchmark import Benchmark


@dataclass(slots=True)
class BenchmarkSuite:
    """Manages and runs collections of benchmarks.

    Stores benchmarks by skill and coordinates batch execution.
    """

    _benchmarks: dict[str, list[Benchmark]] = field(default_factory=dict, init=False, repr=False)

    def add(self, benchmark: Benchmark) -> None:
        """Register a benchmark for a skill.

        Args:
            benchmark: The benchmark to add.
        """
        self._benchmarks.setdefault(benchmark.skill_id, []).append(benchmark)

    def get_for_skill(self, skill_id: str) -> tuple[Benchmark, ...]:
        """Retrieve all benchmarks for a skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            An immutable tuple of benchmarks.
        """
        return tuple(self._benchmarks.get(skill_id, []))

    def count(self, skill_id: str) -> int:
        """Count benchmarks for a skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            The number of registered benchmarks.
        """
        return len(self._benchmarks.get(skill_id, []))

    def remove(self, skill_id: str, benchmark_id: str) -> None:
        """Remove a benchmark by skill and benchmark id.

        Args:
            skill_id: The identifier of the skill.
            benchmark_id: The identifier of the benchmark to remove.
        """
        benchmarks = self._benchmarks.get(skill_id, [])
        self._benchmarks[skill_id] = [b for b in benchmarks if b.id != benchmark_id]
