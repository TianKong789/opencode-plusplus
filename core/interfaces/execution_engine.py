from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.execution import Execution
from core.models.workspace import Workspace


class ExecutionEngine(ABC):
    """Runs code within an isolated workspace environment."""

    @abstractmethod
    def run(self, code: str, workspace: Workspace) -> Execution:
        """Execute code inside the given workspace.

        Args:
            code: The code string to run.
            workspace: The workspace to execute within.

        Returns:
            An execution record capturing the outcome.
        """

    @abstractmethod
    def get_output(self, execution_id: str) -> str | None:
        """Retrieve the captured output of a completed execution.

        Args:
            execution_id: The identifier of the execution.

        Returns:
            The stdout output if available, None otherwise.
        """

    @abstractmethod
    def get_error(self, execution_id: str) -> str | None:
        """Retrieve the error output of a failed execution.

        Args:
            execution_id: The identifier of the execution.

        Returns:
            The stderr output if available, None otherwise.
        """
