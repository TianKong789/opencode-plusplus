from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.experience import Experience


class ExperienceStore(ABC):
    """Stores and retrieves accumulated experiences."""

    @abstractmethod
    def store_experience(self, experience: Experience) -> None:
        """Persist an experience record.

        Args:
            experience: The experience to store.
        """

    @abstractmethod
    def get_experience(self, experience_id: str) -> Experience | None:
        """Retrieve an experience by its identifier.

        Args:
            experience_id: The unique identifier of the experience.

        Returns:
            The experience if found, None otherwise.
        """

    @abstractmethod
    def list_experiences(self) -> tuple[Experience, ...]:
        """Retrieve all stored experiences.

        Returns:
            An immutable tuple of all experiences.
        """
