from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.research import Research
from core.models.task import Task


class Researcher(ABC):
    """Gathers context and findings for tasks."""

    @abstractmethod
    def research(self, task: Task) -> Research:
        """Research a task to gather relevant context.

        Args:
            task: The task to research.

        Returns:
            Research findings and sources.
        """

    @abstractmethod
    def get_research(self, research_id: str) -> Research | None:
        """Retrieve research by its identifier.

        Args:
            research_id: The unique identifier of the research.

        Returns:
            The research if found, None otherwise.
        """
