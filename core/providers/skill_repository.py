from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.skill_repository import SkillRepository


class SkillRepositoryProvider(ABC):
    """Factory for SkillRepository instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> SkillRepository:
        """Create and return a SkillRepository instance."""
