from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Reflection:
    id: str
    evaluation_id: str
    insights: tuple[str, ...]
    improvements: tuple[str, ...]
    root_cause: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Reflection id must not be empty")
        if not self.evaluation_id:
            raise ValueError("Reflection evaluation_id must not be empty")

    def has_actionable_items(self) -> bool:
        return len(self.improvements) > 0
