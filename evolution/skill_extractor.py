from __future__ import annotations

from dataclasses import dataclass

from core.ids import ExperienceId, SkillId
from core.interfaces.skill_extractor import SkillExtractor as SkillExtractorPort
from core.models.experience import Experience
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class DefaultSkillExtractor(SkillExtractorPort):
    """Extracts skills from accumulated experiences.

    Analyzes experience patterns and produces Skill records
    that can be stored in a SkillRepository.
    """

    def extract(self, experiences: tuple[Experience, ...], name: str, description: str) -> Skill:
        if not experiences:
            avg_confidence = 0.0
        else:
            avg_confidence = sum(e.confidence for e in experiences) / len(experiences)

        return Skill(
            id=SkillId(f"skill-{name}"),
            name=name,
            description=description,
            proficiency=min(avg_confidence, 1.0),
            experience_ids=tuple(ExperienceId(e.id) for e in experiences),
            use_count=len(experiences),
        )
