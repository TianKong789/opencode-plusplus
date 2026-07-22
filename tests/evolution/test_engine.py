from evolution.engine import EvolutionEngine
from evolution.loop import EvolutionLoop
from evolution.skill_evolver import SkillEvolver
from benchmarks.metrics import MetricsTracker
from benchmarks.suite import BenchmarkSuite
from core.ids import EvaluationId, ExecutionId, SkillId
from core.models.evaluation import Evaluation, Verdict
from core.models.skill import Skill


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
        engine.metrics.record(ev)
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
        engine.metrics.record(ev)
        assert engine.improvement_delta() == pytest.approx(0.6)


import pytest
