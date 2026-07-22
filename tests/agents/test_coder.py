import pytest

from agents.coder import CoderAgent
from core.ids import PlanId, TaskId
from core.models.plan import Plan, PlanStatus
from core.models.code_artifact import ArtifactStatus


def _make_plan(plan_id: str = "p1", task_id: str = "t1") -> Plan:
    return Plan(
        id=PlanId(plan_id),
        task_id=TaskId(task_id),
        strategy="sequential",
        steps=("step1",),
        status=PlanStatus.APPROVED,
    )


class TestCoderAgent:
    def test_implement_creates_artifact(self) -> None:
        agent = CoderAgent()
        plan = _make_plan()
        artifact = agent.implement(plan)
        assert artifact.plan_id == plan.id
        assert len(artifact.files) == 1
        assert artifact.status == ArtifactStatus.GENERATED

    def test_implement_uses_plan_task_id(self) -> None:
        agent = CoderAgent()
        plan = _make_plan(task_id="task-42")
        artifact = agent.implement(plan)
        assert "task-42" in artifact.files[0]

    def test_implement_includes_summary(self) -> None:
        agent = CoderAgent()
        plan = _make_plan()
        artifact = agent.implement(plan)
        assert plan.strategy in artifact.summary

    def test_get_artifact_returns_none(self) -> None:
        agent = CoderAgent()
        assert agent.get_artifact("any") is None
