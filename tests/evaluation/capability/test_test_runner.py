from __future__ import annotations

import json

from src.opencode.evaluation.capability.test_runner import TestRunner


def test_load_tasks_reads_task_definitions_from_metadata(tmp_path) -> None:
    benchmark_dir = tmp_path / "benchmarks" / "capabilities"
    metadata_path = benchmark_dir / "python" / "metadata.json"
    metadata_path.parent.mkdir(parents=True)
    metadata_path.write_text(
        json.dumps(
            {
                "capability": "python",
                "tasks": [
                    {
                        "task_id": "python-basic-1",
                        "input_data": "return 2 + 2",
                        "expected_output": "4",
                        "difficulty": "basic",
                    }
                ],
            }
        )
    )
    runner = TestRunner(benchmark_dir=benchmark_dir)

    tasks = runner.load_tasks("python")

    assert len(tasks) == 1
    assert tasks[0].task_id == "python-basic-1"
    assert tasks[0].input_data == "return 2 + 2"
    assert tasks[0].expected_output == "4"
    assert tasks[0].capability == "python"
    assert tasks[0].difficulty == "basic"
