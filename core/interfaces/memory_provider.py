from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.experience import Experience
from core.models.skill import Skill


class MemoryProvider(ABC):
    """Stores and retrieves accumulated experiences and skills."""

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

    @abstractmethod
    def store_skill(self, skill: Skill) -> None:
        """Persist a skill record.

        Args:
            skill: The skill to store.
        """

    @abstractmethod
    def get_skill(self, skill_id: str) -> Skill | None:
        """Retrieve a skill by its identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """

    @abstractmethod
    def list_skills(self) -> tuple[Skill, ...]:
        """Retrieve all stored skills.

        Returns:
            An immutable tuple of all skills.
        """
