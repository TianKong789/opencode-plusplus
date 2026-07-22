from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.experience import Experience
from core.models.skill import Skill


class SkillExtractor(ABC):
    """Extracts skills from accumulated experiences."""

    @abstractmethod
    def extract(self, experiences: tuple[Experience, ...], name: str, description: str) -> Skill:
        """Create a skill from a collection of related experiences."""
