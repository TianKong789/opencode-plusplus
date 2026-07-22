from __future__ import annotations

from dataclasses import dataclass

from benchmarks.metrics import MetricsTracker
from benchmarks.suite import BenchmarkSuite
from evolution.loop import EvolutionLoop
from evolution.skill_evolver import SkillEvolver
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class EvolutionEngine:
    """Drives recursive self-improvement through benchmark-driven evolution.

    Coordinates the full loop: run benchmarks → evaluate → evolve skills → track metrics.
    """

    loop: EvolutionLoop
    suite: BenchmarkSuite
    evolver: SkillEvolver
    metrics: MetricsTracker

    def run_generation(
        self,
        skills: tuple[Skill, ...],
        scores: tuple[float, ...],
    ) -> tuple[tuple[Skill, ...], EvolutionLoop]:
        """Run one generation of evolution.

        Args:
            skills: The current skills to evolve.
            scores: Benchmark scores corresponding to each skill.

        Returns:
            A tuple of (evolved skills, updated loop).
        """
        evolved: list[Skill] = []
        for skill, score in zip(skills, scores):
            evolved.append(self.evolver.adapt(skill, score))
        return tuple(evolved), self.loop.record_iteration()

    def is_complete(self) -> bool:
        """Check whether evolution is complete.

        Returns:
            True if the loop says to stop.
        """
        return not self.loop.should_continue()

    def improvement_delta(self, baseline: float | None = None) -> float:
        """Compute improvement over baseline.

        Args:
            baseline: The starting score to compare against.
                If None, uses the first recorded evaluation.

        Returns:
            The score delta, or 0.0 if no data.
        """
        current = self.metrics.average_score()
        if baseline is not None:
            return current - baseline
        return current
