from __future__ import annotations

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.workflow import WorkflowAsset
from core.ids import WorkflowId
from core.models.workflow import Workflow


def _make_workflow(**overrides) -> Workflow:
    defaults = {
        "id": WorkflowId("wf-1"),
        "name": "Test Workflow",
        "description": "A test workflow",
    }
    defaults.update(overrides)
    return Workflow(**defaults)


def _make_workflow_asset(**overrides) -> WorkflowAsset:
    metadata = overrides.pop("metadata", AssetMetadata(asset_id=AssetId("wa-1")))
    content = overrides.pop("content", _make_workflow())
    return WorkflowAsset(metadata=metadata, content=content, **overrides)


def test_workflow_asset_creation() -> None:
    wa = _make_workflow_asset()
    assert wa.id == "wa-1"
    assert wa.version == "0.1.0"
    assert wa.name == "Test Workflow"


def test_workflow_asset_exposes_content_fields() -> None:
    workflow = _make_workflow(name="Deploy Pipeline", description="Deploys to prod")
    wa = _make_workflow_asset(content=workflow)
    assert wa.content.description == "Deploys to prod"
    assert wa.name == "Deploy Pipeline"


def test_workflow_asset_promote() -> None:
    wa = _make_workflow_asset()
    promoted = wa.promote()
    assert promoted.metadata.lifecycle == PromotionStatus.PROMOTED
    assert wa.metadata.lifecycle == PromotionStatus.DRAFT


def test_workflow_asset_archive() -> None:
    wa = _make_workflow_asset()
    archived = wa.archive()
    assert archived.metadata.lifecycle == PromotionStatus.ARCHIVED
    assert wa.metadata.lifecycle == PromotionStatus.DRAFT


def test_workflow_asset_immutable() -> None:
    wa = _make_workflow_asset()
    with pytest.raises(AttributeError):
        wa.metadata = AssetMetadata(asset_id=AssetId("new"))  # type: ignore[misc]


def test_workflow_asset_protocol_conformance() -> None:
    from core.interfaces.asset_repository import AssetProtocol

    wa = _make_workflow_asset()
    assert isinstance(wa, AssetProtocol)


def test_workflow_asset_equality() -> None:
    wa1 = _make_workflow_asset()
    wa2 = _make_workflow_asset()
    assert wa1 == wa2


def test_workflow_asset_inequality() -> None:
    wa1 = _make_workflow_asset()
    metadata2 = AssetMetadata(asset_id=AssetId("wa-2"))
    wa2 = _make_workflow_asset(metadata=metadata2)
    assert wa1 != wa2


def test_workflow_asset_hash() -> None:
    wa1 = _make_workflow_asset()
    wa2 = _make_workflow_asset()
    assert hash(wa1) == hash(wa2)


def test_workflow_asset_in_set() -> None:
    wa1 = _make_workflow_asset()
    wa2 = _make_workflow_asset()
    asset_set = {wa1, wa2}
    assert len(asset_set) == 1
