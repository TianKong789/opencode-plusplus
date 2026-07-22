from __future__ import annotations

from abc import ABC, abstractmethod

from core.ids import TaskCategoryId
from core.models.task import Task


class TaskClassifier(ABC):
    """Classifies tasks into categories for model selection.

    Analyzes task characteristics to determine what capabilities
    are required (e.g., code generation, reasoning, creative writing).
    """

    @abstractmethod
    def classify(self, task: Task) -> TaskCategoryId:
        """Classify a task into a category.

        Args:
            task: The task to classify.

        Returns:
            The category ID that best describes the task.
        """

    @abstractmethod
    def get_requirements(self, category_id: TaskCategoryId) -> tuple[str, ...]:
        """Get the capability requirements for a task category.

        Args:
            category_id: The task category to inspect.

        Returns:
            A tuple of required capability tags (e.g. "code", "reasoning").
        """

    @abstractmethod
    def get_category(self, category_id: TaskCategoryId) -> dict[str, object] | None:
        """Retrieve category metadata by identifier.

        Args:
            category_id: The unique identifier of the category.

        Returns:
            The category metadata if found, None otherwise.
        """

    @abstractmethod
    def list_categories(self) -> tuple[TaskCategoryId, ...]:
        """List all known task categories.

        Returns:
            A tuple of all registered category IDs.
        """

    @abstractmethod
    def register_category(
        self,
        category_id: TaskCategoryId,
        name: str,
        required_capabilities: tuple[str, ...],
    ) -> None:
        """Register a new task category.

        Args:
            category_id: Unique identifier for the category.
            name: Human-readable category name.
            required_capabilities: Capability tags required for this category.
        """
