from __future__ import annotations

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.prompt import PromptAsset


def _make_prompt_asset(**overrides) -> PromptAsset:
    metadata = overrides.pop("metadata", AssetMetadata(asset_id=AssetId("pa-1")))
    return PromptAsset(metadata=metadata, prompt="You are a helpful assistant.", **overrides)


def test_prompt_asset_creation() -> None:
    pa = _make_prompt_asset()
    assert pa.id == "pa-1"
    assert pa.version == "0.1.0"
    assert pa.prompt == "You are a helpful assistant."


def test_prompt_asset_with_description() -> None:
    pa = _make_prompt_asset(description="System prompt for planner")
    assert pa.description == "System prompt for planner"


def test_prompt_asset_promote() -> None:
    pa = _make_prompt_asset()
    promoted = pa.promote()
    assert promoted.metadata.lifecycle == PromotionStatus.PROMOTED
    assert pa.metadata.lifecycle == PromotionStatus.DRAFT


def test_prompt_asset_archive() -> None:
    pa = _make_prompt_asset()
    archived = pa.archive()
    assert archived.metadata.lifecycle == PromotionStatus.ARCHIVED


def test_prompt_asset_validation_empty_prompt() -> None:
    with pytest.raises(ValueError, match="prompt"):
        PromptAsset(
            metadata=AssetMetadata(asset_id=AssetId("pa-2")),
            prompt="",
        )
