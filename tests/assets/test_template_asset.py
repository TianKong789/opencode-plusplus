from __future__ import annotations

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.template import TemplateAsset


def _make_template_asset(**overrides) -> TemplateAsset:
    metadata = overrides.pop("metadata", AssetMetadata(asset_id=AssetId("ta-1")))
    return TemplateAsset(
        metadata=metadata,
        name="Review Template",
        content="# Review\n\nEvaluate the code.",
        **overrides,
    )


def test_template_asset_creation() -> None:
    ta = _make_template_asset()
    assert ta.id == "ta-1"
    assert ta.version == "0.1.0"
    assert ta.name == "Review Template"
    assert ta.template_type == "generic"


def test_template_asset_with_type() -> None:
    ta = _make_template_asset(template_type="review")
    assert ta.template_type == "review"


def test_template_asset_promote() -> None:
    ta = _make_template_asset()
    promoted = ta.promote()
    assert promoted.metadata.lifecycle == PromotionStatus.PROMOTED


def test_template_asset_archive() -> None:
    ta = _make_template_asset()
    archived = ta.archive()
    assert archived.metadata.lifecycle == PromotionStatus.ARCHIVED


def test_template_asset_validation_empty_name() -> None:
    with pytest.raises(ValueError, match="name"):
        TemplateAsset(
            metadata=AssetMetadata(asset_id=AssetId("ta-2")),
            name="",
            content="content",
        )


def test_template_asset_validation_empty_content() -> None:
    with pytest.raises(ValueError, match="content"):
        TemplateAsset(
            metadata=AssetMetadata(asset_id=AssetId("ta-3")),
            name="Template",
            content="",
        )
