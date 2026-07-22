from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from core.ids import ExecutionId, PlanId
from core.interfaces.event_bus import EventBus
from core.interfaces.execution_engine import ExecutionEngine
from core.interfaces.workflow_runner import WorkflowRunner
from core.events.workflow import StepCompleted, StepStarted, WorkflowCompleted, WorkflowStarted
from core.models.execution import Execution, ExecutionStatus
from core.models.workflow import Workflow
from core.models.workflow_step import StepType
from core.models.workspace import Workspace
from core.null_objects import NullEventBus

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class LocalWorkflowRunner(WorkflowRunner):
    """Executes workflows locally by delegating ENGINE steps to an ExecutionEngine.

    Iterates through workflow steps in order.  ENGINE-type steps are
    delegated to the execution engine.  SYSTEM-type steps are logged as
    no-ops.  Other step types are skipped with a warning.

    Publishes lifecycle events to the provided EventBus:
    WorkflowStarted → (StepStarted → StepCompleted)* → WorkflowCompleted.
    """

    engine: ExecutionEngine
    event_bus: EventBus = field(default_factory=NullEventBus)

    def run(self, workflow: Workflow, workspace: Workspace) -> Execution:
        """Execute a workflow inside the given workspace.

        Iterates through each step in the workflow and delegates
        ENGINE-type steps to the execution engine.  Returns an Execution
        with COMPLETED status if all steps succeed, or FAILED on the
        first error.

        Publishes WorkflowStarted before any steps run and
        WorkflowCompleted after all steps finish or on failure.

        Args:
            workflow: The workflow defining the steps to execute.
            workspace: The workspace environment to execute within.

        Returns:
            An execution record capturing the outcome.
        """
        wf_id = str(workflow.id)

        self.event_bus.publish(WorkflowStarted(
            source="workflow_runner",
            workflow_id=wf_id,
            step_count=workflow.step_count(),
        ))

        if workflow.step_count() == 0:
            self.event_bus.publish(WorkflowCompleted(
                source="workflow_runner",
                workflow_id=wf_id,
                success=True,
                step_count=0,
            ))
            return Execution(
                id=ExecutionId(f"exec-wf-{workflow.id}"),
                plan_id=PlanId(f"wf-{workflow.id}"),
                status=ExecutionStatus.COMPLETED,
            )

        outputs: list[str] = []
        for step in workflow.steps:
            self.event_bus.publish(StepStarted(
                source="workflow_runner",
                workflow_id=wf_id,
                step_id=str(step.id),
                step_name=step.name,
            ))

            step_success = True
            elapsed_ms = 0.0
            if step.type == StepType.ENGINE:
                logger.info("Running ENGINE step: %s", step.name)
                t0 = time.monotonic()
                result = self.engine.run(step.target, workspace)
                elapsed_ms = (time.monotonic() - t0) * 1000
                step_success = result.succeeded()
                if step_success:
                    outputs.extend(result.outputs)
            elif step.type == StepType.SYSTEM:
                logger.info("Running SYSTEM step: %s", step.name)
            else:
                logger.warning("Skipping unsupported step type %s: %s", step.type.value, step.name)

            self.event_bus.publish(StepCompleted(
                source="workflow_runner",
                workflow_id=wf_id,
                step_id=str(step.id),
                step_name=step.name,
                success=step_success,
                duration_ms=elapsed_ms,
            ))

            if not step_success:
                self.event_bus.publish(WorkflowCompleted(
                    source="workflow_runner",
                    workflow_id=wf_id,
                    success=False,
                    step_count=workflow.step_count(),
                ))
                return Execution(
                    id=ExecutionId(f"exec-wf-{workflow.id}"),
                    plan_id=PlanId(f"wf-{workflow.id}"),
                    status=ExecutionStatus.FAILED,
                    error=result.error,
                )

        self.event_bus.publish(WorkflowCompleted(
            source="workflow_runner",
            workflow_id=wf_id,
            success=True,
            step_count=workflow.step_count(),
        ))

        return Execution(
            id=ExecutionId(f"exec-wf-{workflow.id}"),
            plan_id=PlanId(f"wf-{workflow.id}"),
            status=ExecutionStatus.COMPLETED,
            outputs=tuple(outputs),
        )
