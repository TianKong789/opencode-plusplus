from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.skill import Skill


@runtime_checkable
class SkillRepository(Protocol):
    """Stores and queries skill records."""

    def save(self, skill: Skill) -> None:
        """Persist a skill, creating or updating as needed.

        Args:
            skill: The skill to save.
        """

    def get(self, skill_id: str) -> Skill | None:
        """Retrieve a skill by its identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """

    def find_by_name(self, name: str) -> Skill | None:
        """Look up a skill by its name.

        Args:
            name: The name to search for.

        Returns:
            The first matching skill, None if not found.
        """

    def list_all(self) -> tuple[Skill, ...]:
        """Retrieve every stored skill.

        Returns:
            An immutable tuple of all skills.
        """

    def delete(self, skill_id: str) -> None:
        """Remove a skill by its identifier.

        Args:
            skill_id: The identifier of the skill to delete.

        Raises:
            KeyError: If no skill exists with the given id.
        """
