from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.models.code_artifact import CodeArtifact
from core.models.test_result import TestResult


@runtime_checkable
class Tester(Protocol):
    """Runs tests on code artifacts."""

    def test(self, artifact: CodeArtifact) -> TestResult:
        """Run tests on a code artifact.

        Args:
            artifact: The code artifact to test.

        Returns:
            Test results with pass/fail counts and verdict.
        """

    def get_result(self, result_id: str) -> TestResult | None:
        """Retrieve test results by their identifier.

        Args:
            result_id: The unique identifier of the test result.

        Returns:
            The test result if found, None otherwise.
        """
