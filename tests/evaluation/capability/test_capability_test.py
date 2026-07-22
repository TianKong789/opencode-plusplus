from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.opencode.evaluation.capability.capabilities import Capability
from src.opencode.evaluation.capability.capability_test import (
    ArchitectureCapabilityTest,
    CapabilityTest,
    CodeReviewCapabilityTest,
    DebuggingCapabilityTest,
    DocumentationCapabilityTest,
    PlanningCapabilityTest,
    PythonCapabilityTest,
    ReasoningCapabilityTest,
    RefactoringCapabilityTest,
    SQLCapabilityTest,
    TestingCapabilityTest,
    get_all_tests,
    get_test_for_capability,
)
from src.opencode.evaluation.capability.models import CapabilityScore, Model


ConcreteCapabilityTest = (
    type[PythonCapabilityTest]
    | type[SQLCapabilityTest]
    | type[ArchitectureCapabilityTest]
    | type[ReasoningCapabilityTest]
    | type[RefactoringCapabilityTest]
    | type[DocumentationCapabilityTest]
    | type[PlanningCapabilityTest]
    | type[TestingCapabilityTest]
    | type[DebuggingCapabilityTest]
    | type[CodeReviewCapabilityTest]
)

CAPABILITY_TEST_CASES: tuple[tuple[ConcreteCapabilityTest, Capability], ...] = (
    (PythonCapabilityTest, Capability.PYTHON),
    (SQLCapabilityTest, Capability.SQL),
    (ArchitectureCapabilityTest, Capability.ARCHITECTURE),
    (ReasoningCapabilityTest, Capability.REASONING),
    (RefactoringCapabilityTest, Capability.REFACTORING),
    (DocumentationCapabilityTest, Capability.DOCUMENTATION),
    (PlanningCapabilityTest, Capability.PLANNING),
    (TestingCapabilityTest, Capability.TESTING),
    (DebuggingCapabilityTest, Capability.DEBUGGING),
    (CodeReviewCapabilityTest, Capability.CODE_REVIEW),
)
CUSTOM_TASKS: tuple[dict[str, object], ...] = (
    {
        "task_id": "custom_task",
        "description": "Run a caller-provided capability task",
        "difficulty": "custom",
    },
)


class TestModel:
    def test_constructs_with_required_fields_and_default_endpoint(self) -> None:
        model = Model(model_id="model-1", provider="provider-1")

        assert model.model_id == "model-1"
        assert model.provider == "provider-1"
        assert model.api_endpoint == ""

    def test_rejects_field_assignment(self) -> None:
        model = Model(model_id="model-1", provider="provider-1")

        with pytest.raises(FrozenInstanceError):
            setattr(model, "model_id", "updated-model")


class TestCapabilityTest:
    def test_cannot_be_instantiated_directly(self) -> None:
        with pytest.raises(TypeError):
            CapabilityTest()


class TestConcreteCapabilityTests:
    @pytest.mark.parametrize(("test_class", "capability"), CAPABILITY_TEST_CASES)
    def test_reports_expected_capability(
        self, test_class: ConcreteCapabilityTest, capability: Capability
    ) -> None:
        capability_test = test_class()

        assert capability_test.capability() is capability

    @pytest.mark.parametrize(("test_class", "capability"), CAPABILITY_TEST_CASES)
    def test_run_returns_a_valid_score_with_evidence(
        self, test_class: ConcreteCapabilityTest, capability: Capability
    ) -> None:
        model = Model(model_id="model-1", provider="provider-1")

        score = test_class().run(model)

        assert isinstance(score, CapabilityScore)
        assert score.capability is capability
        assert 0.0 <= score.score <= 10.0
        assert 0.0 <= score.confidence <= 1.0
        assert score.evidence
        assert all(isinstance(item, str) for item in score.evidence)

    @pytest.mark.parametrize(
        "test_class", tuple(test_class for test_class, _ in CAPABILITY_TEST_CASES)
    )
    def test_load_tasks_returns_complete_default_task_definitions(
        self, test_class: ConcreteCapabilityTest
    ) -> None:
        tasks = test_class().load_tasks()

        assert tasks
        assert isinstance(tasks, tuple)
        for task in tasks:
            assert {"task_id", "description", "difficulty"} <= task.keys()

    @pytest.mark.parametrize(
        "test_class", tuple(test_class for test_class, _ in CAPABILITY_TEST_CASES)
    )
    def test_load_tasks_uses_custom_task_override(
        self, test_class: ConcreteCapabilityTest
    ) -> None:
        capability_test = test_class(_tasks=CUSTOM_TASKS)

        assert capability_test.load_tasks() == CUSTOM_TASKS

    def test_each_default_test_uses_a_distinct_class(self) -> None:
        test_classes = tuple(type(capability_test) for capability_test in get_all_tests())

        assert len(test_classes) == 10
        assert len(set(test_classes)) == 10


class TestCapabilityTestRegistry:
    def test_get_all_tests_returns_the_ten_default_capability_tests(self) -> None:
        tests = get_all_tests()

        assert isinstance(tests, tuple)
        assert len(tests) == 10
        assert all(isinstance(capability_test, CapabilityTest) for capability_test in tests)

    def test_get_test_for_capability_returns_python_test(self) -> None:
        capability_test = get_test_for_capability(Capability.PYTHON)

        assert isinstance(capability_test, PythonCapabilityTest)

    def test_get_test_for_capability_returns_sql_test(self) -> None:
        capability_test = get_test_for_capability(Capability.SQL)

        assert isinstance(capability_test, SQLCapabilityTest)

    def test_get_test_for_all_capabilities_returns_ten_tests_and_ten_nones(self) -> None:
        tests_by_capability = tuple(get_test_for_capability(capability) for capability in Capability)
        registered_tests = tuple(test for test in tests_by_capability if test is not None)
        unsupported_tests = tuple(test for test in tests_by_capability if test is None)

        assert len(Capability) == 20
        assert len(registered_tests) == 10
        assert len(unsupported_tests) == 10
        assert all(isinstance(capability_test, CapabilityTest) for capability_test in registered_tests)

    def test_get_test_for_unsupported_capability_returns_none(self) -> None:
        assert get_test_for_capability(Capability.MATH) is None
