from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class BenchmarkCompleted(BaseEvent):
    """Emitted when the BenchmarkRunner finishes evaluating a skill."""

    benchmark_id: str = ""
    skill_id: str = ""
    score: float = 0.0
    passed: bool = False
