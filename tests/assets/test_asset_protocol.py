from __future__ import annotations

import pytest

from core.assets.benchmark import BenchmarkAsset
from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.prompt import PromptAsset
from core.assets.skill import SkillAsset
from core.assets.template import TemplateAsset
from core.assets.workflow import WorkflowAsset
from core.ids import BenchmarkId, SkillId, WorkflowId
from core.interfaces.asset_repository import AssetProtocol
from core.models.benchmark import Benchmark
from core.models.skill import Skill
from core.models.workflow import Workflow


def _make_skill_asset(asset_id: str = "sa-1") -> SkillAsset:
    metadata = AssetMetadata(asset_id=AssetId(asset_id))
    content = Skill(id=SkillId("skill-1"), name="Test Skill", description="A test skill")
    return SkillAsset(metadata=metadata, content=content)


def _make_prompt_asset(asset_id: str = "pa-1") -> PromptAsset:
    metadata = AssetMetadata(asset_id=AssetId(asset_id))
    return PromptAsset(metadata=metadata, prompt="Test prompt")


def _make_benchmark_asset(asset_id: str = "ba-1") -> BenchmarkAsset:
    metadata = AssetMetadata(asset_id=AssetId(asset_id))
    content = Benchmark(
        id=BenchmarkId("bench-1"),
        skill_id=SkillId("skill-1"),
        name="Test Benchmark",
        input_data="test input",
        expected_output="test output",
    )
    return BenchmarkAsset(metadata=metadata, content=content)


def _make_template_asset(asset_id: str = "ta-1") -> TemplateAsset:
    metadata = AssetMetadata(asset_id=AssetId(asset_id))
    return TemplateAsset(metadata=metadata, name="Test Template", content="Template content")


def _make_workflow_asset(asset_id: str = "wa-1") -> WorkflowAsset:
    metadata = AssetMetadata(asset_id=AssetId(asset_id))
    content = Workflow(
        id=WorkflowId("wf-1"),
        name="Test Workflow",
        description="A test workflow",
    )
    return WorkflowAsset(metadata=metadata, content=content)


class TestAssetProtocolConformance:
    """Test that all asset types implement AssetProtocol."""

    def test_skill_asset_is_protocol(self) -> None:
        sa = _make_skill_asset()
        assert isinstance(sa, AssetProtocol)

    def test_prompt_asset_is_protocol(self) -> None:
        pa = _make_prompt_asset()
        assert isinstance(pa, AssetProtocol)

    def test_benchmark_asset_is_protocol(self) -> None:
        ba = _make_benchmark_asset()
        assert isinstance(ba, AssetProtocol)

    def test_template_asset_is_protocol(self) -> None:
        ta = _make_template_asset()
        assert isinstance(ta, AssetProtocol)

    def test_workflow_asset_is_protocol(self) -> None:
        wa = _make_workflow_asset()
        assert isinstance(wa, AssetProtocol)

    def test_protocol_has_id(self) -> None:
        sa = _make_skill_asset()
        assert hasattr(sa, "id")
        assert isinstance(sa.id, AssetId)

    def test_protocol_has_metadata(self) -> None:
        sa = _make_skill_asset()
        assert hasattr(sa, "metadata")
        assert isinstance(sa.metadata, AssetMetadata)


class TestSkillAssetEquality:
    """Test SkillAsset equality and hashing."""

    def test_equal_same_id(self) -> None:
        sa1 = _make_skill_asset("sa-1")
        sa2 = _make_skill_asset("sa-1")
        assert sa1 == sa2

    def test_not_equal_different_id(self) -> None:
        sa1 = _make_skill_asset("sa-1")
        sa2 = _make_skill_asset("sa-2")
        assert sa1 != sa2

    def test_not_equal_different_type(self) -> None:
        sa = _make_skill_asset("sa-1")
        pa = _make_prompt_asset("sa-1")
        assert sa != pa

    def test_hash_same_id(self) -> None:
        sa1 = _make_skill_asset("sa-1")
        sa2 = _make_skill_asset("sa-1")
        assert hash(sa1) == hash(sa2)

    def test_hash_different_id(self) -> None:
        sa1 = _make_skill_asset("sa-1")
        sa2 = _make_skill_asset("sa-2")
        assert hash(sa1) != hash(sa2)

    def test_usable_in_set(self) -> None:
        sa1 = _make_skill_asset("sa-1")
        sa2 = _make_skill_asset("sa-1")  # Same ID
        asset_set = {sa1, sa2}
        assert len(asset_set) == 1

    def test_usable_as_dict_key(self) -> None:
        sa = _make_skill_asset("sa-1")
        d = {sa: "value"}
        assert d[sa] == "value"


class TestPromptAssetEquality:
    """Test PromptAsset equality and hashing."""

    def test_equal_same_id(self) -> None:
        pa1 = _make_prompt_asset("pa-1")
        pa2 = _make_prompt_asset("pa-1")
        assert pa1 == pa2

    def test_not_equal_different_id(self) -> None:
        pa1 = _make_prompt_asset("pa-1")
        pa2 = _make_prompt_asset("pa-2")
        assert pa1 != pa2

    def test_hash_same_id(self) -> None:
        pa1 = _make_prompt_asset("pa-1")
        pa2 = _make_prompt_asset("pa-1")
        assert hash(pa1) == hash(pa2)

    def test_usable_in_set(self) -> None:
        pa1 = _make_prompt_asset("pa-1")
        pa2 = _make_prompt_asset("pa-1")
        asset_set = {pa1, pa2}
        assert len(asset_set) == 1


class TestBenchmarkAssetEquality:
    """Test BenchmarkAsset equality and hashing."""

    def test_equal_same_id(self) -> None:
        ba1 = _make_benchmark_asset("ba-1")
        ba2 = _make_benchmark_asset("ba-1")
        assert ba1 == ba2

    def test_not_equal_different_id(self) -> None:
        ba1 = _make_benchmark_asset("ba-1")
        ba2 = _make_benchmark_asset("ba-2")
        assert ba1 != ba2

    def test_hash_same_id(self) -> None:
        ba1 = _make_benchmark_asset("ba-1")
        ba2 = _make_benchmark_asset("ba-1")
        assert hash(ba1) == hash(ba2)

    def test_usable_in_set(self) -> None:
        ba1 = _make_benchmark_asset("ba-1")
        ba2 = _make_benchmark_asset("ba-1")
        asset_set = {ba1, ba2}
        assert len(asset_set) == 1


class TestTemplateAssetEquality:
    """Test TemplateAsset equality and hashing."""

    def test_equal_same_id(self) -> None:
        ta1 = _make_template_asset("ta-1")
        ta2 = _make_template_asset("ta-1")
        assert ta1 == ta2

    def test_not_equal_different_id(self) -> None:
        ta1 = _make_template_asset("ta-1")
        ta2 = _make_template_asset("ta-2")
        assert ta1 != ta2

    def test_hash_same_id(self) -> None:
        ta1 = _make_template_asset("ta-1")
        ta2 = _make_template_asset("ta-1")
        assert hash(ta1) == hash(ta2)

    def test_usable_in_set(self) -> None:
        ta1 = _make_template_asset("ta-1")
        ta2 = _make_template_asset("ta-1")
        asset_set = {ta1, ta2}
        assert len(asset_set) == 1


class TestWorkflowAssetEquality:
    """Test WorkflowAsset equality and hashing."""

    def test_equal_same_id(self) -> None:
        wa1 = _make_workflow_asset("wa-1")
        wa2 = _make_workflow_asset("wa-1")
        assert wa1 == wa2

    def test_not_equal_different_id(self) -> None:
        wa1 = _make_workflow_asset("wa-1")
        wa2 = _make_workflow_asset("wa-2")
        assert wa1 != wa2

    def test_hash_same_id(self) -> None:
        wa1 = _make_workflow_asset("wa-1")
        wa2 = _make_workflow_asset("wa-1")
        assert hash(wa1) == hash(wa2)

    def test_usable_in_set(self) -> None:
        wa1 = _make_workflow_asset("wa-1")
        wa2 = _make_workflow_asset("wa-1")
        asset_set = {wa1, wa2}
        assert len(asset_set) == 1
