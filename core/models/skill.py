from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Skill:
    id: str
    name: str
    description: str
    proficiency: float = 0.0
    experience_ids: tuple[str, ...] = ()
    use_count: int = 0

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Skill id must not be empty")
        if not self.name:
            raise ValueError("Skill name must not be empty")
        if not 0.0 <= self.proficiency <= 1.0:
            raise ValueError("Skill proficiency must be between 0.0 and 1.0")
        if self.use_count < 0:
            raise ValueError("Skill use_count must not be negative")

    def is_mastered(self, threshold: float = 0.9) -> bool:
        return self.proficiency >= threshold
