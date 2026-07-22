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
from src.opencode.evaluation.capability.models import ModelCapabilityProfile
from src.opencode.evaluation.capability.registry import ModelRegistry
from src.opencode.routing.policies import BalancedPolicy, RoutingContext, RoutingPolicy


@dataclass
class ModelRouter:
    """Routes tasks to optimal models.

    Coordinates between model registry, capability assessor, and
    routing policies to select the best model for each task.
    """

    registry: ModelRegistry
    assessor: CapabilityAssessor
    policy: RoutingPolicy = field(default_factory=BalancedPolicy)
    _routing_history: dict[str, list[ModelId]] = field(default_factory=dict)
    _category_preferred: dict[TaskCategoryId, ModelId] = field(default_factory=dict)

    def route(self, task: Task, capability: Capability = Capability.REASONING) -> ModelId:
        """Select the optimal model for a task.

        Uses the configured routing policy to score candidates
        from the registry.

        Args:
            task: The task to route.
            capability: The capability to assess (default: REASONING).

        Returns:
            The model ID best suited for the task.
        """
        profiles = self._build_profiles(capability)

        if not profiles:
            raise ValueError("No models available in registry")

        context = RoutingContext(
            profiles=profiles,
            task_description=task.description,
        )

        result = self.policy.select(context)
        if result is None:
            raise ValueError("No model meets policy criteria")

        if task.id not in self._routing_history:
            self._routing_history[task.id] = []
        self._routing_history[task.id].append(result)

        return result

    def route_by_category(self, category_id: TaskCategoryId) -> ModelId:
        """Select the optimal model for a task category.

        Args:
            category_id: The task category to route.

        Returns:
            The model ID best suited for the category.
        """
        if category_id in self._category_preferred:
            return self._category_preferred[category_id]

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

    def _build_profiles(self, capability: Capability) -> tuple[ModelCapabilityProfile, ...]:
        """Build capability profiles for all registered models.

        Args:
            capability: The capability to assess.

        Returns:
            Tuple of profiles for routing decisions.
        """
        profiles: list[ModelCapabilityProfile] = []
        for model_id in self.registry.list_models():
            metadata = self.registry.get(model_id)
            if metadata is None:
                continue

            model = Model(
                model_id=str(model_id),
                provider=str(metadata.get("provider", "unknown")),
            )

            result = self.assessor.assess(model, capability)
            score = result.score if result is not None else 0.0

            profile = ModelCapabilityProfile(
                model_id=str(model_id),
                model_name=str(metadata.get("name", "")),
                provider=str(metadata.get("provider", "unknown")),
                version="1.0",
                context_window=128000,
                max_output_tokens=8192,
                average_latency_ms=100.0,
                estimated_cost=0.001,
                capability_scores=(),
                overall_score=min(score, 10.0),
            )
            profiles.append(profile)

        return tuple(profiles)
