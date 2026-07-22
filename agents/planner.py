from __future__ import annotations

from dataclasses import dataclass

from core.ids import PlanId, TaskId
from core.interfaces.planner import Planner
from core.models.plan import Plan, PlanStatus
from core.models.task import Task


@dataclass(slots=True, frozen=True)
class PlannerAgent(Planner):
    """Creates and manages execution plans for tasks.

    Placeholder implementation — replace with LLM-driven planning
    for production use.
    """

    def create_plan(self, task: Task) -> Plan:
        return Plan(
            id=PlanId(f"plan-{task.id}"),
            task_id=TaskId(task.id),
            strategy="sequential",
            steps=(f"Execute task: {task.title}",),
            status=PlanStatus.DRAFT,
        )

    def approve_plan(self, plan: Plan) -> Plan:
        return Plan(
            id=plan.id,
            task_id=plan.task_id,
            strategy=plan.strategy,
            steps=plan.steps,
            status=PlanStatus.APPROVED,
        )

    def get_plan(self, plan_id: str) -> Plan | None:
        return None
