from __future__ import annotations

from dataclasses import dataclass, field

from core.interfaces.reflection_repository import ReflectionRepository
from core.models.reflection import Reflection


@dataclass(slots=True)
class InMemoryReflectionRepository(ReflectionRepository):
    """In-memory reflection repository.

    Suitable for development and testing.  Replace with a file-backed
    or database-backed implementation for production use.
    """

    _reflections: dict[str, Reflection] = field(
        default_factory=dict, init=False, repr=False
    )

    def save(self, reflection: Reflection) -> None:
        """Persist a reflection, creating or updating as needed.

        Args:
            reflection: The reflection to save.
        """
        self._reflections[reflection.id] = reflection

    def get(self, reflection_id: str) -> Reflection | None:
        """Retrieve a reflection by its identifier.

        Args:
            reflection_id: The unique identifier of the reflection.

        Returns:
            The reflection if found, None otherwise.
        """
        return self._reflections.get(reflection_id)

    def find_by_evaluation(self, evaluation_id: str) -> Reflection | None:
        """Look up a reflection by its source evaluation.

        Args:
            evaluation_id: The evaluation identifier to search for.

        Returns:
            The first matching reflection, None if not found.
        """
        for reflection in self._reflections.values():
            if reflection.evaluation_id == evaluation_id:
                return reflection
        return None

    def list_all(self) -> tuple[Reflection, ...]:
        """Retrieve every stored reflection.

        Returns:
            An immutable tuple of all reflections.
        """
        return tuple(self._reflections.values())

    def search(self, query: str) -> tuple[Reflection, ...]:
        """Search reflections by keyword in insights, improvements, or root cause.

        Matching is case-insensitive substring search across all text
        fields of the reflection.

        Args:
            query: A keyword or phrase to match against reflection content.

        Returns:
            A tuple of matching reflections.
        """
        lower_query = query.lower()
        results: list[Reflection] = []
        for reflection in self._reflections.values():
            searchable = " ".join([
                *reflection.insights,
                *reflection.improvements,
                reflection.root_cause,
            ]).lower()
            if lower_query in searchable:
                results.append(reflection)
        return tuple(results)

    def delete(self, reflection_id: str) -> None:
        """Remove a reflection by its identifier.

        Args:
            reflection_id: The identifier of the reflection to delete.

        Raises:
            KeyError: If no reflection exists with the given id.
        """
        if reflection_id not in self._reflections:
            raise KeyError(f"Reflection not found: {reflection_id}")
        del self._reflections[reflection_id]
