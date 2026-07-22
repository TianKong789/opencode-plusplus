from __future__ import annotations

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.skill import SkillAsset
from core.ids import ExperienceId, SkillId
from core.models.skill import Skill


def _make_skill(**overrides) -> Skill:
    defaults = {
        "id": SkillId("skill-1"),
        "name": "Test Skill",
        "description": "A test skill",
    }
    defaults.update(overrides)
    return Skill(**defaults)


def _make_skill_asset(**overrides) -> SkillAsset:
    metadata = overrides.pop("metadata", AssetMetadata(asset_id=AssetId("sa-1")))
    content = overrides.pop("content", _make_skill())
    return SkillAsset(metadata=metadata, content=content, **overrides)


def test_skill_asset_creation() -> None:
    sa = _make_skill_asset()
    assert sa.id == "sa-1"
    assert sa.version == "0.1.0"
    assert sa.name == "Test Skill"


def test_skill_asset_exposes_content_fields() -> None:
    skill = _make_skill(name="Python", proficiency=0.8)
    sa = _make_skill_asset(content=skill)
    assert sa.content.proficiency == 0.8
    assert sa.name == "Python"


def test_skill_asset_promote() -> None:
    sa = _make_skill_asset()
    promoted = sa.promote()
    assert promoted.metadata.lifecycle == PromotionStatus.PROMOTED
    assert sa.metadata.lifecycle == PromotionStatus.DRAFT


def test_skill_asset_archive() -> None:
    sa = _make_skill_asset()
    archived = sa.archive()
    assert archived.metadata.lifecycle == PromotionStatus.ARCHIVED
    assert sa.metadata.lifecycle == PromotionStatus.DRAFT


def test_skill_asset_immutable() -> None:
    sa = _make_skill_asset()
    with pytest.raises(AttributeError):
        sa.metadata = AssetMetadata(asset_id=AssetId("new"))  # type: ignore[misc]
