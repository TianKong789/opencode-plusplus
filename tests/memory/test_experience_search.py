import pytest

from core.ids import ExperienceId, ReflectionId
from core.models.experience import Experience
from memory.experience_store import ExperienceStore


def _make_experience(
    eid: str = "e1",
    lesson: str = "use type hints",
    context: str = "lack of type safety",
    confidence: float = 0.9,
) -> Experience:
    return Experience(
        id=ExperienceId(eid),
        reflection_id=ReflectionId("r1"),
        lesson=lesson,
        context=context,
        confidence=confidence,
    )


class TestSearchExperiences:
    def test_search_by_lesson(self) -> None:
        store = ExperienceStore()
        exp = _make_experience(lesson="use type hints everywhere")
        store.store_experience(exp)
        results = store.search_experiences("type hints")
        assert len(results) == 1
        assert results[0] == exp

    def test_search_by_context(self) -> None:
        store = ExperienceStore()
        exp = _make_experience(context="N+1 query causing slow responses")
        store.store_experience(exp)
        results = store.search_experiences("N+1")
        assert len(results) == 1

    def test_search_case_insensitive(self) -> None:
        store = ExperienceStore()
        exp = _make_experience(lesson="Use Type Hints")
        store.store_experience(exp)
        results = store.search_experiences("type hints")
        assert len(results) == 1

    def test_search_no_match(self) -> None:
        store = ExperienceStore()
        exp = _make_experience(lesson="use type hints")
        store.store_experience(exp)
        results = store.search_experiences("refactoring")
        assert len(results) == 0

    def test_search_multiple_results(self) -> None:
        store = ExperienceStore()
        exp1 = _make_experience(eid="e1", lesson="use type hints")
        exp2 = _make_experience(eid="e2", context="type safety matters")
        store.store_experience(exp1)
        store.store_experience(exp2)
        results = store.search_experiences("type")
        assert len(results) == 2

    def test_search_empty_store(self) -> None:
        store = ExperienceStore()
        results = store.search_experiences("anything")
        assert results == ()


class TestDeleteExperience:
    def test_delete_existing(self) -> None:
        store = ExperienceStore()
        exp = _make_experience()
        store.store_experience(exp)
        store.delete_experience("e1")
        assert store.get_experience("e1") is None
        assert len(store.list_experiences()) == 0

    def test_delete_missing_raises(self) -> None:
        store = ExperienceStore()
        with pytest.raises(KeyError, match="Experience not found"):
            store.delete_experience("nonexistent")

    def test_delete_only_removes_target(self) -> None:
        store = ExperienceStore()
        exp1 = _make_experience(eid="e1")
        exp2 = _make_experience(eid="e2")
        store.store_experience(exp1)
        store.store_experience(exp2)
        store.delete_experience("e1")
        assert store.get_experience("e1") is None
        assert store.get_experience("e2") == exp2
