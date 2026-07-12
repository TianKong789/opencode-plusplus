from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.execution import Execution
from core.models.plan import Plan


class Executor(ABC):
    """Runs plans and manages execution lifecycle."""

    @abstractmethod
    def execute(self, plan: Plan) -> Execution:
        """Execute an approved plan.

        Args:
            plan: The plan to execute. Must have APPROVED status.

        Returns:
            An execution record with QUEUED or RUNNING status.
        """

    @abstractmethod
    def cancel(self, execution_id: str) -> Execution:
        """Cancel a running execution.

        Args:
            execution_id: The identifier of the execution to cancel.

        Returns:
            The execution with CANCELLED or terminal status.

        Raises:
            KeyError: If no execution exists with the given id.
        """

    @abstractmethod
    def get_status(self, execution_id: str) -> Execution | None:
        """Retrieve the current state of an execution.

        Args:
            execution_id: The identifier of the execution.

        Returns:
            The execution if found, None otherwise.
        """
