from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Experience:
    id: str
    reflection_id: str
    lesson: str
    context: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Experience id must not be empty")
        if not self.reflection_id:
            raise ValueError("Experience reflection_id must not be empty")
        if not self.lesson:
            raise ValueError("Experience lesson must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Experience confidence must be between 0.0 and 1.0")
