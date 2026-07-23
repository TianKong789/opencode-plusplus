from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.execution import Execution
from core.models.workspace import Workspace


@runtime_checkable
class ExecutionEngine(Protocol):
    """Runs code within an isolated workspace environment."""

    def run(self, code: str, workspace: Workspace) -> Execution:
        """Execute code inside the given workspace.

        Args:
            code: The code string to run.
            workspace: The workspace to execute within.

        Returns:
            An execution record capturing the outcome.
        """

    def get_output(self, execution_id: str) -> str | None:
        """Retrieve the captured output of a completed execution.

        Args:
            execution_id: The identifier of the execution.

        Returns:
            The stdout output if available, None otherwise.
        """

    def get_error(self, execution_id: str) -> str | None:
        """Retrieve the error output of a failed execution.

        Args:
            execution_id: The identifier of the execution.

        Returns:
            The stderr output if available, None otherwise.
        """
