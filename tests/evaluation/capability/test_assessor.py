from __future__ import annotations

from core.interfaces import CapabilityTest
from core.models import Capability, CapabilityScore, Model
from src.opencode.evaluation.capability.assessor import CapabilityAssessor
from src.opencode.evaluation.capability.capability_test import (
    PythonCapabilityTest,
    SQLCapabilityTest,
)


class CustomMathCapabilityTest(CapabilityTest):
    def capability(self) -> Capability:
        return Capability.MATH

    def run(self, model: Model) -> CapabilityScore:
        return CapabilityScore(
            capability=Capability.MATH,
            score=9.0,
            confidence=0.9,
            evidence=(f"Assessed math capability for {model.model_id}",),
        )

    def load_tasks(self) -> tuple[dict[str, object], ...]:
        return (
            {
                "task_id": "math_custom",
                "description": "Solve a custom arithmetic task",
                "difficulty": "basic",
            },
        )


class TestCapabilityAssessorRegistration:
    def test_default_construction_has_no_tests(self) -> None:
        assessor = CapabilityAssessor()

        assert len(assessor._tests) == 0

    def test_explicit_construction_injects_provided_tests(self) -> None:
        tests = {Capability.PYTHON: PythonCapabilityTest(), Capability.SQL: SQLCapabilityTest()}
        assessor = CapabilityAssessor(_tests=tests)

        assert len(assessor._tests) == 2
        assert all(isinstance(test, CapabilityTest) for test in assessor._tests.values())

    def test_list_capabilities_returns_injected_capabilities(self) -> None:
        tests = {Capability.PYTHON: PythonCapabilityTest(), Capability.SQL: SQLCapabilityTest()}
        assessor = CapabilityAssessor(_tests=tests)

        capabilities = assessor.list_capabilities()

        assert isinstance(capabilities, tuple)
        assert len(capabilities) == 2
        assert all(isinstance(capability, Capability) for capability in capabilities)

    def test_register_test_adds_a_custom_test(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        custom_test = CustomMathCapabilityTest()

        assessor.register_test(custom_test)

        assert assessor.get_test(Capability.MATH) is custom_test
        assert assessor.list_capabilities() == (Capability.PYTHON, Capability.MATH)

    def test_register_test_overwrites_existing_capability_test(self) -> None:
        original_test = PythonCapabilityTest()
        replacement_test = PythonCapabilityTest(
            _tasks=(
                {
                    "task_id": "replacement_python",
                    "description": "Run replacement Python capability task",
                    "difficulty": "custom",
                },
            )
        )
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: original_test})

        assessor.register_test(replacement_test)

        assert assessor.get_test(Capability.PYTHON) is replacement_test

    def test_get_test_returns_matching_registered_test(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})

        assert isinstance(assessor.get_test(Capability.PYTHON), PythonCapabilityTest)

    def test_get_test_returns_none_for_unregistered_capability(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.MATH: CustomMathCapabilityTest()})

        assert assessor.get_test(Capability.PYTHON) is None


class TestCapabilityAssessorAssessment:
    def test_assess_returns_score_for_registered_capability(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        model = Model(model_id="model-1", provider="provider-1")

        score = assessor.assess(model, Capability.PYTHON)

        assert isinstance(score, CapabilityScore)
        assert score.capability is Capability.PYTHON

    def test_assess_returns_none_for_unregistered_capability(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        model = Model(model_id="model-1", provider="provider-1")

        score = assessor.assess(model, Capability.MATH)

        assert score is None
        assert assessor.get_results(model.model_id) == ()

    def test_assess_stores_and_returns_result_for_model(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        model = Model(model_id="model-1", provider="provider-1")

        score = assessor.assess(model, Capability.PYTHON)

        assert score is not None
        assert assessor.get_results(model.model_id) == (score,)

    def test_assess_all_returns_and_stores_scores_for_all_registered_tests(self) -> None:
        assessor = CapabilityAssessor(
            _tests={
                Capability.PYTHON: PythonCapabilityTest(),
                Capability.SQL: SQLCapabilityTest(),
            }
        )
        model = Model(model_id="model-1", provider="provider-1")

        scores = assessor.assess_all(model)

        assert len(scores) == len(assessor._tests)
        assert {score.capability for score in scores} == {Capability.PYTHON, Capability.SQL}
        assert assessor.get_results(model.model_id) == scores

    def test_get_results_returns_empty_tuple_for_unknown_model(self) -> None:
        assessor = CapabilityAssessor()

        assert assessor.get_results("unknown-model") == ()


class TestCapabilityAssessorResults:
    def test_clear_results_for_model_removes_only_that_models_results(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        first_model = Model(model_id="model-1", provider="provider-1")
        second_model = Model(model_id="model-2", provider="provider-1")
        second_score = assessor.assess(second_model, Capability.PYTHON)
        assessor.assess(first_model, Capability.PYTHON)

        assessor.clear_results(first_model.model_id)

        assert assessor.get_results(first_model.model_id) == ()
        assert assessor.get_results(second_model.model_id) == (second_score,)

    def test_clear_results_without_model_removes_all_results(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        first_model = Model(model_id="model-1", provider="provider-1")
        second_model = Model(model_id="model-2", provider="provider-1")
        assessor.assess(first_model, Capability.PYTHON)
        assessor.assess(second_model, Capability.PYTHON)

        assessor.clear_results()

        assert assessor.get_results(first_model.model_id) == ()
        assert assessor.get_results(second_model.model_id) == ()

    def test_clear_results_for_unknown_model_is_a_no_op(self) -> None:
        assessor = CapabilityAssessor(_tests={Capability.PYTHON: PythonCapabilityTest()})
        model = Model(model_id="model-1", provider="provider-1")
        score = assessor.assess(model, Capability.PYTHON)

        assessor.clear_results("unknown-model")

        assert assessor.get_results(model.model_id) == (score,)
