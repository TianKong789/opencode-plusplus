from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class ExperienceStored(BaseEvent):
    """Emitted when a new experience is persisted to memory."""

    experience_id: str = ""
    reflection_id: str = ""
    lesson: str = ""
