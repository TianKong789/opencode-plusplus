from __future__ import annotations

from dataclasses import dataclass, field

from core.exceptions import SkillError
from core.interfaces.skill_repository import SkillRepository
from core.models.skill import Skill


@dataclass(slots=True)
class InMemorySkillRepository(SkillRepository):
    """In-memory skill repository.

    Suitable for development and testing. Replace with a file-backed
    or database-backed implementation for production use.
    """

    _skills: dict[str, Skill] = field(default_factory=dict, init=False, repr=False)

    def save(self, skill: Skill) -> None:
        """Persist a skill, creating or updating as needed.

        Args:
            skill: The skill to save.
        """
        self._skills[skill.id] = skill

    def get(self, skill_id: str) -> Skill | None:
        """Retrieve a skill by its identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """
        return self._skills.get(skill_id)

    def find_by_name(self, name: str) -> Skill | None:
        """Look up a skill by its name.

        Args:
            name: The name to search for.

        Returns:
            The first matching skill, None if not found.
        """
        for skill in self._skills.values():
            if skill.name == name:
                return skill
        return None

    def list_all(self) -> tuple[Skill, ...]:
        """Retrieve every stored skill.

        Returns:
            An immutable tuple of all skills.
        """
        return tuple(self._skills.values())

    def delete(self, skill_id: str) -> None:
        """Remove a skill by its identifier.

        Args:
            skill_id: The identifier of the skill to delete.

        Raises:
            SkillError: If no skill exists with the given id.
        """
        if skill_id not in self._skills:
            raise SkillError(f"Skill not found: {skill_id}")
        del self._skills[skill_id]
