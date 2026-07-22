from __future__ import annotations

from dataclasses import dataclass

from core.ids import ResearchId
from core.interfaces.llm_executor import LLMExecutor
from core.interfaces.researcher import Researcher
from core.models.research import Research
from core.models.task import Task


@dataclass(slots=True, frozen=True)
class LLMResearcherAgent(Researcher):
    """LLM-driven research agent.

    Uses an LLM to gather context and findings for tasks.
    """

    llm: LLMExecutor

    def research(self, task: Task) -> Research:
        prompt = (
            f"Research this task:\n"
            f"Title: {task.title}\n"
            f"Description: {task.description}\n"
            f"Provide findings, sources, and a summary."
        )
        response = self.llm.execute(prompt)
        findings: tuple[str, ...] = ()
        if response:
            findings = (response[:200],)
        elif task.description:
            findings = (f"Task requires: {task.description}",)

        return Research(
            id=ResearchId(f"res-{task.id}"),
            task_id=task.id,
            findings=findings,
            summary=f"Research for: {task.title}",
        )

    def get_research(self, research_id: str) -> Research | None:
        return None
