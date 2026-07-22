from __future__ import annotations

from dataclasses import dataclass, field

from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class SkillRegistry:
    """Skill versioning and lookup registry.

    Maintains versioned skill records and provides promotion
    from experimental to production status.
    """

    _production: dict[str, Skill] = field(default_factory=dict, init=False, repr=False)
    _experimental: dict[str, Skill] = field(default_factory=dict, init=False, repr=False)

    def register(self, skill: Skill, experimental: bool = True) -> None:
        """Register a skill as experimental or production.

        Args:
            skill: The skill to register.
            experimental: If True, register as experimental.
        """
        if experimental:
            self._experimental[skill.id] = skill
        else:
            self._production[skill.id] = skill

    def promote(self, skill_id: str) -> Skill | None:
        """Promote a skill from experimental to production.

        Args:
            skill_id: The identifier of the skill to promote.

        Returns:
            The promoted skill, None if not found in experimental.
        """
        skill = self._experimental.pop(skill_id, None)
        if skill is not None:
            self._production[skill_id] = skill
        return skill

    def get_production(self, skill_id: str) -> Skill | None:
        """Retrieve a production skill by identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """
        return self._production.get(skill_id)

    def get_experimental(self, skill_id: str) -> Skill | None:
        """Retrieve an experimental skill by identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """
        return self._experimental.get(skill_id)

    def list_production(self) -> tuple[Skill, ...]:
        """Retrieve all production skills.

        Returns:
            An immutable tuple of production skills.
        """
        return tuple(self._production.values())

    def list_experimental(self) -> tuple[Skill, ...]:
        """Retrieve all experimental skills.

        Returns:
            An immutable tuple of experimental skills.
        """
        return tuple(self._experimental.values())
