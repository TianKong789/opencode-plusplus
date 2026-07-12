from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.skill import Skill


class SkillRepository(ABC):
    """Stores and queries skill records."""

    @abstractmethod
    def save(self, skill: Skill) -> None:
        """Persist a skill, creating or updating as needed.

        Args:
            skill: The skill to save.
        """

    @abstractmethod
    def get(self, skill_id: str) -> Skill | None:
        """Retrieve a skill by its identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """

    @abstractmethod
    def find_by_name(self, name: str) -> Skill | None:
        """Look up a skill by its name.

        Args:
            name: The name to search for.

        Returns:
            The first matching skill, None if not found.
        """

    @abstractmethod
    def list_all(self) -> tuple[Skill, ...]:
        """Retrieve every stored skill.

        Returns:
            An immutable tuple of all skills.
        """

    @abstractmethod
    def delete(self, skill_id: str) -> None:
        """Remove a skill by its identifier.

        Args:
            skill_id: The identifier of the skill to delete.

        Raises:
            KeyError: If no skill exists with the given id.
        """
