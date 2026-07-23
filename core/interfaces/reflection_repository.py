from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.reflection import Reflection


@runtime_checkable
class ReflectionRepository(Protocol):
    """Stores and queries reflection records."""

    def save(self, reflection: Reflection) -> None:
        """Persist a reflection, creating or updating as needed.

        Args:
            reflection: The reflection to save.
        """

    def get(self, reflection_id: str) -> Reflection | None:
        """Retrieve a reflection by its identifier.

        Args:
            reflection_id: The unique identifier of the reflection.

        Returns:
            The reflection if found, None otherwise.
        """

    def find_by_evaluation(self, evaluation_id: str) -> Reflection | None:
        """Look up a reflection by its source evaluation.

        Args:
            evaluation_id: The evaluation identifier to search for.

        Returns:
            The first matching reflection, None if not found.
        """

    def list_all(self) -> tuple[Reflection, ...]:
        """Retrieve every stored reflection.

        Returns:
            An immutable tuple of all reflections.
        """

    def search(self, query: str) -> tuple[Reflection, ...]:
        """Search reflections by keyword in insights, improvements, or root cause.

        Args:
            query: A keyword or phrase to match against reflection content.

        Returns:
            A tuple of matching reflections, ordered by relevance.
        """

    def delete(self, reflection_id: str) -> None:
        """Remove a reflection by its identifier.

        Args:
            reflection_id: The identifier of the reflection to delete.

        Raises:
            KeyError: If no reflection exists with the given id.
        """
