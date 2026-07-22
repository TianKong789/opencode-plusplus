from __future__ import annotations

import pytest

from core.ids import ModelId
from src.opencode.evaluation.capability.registry import ModelRegistry


class TestModelRegistryRegistration:
    def test_stores_model_metadata(self) -> None:
        registry = ModelRegistry()
        model_id = ModelId("model-1")

        registry.register(model_id, "Model One", "acme")

        assert registry.get(model_id) == {
            "name": "Model One",
            "provider": "acme",
            "capabilities": (),
        }

    def test_stores_capabilities_tuple(self) -> None:
        registry = ModelRegistry()
        model_id = ModelId("model-1")
        capabilities = ("tools", "reasoning")

        registry.register(model_id, "Model One", "acme", capabilities)

        assert registry.get(model_id) == {
            "name": "Model One",
            "provider": "acme",
            "capabilities": capabilities,
        }

    def test_overwrites_existing_model_with_same_id(self) -> None:
        registry = ModelRegistry()
        model_id = ModelId("model-1")
        registry.register(model_id, "Original", "acme", ("tools",))

        registry.register(model_id, "Replacement", "other", ("images",))

        assert registry.get(model_id) == {
            "name": "Replacement",
            "provider": "other",
            "capabilities": ("images",),
        }


class TestModelRegistryLookup:
    def test_returns_metadata_for_registered_model(self) -> None:
        registry = ModelRegistry()
        model_id = ModelId("model-1")
        registry.register(model_id, "Model One", "acme", ("tools",))

        metadata = registry.get(model_id)

        assert metadata == {
            "name": "Model One",
            "provider": "acme",
            "capabilities": ("tools",),
        }

    def test_returns_none_for_unknown_model_id(self) -> None:
        registry = ModelRegistry()

        assert registry.get(ModelId("unknown-model")) is None


class TestModelRegistryListing:
    def test_returns_empty_tuple_when_registry_is_empty(self) -> None:
        registry = ModelRegistry()

        assert registry.list_models() == ()

    def test_returns_all_registered_model_ids(self) -> None:
        registry = ModelRegistry()
        first_model = ModelId("model-1")
        second_model = ModelId("model-2")
        registry.register(first_model, "Model One", "acme")
        registry.register(second_model, "Model Two", "other")

        assert registry.list_models() == (first_model, second_model)

    def test_returns_models_as_a_tuple(self) -> None:
        registry = ModelRegistry()
        registry.register(ModelId("model-1"), "Model One", "acme")

        assert isinstance(registry.list_models(), tuple)

    def test_returns_models_with_matching_capability(self) -> None:
        registry = ModelRegistry()
        matching_model = ModelId("model-1")
        registry.register(matching_model, "Model One", "acme", ("tools", "reasoning"))

        assert registry.list_by_capability("tools") == (matching_model,)

    def test_returns_empty_tuple_when_no_models_match_capability(self) -> None:
        registry = ModelRegistry()
        registry.register(ModelId("model-1"), "Model One", "acme", ("tools",))

        assert registry.list_by_capability("images") == ()

    def test_filters_matching_capability_among_multiple_models(self) -> None:
        registry = ModelRegistry()
        tool_model = ModelId("tool-model")
        image_model = ModelId("image-model")
        hybrid_model = ModelId("hybrid-model")
        registry.register(tool_model, "Tool Model", "acme", ("tools",))
        registry.register(image_model, "Image Model", "other", ("images",))
        registry.register(hybrid_model, "Hybrid Model", "acme", ("tools", "images"))

        assert registry.list_by_capability("tools") == (tool_model, hybrid_model)


class TestModelRegistryRemoval:
    def test_deletes_registered_model(self) -> None:
        registry = ModelRegistry()
        model_id = ModelId("model-1")
        registry.register(model_id, "Model One", "acme")

        registry.remove(model_id)

        assert registry.get(model_id) is None

    def test_raises_key_error_for_unknown_model_id(self) -> None:
        registry = ModelRegistry()

        with pytest.raises(KeyError, match="unknown-model"):
            registry.remove(ModelId("unknown-model"))


class TestModelRegistryCount:
    def test_returns_zero_when_empty(self) -> None:
        registry = ModelRegistry()

        assert registry.count() == 0

    def test_returns_count_after_registrations(self) -> None:
        registry = ModelRegistry()
        registry.register(ModelId("model-1"), "Model One", "acme")
        registry.register(ModelId("model-2"), "Model Two", "other")

        assert registry.count() == 2

    def test_decrements_after_removal(self) -> None:
        registry = ModelRegistry()
        first_model = ModelId("model-1")
        registry.register(first_model, "Model One", "acme")
        registry.register(ModelId("model-2"), "Model Two", "other")

        registry.remove(first_model)

        assert registry.count() == 1


class TestModelRegistryLifecycle:
    def test_register_list_remove_and_count_models(self) -> None:
        registry = ModelRegistry()
        first_model = ModelId("model-1")
        second_model = ModelId("model-2")
        third_model = ModelId("model-3")
        registry.register(first_model, "Model One", "acme", ("tools",))
        registry.register(second_model, "Model Two", "other", ("images",))
        registry.register(third_model, "Model Three", "acme", ("tools", "images"))

        assert registry.list_models() == (first_model, second_model, third_model)

        registry.remove(second_model)

        assert registry.count() == 2
