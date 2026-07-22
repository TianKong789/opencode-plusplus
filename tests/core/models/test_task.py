from core.ids import TaskId
from core.models.task import Task, TaskStatus


def test_task_creation() -> None:
    task = Task(id=TaskId("t1"), title="Test", description="desc")
    assert task.id == "t1"
    assert task.status == TaskStatus.PENDING


def test_task_is_terminal() -> None:
    task = Task(id=TaskId("t1"), title="Test", description="desc", status=TaskStatus.COMPLETED)
    assert task.is_terminal() is True


def test_task_is_root() -> None:
    task = Task(id=TaskId("t1"), title="Test", description="desc")
    assert task.is_root() is True

    child = Task(id=TaskId("t2"), title="Child", description="desc", parent_id=TaskId("t1"))
    assert child.is_root() is False


def test_task_has_tag() -> None:
    task = Task(id=TaskId("t1"), title="Test", description="desc", tags=("bug", "urgent"))
    assert task.has_tag("bug") is True
    assert task.has_tag("feature") is False
