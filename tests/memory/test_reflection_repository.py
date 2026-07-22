import pytest

from core.ids import EvaluationId, ReflectionId
from core.models.reflection import Reflection
from memory.reflection_repository import InMemoryReflectionRepository


def _make_reflection(
    rid: str = "r1",
    eval_id: str = "ev1",
    insights: tuple[str, ...] = ("use type hints",),
    improvements: tuple[str, ...] = ("add docstrings",),
    root_cause: str = "lack of documentation",
) -> Reflection:
    return Reflection(
        id=ReflectionId(rid),
        evaluation_id=EvaluationId(eval_id),
        insights=insights,
        improvements=improvements,
        root_cause=root_cause,
    )


class TestSaveAndGet:
    def test_save_and_retrieve(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection()
        repo.save(ref)
        assert repo.get("r1") == ref

    def test_get_missing_returns_none(self) -> None:
        repo = InMemoryReflectionRepository()
        assert repo.get("nonexistent") is None

    def test_save_overwrites_existing(self) -> None:
        repo = InMemoryReflectionRepository()
        ref1 = _make_reflection(rid="r1", insights=("old",))
        ref2 = _make_reflection(rid="r1", insights=("new",))
        repo.save(ref1)
        repo.save(ref2)
        assert repo.get("r1") == ref2
        assert len(repo.list_all()) == 1


class TestFindByEvaluation:
    def test_find_existing(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection(eval_id="ev42")
        repo.save(ref)
        assert repo.find_by_evaluation("ev42") == ref

    def test_find_missing_returns_none(self) -> None:
        repo = InMemoryReflectionRepository()
        assert repo.find_by_evaluation("nonexistent") is None

    def test_find_returns_first_match(self) -> None:
        repo = InMemoryReflectionRepository()
        ref1 = _make_reflection(rid="r1", eval_id="ev1")
        ref2 = _make_reflection(rid="r2", eval_id="ev1")
        repo.save(ref1)
        repo.save(ref2)
        result = repo.find_by_evaluation("ev1")
        assert result is not None
        assert result.id in ("r1", "r2")


class TestListAll:
    def test_empty_store(self) -> None:
        repo = InMemoryReflectionRepository()
        assert repo.list_all() == ()

    def test_multiple_reflections(self) -> None:
        repo = InMemoryReflectionRepository()
        ref1 = _make_reflection(rid="r1")
        ref2 = _make_reflection(rid="r2")
        repo.save(ref1)
        repo.save(ref2)
        result = repo.list_all()
        assert len(result) == 2
        assert ref1 in result
        assert ref2 in result


class TestSearch:
    def test_search_by_insight(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection(insights=("use type hints", "add tests"))
        repo.save(ref)
        results = repo.search("type hints")
        assert len(results) == 1
        assert results[0] == ref

    def test_search_by_improvement(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection(improvements=("optimize queries",))
        repo.save(ref)
        results = repo.search("optimize")
        assert len(results) == 1

    def test_search_by_root_cause(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection(root_cause="N+1 query pattern")
        repo.save(ref)
        results = repo.search("N+1")
        assert len(results) == 1

    def test_search_case_insensitive(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection(insights=("Use Type Hints",))
        repo.save(ref)
        results = repo.search("type hints")
        assert len(results) == 1

    def test_search_no_match(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection(insights=("use type hints",))
        repo.save(ref)
        results = repo.search("refactoring")
        assert len(results) == 0

    def test_search_multiple_results(self) -> None:
        repo = InMemoryReflectionRepository()
        ref1 = _make_reflection(rid="r1", insights=("use type hints",))
        ref2 = _make_reflection(rid="r2", root_cause="missing type hints")
        repo.save(ref1)
        repo.save(ref2)
        results = repo.search("type hints")
        assert len(results) == 2


class TestDelete:
    def test_delete_existing(self) -> None:
        repo = InMemoryReflectionRepository()
        ref = _make_reflection()
        repo.save(ref)
        repo.delete("r1")
        assert repo.get("r1") is None
        assert len(repo.list_all()) == 0

    def test_delete_missing_raises(self) -> None:
        repo = InMemoryReflectionRepository()
        with pytest.raises(KeyError, match="Reflection not found"):
            repo.delete("nonexistent")

    def test_delete_only_removes_target(self) -> None:
        repo = InMemoryReflectionRepository()
        ref1 = _make_reflection(rid="r1")
        ref2 = _make_reflection(rid="r2")
        repo.save(ref1)
        repo.save(ref2)
        repo.delete("r1")
        assert repo.get("r1") is None
        assert repo.get("r2") == ref2
