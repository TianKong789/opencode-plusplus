from __future__ import annotations

from dataclasses import dataclass, field

from core.events.base import BaseEvent


@dataclass(slots=True, frozen=True)
class SkillExtracted(BaseEvent):
    """Emitted when a new skill is extracted from experiences."""

    skill_id: str = ""
    name: str = ""
    experience_ids: tuple[str, ...] = ()
