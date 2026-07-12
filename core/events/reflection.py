from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class ReflectionCompleted(BaseEvent):
    """Emitted when the Reflector finishes analyzing an evaluation."""

    reflection_id: str = ""
    evaluation_id: str = ""
    insight_count: int = 0
