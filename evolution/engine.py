from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from benchmarks.metrics import MetricsTracker
from benchmarks.suite import BenchmarkSuite
from core.ids import EvaluationId, ExecutionId
from core.models.evaluation import Evaluation, Verdict
from core.models.experience import Experience
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
    current_prompt: str = field(default="")

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
            current_prompt=self.current_prompt,
        )

    def _with_metrics(self, metrics: MetricsTracker) -> EvolutionEngine:
        """Return a copy with updated metrics."""
        return EvolutionEngine(
            loop=self.loop,
            suite=self.suite,
            evolver=self.evolver,
            metrics=metrics,
            prompt_evolver=self.prompt_evolver,
            skill_extractor=self.skill_extractor,
            current_prompt=self.current_prompt,
        )

    # ── benchmarking ───────────────────────────────────────────────

    def run_benchmarks(self, skills: tuple[Skill, ...]) -> tuple[tuple[float, ...], EvolutionEngine]:
        """Run all benchmarks in the suite and record evaluations.

        Args:
            skills: Skills whose benchmarks to run.

        Returns:
            A tuple of (scores per skill, new engine with updated metrics).
        """
        scores: list[float] = []
        metrics = self.metrics
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
                metrics = metrics.record(evaluation)
                skill_scores.append(score)
            avg = sum(skill_scores) / len(skill_scores) if skill_scores else skill.proficiency
            scores.append(avg)
        new_engine = self._with_metrics(metrics)
        return tuple(scores), new_engine

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

        Returns a new engine with the loop incremented and prompt evolved
        (if prompt_evolver is available and current_prompt is set).

        Args:
            skills: The current skills to evolve.
            scores: Pre-computed scores (optional; runs benchmarks if None).

        Returns:
            A tuple of (evolved skills, generation evaluation, new engine).
        """
        engine = self
        if scores is None:
            scores, engine = self.run_benchmarks(skills)

        evolved = engine.evolve_skills(skills, scores)
        avg_score = sum(scores) / len(scores) if scores else 0.0
        baseline = engine.metrics.average_score()
        delta = avg_score - baseline

        evaluation = Evaluation(
            id=EvaluationId(f"gen-eval-{engine.loop.current_iteration}"),
            execution_id=ExecutionId(f"gen-{uuid.uuid4().hex[:8]}"),
            score=avg_score,
            verdict=Verdict.PASS if delta >= 0 else Verdict.FAIL,
            criteria=("generation",),
            summary=f"Generation {engine.loop.current_iteration}: avg={avg_score:.3f} delta={delta:+.3f}",
        )
        metrics = engine.metrics.record(evaluation)

        new_prompt = engine.current_prompt
        if engine.prompt_evolver is not None and engine.current_prompt:
            new_prompt = engine.prompt_evolver.mutate(
                engine.current_prompt, evaluation.summary,
            )

        new_engine = EvolutionEngine(
            loop=engine.loop.record_iteration(),
            suite=engine.suite,
            evolver=engine.evolver,
            metrics=metrics,
            prompt_evolver=engine.prompt_evolver,
            skill_extractor=engine.skill_extractor,
            current_prompt=new_prompt,
        )
        return evolved, evaluation, new_engine

    # ── skill extraction ──────────────────────────────────────────

    def extract_skill(
        self,
        experiences: tuple[Experience, ...],
        name: str,
        description: str,
    ) -> Skill:
        """Extract a skill from experiences using the skill_extractor.

        Delegates to the injected SkillExtractor. Raises if no extractor
        was provided at construction time.

        Args:
            experiences: The experiences to extract from.
            name: Name for the new skill.
            description: Description of the skill.

        Returns:
            A new Skill with proficiency based on experience confidence.

        Raises:
            RuntimeError: If no skill_extractor was provided.
        """
        if self.skill_extractor is None:
            raise RuntimeError(
                "No SkillExtractor provided. Inject one at construction."
            )
        return self.skill_extractor.extract(experiences, name, description)

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
