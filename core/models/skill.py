from __future__ import annotations

from dataclasses import dataclass

from core.ids import ExperienceId, SkillId


@dataclass(slots=True, frozen=True)
class Skill:
    id: SkillId
    name: str
    description: str
    category: str = ""
    level: str = ""
    version: str = "0.1.0"
    proficiency: float = 0.0
    benchmark_score: float = 0.0
    confidence: float = 0.0
    experience_ids: tuple[ExperienceId, ...] = ()
    use_count: int = 0
    dependencies: tuple[str, ...] = ()
    successors: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Skill id must not be empty")
        if not self.name:
            raise ValueError("Skill name must not be empty")
        if not 0.0 <= self.proficiency <= 1.0:
            raise ValueError("Skill proficiency must be between 0.0 and 1.0")
        if not 0.0 <= self.benchmark_score <= 1.0:
            raise ValueError("Skill benchmark_score must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Skill confidence must be between 0.0 and 1.0")
        if self.use_count < 0:
            raise ValueError("Skill use_count must not be negative")

    def is_mastered(self, threshold: float = 0.9) -> bool:
        return self.proficiency >= threshold
