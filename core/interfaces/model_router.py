from __future__ import annotations

from abc import ABC, abstractmethod

from core.ids import ModelId, TaskCategoryId
from core.models.task import Task


class ModelRouter(ABC):
    """Routes tasks to the optimal model based on classification and capabilities.

    Coordinates between TaskClassifier and CapabilityAssessor to
    select the best model for a given task.
    """

    @abstractmethod
    def route(self, task: Task) -> ModelId:
        """Select the optimal model for a task.

        Args:
            task: The task to route.

        Returns:
            The model ID best suited for the task.
        """

    @abstractmethod
    def route_by_category(self, category_id: TaskCategoryId) -> ModelId:
        """Select the optimal model for a task category.

        Args:
            category_id: The task category to route.

        Returns:
            The model ID best suited for the category.
        """

    @abstractmethod
    def get_routing_history(self, task_id: str) -> tuple[ModelId, ...]:
        """Get the history of models routed for a task.

        Args:
            task_id: The task identifier to look up.

        Returns:
            A tuple of model IDs that were routed for this task.
        """

    @abstractmethod
    def get_preferred_model(self, category_id: TaskCategoryId) -> ModelId | None:
        """Get the preferred model for a category based on past performance.

        Args:
            category_id: The task category to inspect.

        Returns:
            The preferred model ID, or None if no history exists.
        """
