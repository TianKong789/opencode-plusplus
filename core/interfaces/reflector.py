from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.evaluation import Evaluation
from core.models.reflection import Reflection


@runtime_checkable
class Reflector(Protocol):
    """Analyzes evaluations to extract insights and improvement actions."""

    def reflect(self, evaluation: Evaluation) -> Reflection:
        """Generate a reflection from an evaluation.

        Args:
            evaluation: The evaluation to reflect upon.

        Returns:
            A reflection containing insights and improvement steps.
        """

    def get_reflection(self, reflection_id: str) -> Reflection | None:
        """Retrieve a reflection by its identifier.

        Args:
            reflection_id: The unique identifier of the reflection.

        Returns:
            The reflection if found, None otherwise.
        """
