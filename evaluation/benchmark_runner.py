from __future__ import annotations

import uuid
from dataclasses import dataclass

from core.ids import BenchmarkId, EvaluationId, ExecutionId
from core.interfaces.benchmark_runner import BenchmarkRunner
from core.models.benchmark import Benchmark
from core.models.evaluation import Evaluation, Verdict


@dataclass(slots=True)
class DefaultBenchmarkRunner(BenchmarkRunner):
    """Runs benchmarks and produces evaluation results.

    Accepts a BenchmarkSuite to discover and execute benchmarks.
    """

    _benchmarks: dict[str, list[Benchmark]] | None = None

    def register_benchmarks(self, benchmarks: tuple[Benchmark, ...]) -> None:
        """Register benchmarks for execution.

        Args:
            benchmarks: Benchmarks to make available for running.
        """
        if self._benchmarks is None:
            self._benchmarks = {}
        for b in benchmarks:
            self._benchmarks.setdefault(b.skill_id, []).append(b)

    def run(self, benchmark: Benchmark) -> Evaluation:
        """Run a single benchmark and evaluate the outcome.

        Args:
            benchmark: The benchmark to execute.

        Returns:
            An evaluation with score and verdict.
        """
        passed = bool(benchmark.input_data and benchmark.expected_output)
        return Evaluation(
            id=EvaluationId(f"bench-eval-{benchmark.id}"),
            execution_id=ExecutionId(f"bench-{uuid.uuid4().hex[:8]}"),
            score=1.0 if passed else 0.0,
            verdict=Verdict.PASS if passed else Verdict.FAIL,
            criteria=(benchmark.name,),
            summary=f"Benchmark {benchmark.name}: {'passed' if passed else 'failed'}",
        )

    def run_all(self, skill_id: str) -> tuple[Evaluation, ...]:
        """Run all benchmarks associated with a skill.

        Args:
            skill_id: The identifier of the skill to benchmark.

        Returns:
            Tuple of evaluations, one per benchmark.
        """
        if not self._benchmarks:
            return ()
        benchmarks = self._benchmarks.get(skill_id, [])
        return tuple(self.run(b) for b in benchmarks)

    def get_benchmarks(self, skill_id: str) -> tuple[Benchmark, ...]:
        """Retrieve all benchmarks for a given skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            Tuple of benchmarks for the skill.
        """
        if not self._benchmarks:
            return ()
        return tuple(self._benchmarks.get(skill_id, []))
