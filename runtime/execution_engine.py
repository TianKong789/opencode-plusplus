from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.ids import ExecutionId, PlanId
from core.interfaces.execution_engine import ExecutionEngine
from core.models.execution import Execution, ExecutionStatus
from core.models.workspace import Workspace


@dataclass(slots=True, frozen=True)
class LocalExecutionEngine(ExecutionEngine):
    """Stub execution engine that writes hello.txt and returns success."""

    def run(self, code: str, workspace: Workspace) -> Execution:
        """Write ``hello.txt`` into the workspace and return a completed execution.

        Args:
            code: Ignored — present to satisfy the interface contract.
            workspace: The workspace to write into.

        Returns:
            An Execution with COMPLETED status.
        """
        (Path(workspace.root_path) / "hello.txt").write_text("hello")
        return Execution(
            id=ExecutionId("exec-stub"),
            plan_id=PlanId("plan-stub"),
            status=ExecutionStatus.COMPLETED,
            outputs=("hello",),
        )

    def get_output(self, execution_id: str) -> str | None:
        return None

    def get_error(self, execution_id: str) -> str | None:
        return None
