import tempfile
from pathlib import Path

from core.ids import SkillId
from core.models.skill import Skill
from memory.file_skill_repository import FileSkillRepository


def _make_skill(skill_id: str = "s1") -> Skill:
    return Skill(
        id=SkillId(skill_id),
        name="python",
        description="Python programming",
    )


class TestFileSkillRepository:
    def test_save_and_retrieve(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = FileSkillRepository(base_path=Path(tmpdir))
            skill = _make_skill()
            repo.save(skill)
            assert repo.get("s1") == skill

    def test_persistence_across_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            repo1 = FileSkillRepository(base_path=path)
            repo1.save(_make_skill())
            repo2 = FileSkillRepository(base_path=path)
            assert repo2.get("s1") is not None

    def test_find_by_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = FileSkillRepository(base_path=Path(tmpdir))
            repo.save(_make_skill())
            found = repo.find_by_name("python")
            assert found is not None
            assert found.id == "s1"

    def test_delete(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = FileSkillRepository(base_path=Path(tmpdir))
            repo.save(_make_skill())
            repo.delete("s1")
            assert repo.get("s1") is None
