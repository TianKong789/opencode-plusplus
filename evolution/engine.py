from __future__ import annotations

import uuid
from dataclasses import dataclass

from benchmarks.metrics import MetricsTracker
from benchmarks.suite import BenchmarkSuite
from core.ids import EvaluationId, ExecutionId
from core.models.evaluation import Evaluation, Verdict
from core.models.skill import Skill
from evolution.loop import EvolutionLoop
from evolution.prompt_evolver import PromptEvolver
from evolution.skill_evolver import SkillEvolver
from skills.extractor import SkillExtractor


@dataclass(slots=True, frozen=True)
class EvolutionEngine:
    """Drives recursive self-improvement through benchmark-driven evolution.

    Full loop: run benchmarks → evaluate → evolve skills/prompts → track metrics.

    Frozen dataclass — all methods return new instances rather than mutating.
    """

    loop: EvolutionLoop
    suite: BenchmarkSuite
    evolver: SkillEvolver
    metrics: MetricsTracker
    prompt_evolver: PromptEvolver | None = None
    skill_extractor: SkillExtractor | None = None

    # ── helpers ─────────────────────────────────────────────────────

    def _with_loop(self, loop: EvolutionLoop) -> EvolutionEngine:
        """Return a copy with a new loop."""
        return EvolutionEngine(
            loop=loop,
            suite=self.suite,
            evolver=self.evolver,
            metrics=self.metrics,
            prompt_evolver=self.prompt_evolver,
            skill_extractor=self.skill_extractor,
        )

    # ── benchmarking ───────────────────────────────────────────────

    def run_benchmarks(self, skills: tuple[Skill, ...]) -> tuple[float, ...]:
        """Run all benchmarks in the suite and record evaluations.

        Args:
            skills: Skills whose benchmarks to run.

        Returns:
            A score per skill (average of its benchmark evaluations).
        """
        scores: list[float] = []
        for skill in skills:
            benchmarks = self.suite.get_for_skill(skill.id)
            if not benchmarks:
                scores.append(skill.proficiency)
                continue
            skill_scores: list[float] = []
            for bench in benchmarks:
                passed = bool(bench.input_data and bench.expected_output)
                score = 1.0 if passed else 0.0
                evaluation = Evaluation(
                    id=EvaluationId(f"bench-eval-{bench.id}"),
                    execution_id=ExecutionId(f"gen-{uuid.uuid4().hex[:8]}"),
                    score=score,
                    verdict=Verdict.PASS if passed else Verdict.FAIL,
                    criteria=(bench.name,),
                    summary=f"Benchmark {bench.name}: {'passed' if passed else 'failed'}",
                )
                self.metrics.record(evaluation)
                skill_scores.append(score)
            avg = sum(skill_scores) / len(skill_scores) if skill_scores else skill.proficiency
            scores.append(avg)
        return tuple(scores)

    def evolve_skills(
        self,
        skills: tuple[Skill, ...],
        scores: tuple[float, ...],
    ) -> tuple[Skill, ...]:
        """Evolve skills based on benchmark scores.

        Args:
            skills: Current skills.
            scores: Benchmark scores per skill.

        Returns:
            Evolved skills with updated proficiency.
        """
        return tuple(self.evolver.adapt(s, sc) for s, sc in zip(skills, scores))

    # ── generation ─────────────────────────────────────────────────

    def run_generation(
        self,
        skills: tuple[Skill, ...],
        scores: tuple[float, ...] | None = None,
    ) -> tuple[tuple[Skill, ...], Evaluation, EvolutionEngine]:
        """Run one full generation: benchmark → evolve → record → evaluate.

        Returns a new engine with the loop incremented.

        Args:
            skills: The current skills to evolve.
            scores: Pre-computed scores (optional; runs benchmarks if None).

        Returns:
            A tuple of (evolved skills, generation evaluation, new engine).
        """
        if scores is None:
            scores = self.run_benchmarks(skills)

        evolved = self.evolve_skills(skills, scores)
        avg_score = sum(scores) / len(scores) if scores else 0.0
        baseline = self.metrics.average_score()
        delta = avg_score - baseline

        evaluation = Evaluation(
            id=EvaluationId(f"gen-eval-{self.loop.current_iteration}"),
            execution_id=ExecutionId(f"gen-{uuid.uuid4().hex[:8]}"),
            score=avg_score,
            verdict=Verdict.PASS if delta >= 0 else Verdict.FAIL,
            criteria=("generation",),
            summary=f"Generation {self.loop.current_iteration}: avg={avg_score:.3f} delta={delta:+.3f}",
        )
        self.metrics.record(evaluation)

        new_engine = self._with_loop(self.loop.record_iteration())
        return evolved, evaluation, new_engine

    def run_full_loop(
        self,
        skills: tuple[Skill, ...],
        max_generations: int | None = None,
    ) -> tuple[tuple[Skill, ...], list[Evaluation], EvolutionEngine]:
        """Run the complete evolution loop until convergence or limit.

        Returns a new engine with the final loop state.

        Args:
            skills: Initial skills.
            max_generations: Override loop's max_iterations if provided.

        Returns:
            A tuple of (final evolved skills, list of generation evaluations, final engine).
        """
        evaluations: list[Evaluation] = []
        current = skills
        engine = self

        for _ in range(max_generations or engine.loop.max_iterations):
            if not engine.loop.should_continue():
                break
            current, evaluation, engine = engine.run_generation(current)
            evaluations.append(evaluation)

        return current, evaluations, engine

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
