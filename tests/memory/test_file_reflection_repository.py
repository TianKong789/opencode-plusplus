import tempfile
from pathlib import Path

from core.ids import EvaluationId, ReflectionId
from core.models.reflection import Reflection
from memory.file_reflection_repository import FileReflectionRepository


def _make_reflection(rid: str = "r1") -> Reflection:
    return Reflection(
        id=ReflectionId(rid),
        evaluation_id=EvaluationId("ev1"),
        insights=("use type hints",),
        improvements=("add docstrings",),
        root_cause="lack of documentation",
    )


class TestFileReflectionRepository:
    def test_save_and_retrieve(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = FileReflectionRepository(base_path=Path(tmpdir))
            ref = _make_reflection()
            repo.save(ref)
            assert repo.get("r1") == ref

    def test_persistence_across_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            repo1 = FileReflectionRepository(base_path=path)
            repo1.save(_make_reflection())
            repo2 = FileReflectionRepository(base_path=path)
            assert repo2.get("r1") is not None

    def test_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = FileReflectionRepository(base_path=Path(tmpdir))
            repo.save(_make_reflection())
            results = repo.search("type hints")
            assert len(results) == 1

    def test_delete(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = FileReflectionRepository(base_path=Path(tmpdir))
            repo.save(_make_reflection())
            repo.delete("r1")
            assert repo.get("r1") is None
