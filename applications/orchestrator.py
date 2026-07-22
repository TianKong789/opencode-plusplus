from __future__ import annotations

import logging
from dataclasses import dataclass

from applications.services import ExperienceCapture
from core.events import (
    EvaluationCompleted,
    PlanGenerated,
    ReflectionCompleted,
    TaskReceived,
    WorkflowCompleted,
    WorkflowStarted,
)
from core.ids import WorkflowId, WorkflowStepId
from core.interfaces.evaluator import Evaluator
from core.interfaces.event_bus import EventBus
from core.interfaces.git_manager import GitManager
from core.interfaces.planner import Planner
from core.interfaces.reflector import Reflector
from core.interfaces.workflow_runner import WorkflowRunner
from core.interfaces.workspace_manager import WorkspaceManager
from core.models.plan import Plan
from core.models.reflection import Reflection
from core.models.task import Task
from core.models.workflow import Workflow
from core.models.workflow_step import StepType, WorkflowStep
logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class Orchestrator:
    """Coordinates the application lifecycle and publishes its stage events."""

    planner: Planner
    workflow_runner: WorkflowRunner
    workspace_manager: WorkspaceManager
    evaluator: Evaluator
    reflector: Reflector
    experience_service: ExperienceCapture
    git_manager: GitManager
    event_bus: EventBus
    workspace_base: str = "/tmp/opencode-workspaces"

    def run(self, task: Task) -> Reflection:
        logger.info("Orchestrator starting task: %s", task.title)
        self.event_bus.publish(
            TaskReceived(
                source="orchestrator",
                task_id=task.id,
                title=task.title,
            )
        )

        plan = self.planner.create_plan(task)
        self.event_bus.publish(
            PlanGenerated(
                source="orchestrator",
                plan_id=plan.id,
                task_id=plan.task_id,
                step_count=plan.step_count(),
            )
        )

        workspace = self.workspace_manager.create(
            name=f"task-{task.id}",
            root_path=f"{self.workspace_base}/{task.id}",
        )

        self.git_manager.initialize_if_needed(workspace.root_path)

        workflow = self._plan_to_workflow(plan)
        self.event_bus.publish(
            WorkflowStarted(
                source="orchestrator",
                workflow_id=workflow.id,
                step_count=workflow.step_count(),
            )
        )
        execution = self.workflow_runner.run(workflow, workspace)
        self.event_bus.publish(
            WorkflowCompleted(
                source="orchestrator",
                workflow_id=workflow.id,
                success=execution.succeeded(),
                step_count=workflow.step_count(),
            )
        )

        self.git_manager.commit(workspace, message="Workflow completed")

        evaluation = self.evaluator.evaluate(execution)
        self.event_bus.publish(
            EvaluationCompleted(
                source="orchestrator",
                evaluation_id=evaluation.id,
                execution_id=evaluation.execution_id,
                score=evaluation.score,
                verdict=evaluation.verdict.value,
            )
        )

        reflection = self.reflector.reflect(evaluation)
        self.event_bus.publish(
            ReflectionCompleted(
                source="orchestrator",
                reflection_id=reflection.id,
                evaluation_id=reflection.evaluation_id,
                insight_count=len(reflection.insights),
            )
        )

        self.experience_service.capture(reflection)

        self.workspace_manager.destroy(workspace.id)

        logger.info("Orchestrator finished task: %s", task.title)
        return reflection

    @staticmethod
    def _plan_to_workflow(plan: Plan) -> Workflow:
        steps = tuple(
            WorkflowStep(
                id=WorkflowStepId(f"step-{plan.id}-{i}"),
                name=f"Step {i + 1}",
                type=StepType.ENGINE,
                target=step_text,
            )
            for i, step_text in enumerate(plan.steps)
        )
        return Workflow(
            id=WorkflowId(f"wf-{plan.id}"),
            name=f"Workflow for {plan.task_id}",
            description=f"Auto-generated from plan {plan.id}",
            steps=steps,
        )
