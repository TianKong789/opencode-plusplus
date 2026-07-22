from __future__ import annotations

import pytest

from core.ids import ModelId, TaskCategoryId, TaskId
from core.models.task import Task
from src.opencode.evaluation.capability.assessor import CapabilityAssessor
from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.capability_test import CapabilityTest, Model
from src.opencode.evaluation.capability.models import CapabilityScore
from src.opencode.evaluation.capability.registry import ModelRegistry
from src.opencode.routing.router import ModelRouter


class _ModelScoreTest(CapabilityTest):
    def __init__(self, capability_value: Capability, scores: tuple[tuple[str, float], ...]) -> None:
        self._capability_value = capability_value
        self._scores = scores

    def capability(self) -> Capability:
        return self._capability_value

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        return ()

    def run(self, model: Model) -> CapabilityScore:
        scores = dict(self._scores)
        return CapabilityScore(capability=self._capability_value, score=scores[model.model_id])


def _make_router(
    scores: tuple[tuple[str, float], ...], models: tuple[tuple[str, str], ...]
) -> ModelRouter:
    registry = ModelRegistry()
    for model_id, provider in models:
        registry.register(ModelId(model_id), model_id, provider)
    assessor = CapabilityAssessor(
        _tests={Capability.REASONING: _ModelScoreTest(Capability.REASONING, scores)}
    )
    return ModelRouter(registry=registry, assessor=assessor)


def _make_task(task_id: str = "task-1") -> Task:
    return Task(id=TaskId(task_id), title="Route task", description="Select a model")


def test_route_selects_highest_scoring_model_when_capability_is_requested() -> None:
    router = _make_router(
        (("low", 3.0), ("high", 9.0)), (("low", "provider-a"), ("high", "provider-b"))
    )

    selected = router.route(_make_task(), Capability.REASONING)

    assert selected == ModelId("high")


def test_route_records_selected_model_when_routing_task() -> None:
    router = _make_router((("best", 9.0),), (("best", "provider"),))
    task = _make_task()

    router.route(task)

    assert router.get_routing_history(task.id) == (ModelId("best"),)


def test_route_accumulates_history_when_task_is_routed_multiple_times() -> None:
    router = _make_router((("best", 9.0),), (("best", "provider"),))
    task = _make_task()

    router.route(task)
    router.route(task)

    assert router.get_routing_history(task.id) == (ModelId("best"), ModelId("best"))


def test_route_raises_value_error_when_registry_is_empty() -> None:
    router = ModelRouter(registry=ModelRegistry(), assessor=CapabilityAssessor(_tests={}))

    with pytest.raises(ValueError, match="No models available in registry"):
        router.route(_make_task())


def test_route_uses_requested_capability_when_custom_capability_is_provided() -> None:
    registry = ModelRegistry()
    registry.register(ModelId("reasoner"), "Reasoner", "provider-a")
    registry.register(ModelId("pythonista"), "Pythonista", "provider-b")
    assessor = CapabilityAssessor(
        _tests={
            Capability.REASONING: _ModelScoreTest(
                Capability.REASONING, (("reasoner", 9.0), ("pythonista", 1.0))
            ),
            Capability.PYTHON: _ModelScoreTest(
                Capability.PYTHON, (("reasoner", 1.0), ("pythonista", 9.0))
            ),
        }
    )
    router = ModelRouter(registry=registry, assessor=assessor)

    selected = router.route(_make_task(), Capability.PYTHON)

    assert selected == ModelId("pythonista")


def test_route_uses_reasoning_when_capability_is_omitted() -> None:
    router = _make_router(
        (("reasoner", 9.0), ("other", 1.0)),
        (("reasoner", "provider-a"), ("other", "provider-b")),
    )

    selected = router.route(_make_task())

    assert selected == ModelId("reasoner")


def test_get_routing_history_returns_empty_tuple_when_task_is_unknown() -> None:
    router = _make_router((("best", 9.0),), (("best", "provider"),))

    assert router.get_routing_history(TaskId("unknown")) == ()


def test_get_routing_history_returns_model_ids_when_task_has_been_routed() -> None:
    router = _make_router((("best", 9.0),), (("best", "provider"),))
    task = _make_task()
    router.route(task)

    history = router.get_routing_history(task.id)

    assert history == (ModelId("best"),)
    assert all(isinstance(model_id, ModelId) for model_id in history)


def test_route_by_category_uses_preferred_model_when_preference_is_set() -> None:
    router = _make_router((("default", 9.0),), (("default", "provider"),))
    category = TaskCategoryId("coding")
    preferred = ModelId("preferred")
    router.set_preferred_model(category, preferred)

    assert router.route_by_category(category) == preferred


def test_route_by_category_uses_first_registered_model_when_preference_is_missing() -> None:
    router = _make_router(
        (("first", 9.0), ("second", 8.0)),
        (("first", "provider-a"), ("second", "provider-b")),
    )

    assert router.route_by_category(TaskCategoryId("coding")) == ModelId("first")


def test_route_by_category_raises_value_error_when_registry_is_empty() -> None:
    router = ModelRouter(registry=ModelRegistry(), assessor=CapabilityAssessor(_tests={}))

    with pytest.raises(ValueError, match="No models available in registry"):
        router.route_by_category(TaskCategoryId("coding"))


def test_get_preferred_model_returns_none_when_category_has_no_preference() -> None:
    router = _make_router((("default", 9.0),), (("default", "provider"),))

    assert router.get_preferred_model(TaskCategoryId("coding")) is None


def test_get_preferred_model_returns_model_when_category_has_preference() -> None:
    router = _make_router((("default", 9.0),), (("default", "provider"),))
    category = TaskCategoryId("coding")
    router.set_preferred_model(category, ModelId("preferred"))

    assert router.get_preferred_model(category) == ModelId("preferred")


def test_set_preferred_model_stores_model_for_category() -> None:
    router = _make_router((("default", 9.0),), (("default", "provider"),))
    category = TaskCategoryId("coding")
    preferred = ModelId("preferred")

    router.set_preferred_model(category, preferred)

    assert router.get_preferred_model(category) == preferred
