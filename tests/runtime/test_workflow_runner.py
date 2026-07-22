from __future__ import annotations

from core.events.base import BaseEvent
from core.events.workflow import StepCompleted, StepStarted, WorkflowCompleted, WorkflowStarted
from core.ids import ExecutionId, PlanId, WorkflowId, WorkflowStepId
from core.interfaces.workflow_runner import WorkflowRunner
from core.models.execution import Execution, ExecutionStatus
from core.models.workflow import Workflow
from core.models.workflow_step import StepType, WorkflowStep
from core.models.workspace import Workspace
from runtime.event_bus import SyncEventBus
from runtime.workflow_runner import LocalWorkflowRunner


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class StubEngine:
    """Minimal ExecutionEngine stub for testing WorkflowRunner."""

    def __init__(self, result: Execution | None = None) -> None:
        self._result = result or Execution(
            id=ExecutionId("exec-stub"),
            plan_id=PlanId("plan-stub"),
            status=ExecutionStatus.COMPLETED,
            outputs=("ok",),
        )
        self.run_calls: list[str] = []

    def run(self, code: str, workspace: Workspace) -> Execution:  # type: ignore[override]
        self.run_calls.append(code)
        return self._result

    def get_output(self, execution_id: str) -> str | None:  # type: ignore[override]
        return None

    def get_error(self, execution_id: str) -> str | None:  # type: ignore[override]
        return None


def _make_workspace() -> Workspace:
    return Workspace(id=WorkflowId("ws-test"), name="test", root_path="/tmp/test")


def _make_workflow(*steps: WorkflowStep) -> Workflow:
    return Workflow(
        id=WorkflowId("wf-test"),
        name="test-workflow",
        description="test",
        steps=steps,
    )


def _engine_step(target: str = "print(1)", step_id: str = "step-1", name: str = "Run code") -> WorkflowStep:
    return WorkflowStep(
        id=WorkflowStepId(step_id),
        name=name,
        type=StepType.ENGINE,
        target=target,
    )


def _system_step(name: str = "init", target: str = "noop") -> WorkflowStep:
    return WorkflowStep(
        id=WorkflowStepId("step-sys"),
        name=name,
        type=StepType.SYSTEM,
        target=target,
    )


def _capture_events(bus: SyncEventBus) -> list[BaseEvent]:
    """Subscribe to all four workflow event types and return collected events."""
    events: list[BaseEvent] = []
    for evt_type in (WorkflowStarted, StepStarted, StepCompleted, WorkflowCompleted):
        bus.subscribe(evt_type, lambda e, _events=events: _events.append(e))
    return events


# ---------------------------------------------------------------------------
# Interface compliance
# ---------------------------------------------------------------------------


def test_workflow_runner_is_abstract() -> None:
    import pytest

    with pytest.raises(TypeError):
        WorkflowRunner()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# LocalWorkflowRunner — execution
# ---------------------------------------------------------------------------


def test_run_empty_workflow_returns_completed() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow()

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.COMPLETED
    assert result.outputs == ()


def test_run_single_engine_step() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(_engine_step("x = 1"))

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.COMPLETED
    assert engine.run_calls == ["x = 1"]
    assert result.outputs == ("ok",)


def test_run_multiple_engine_steps() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(
        _engine_step("a"),
        _engine_step("b"),
        _engine_step("c"),
    )

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.COMPLETED
    assert engine.run_calls == ["a", "b", "c"]


def test_run_collects_outputs_from_all_steps() -> None:
    engine = StubEngine(
        result=Execution(
            id=ExecutionId("e1"),
            plan_id=PlanId("plan-stub"),
            status=ExecutionStatus.COMPLETED,
            outputs=("out1", "out2"),
        )
    )
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(_engine_step("a"), _engine_step("b"))

    result = runner.run(workflow, ws)

    assert result.outputs == ("out1", "out2", "out1", "out2")


def test_run_stops_on_engine_failure() -> None:
    engine = StubEngine(
        result=Execution(
            id=ExecutionId("e1"),
            plan_id=PlanId("plan-stub"),
            status=ExecutionStatus.FAILED,
            error="boom",
        )
    )
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(_engine_step("a"), _engine_step("b"))

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.FAILED
    assert result.error == "boom"
    assert engine.run_calls == ["a"]  # second step never ran


def test_run_skips_non_engine_steps() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(_system_step("skip-me", "noop"), _engine_step("x"))

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.COMPLETED
    assert engine.run_calls == ["x"]


def test_run_system_step_completes_without_engine_call() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(_system_step("init", "setup_workspace"))

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.COMPLETED
    assert result.outputs == ()
    assert engine.run_calls == []


def test_run_mixed_engine_and_system_steps() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(
        _system_step("setup", "prepare"),
        _engine_step("run_tests"),
        _system_step("cleanup", "teardown"),
        _engine_step("deploy"),
    )

    result = runner.run(workflow, ws)

    assert result.status == ExecutionStatus.COMPLETED
    assert engine.run_calls == ["run_tests", "deploy"]
    assert result.outputs == ("ok", "ok")


def test_run_execution_id_prefixes_workflow_id() -> None:
    engine = StubEngine()
    runner = LocalWorkflowRunner(engine=engine)
    ws = _make_workspace()
    workflow = _make_workflow(_engine_step())

    result = runner.run(workflow, ws)

    assert result.id.startswith("exec-wf-")


# ---------------------------------------------------------------------------
# LocalWorkflowRunner — event publication
# ---------------------------------------------------------------------------


def test_empty_workflow_publishes_started_then_completed() -> None:
    bus = SyncEventBus()
    runner = LocalWorkflowRunner(engine=StubEngine(), event_bus=bus)
    events = _capture_events(bus)
    ws = _make_workspace()
    workflow = _make_workflow()

    runner.run(workflow, ws)

    assert len(events) == 2
    assert isinstance(events[0], WorkflowStarted)
    assert isinstance(events[1], WorkflowCompleted)
    assert events[0].step_count == 0
    assert events[1].success is True


def test_single_step_publishes_full_lifecycle() -> None:
    bus = SyncEventBus()
    runner = LocalWorkflowRunner(engine=StubEngine(), event_bus=bus)
    events = _capture_events(bus)
    ws = _make_workspace()
    workflow = _make_workflow(_engine_step("code"))

    runner.run(workflow, ws)

    types = [type(e) for e in events]
    assert types == [WorkflowStarted, StepStarted, StepCompleted, WorkflowCompleted]
    assert events[0].workflow_id == str(workflow.id)  # type: ignore[attr-defined]
    assert events[1].step_name == "Run code"  # type: ignore[attr-defined]
    assert events[2].success is True  # type: ignore[attr-defined]
    assert events[3].success is True  # type: ignore[attr-defined]


def test_multiple_steps_publish_events_in_order() -> None:
    bus = SyncEventBus()
    runner = LocalWorkflowRunner(engine=StubEngine(), event_bus=bus)
    events = _capture_events(bus)
    ws = _make_workspace()
    workflow = _make_workflow(
        _engine_step("a", step_id="s1", name="First"),
        _engine_step("b", step_id="s2", name="Second"),
    )

    runner.run(workflow, ws)

    # Started → StepStarted(s1) → StepCompleted(s1) → StepStarted(s2) → StepCompleted(s2) → Completed
    assert len(events) == 6
    assert isinstance(events[0], WorkflowStarted)
    assert isinstance(events[1], StepStarted)
    assert events[1].step_id == "s1"  # type: ignore[attr-defined]
    assert isinstance(events[2], StepCompleted)
    assert isinstance(events[3], StepStarted)
    assert events[3].step_id == "s2"  # type: ignore[attr-defined]
    assert isinstance(events[4], StepCompleted)
    assert isinstance(events[5], WorkflowCompleted)
    assert events[5].success is True  # type: ignore[attr-defined]


def test_failure_publishes_completed_with_success_false() -> None:
    bus = SyncEventBus()
    engine = StubEngine(
        result=Execution(
            id=ExecutionId("e1"),
            plan_id=PlanId("plan-stub"),
            status=ExecutionStatus.FAILED,
            error="boom",
        )
    )
    runner = LocalWorkflowRunner(engine=engine, event_bus=bus)
    events = _capture_events(bus)
    ws = _make_workspace()
    workflow = _make_workflow(_engine_step("a"), _engine_step("b"))

    runner.run(workflow, ws)

    # Started → StepStarted(s1) → StepCompleted(s1, fail) → Completed(fail)
    assert len(events) == 4
    assert isinstance(events[2], StepCompleted)
    assert events[2].success is False  # type: ignore[attr-defined]
    assert isinstance(events[3], WorkflowCompleted)
    assert events[3].success is False  # type: ignore[attr-defined]
    # StepStarted(s2) never published — fail-fast
