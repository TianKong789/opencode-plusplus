from __future__ import annotations

from dataclasses import dataclass

from core.exceptions import ExecutionError
from core.ids import ExecutionId, PlanId
from core.interfaces.executor import Executor
from core.models.execution import Execution, ExecutionStatus
from core.models.plan import Plan


@dataclass(slots=True, frozen=True)
class ExecutorAgent(Executor):
    """Runs plans and manages execution lifecycle.

    Placeholder implementation — replace with LLM-driven execution
    for production use.
    """

    def execute(self, plan: Plan) -> Execution:
        """Execute an approved plan.

        Args:
            plan: The plan to execute. Must have APPROVED status.

        Returns:
            An execution record with COMPLETED status.
        """
        return Execution(
            id=ExecutionId(f"exec-{plan.id}"),
            plan_id=PlanId(plan.id),
            status=ExecutionStatus.COMPLETED,
            outputs=(f"Executed plan: {plan.strategy}",),
        )

    def cancel(self, execution_id: str) -> Execution:
        """Cancel a running execution.

        Args:
            execution_id: The identifier of the execution to cancel.

        Returns:
            The execution with FAILED status.

        Raises:
            ExecutionError: Always, since cancellation is not supported yet.
        """
        raise ExecutionError(f"Cannot cancel execution: {execution_id}")

    def get_status(self, execution_id: str) -> Execution | None:
        """Retrieve the current state of an execution.

        Args:
            execution_id: The identifier of the execution.

        Returns:
            None — executions are not persisted in this implementation.
        """
        return None
