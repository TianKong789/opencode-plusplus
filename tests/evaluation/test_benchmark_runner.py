from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.ids import BenchmarkId, SkillId
from core.models.benchmark import Benchmark
from core.models.evaluation import Verdict
from benchmarks.benchmark_runner import DefaultBenchmarkRunner


def _write_metadata(capability_dir: Path, capability: str) -> None:
    capability_dir.mkdir(parents=True)
    (capability_dir / "metadata.json").write_text(
        json.dumps(
            {
                "capability": capability,
                "version": "0.1.0",
                "description": f"{capability} benchmark",
                "scoring": {"correctness": 1.0},
                "difficulty_levels": ["basic"],
            }
        ),
        encoding="utf-8",
    )


def test_discover_benchmarks_returns_capabilities_in_name_order_and_skips_malformed_metadata(
    tmp_path: Path,
) -> None:
    # Given: capability metadata in non-deterministic creation order and one malformed file.
    capabilities_dir = tmp_path / "capabilities"
    _write_metadata(capabilities_dir / "zeta", "zeta")
    _write_metadata(capabilities_dir / "alpha", "alpha")
    malformed_dir = capabilities_dir / "malformed"
    malformed_dir.mkdir()
    (malformed_dir / "metadata.json").write_text("{", encoding="utf-8")
    incomplete_dir = capabilities_dir / "incomplete"
    incomplete_dir.mkdir()
    (incomplete_dir / "metadata.json").write_text(
        json.dumps({"capability": "incomplete", "description": "Incomplete benchmark"}),
        encoding="utf-8",
    )

    # When: benchmarks are discovered from the capability directory.
    benchmarks = DefaultBenchmarkRunner().discover_benchmarks(capabilities_dir)

    # Then: valid metadata becomes ordered, runnable benchmark definitions.
    assert tuple(benchmark.id for benchmark in benchmarks) == (
        BenchmarkId("alpha"),
        BenchmarkId("zeta"),
    )
    assert tuple(benchmark.skill_id for benchmark in benchmarks) == (
        SkillId("alpha"),
        SkillId("zeta"),
    )
    assert all(benchmark.input_data and benchmark.expected_output for benchmark in benchmarks)


def test_run_all_discovers_benchmarks_when_none_are_registered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given: an otherwise empty runner and a filesystem capability benchmark.
    _write_metadata(tmp_path / "benchmarks" / "capabilities" / "python", "python")
    monkeypatch.chdir(tmp_path)
    runner = DefaultBenchmarkRunner()

    # When: the capability is run without manual registration.
    evaluations = runner.run_all("python")

    # Then: discovery is reported without treating a benchmark definition as a pass.
    assert len(evaluations) == 1
    assert evaluations[0].verdict is Verdict.PARTIAL
    assert evaluations[0].score == 0.5


def test_run_all_uses_registered_benchmarks_without_filesystem_discovery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given: a runner with a manually registered benchmark and no benchmark assets.
    monkeypatch.chdir(tmp_path)
    benchmark = Benchmark(
        id=BenchmarkId("manual"),
        skill_id=SkillId("python"),
        name="Manual benchmark",
        input_data="input",
        expected_output="output",
    )
    runner = DefaultBenchmarkRunner()
    runner.register_benchmarks((benchmark,))

    # When: the registered capability is run.
    evaluations = runner.run_all("python")

    # Then: registration does not convert an unevaluated benchmark into a pass.
    assert len(evaluations) == 1
    assert evaluations[0].verdict is Verdict.PARTIAL
    assert evaluations[0].score == 0.5
