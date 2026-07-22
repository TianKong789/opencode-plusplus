import pytest

from evolution.engine import EvolutionEngine
from evolution.loop import EvolutionLoop
from evolution.skill_evolver import SkillEvolver
from benchmarks.metrics import MetricsTracker
from benchmarks.suite import BenchmarkSuite
from core.ids import EvaluationId, ExecutionId, ExperienceId, ReflectionId, SkillId
from core.models.evaluation import Evaluation, Verdict
from core.models.experience import Experience
from core.models.skill import Skill
from memory.experience_store import ExperienceStore
from memory.reflection_repository import InMemoryReflectionRepository
from memory.skill_repository import InMemorySkillRepository
from evolution.skill_extractor import DefaultSkillExtractor


def _make_skill(
    skill_id: str = "s1",
    name: str = "python",
    proficiency: float = 0.5,
) -> Skill:
    return Skill(
        id=SkillId(skill_id),
        name=name,
        description="test",
        proficiency=proficiency,
    )


def _make_engine(max_iter: int = 3) -> EvolutionEngine:
    return EvolutionEngine(
        loop=EvolutionLoop(max_iterations=max_iter),
        suite=BenchmarkSuite(),
        evolver=SkillEvolver(),
        metrics=MetricsTracker(),
    )


class TestEvolutionEngine:
    def test_run_generation_evolves_skills(self) -> None:
        engine = _make_engine()
        skill = _make_skill(proficiency=0.5)
        evolved, evaluation, new_engine = engine.run_generation((skill,), (0.8,))
        assert len(evolved) == 1
        assert evolved[0].use_count == skill.use_count + 1
        assert evaluation.score == 0.8
        assert new_engine.loop.current_iteration == 1

    def test_run_generation_multiple_skills(self) -> None:
        engine = _make_engine()
        s1 = _make_skill(skill_id="s1", proficiency=0.3)
        s2 = _make_skill(skill_id="s2", proficiency=0.7)
        evolved, _, _ = engine.run_generation((s1, s2), (0.9, 0.4))
        assert len(evolved) == 2
        assert evolved[0].use_count == 1
        assert evolved[1].use_count == 1

    def test_run_generation_persists_evolved_skills_and_outcome(self) -> None:
        experience_store = ExperienceStore()
        reflection_repository = InMemoryReflectionRepository()
        skill_repository = InMemorySkillRepository()
        engine = EvolutionEngine(
            loop=EvolutionLoop(max_iterations=3),
            suite=BenchmarkSuite(),
            evolver=SkillEvolver(),
            metrics=MetricsTracker(),
            experience_store=experience_store,
            reflection_repository=reflection_repository,
            skill_repository=skill_repository,
        )
        skill = _make_skill()
        engine = engine._with_loop(engine.loop)

        evolved, evaluation, new_engine = engine.run_generation((skill,))

        assert skill_repository.get(skill.id) == evolved[0]
        assert new_engine.experience_store is experience_store
        assert new_engine.reflection_repository is reflection_repository
        assert new_engine.skill_repository is skill_repository
        experiences = experience_store.list_experiences()
        assert len(experiences) == 1
        assert experiences[0].confidence == evaluation.score
        reflection = reflection_repository.get(experiences[0].reflection_id)
        assert reflection is not None
        assert reflection.evaluation_id == evaluation.id

    def test_persist_results_saves_supplied_generation_results(self) -> None:
        experience_store = ExperienceStore()
        reflection_repository = InMemoryReflectionRepository()
        skill_repository = InMemorySkillRepository()
        engine = EvolutionEngine(
            loop=EvolutionLoop(max_iterations=3),
            suite=BenchmarkSuite(),
            evolver=SkillEvolver(),
            metrics=MetricsTracker(),
            experience_store=experience_store,
            reflection_repository=reflection_repository,
            skill_repository=skill_repository,
        )
        skill = _make_skill()
        evaluation = Evaluation(
            id=EvaluationId("generation"),
            execution_id=ExecutionId("execution"),
            score=0.75,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary="Generation succeeded",
        )

        engine.persist_results((skill,), evaluation)

        assert skill_repository.get(skill.id) == skill
        experience = experience_store.list_experiences()[0]
        assert experience.lesson == evaluation.summary
        assert reflection_repository.get(experience.reflection_id) is not None

    def test_extract_skill_persists_result(self) -> None:
        skill_repository = InMemorySkillRepository()
        engine = EvolutionEngine(
            loop=EvolutionLoop(max_iterations=3),
            suite=BenchmarkSuite(),
            evolver=SkillEvolver(),
            metrics=MetricsTracker(),
            skill_extractor=DefaultSkillExtractor(),
            skill_repository=skill_repository,
        )
        experience = Experience(
            id=ExperienceId("experience"),
            reflection_id=ReflectionId("reflection"),
            lesson="Prefer exhaustive tests",
            context="evolution",
            confidence=0.9,
        )

        extracted = engine.extract_skill((experience,), "testing", "Testing discipline")

        assert skill_repository.get(extracted.id) == extracted

    def test_is_complete_false_initially(self) -> None:
        engine = _make_engine()
        assert not engine.is_complete()

    def test_is_complete_after_iterations(self) -> None:
        engine = _make_engine(max_iter=2)
        skill = _make_skill()
        _, _, engine = engine.run_generation((skill,), (0.8,))
        assert not engine.is_complete()
        _, _, engine = engine.run_generation((skill,), (0.9,))
        assert engine.is_complete()

    def test_improvement_delta_zero_with_no_data(self) -> None:
        engine = _make_engine()
        assert engine.improvement_delta() == 0.0

    def test_improvement_delta_with_baseline(self) -> None:
        engine = _make_engine()
        ev = Evaluation(
            id=EvaluationId("ev1"),
            execution_id=ExecutionId("ex1"),
            score=0.8,
            verdict=Verdict.PASS,
            criteria=("quality",),
        )
        engine = engine._with_metrics(engine.metrics.record(ev))
        assert engine.improvement_delta(baseline=0.5) == pytest.approx(0.3)

    def test_improvement_delta_without_baseline(self) -> None:
        engine = _make_engine()
        ev = Evaluation(
            id=EvaluationId("ev1"),
            execution_id=ExecutionId("ex1"),
            score=0.6,
            verdict=Verdict.PASS,
            criteria=("quality",),
        )
        engine = engine._with_metrics(engine.metrics.record(ev))
        assert engine.improvement_delta() == pytest.approx(0.6)
