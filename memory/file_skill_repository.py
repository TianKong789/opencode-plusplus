from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from core.exceptions import SkillError
from core.interfaces.skill_repository import SkillRepository
from core.models.skill import Skill


@dataclass(slots=True)
class FileSkillRepository(SkillRepository):
    """File-backed skill repository.

    Persists skills as JSON files in a directory.
    """

    base_path: Path
    _skills: dict[str, Skill] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        skills_file = self.base_path / "skills.json"
        if skills_file.exists():
            data = json.loads(skills_file.read_text())
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
        skills_file = self.base_path / "skills.json"
        data = [
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
        skills_file.write_text(json.dumps(data, indent=2))

    def save(self, skill: Skill) -> None:
        self._skills[skill.id] = skill
        self._save()

    def get(self, skill_id: str) -> Skill | None:
        return self._skills.get(skill_id)

    def find_by_name(self, name: str) -> Skill | None:
        for skill in self._skills.values():
            if skill.name == name:
                return skill
        return None

    def list_all(self) -> tuple[Skill, ...]:
        return tuple(self._skills.values())

    def delete(self, skill_id: str) -> None:
        if skill_id not in self._skills:
            raise SkillError(f"Skill not found: {skill_id}")
        del self._skills[skill_id]
        self._save()
