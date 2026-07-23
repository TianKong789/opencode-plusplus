"""Tests for application services."""

from __future__ import annotations

from core.ids import EvaluationId, ExecutionId, ExperienceId, ReflectionId, SkillId
from core.models.evaluation import Evaluation, Verdict
from core.models.skill import Skill
from applications.services import EvolutionPersistenceService
from memory.experience_store import ExperienceStore
from memory.reflection_repository import InMemoryReflectionRepository
from memory.skill_repository import InMemorySkillRepository


class TestEvolutionPersistenceService:
    """Tests for EvolutionPersistenceService.persist()."""

    def test_persist_saves_skills_when_repository_provided(self) -> None:
        skill_repository = InMemorySkillRepository()
        service = EvolutionPersistenceService(skill_repository=skill_repository)
        skill = Skill(
            id=SkillId("s1"),
            name="python",
            description="Python programming",
            proficiency=0.8,
        )
        evaluation = Evaluation(
            id=EvaluationId("gen-eval-1"),
            execution_id=ExecutionId("exec-1"),
            score=0.8,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary="Generation 1",
        )

        service.persist((skill,), evaluation)

        assert skill_repository.get(skill.id) == skill

    def test_persist_creates_reflection_when_repository_provided(self) -> None:
        reflection_repository = InMemoryReflectionRepository()
        service = EvolutionPersistenceService(reflection_repository=reflection_repository)
        skill = Skill(
            id=SkillId("s1"),
            name="python",
            description="Python programming",
            proficiency=0.8,
        )
        evaluation = Evaluation(
            id=EvaluationId("gen-eval-1"),
            execution_id=ExecutionId("exec-1"),
            score=0.8,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary="Generation 1",
        )

        service.persist((skill,), evaluation)

        experiences = reflection_repository.list_all()
        assert len(experiences) == 1
        assert experiences[0].evaluation_id == evaluation.id

    def test_persist_creates_experience_when_store_provided(self) -> None:
        experience_store = ExperienceStore()
        service = EvolutionPersistenceService(experience_store=experience_store)
        skill = Skill(
            id=SkillId("s1"),
            name="python",
            description="Python programming",
            proficiency=0.8,
        )
        evaluation = Evaluation(
            id=EvaluationId("gen-eval-1"),
            execution_id=ExecutionId("exec-1"),
            score=0.8,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary="Generation 1",
        )

        service.persist((skill,), evaluation)

        experiences = experience_store.list_experiences()
        assert len(experiences) == 1
        assert experiences[0].confidence == evaluation.score

    def test_persist_handles_no_repositories_gracefully(self) -> None:
        service = EvolutionPersistenceService()
        skill = Skill(
            id=SkillId("s1"),
            name="python",
            description="Python programming",
            proficiency=0.8,
        )
        evaluation = Evaluation(
            id=EvaluationId("gen-eval-1"),
            execution_id=ExecutionId("exec-1"),
            score=0.8,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary="Generation 1",
        )

        # Should not raise
        service.persist((skill,), evaluation)

    def test_persist_saves_multiple_skills(self) -> None:
        skill_repository = InMemorySkillRepository()
        service = EvolutionPersistenceService(skill_repository=skill_repository)
        skills = (
            Skill(id=SkillId("s1"), name="python", description="Python", proficiency=0.8),
            Skill(id=SkillId("s2"), name="rust", description="Rust", proficiency=0.6),
        )
        evaluation = Evaluation(
            id=EvaluationId("gen-eval-1"),
            execution_id=ExecutionId("exec-1"),
            score=0.7,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary="Generation 1",
        )

        service.persist(skills, evaluation)

        assert skill_repository.get("s1") == skills[0]
        assert skill_repository.get("s2") == skills[1]

    def test_persist_uses_fallback_lesson_when_summary_is_none(self) -> None:
        experience_store = ExperienceStore()
        service = EvolutionPersistenceService(experience_store=experience_store)
        skill = Skill(
            id=SkillId("s1"),
            name="python",
            description="Python programming",
            proficiency=0.8,
        )
        evaluation = Evaluation(
            id=EvaluationId("gen-eval-1"),
            execution_id=ExecutionId("exec-1"),
            score=0.8,
            verdict=Verdict.PASS,
            criteria=("generation",),
            summary=None,
        )

        service.persist((skill,), evaluation)

        experiences = experience_store.list_experiences()
        assert len(experiences) == 1
        assert "gen-eval-1" in experiences[0].lesson
