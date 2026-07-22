from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.execution_engine import ExecutionEngine


class ExecutionEngineProvider(ABC):
    """Factory for ExecutionEngine instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> ExecutionEngine:
        """Create and return an ExecutionEngine instance."""
