from __future__ import annotations

from abc import ABC, abstractmethod


class WorkspaceManagerProvider(ABC):
    """Factory for WorkspaceManager instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> object:
        """Create and return a WorkspaceManager instance."""
