from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.ids import ModelId, TaskCategoryId
from core.models.task import Task


@runtime_checkable
class ModelRouter(Protocol):
    """Routes tasks to the optimal model based on classification and capabilities.

    Coordinates between TaskClassifier and CapabilityAssessor to
    select the best model for a given task.
    """

    def route(self, task: Task) -> ModelId:
        """Select the optimal model for a task.

        Args:
            task: The task to route.

        Returns:
            The model ID best suited for the task.
        """

    def route_by_category(self, category_id: TaskCategoryId) -> ModelId:
        """Select the optimal model for a task category.

        Args:
            category_id: The task category to route.

        Returns:
            The model ID best suited for the category.
        """

    def get_routing_history(self, task_id: str) -> tuple[ModelId, ...]:
        """Get the history of models routed for a task.

        Args:
            task_id: The task identifier to look up.

        Returns:
            A tuple of model IDs that were routed for this task.
        """

    def get_preferred_model(self, category_id: TaskCategoryId) -> ModelId | None:
        """Get the preferred model for a category based on past performance.

        Args:
            category_id: The task category to inspect.

        Returns:
            The preferred model ID, or None if no history exists.
        """
