from __future__ import annotations

import pytest

from core.assets.metadata import AssetId, AssetMetadata, PromotionStatus
from core.assets.benchmark import BenchmarkAsset
from core.ids import BenchmarkId, SkillId
from core.models.benchmark import Benchmark


def _make_benchmark(**overrides) -> Benchmark:
    defaults = {
        "id": BenchmarkId("bench-1"),
        "skill_id": SkillId("skill-1"),
        "name": "Test Benchmark",
        "input_data": "input",
        "expected_output": "output",
    }
    defaults.update(overrides)
    return Benchmark(**defaults)


def _make_benchmark_asset(**overrides) -> BenchmarkAsset:
    metadata = overrides.pop("metadata", AssetMetadata(asset_id=AssetId("ba-1")))
    content = overrides.pop("content", _make_benchmark())
    return BenchmarkAsset(metadata=metadata, content=content, **overrides)


def test_benchmark_asset_creation() -> None:
    ba = _make_benchmark_asset()
    assert ba.id == "ba-1"
    assert ba.version == "0.1.0"
    assert ba.name == "Test Benchmark"


def test_benchmark_asset_exposes_content_fields() -> None:
    bench = _make_benchmark(timeout_ms=5000.0)
    ba = _make_benchmark_asset(content=bench)
    assert ba.content.timeout_ms == 5000.0


def test_benchmark_asset_promote() -> None:
    ba = _make_benchmark_asset()
    promoted = ba.promote()
    assert promoted.metadata.lifecycle == PromotionStatus.PROMOTED


def test_benchmark_asset_archive() -> None:
    ba = _make_benchmark_asset()
    archived = ba.archive()
    assert archived.metadata.lifecycle == PromotionStatus.ARCHIVED
