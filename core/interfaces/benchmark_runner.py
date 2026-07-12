from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.benchmark import Benchmark
from core.models.evaluation import Evaluation


class BenchmarkRunner(ABC):
    """Executes benchmarks and produces evaluation results."""

    @abstractmethod
    def run(self, benchmark: Benchmark) -> Evaluation:
        """Run a single benchmark and evaluate the outcome.

        Args:
            benchmark: The benchmark to execute.

        Returns:
            An evaluation with score and verdict.
        """

    @abstractmethod
    def run_all(self, skill_id: str) -> tuple[Evaluation, ...]:
        """Run all benchmarks associated with a skill.

        Args:
            skill_id: The identifier of the skill to benchmark.

        Returns:
            An immutable tuple of evaluations, one per benchmark.
        """

    @abstractmethod
    def get_benchmarks(self, skill_id: str) -> tuple[Benchmark, ...]:
        """Retrieve all benchmarks for a given skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            An immutable tuple of benchmarks.
        """
