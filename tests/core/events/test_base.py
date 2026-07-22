from core.events.base import BaseEvent
from core.events.task import TaskCreated


def test_base_event_has_id_and_timestamp() -> None:
    event = BaseEvent(source="test")
    assert event.id
    assert event.timestamp > 0


def test_task_created_inherits_base_event() -> None:
    event = TaskCreated(source="test", task_id="t1", title="Fix bug")
    assert isinstance(event, BaseEvent)
    assert event.task_id == "t1"
