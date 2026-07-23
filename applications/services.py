from __future__ import annotations

from dataclasses import dataclass

from core.events.experience import ExperienceStored
from core.ids import ExperienceId, ReflectionId
from core.interfaces.event_bus import EventBus
from core.interfaces.experience_store import ExperienceStore
from core.interfaces.reflection_repository import ReflectionRepository
from core.interfaces.skill_repository import SkillRepository
from core.models.evaluation import Evaluation
from core.models.experience import Experience
from core.models.reflection import Reflection
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class ExperienceCapture:
    """Converts reflections into durable experiences and publishes the result."""

    experience_store: ExperienceStore
    event_bus: EventBus

    def capture(self, reflection: Reflection) -> Experience:
        lesson = reflection.insights[0] if reflection.insights else reflection.root_cause
        context = reflection.root_cause or "; ".join(reflection.insights)

        experience = Experience(
            id=ExperienceId(f"exp-{reflection.id}"),
            reflection_id=reflection.id,
            lesson=lesson,
            context=context,
        )
        self.experience_store.store_experience(experience)
        self.event_bus.publish(
            ExperienceStored(
                source="experience_capture",
                experience_id=experience.id,
                reflection_id=reflection.id,
                lesson=experience.lesson,
            )
        )
        return experience


@dataclass(slots=True, frozen=True)
class EvolutionPersistenceService:
    """Persists evolution results (skills, reflections, experiences).

    Implements ``core.interfaces.evolution_persistence.EvolutionPersistence``.
    """

    skill_repository: SkillRepository | None = None
    reflection_repository: ReflectionRepository | None = None
    experience_store: ExperienceStore | None = None

    def persist(
        self,
        skills: tuple[Skill, ...],
        evaluation: Evaluation,
    ) -> None:
        if self.skill_repository is not None:
            for skill in skills:
                self.skill_repository.save(skill)

        lesson = evaluation.summary or f"Generation {evaluation.id}: score={evaluation.score:.3f}"
        reflection = Reflection(
            id=ReflectionId(f"generation-reflection-{evaluation.id}"),
            evaluation_id=evaluation.id,
            insights=(lesson,),
            improvements=tuple(
                f"{skill.name}: proficiency={skill.proficiency:.3f}" for skill in skills
            ),
            root_cause=evaluation.verdict.value,
        )
        if self.reflection_repository is not None:
            self.reflection_repository.save(reflection)

        if self.experience_store is not None:
            self.experience_store.store_experience(
                Experience(
                    id=ExperienceId(f"generation-experience-{evaluation.id}"),
                    reflection_id=reflection.id,
                    lesson=lesson,
                    context=(
                        f"criteria={', '.join(evaluation.criteria)} "
                        f"score={evaluation.score:.3f} verdict={evaluation.verdict.value}"
                    ),
                    confidence=evaluation.score,
                )
            )
