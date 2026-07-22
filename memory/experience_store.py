from __future__ import annotations

from dataclasses import dataclass, field

from core.interfaces.experience_store import ExperienceStore as ExperienceStorePort
from core.models.experience import Experience


@dataclass(slots=True)
class ExperienceStore(ExperienceStorePort):
    """In-memory experience store.

    Suitable for development and testing. Replace with a persistent
    backend for production use.
    """

    _experiences: dict[str, Experience] = field(default_factory=dict, init=False, repr=False)

    def store_experience(self, experience: Experience) -> None:
        self._experiences[experience.id] = experience

    def get_experience(self, experience_id: str) -> Experience | None:
        return self._experiences.get(experience_id)

    def list_experiences(self) -> tuple[Experience, ...]:
        return tuple(self._experiences.values())

    def search_experiences(self, query: str) -> tuple[Experience, ...]:
        lower_query = query.lower()
        results: list[Experience] = []
        for exp in self._experiences.values():
            searchable = f"{exp.lesson} {exp.context}".lower()
            if lower_query in searchable:
                results.append(exp)
        return tuple(results)

    def delete_experience(self, experience_id: str) -> None:
        if experience_id not in self._experiences:
            raise KeyError(f"Experience not found: {experience_id}")
        del self._experiences[experience_id]
