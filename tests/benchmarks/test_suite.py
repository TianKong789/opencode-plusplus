from benchmarks.suite import BenchmarkSuite
from core.ids import BenchmarkId, SkillId
from core.models.benchmark import Benchmark


def test_add_and_retrieve_benchmarks() -> None:
    suite = BenchmarkSuite()
    bench = Benchmark(
        id=BenchmarkId("b1"),
        skill_id=SkillId("s1"),
        name="test",
        input_data="x",
        expected_output="y",
    )
    suite.add(bench)
    assert suite.count("s1") == 1
    assert suite.get_for_skill("s1") == (bench,)
