from __future__ import annotations

from abc import ABC, abstractmethod


class SkillRepositoryProvider(ABC):
    """Factory for SkillRepository instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> object:
        """Create and return a SkillRepository instance."""
