from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.execution import Execution
from core.models.workflow import Workflow
from core.models.workspace import Workspace


@runtime_checkable
class WorkflowRunner(Protocol):
    """Executes workflows within workspace environments.

    The WorkflowRunner is the kernel of the Runtime layer.  It iterates
    through workflow steps and delegates to the appropriate executor
    (ExecutionEngine for code steps, agents for agent steps, etc.).
    """

    def run(self, workflow: Workflow, workspace: Workspace) -> Execution:
        """Execute a workflow inside the given workspace.

        Args:
            workflow: The workflow defining the steps to execute.
            workspace: The workspace environment to execute within.

        Returns:
            An execution record capturing the outcome.
        """
