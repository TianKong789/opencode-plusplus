from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.reflector import Reflector


class ReflectorProvider(ABC):
    """Factory for Reflector instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> Reflector:
        """Create and return a Reflector instance."""
