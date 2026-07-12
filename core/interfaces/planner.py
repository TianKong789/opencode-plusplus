from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.plan import Plan
from core.models.task import Task


class Planner(ABC):
    """Creates and manages execution plans for tasks."""

    @abstractmethod
    def create_plan(self, task: Task) -> Plan:
        """Create a plan for the given task.

        Args:
            task: The task to create a plan for.

        Returns:
            A new plan with DRAFT status.
        """

    @abstractmethod
    def approve_plan(self, plan: Plan) -> Plan:
        """Approve a draft plan, marking it ready for execution.

        Args:
            plan: The plan to approve.

        Returns:
            The plan with APPROVED status.
        """

    @abstractmethod
    def get_plan(self, plan_id: str) -> Plan | None:
        """Retrieve a plan by its identifier.

        Args:
            plan_id: The unique identifier of the plan.

        Returns:
            The plan if found, None otherwise.
        """
