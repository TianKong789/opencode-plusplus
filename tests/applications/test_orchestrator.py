from __future__ import annotations

from unittest.mock import MagicMock

from applications.orchestrator import Orchestrator
from core.events import (
    EvaluationCompleted,
    PlanGenerated,
    ReflectionCompleted,
    TaskReceived,
    WorkflowCompleted,
    WorkflowStarted,
)
from core.events.base import BaseEvent
from core.ids import (
    EvaluationId,
    ExecutionId,
    PlanId,
    ReflectionId,
    TaskId,
    WorkspaceId,
)
from core.models.evaluation import Evaluation, Verdict
from core.models.execution import Execution, ExecutionStatus
from core.models.plan import Plan, PlanStatus
from core.models.reflection import Reflection
from core.models.task import Task
from core.models.workspace import Workspace
from runtime.event_bus import SyncEventBus


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_planner() -> MagicMock:
    planner = MagicMock()
    planner.create_plan.return_value = Plan(
        id=PlanId("plan-1"),
        task_id=TaskId("task-1"),
        strategy="do stuff",
        steps=("step-a", "step-b"),
        status=PlanStatus.APPROVED,
    )
    return planner


def _mock_workflow_runner() -> MagicMock:
    runner = MagicMock()
    runner.run.return_value = Execution(
        id=ExecutionId("exec-1"),
        plan_id=PlanId("plan-1"),
        status=ExecutionStatus.COMPLETED,
        outputs=("result",),
    )
    return runner


def _mock_workspace_manager() -> MagicMock:
    mgr = MagicMock()
    mgr.create.return_value = Workspace(
        id=WorkspaceId("ws-1"),
        name="task-task-1",
        root_path="/tmp/opencode-workspaces/task-1",
    )
    return mgr


def _mock_evaluator() -> MagicMock:
    evaluator = MagicMock()
    evaluator.evaluate.return_value = Evaluation(
        id=EvaluationId("eval-1"),
        execution_id=ExecutionId("exec-1"),
        score=0.9,
        verdict=Verdict.PASS,
        criteria=("correctness",),
    )
    return evaluator


def _mock_reflector() -> MagicMock:
    reflector = MagicMock()
    reflector.reflect.return_value = Reflection(
        id=ReflectionId("refl-1"),
        evaluation_id=EvaluationId("eval-1"),
        insights=("good job",),
        improvements=("none",),
    )
    return reflector


def _mock_experience_service() -> MagicMock:
    return MagicMock()


def _mock_git_manager() -> MagicMock:
    return MagicMock()


def _make_task() -> Task:
    return Task(id=TaskId("task-1"), title="Test task", description="desc")


def _make_orchestrator(**overrides: MagicMock) -> Orchestrator:
    defaults = {
        "planner": _mock_planner(),
        "workflow_runner": _mock_workflow_runner(),
        "workspace_manager": _mock_workspace_manager(),
        "evaluator": _mock_evaluator(),
        "reflector": _mock_reflector(),
        "experience_service": _mock_experience_service(),
        "git_manager": _mock_git_manager(),
        "event_bus": SyncEventBus(),
    }
    defaults.update(overrides)
    return Orchestrator(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Orchestrator dataclass structure
# ---------------------------------------------------------------------------


def test_orchestrator_is_dataclass() -> None:
    from dataclasses import fields

    field_names = [f.name for f in fields(Orchestrator)]
    assert "planner" in field_names
    assert "workflow_runner" in field_names
    assert "workspace_manager" in field_names
    assert "evaluator" in field_names
    assert "reflector" in field_names
    assert "experience_service" in field_names
    assert "git_manager" in field_names
    assert "workspace_base" in field_names
    assert "event_bus" in field_names


# ---------------------------------------------------------------------------
# Orchestrator.run() integration
# ---------------------------------------------------------------------------


def test_run_returns_reflection_and_emits_lifecycle_events() -> None:
    event_bus = SyncEventBus()
    events: list[BaseEvent] = []
    event_bus.subscribe(TaskReceived, events.append)
    event_bus.subscribe(PlanGenerated, events.append)
    event_bus.subscribe(WorkflowStarted, events.append)
    event_bus.subscribe(WorkflowCompleted, events.append)
    event_bus.subscribe(EvaluationCompleted, events.append)
    event_bus.subscribe(ReflectionCompleted, events.append)

    orch = _make_orchestrator(event_bus=event_bus)
    result = orch.run(_make_task())

    assert isinstance(result, Reflection)
    assert result.id == "refl-1"
    assert [type(event) for event in events] == [
        TaskReceived,
        PlanGenerated,
        WorkflowStarted,
        WorkflowCompleted,
        EvaluationCompleted,
        ReflectionCompleted,
    ]


def test_run_calls_planner_with_task() -> None:
    planner = _mock_planner()
    orch = _make_orchestrator(planner=planner)
    task = _make_task()
    orch.run(task)
    planner.create_plan.assert_called_once_with(task)


def test_run_creates_workspace() -> None:
    ws_mgr = _mock_workspace_manager()
    orch = _make_orchestrator(workspace_manager=ws_mgr)
    orch.run(_make_task())
    ws_mgr.create.assert_called_once()


def test_run_destroys_workspace() -> None:
    ws_mgr = _mock_workspace_manager()
    orch = _make_orchestrator(workspace_manager=ws_mgr)
    orch.run(_make_task())
    ws_mgr.destroy.assert_called_once_with(WorkspaceId("ws-1"))


def test_run_delegates_to_workflow_runner() -> None:
    runner = _mock_workflow_runner()
    orch = _make_orchestrator(workflow_runner=runner)
    orch.run(_make_task())
    runner.run.assert_called_once()


def test_run_evaluates_execution() -> None:
    evaluator = _mock_evaluator()
    orch = _make_orchestrator(evaluator=evaluator)
    orch.run(_make_task())
    evaluator.evaluate.assert_called_once()


def test_run_reflects_on_evaluation() -> None:
    reflector = _mock_reflector()
    orch = _make_orchestrator(reflector=reflector)
    orch.run(_make_task())
    reflector.reflect.assert_called_once()


def test_run_captures_experience() -> None:
    exp_svc = _mock_experience_service()
    orch = _make_orchestrator(experience_service=exp_svc)
    orch.run(_make_task())
    exp_svc.capture.assert_called_once()


def test_run_initializes_git() -> None:
    git_mgr = _mock_git_manager()
    orch = _make_orchestrator(git_manager=git_mgr)
    orch.run(_make_task())
    git_mgr.initialize_if_needed.assert_called_once_with("/tmp/opencode-workspaces/task-1")


def test_run_commits_after_execution() -> None:
    git_mgr = _mock_git_manager()
    orch = _make_orchestrator(git_manager=git_mgr)
    orch.run(_make_task())
    git_mgr.commit.assert_called_once()
    call_args = git_mgr.commit.call_args
    assert call_args.kwargs["message"] == "Workflow completed"


def test_plan_to_workflow_converts_steps() -> None:
    plan = Plan(
        id=PlanId("p1"),
        task_id=TaskId("t1"),
        strategy="test",
        steps=("a", "b", "c"),
    )
    workflow = Orchestrator._plan_to_workflow(plan)

    assert workflow.step_count() == 3
    assert workflow.id == "wf-p1"
    for i, step in enumerate(workflow.steps):
        assert step.target == ("a", "b", "c")[i]
        assert step.name == f"Step {i + 1}"


def test_plan_to_workflow_empty_steps() -> None:
    plan = Plan(
        id=PlanId("p2"),
        task_id=TaskId("t2"),
        strategy="test",
        steps=("only",),
    )
    workflow = Orchestrator._plan_to_workflow(plan)
    assert workflow.step_count() == 1
