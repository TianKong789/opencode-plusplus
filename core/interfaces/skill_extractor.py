from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.experience import Experience
from core.models.skill import Skill


@runtime_checkable
class SkillExtractor(Protocol):
    """Extracts skills from accumulated experiences."""

    def extract(self, experiences: tuple[Experience, ...], name: str, description: str) -> Skill:
        """Create a skill from a collection of related experiences."""
