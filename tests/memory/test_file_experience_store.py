import tempfile
from pathlib import Path

from core.ids import ExperienceId, ReflectionId
from core.models.experience import Experience
from memory.file_experience_store import FileExperienceStore


def _make_experience(eid: str = "e1") -> Experience:
    return Experience(
        id=ExperienceId(eid),
        reflection_id=ReflectionId("r1"),
        lesson="use type hints",
        context="lack of type safety",
    )


class TestFileExperienceStore:
    def test_store_and_retrieve(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileExperienceStore(base_path=Path(tmpdir))
            exp = _make_experience()
            store.store_experience(exp)
            assert store.get_experience("e1") == exp

    def test_persistence_across_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            store1 = FileExperienceStore(base_path=path)
            store1.store_experience(_make_experience())
            store2 = FileExperienceStore(base_path=path)
            assert store2.get_experience("e1") is not None

    def test_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileExperienceStore(base_path=Path(tmpdir))
            store.store_experience(_make_experience())
            results = store.search_experiences("type hints")
            assert len(results) == 1

    def test_delete(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FileExperienceStore(base_path=Path(tmpdir))
            store.store_experience(_make_experience())
            store.delete_experience("e1")
            assert store.get_experience("e1") is None
