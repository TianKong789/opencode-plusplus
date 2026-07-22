"""OpenCode execution adapter.

Bridges the core ExecutionEngine interface to the opencode CLI,
allowing the runtime to execute tasks through OpenCode.
"""

from __future__ import annotations

import subprocess
import uuid
from dataclasses import dataclass, field

from core.ids import ExecutionId, PlanId
from core.interfaces.execution_engine import ExecutionEngine
from core.models.execution import Execution, ExecutionStatus
from core.models.workspace import Workspace


@dataclass
class OpenCodeAdapter(ExecutionEngine):
    """ExecutionEngine that delegates to the opencode CLI.

    Runs tasks via ``opencode run`` and captures stdout/stderr.
    """

    opencode_bin: str = "opencode"
    timeout_seconds: float = 120.0
    _outputs: dict[str, str] = field(default_factory=dict)
    _errors: dict[str, str] = field(default_factory=dict)

    def run(self, code: str, workspace: Workspace) -> Execution:
        execution_id = str(uuid.uuid4())[:12]
        plan_id = str(uuid.uuid4())[:12]

        try:
            result = subprocess.run(
                [self.opencode_bin, "run", code],
                cwd=workspace.root_path,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )

            self._outputs[execution_id] = result.stdout
            if result.stderr:
                self._errors[execution_id] = result.stderr

            status = (
                ExecutionStatus.COMPLETED if result.returncode == 0 else ExecutionStatus.FAILED
            )

            return Execution(
                id=ExecutionId(f"exec-{execution_id}"),
                plan_id=PlanId(f"plan-{plan_id}"),
                status=status,
                outputs=(result.stdout,) if result.stdout else (),
                error=result.stderr if result.returncode != 0 else None,
            )

        except subprocess.TimeoutExpired:
            self._errors[execution_id] = "Execution timed out"
            return Execution(
                id=ExecutionId(f"exec-{execution_id}"),
                plan_id=PlanId(f"plan-{plan_id}"),
                status=ExecutionStatus.TIMED_OUT,
                error="Execution timed out",
            )
        except FileNotFoundError:
            self._errors[execution_id] = f"opencode binary not found: {self.opencode_bin}"
            return Execution(
                id=ExecutionId(f"exec-{execution_id}"),
                plan_id=PlanId(f"plan-{plan_id}"),
                status=ExecutionStatus.FAILED,
                error=f"opencode binary not found: {self.opencode_bin}",
            )

    def get_output(self, execution_id: str) -> str | None:
        return self._outputs.get(execution_id)

    def get_error(self, execution_id: str) -> str | None:
        return self._errors.get(execution_id)
