from __future__ import annotations

from dataclasses import dataclass, field

from core.events.plan import PlanGenerated
from core.ids import PlanId, TaskId
from core.interfaces.event_bus import EventBus
from core.interfaces.planner import Planner
from core.models.plan import Plan, PlanStatus
from core.models.task import Task
from core.null_objects import NullEventBus


@dataclass(slots=True, frozen=True)
class PlannerAgent(Planner):
    """Creates and manages execution plans for tasks.

    Placeholder implementation — replace with LLM-driven planning
    for production use.
    """

    event_bus: EventBus = field(default_factory=NullEventBus)

    def create_plan(self, task: Task) -> Plan:
        plan = Plan(
            id=PlanId(f"plan-{task.id}"),
            task_id=TaskId(task.id),
            strategy="sequential",
            steps=(f"Execute task: {task.title}",),
            status=PlanStatus.DRAFT,
        )
        self.event_bus.publish(
            PlanGenerated(
                source="planner",
                plan_id=plan.id,
                task_id=task.id,
                step_count=plan.step_count(),
            )
        )
        return plan

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
