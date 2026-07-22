from __future__ import annotations

from dataclasses import dataclass

from core.ids import TestResultId
from core.interfaces.tester import Tester
from core.models.code_artifact import CodeArtifact
from core.models.test_result import TestResult, TestVerdict


@dataclass(slots=True, frozen=True)
class TesterAgent(Tester):
    """Runs tests on code artifacts.

    Placeholder implementation — replace with actual test runner
    integration for production use.
    """

    def test(self, artifact: CodeArtifact) -> TestResult:
        """Run tests on a code artifact.

        Args:
            artifact: The code artifact to test.

        Returns:
            Test results — passes if artifact has files, fails otherwise.
        """
        if artifact.files:
            return TestResult(
                id=TestResultId(f"tr-{artifact.id}"),
                artifact_id=artifact.id,
                verdict=TestVerdict.PASS,
                passed=1,
                failed=0,
                summary="Placeholder test passed.",
            )
        return TestResult(
            id=TestResultId(f"tr-{artifact.id}"),
            artifact_id=artifact.id,
            verdict=TestVerdict.FAIL,
            passed=0,
            failed=1,
            errors=("No files to test.",),
            summary="No files in artifact.",
        )

    def get_result(self, result_id: str) -> TestResult | None:
        """Retrieve test results by their identifier.

        Args:
            result_id: The unique identifier of the test result.

        Returns:
            None — results are not persisted in this implementation.
        """
        return None
