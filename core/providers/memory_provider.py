from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.memory_provider import MemoryProvider


class MemoryProviderProvider(ABC):
    """Factory for MemoryProvider instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> MemoryProvider:
        """Create and return a MemoryProvider instance."""
