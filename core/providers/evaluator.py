from __future__ import annotations

from abc import ABC, abstractmethod

from core.interfaces.evaluator import Evaluator


class EvaluatorProvider(ABC):
    """Factory for Evaluator instances.

    Override ``create`` in concrete subclasses to wire a real implementation.
    """

    @abstractmethod
    def create(self) -> Evaluator:
        """Create and return an Evaluator instance."""
