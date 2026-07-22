from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.code_artifact import CodeArtifact
from core.models.test_result import TestResult


class Tester(ABC):
    """Runs tests on code artifacts."""

    @abstractmethod
    def test(self, artifact: CodeArtifact) -> TestResult:
        """Run tests on a code artifact.

        Args:
            artifact: The code artifact to test.

        Returns:
            Test results with pass/fail counts and verdict.
        """

    @abstractmethod
    def get_result(self, result_id: str) -> TestResult | None:
        """Retrieve test results by their identifier.

        Args:
            result_id: The unique identifier of the test result.

        Returns:
            The test result if found, None otherwise.
        """
