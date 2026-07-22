from agents.planner import PlannerAgent
from core.ids import TaskId
from core.models.task import Task


def test_create_and_approve_plan() -> None:
    agent = PlannerAgent()
    task = Task(id=TaskId("t1"), title="Test", description="desc")
    plan = agent.create_plan(task)
    assert plan.task_id == "t1"
    assert plan.status.value == "draft"

    approved = agent.approve_plan(plan)
    assert approved.status.value == "approved"
