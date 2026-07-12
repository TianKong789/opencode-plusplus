from __future__ import annotations

from dataclasses import dataclass

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class SkillCreated(BaseEvent):
    """Emitted when a new skill is registered in the repository."""

    skill_id: str = ""
    name: str = ""
