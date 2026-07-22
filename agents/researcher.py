from __future__ import annotations

from dataclasses import dataclass

from core.ids import ResearchId
from core.interfaces.researcher import Researcher
from core.models.research import Research
from core.models.task import Task


@dataclass(slots=True, frozen=True)
class ResearcherAgent(Researcher):
    """Gathers context and findings for tasks.

    Placeholder implementation — replace with LLM-driven research
    for production use.
    """

    def research(self, task: Task) -> Research:
        """Research a task to gather context.

        Args:
            task: The task to research.

        Returns:
            Research findings derived from the task description.
        """
        findings: tuple[str, ...] = ()
        if task.description:
            findings = (f"Task requires: {task.description}",)

        return Research(
            id=ResearchId(f"res-{task.id}"),
            task_id=task.id,
            findings=findings,
            summary=f"Research for: {task.title}",
        )

    def get_research(self, research_id: str) -> Research | None:
        """Retrieve research by its identifier.

        Args:
            research_id: The unique identifier of the research.

        Returns:
            None — research is not persisted in this implementation.
        """
        return None
