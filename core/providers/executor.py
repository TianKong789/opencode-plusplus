from __future__ import annotations

from abc import ABC, abstractmethod


class ExecutorProvider(ABC):
    """Factory for Executor instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> object:
        """Create and return an Executor instance."""
