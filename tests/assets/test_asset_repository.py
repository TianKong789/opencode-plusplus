from __future__ import annotations

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.skill import SkillAsset
from core.assets.prompt import PromptAsset
from core.ids import SkillId
from core.models.skill import Skill
from memory.asset_repository import InMemoryAssetRepository


def _make_skill_asset(id_str: str = "sa-1", **overrides) -> SkillAsset:
    defaults = {
        "metadata": AssetMetadata(asset_id=AssetId(id_str)),
        "content": Skill(id=SkillId("skill-1"), name="Test", description="desc"),
    }
    defaults.update(overrides)
    return SkillAsset(**defaults)


def _make_prompt_asset(id_str: str = "pa-1") -> PromptAsset:
    return PromptAsset(
        metadata=AssetMetadata(asset_id=AssetId(id_str)),
        prompt="test prompt",
    )


def test_store_and_get() -> None:
    repo = InMemoryAssetRepository()
    sa = _make_skill_asset()
    repo.store(sa)
    retrieved = repo.get(AssetId("sa-1"))
    assert retrieved is sa


def test_get_returns_none_for_missing() -> None:
    repo = InMemoryAssetRepository()
    assert repo.get(AssetId("missing")) is None


def test_store_duplicate_raises() -> None:
    repo = InMemoryAssetRepository()
    repo.store(_make_skill_asset())
    with pytest.raises(ValueError, match="already exists"):
        repo.store(_make_skill_asset())


def test_list_by_type() -> None:
    repo = InMemoryAssetRepository()
    repo.store(_make_skill_asset("sa-1"))
    repo.store(_make_skill_asset("sa-2"))
    repo.store(_make_prompt_asset("pa-1"))

    skills = repo.list_by_type(SkillAsset)
    assert len(skills) == 2

    prompts = repo.list_by_type(PromptAsset)
    assert len(prompts) == 1


def test_list_by_status() -> None:
    repo = InMemoryAssetRepository()
    repo.store(_make_skill_asset("sa-1"))
    promoted = _make_skill_asset("sa-2").promote()
    repo.store(promoted)

    drafts = repo.list_by_status(PromotionStatus.DRAFT)
    assert len(drafts) == 1

    promoted_assets = repo.list_by_status(PromotionStatus.PROMOTED)
    assert len(promoted_assets) == 1


def test_update() -> None:
    repo = InMemoryAssetRepository()
    sa = _make_skill_asset()
    repo.store(sa)
    updated = sa.promote()
    repo.update(updated)
    retrieved = repo.get(AssetId("sa-1"))
    assert retrieved.metadata.lifecycle == PromotionStatus.PROMOTED


def test_update_missing_raises() -> None:
    repo = InMemoryAssetRepository()
    with pytest.raises(KeyError, match="not found"):
        repo.update(_make_skill_asset())


def test_delete() -> None:
    repo = InMemoryAssetRepository()
    sa = _make_skill_asset()
    repo.store(sa)
    repo.delete(AssetId("sa-1"))
    assert repo.get(AssetId("sa-1")) is None


def test_delete_missing_raises() -> None:
    repo = InMemoryAssetRepository()
    with pytest.raises(KeyError, match="not found"):
        repo.delete(AssetId("missing"))


def test_count() -> None:
    repo = InMemoryAssetRepository()
    assert repo.count() == 0
    repo.store(_make_skill_asset("sa-1"))
    repo.store(_make_prompt_asset("pa-1"))
    assert repo.count() == 2
