from __future__ import annotations

import pytest

from core.events.base import BaseEvent
from core.events.execution import ExecutionCompleted
from core.events.workflow import WorkflowStarted, StepStarted, StepCompleted, WorkflowCompleted
from core.interfaces.event_bus import EventBus
from runtime.event_bus import SyncEventBus, NullEventBus


# ---------------------------------------------------------------------------
# Interface compliance
# ---------------------------------------------------------------------------


def test_event_bus_is_abstract() -> None:
    with pytest.raises(TypeError):
        EventBus()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# SyncEventBus
# ---------------------------------------------------------------------------


def test_sync_event_bus_publish_dispatches() -> None:
    bus = SyncEventBus()
    received: list[BaseEvent] = []
    bus.subscribe(BaseEvent, lambda e: received.append(e))
    bus.publish(BaseEvent(source="test"))
    assert len(received) == 1


def test_sync_event_bus_subscribe_wrong_type_not_triggered() -> None:
    bus = SyncEventBus()
    received: list[BaseEvent] = []
    bus.subscribe(ExecutionCompleted, lambda e: received.append(e))
    bus.publish(BaseEvent(source="test"))
    assert len(received) == 0


def test_sync_event_bus_multiple_subscribers() -> None:
    bus = SyncEventBus()
    calls: list[str] = []
    bus.subscribe(BaseEvent, lambda e: calls.append("a"))
    bus.subscribe(BaseEvent, lambda e: calls.append("b"))
    bus.publish(BaseEvent(source="test"))
    assert calls == ["a", "b"]


def test_sync_event_bus_exact_type_match() -> None:
    bus = SyncEventBus()
    received: list[BaseEvent] = []
    bus.subscribe(WorkflowStarted, lambda e: received.append(e))
    bus.publish(WorkflowStarted(source="runner", workflow_id="wf-1", step_count=3))
    assert len(received) == 1
    assert isinstance(received[0], WorkflowStarted)


def test_sync_event_bus_subclass_not_triggered() -> None:
    """Subscribers to BaseEvent should NOT be triggered by subclass events."""
    bus = SyncEventBus()
    received: list[BaseEvent] = []
    bus.subscribe(BaseEvent, lambda e: received.append(e))
    # StepStarted is a subclass of BaseEvent; only exact type match triggers
    bus.publish(StepStarted(source="runner", workflow_id="wf-1", step_id="s1", step_name="init"))
    # No handlers registered for StepStarted, so nothing fires
    assert len(received) == 0


# ---------------------------------------------------------------------------
# NullEventBus (true no-op)
# ---------------------------------------------------------------------------


def test_null_event_bus_publish_does_not_raise() -> None:
    bus = NullEventBus()
    bus.publish(BaseEvent(source="test"))


def test_null_event_bus_subscribe_then_publish_dispatches_nothing() -> None:
    bus = NullEventBus()
    received: list[BaseEvent] = []
    bus.subscribe(BaseEvent, lambda e: received.append(e))
    bus.publish(BaseEvent(source="test"))
    assert len(received) == 0
