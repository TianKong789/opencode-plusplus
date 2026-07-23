from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.experience import Experience


@runtime_checkable
class ExperienceStore(Protocol):
    """Stores and retrieves accumulated experiences."""

    def store_experience(self, experience: Experience) -> None:
        """Persist an experience record.

        Args:
            experience: The experience to store.
        """

    def get_experience(self, experience_id: str) -> Experience | None:
        """Retrieve an experience by its identifier.

        Args:
            experience_id: The unique identifier of the experience.

        Returns:
            The experience if found, None otherwise.
        """

    def list_experiences(self) -> tuple[Experience, ...]:
        """Retrieve all stored experiences.

        Returns:
            An immutable tuple of all experiences.
        """
