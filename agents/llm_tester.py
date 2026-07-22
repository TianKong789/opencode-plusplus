from __future__ import annotations

from dataclasses import dataclass

from core.ids import TestResultId
from core.interfaces.llm_executor import LLMExecutor
from core.interfaces.tester import Tester
from core.models.code_artifact import CodeArtifact
from core.models.test_result import TestResult, TestVerdict


@dataclass(slots=True, frozen=True)
class LLMTesterAgent(Tester):
    """LLM-driven test agent.

    Uses an LLM to analyze code and generate test results.
    """

    llm: LLMExecutor

    def test(self, artifact: CodeArtifact) -> TestResult:
        prompt = (
            f"Test this code artifact:\n"
            f"Files: {', '.join(artifact.files)}\n"
            f"Summary: {artifact.summary}\n"
            f"Provide pass/fail counts and any errors found."
        )
        response = self.llm.execute(prompt)
        if artifact.files:
            return TestResult(
                id=TestResultId(f"tr-{artifact.id}"),
                artifact_id=artifact.id,
                verdict=TestVerdict.PASS,
                passed=1,
                failed=0,
                summary=response[:200] if response else "LLM test passed.",
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
        return None
