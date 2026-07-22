from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from core.interfaces.memory_provider import MemoryProvider
from core.models.experience import Experience
from core.models.skill import Skill


@dataclass(slots=True, frozen=True)
class FileExperienceStore(MemoryProvider):
    """File-backed experience and skill store.

    Persists experiences and skills as JSON files in a directory.
    """

    base_path: Path
    _experiences: dict[str, Experience] = field(default_factory=dict, init=False, repr=False)
    _skills: dict[str, Skill] = field(default_factory=dict, init=False, repr=False)

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

        skill_file = self.base_path / "skills.json"
        if skill_file.exists():
            data = json.loads(skill_file.read_text())
            for item in data:
                skill = Skill(
                    id=item["id"],
                    name=item["name"],
                    description=item["description"],
                    category=item.get("category", ""),
                    level=item.get("level", ""),
                    version=item.get("version", "0.1.0"),
                    proficiency=item.get("proficiency", 0.0),
                    benchmark_score=item.get("benchmark_score", 0.0),
                    confidence=item.get("confidence", 0.0),
                    experience_ids=tuple(item.get("experience_ids", [])),
                    use_count=item.get("use_count", 0),
                    dependencies=tuple(item.get("dependencies", [])),
                    successors=tuple(item.get("successors", [])),
                )
                self._skills[skill.id] = skill

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

        skill_file = self.base_path / "skills.json"
        skill_data = [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "category": s.category,
                "level": s.level,
                "version": s.version,
                "proficiency": s.proficiency,
                "benchmark_score": s.benchmark_score,
                "confidence": s.confidence,
                "experience_ids": list(s.experience_ids),
                "use_count": s.use_count,
                "dependencies": list(s.dependencies),
                "successors": list(s.successors),
            }
            for s in self._skills.values()
        ]
        skill_file.write_text(json.dumps(skill_data, indent=2))

    def store_experience(self, experience: Experience) -> None:
        self._experiences[experience.id] = experience
        self._save()

    def get_experience(self, experience_id: str) -> Experience | None:
        return self._experiences.get(experience_id)

    def list_experiences(self) -> tuple[Experience, ...]:
        return tuple(self._experiences.values())

    def store_skill(self, skill: Skill) -> None:
        self._skills[skill.id] = skill
        self._save()

    def get_skill(self, skill_id: str) -> Skill | None:
        return self._skills.get(skill_id)

    def list_skills(self) -> tuple[Skill, ...]:
        return tuple(self._skills.values())

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
