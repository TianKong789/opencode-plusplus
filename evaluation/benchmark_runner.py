from __future__ import annotations

from dataclasses import dataclass

from core.ids import EvaluationId, ExecutionId
from core.interfaces.benchmark_runner import BenchmarkRunner
from core.models.benchmark import Benchmark
from core.models.evaluation import Evaluation, Verdict


@dataclass(slots=True, frozen=True)
class DefaultBenchmarkRunner(BenchmarkRunner):
    """Runs benchmarks and produces evaluation results.

    Placeholder implementation — replace with actual code execution
    for production use.
    """

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
            execution_id=ExecutionId(""),
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
            An empty tuple — no benchmarks registered yet.
        """
        return ()

    def get_benchmarks(self, skill_id: str) -> tuple[Benchmark, ...]:
        """Retrieve all benchmarks for a given skill.

        Args:
            skill_id: The identifier of the skill.

        Returns:
            An empty tuple — no benchmarks registered yet.
        """
        return ()
