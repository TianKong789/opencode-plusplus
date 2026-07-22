from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from pathlib import Path

from core.ids import BenchmarkId, EvaluationId, ExecutionId, SkillId
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

    def discover_benchmarks(self, benchmark_dir: Path) -> tuple[Benchmark, ...]:
        """Create benchmarks from capability metadata stored below a benchmark directory."""
        capabilities_dir = benchmark_dir / "capabilities"
        discovery_dir = capabilities_dir if capabilities_dir.is_dir() else benchmark_dir
        benchmarks: list[Benchmark] = []

        for metadata_path in discovery_dir.glob("*/metadata.json"):
            try:
                metadata_text = metadata_path.read_text(encoding="utf-8")
                metadata = json.loads(metadata_text)
                capability = metadata["capability"]
                version = metadata["version"]
                description = metadata["description"]
                scoring = metadata["scoring"]
                difficulty_levels = metadata["difficulty_levels"]
            except (json.JSONDecodeError, KeyError, OSError, TypeError, UnicodeDecodeError):
                continue

            if not isinstance(capability, str) or not capability:
                continue
            if not isinstance(description, str) or not description:
                continue
            if not isinstance(version, str) or not version:
                continue
            if not isinstance(scoring, dict) or not scoring:
                continue
            if not isinstance(difficulty_levels, list) or not difficulty_levels:
                continue
            if not all(isinstance(level, str) and level for level in difficulty_levels):
                continue

            try:
                benchmarks.append(
                    Benchmark(
                        id=BenchmarkId(capability),
                        skill_id=SkillId(capability),
                        name=description,
                        input_data=metadata_text,
                        expected_output=description,
                    )
                )
            except ValueError:
                continue

        return tuple(sorted(benchmarks, key=lambda benchmark: benchmark.skill_id))

    def run(self, benchmark: Benchmark) -> Evaluation:
        """Run a single benchmark and evaluate the outcome.

        Args:
            benchmark: The benchmark to execute.

        Returns:
            An evaluation with score and verdict.
        """
        return Evaluation(
            id=EvaluationId(f"bench-eval-{benchmark.id}"),
            execution_id=ExecutionId(f"bench-{uuid.uuid4().hex[:8]}"),
            score=0.5,
            verdict=Verdict.PARTIAL,
            criteria=("discovered", benchmark.name),
            summary=f"Benchmark {benchmark.name}: discovered; awaiting capability evaluation",
        )

    def run_all(self, skill_id: str) -> tuple[Evaluation, ...]:
        """Run all benchmarks associated with a skill.

        Args:
            skill_id: The identifier of the skill to benchmark.

        Returns:
            Tuple of evaluations, one per benchmark.
        """
        if not self._benchmarks:
            self.register_benchmarks(self.discover_benchmarks(Path("benchmarks/capabilities")))
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
