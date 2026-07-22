import pytest

from core.exceptions import (
    EvaluationError,
    EvolutionError,
    ExecutionError,
    MemoryStoreError,
    PlanningError,
    ProjectError,
    SkillError,
    WorkspaceError,
)


def test_inheritance() -> None:
    for cls in [
        PlanningError,
        ExecutionError,
        EvaluationError,
        MemoryStoreError,
        EvolutionError,
        SkillError,
        WorkspaceError,
    ]:
        assert issubclass(cls, ProjectError)


def test_catch_as_base() -> None:
    with pytest.raises(ProjectError):
        raise PlanningError("test")
