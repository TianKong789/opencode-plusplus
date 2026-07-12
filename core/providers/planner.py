from __future__ import annotations

from abc import ABC, abstractmethod


class PlannerProvider(ABC):
    """Factory for Planner instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> object:
        """Create and return a Planner instance."""
