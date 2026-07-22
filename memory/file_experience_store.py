from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from core.interfaces.experience_store import ExperienceStore as ExperienceStorePort
from core.models.experience import Experience


@dataclass(slots=True)
class FileExperienceStore(ExperienceStorePort):
    """File-backed experience store.

    Persists experiences as JSON files in a directory.
    """

    base_path: Path
    _experiences: dict[str, Experience] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        exp_file = self.base_path / "experiences.json"
        if exp_file.exists():
            data = json.loads(exp_file.read_text())
            for item in data:
                exp = Experience(
                    id=item["id"],
                    reflection_id=item["reflection_id"],
                    lesson=item["lesson"],
                    context=item["context"],
                    confidence=item.get("confidence", 1.0),
                )
                self._experiences[exp.id] = exp

    def _save(self) -> None:
        exp_file = self.base_path / "experiences.json"
        exp_data = [
            {
                "id": e.id,
                "reflection_id": e.reflection_id,
                "lesson": e.lesson,
                "context": e.context,
                "confidence": e.confidence,
            }
            for e in self._experiences.values()
        ]
        exp_file.write_text(json.dumps(exp_data, indent=2))

    def store_experience(self, experience: Experience) -> None:
        self._experiences[experience.id] = experience
        self._save()

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
        self._save()
