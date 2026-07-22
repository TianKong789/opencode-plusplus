from __future__ import annotations

from datetime import datetime, timezone

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus


def test_asset_id_is_string_subclass() -> None:
    aid = AssetId("asset-1")
    assert isinstance(aid, str)
    assert aid == "asset-1"


def test_promotion_status_values() -> None:
    assert PromotionStatus.DRAFT.value == "draft"
    assert PromotionStatus.APPROVED.value == "approved"
    assert PromotionStatus.PROMOTED.value == "promoted"
    assert PromotionStatus.ARCHIVED.value == "archived"


def test_asset_metadata_creation() -> None:
    meta = AssetMetadata(asset_id=AssetId("a-1"))
    assert meta.asset_id == "a-1"
    assert meta.version == "0.1.0"
    assert meta.lifecycle == PromotionStatus.DRAFT
    assert meta.parent is None
    assert meta.tags == ()
    assert meta.provenance == ""


def test_asset_metadata_with_custom_fields() -> None:
    now = datetime.now(timezone.utc)
    meta = AssetMetadata(
        asset_id=AssetId("a-2"),
        version="1.0.0",
        created_at=now,
        created_by="planner",
        parent=AssetId("a-1"),
        tags=("ui", "critical"),
        provenance="planner",
        lifecycle=PromotionStatus.APPROVED,
    )
    assert meta.version == "1.0.0"
    assert meta.created_by == "planner"
    assert meta.parent == "a-1"
    assert meta.has_tag("ui")
    assert not meta.has_tag("missing")


def test_asset_metadata_validation_empty_id() -> None:
    with pytest.raises(ValueError, match="asset_id"):
        AssetMetadata(asset_id=AssetId(""))


def test_asset_metadata_validation_empty_version() -> None:
    with pytest.raises(ValueError, match="version"):
        AssetMetadata(asset_id=AssetId("a-1"), version="")


def test_asset_metadata_query_helpers() -> None:
    draft = AssetMetadata(asset_id=AssetId("d"), lifecycle=PromotionStatus.DRAFT)
    approved = AssetMetadata(asset_id=AssetId("a"), lifecycle=PromotionStatus.APPROVED)
    promoted = AssetMetadata(asset_id=AssetId("p"), lifecycle=PromotionStatus.PROMOTED)
    archived = AssetMetadata(asset_id=AssetId("x"), lifecycle=PromotionStatus.ARCHIVED)

    assert not draft.is_approved()
    assert approved.is_approved()
    assert promoted.is_promoted()
    assert archived.is_archived()
