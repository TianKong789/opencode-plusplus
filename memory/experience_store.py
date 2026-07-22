from __future__ import annotations

from dataclasses import dataclass, field

from core.interfaces.memory_provider import MemoryProvider
from core.models.experience import Experience
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class ExperienceStore(MemoryProvider):
    """In-memory experience and skill store.

    Suitable for development and testing. Replace with a persistent
    backend for production use.
    """

    _experiences: dict[str, Experience] = field(default_factory=dict, init=False, repr=False)
    _skills: dict[str, Skill] = field(default_factory=dict, init=False, repr=False)

    def store_experience(self, experience: Experience) -> None:
        """Persist an experience record.

        Args:
            experience: The experience to store.
        """
        self._experiences[experience.id] = experience

    def get_experience(self, experience_id: str) -> Experience | None:
        """Retrieve an experience by its identifier.

        Args:
            experience_id: The unique identifier of the experience.

        Returns:
            The experience if found, None otherwise.
        """
        return self._experiences.get(experience_id)

    def list_experiences(self) -> tuple[Experience, ...]:
        """Retrieve all stored experiences.

        Returns:
            An immutable tuple of all experiences.
        """
        return tuple(self._experiences.values())

    def store_skill(self, skill: Skill) -> None:
        """Persist a skill record.

        Args:
            skill: The skill to store.
        """
        self._skills[skill.id] = skill

    def get_skill(self, skill_id: str) -> Skill | None:
        """Retrieve a skill by its identifier.

        Args:
            skill_id: The unique identifier of the skill.

        Returns:
            The skill if found, None otherwise.
        """
        return self._skills.get(skill_id)

    def list_skills(self) -> tuple[Skill, ...]:
        """Retrieve all stored skills.

        Returns:
            An immutable tuple of all skills.
        """
        return tuple(self._skills.values())

    def search_experiences(self, query: str) -> tuple[Experience, ...]:
        """Search experiences by keyword in lesson or context.

        Matching is case-insensitive substring search.

        Args:
            query: A keyword or phrase to match against experience content.

        Returns:
            A tuple of matching experiences.
        """
        lower_query = query.lower()
        results: list[Experience] = []
        for exp in self._experiences.values():
            searchable = f"{exp.lesson} {exp.context}".lower()
            if lower_query in searchable:
                results.append(exp)
        return tuple(results)

    def delete_experience(self, experience_id: str) -> None:
        """Remove an experience by its identifier.

        Args:
            experience_id: The identifier of the experience to delete.

        Raises:
            KeyError: If no experience exists with the given id.
        """
        if experience_id not in self._experiences:
            raise KeyError(f"Experience not found: {experience_id}")
        del self._experiences[experience_id]
