from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.workspace_manager import WorkspaceManager


class WorkspaceManagerProvider(ABC):
    """Factory for WorkspaceManager instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> WorkspaceManager:
        """Create and return a WorkspaceManager instance."""
