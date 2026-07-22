from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.executor import Executor


class ExecutorProvider(ABC):
    """Factory for Executor instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> Executor:
        """Create and return an Executor instance."""
