from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from core.interfaces.reflection_repository import ReflectionRepository
from core.models.reflection import Reflection


@dataclass(slots=True)
class FileReflectionRepository(ReflectionRepository):
    """File-backed reflection repository.

    Persists reflections as JSON files in a directory.
    """

    base_path: Path
    _reflections: dict[str, Reflection] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        reflections_file = self.base_path / "reflections.json"
        if reflections_file.exists():
            data = json.loads(reflections_file.read_text())
            for item in data:
                ref = Reflection(
                    id=item["id"],
                    evaluation_id=item["evaluation_id"],
                    insights=tuple(item.get("insights", [])),
                    improvements=tuple(item.get("improvements", [])),
                    root_cause=item.get("root_cause", ""),
                )
                self._reflections[ref.id] = ref

    def _save(self) -> None:
        reflections_file = self.base_path / "reflections.json"
        data = [
            {
                "id": r.id,
                "evaluation_id": r.evaluation_id,
                "insights": list(r.insights),
                "improvements": list(r.improvements),
                "root_cause": r.root_cause,
            }
            for r in self._reflections.values()
        ]
        reflections_file.write_text(json.dumps(data, indent=2))

    def save(self, reflection: Reflection) -> None:
        self._reflections[reflection.id] = reflection
        self._save()

    def get(self, reflection_id: str) -> Reflection | None:
        return self._reflections.get(reflection_id)

    def find_by_evaluation(self, evaluation_id: str) -> Reflection | None:
        for reflection in self._reflections.values():
            if reflection.evaluation_id == evaluation_id:
                return reflection
        return None

    def list_all(self) -> tuple[Reflection, ...]:
        return tuple(self._reflections.values())

    def search(self, query: str) -> tuple[Reflection, ...]:
        lower_query = query.lower()
        results: list[Reflection] = []
        for reflection in self._reflections.values():
            searchable = " ".join([
                *reflection.insights,
                *reflection.improvements,
                reflection.root_cause,
            ]).lower()
            if lower_query in searchable:
                results.append(reflection)
        return tuple(results)

    def delete(self, reflection_id: str) -> None:
        if reflection_id not in self._reflections:
            raise KeyError(f"Reflection not found: {reflection_id}")
        del self._reflections[reflection_id]
        self._save()
