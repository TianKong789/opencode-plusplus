from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.git_manager import GitManager


class GitManagerProvider(ABC):
    """Factory for GitManager instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> GitManager:
        """Create and return a GitManager instance."""
