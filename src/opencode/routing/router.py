"""Model router implementation.

Routes tasks to the optimal model based on classification and
capability assessment.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.ids import ModelId, TaskCategoryId
from core.models.task import Task

from src.opencode.evaluation.capability.assessor import CapabilityAssessor
from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.capability_test import Model
from src.opencode.evaluation.capability.registry import ModelRegistry


@dataclass
class ModelRouter:
    """Routes tasks to optimal models.

    Coordinates between model registry and capability assessor
    to select the best model for each task.
    """

    registry: ModelRegistry
    assessor: CapabilityAssessor
    _routing_history: dict[str, list[ModelId]] = field(default_factory=dict)
    _category_preferred: dict[TaskCategoryId, ModelId] = field(default_factory=dict)

    def route(self, task: Task, capability: Capability = Capability.REASONING) -> ModelId:
        """Select the optimal model for a task.

        Args:
            task: The task to route.
            capability: The capability to assess (default: REASONING).

        Returns:
            The model ID best suited for the task.
        """
        best_model: ModelId | None = None
        best_score = -1.0

        for model_id in self.registry.list_models():
            metadata = self.registry.get(model_id)
            if metadata is None:
                continue

            model = Model(
                model_id=str(model_id),
                provider=str(metadata.get("provider", "unknown")),
            )

            result = self.assessor.assess(model, capability)
            if result is not None and result.score > best_score:
                best_score = result.score
                best_model = model_id

        if best_model is None:
            raise ValueError("No models available in registry")

        if task.id not in self._routing_history:
            self._routing_history[task.id] = []
        self._routing_history[task.id].append(best_model)

        return best_model

    def route_by_category(self, category_id: TaskCategoryId) -> ModelId:
        """Select the optimal model for a task category.

        Args:
            category_id: The task category to route.

        Returns:
            The model ID best suited for the category.
        """
        # Check for preferred model first
        if category_id in self._category_preferred:
            return self._category_preferred[category_id]

        # Default to first available model
        models = self.registry.list_models()
        if not models:
            raise ValueError("No models available in registry")

        return models[0]

    def get_routing_history(self, task_id: str) -> tuple[ModelId, ...]:
        """Get the history of models routed for a task.

        Args:
            task_id: The task identifier to look up.

        Returns:
            A tuple of model IDs that were routed for this task.
        """
        return tuple(self._routing_history.get(task_id, []))

    def get_preferred_model(self, category_id: TaskCategoryId) -> ModelId | None:
        """Get the preferred model for a category based on past performance.

        Args:
            category_id: The task category to inspect.

        Returns:
            The preferred model ID, or None if no history exists.
        """
        return self._category_preferred.get(category_id)

    def set_preferred_model(
        self,
        category_id: TaskCategoryId,
        model_id: ModelId,
    ) -> None:
        """Set the preferred model for a category.

        Args:
            category_id: The task category.
            model_id: The model to prefer.
        """
        self._category_preferred[category_id] = model_id
