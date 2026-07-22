from __future__ import annotations

from dataclasses import dataclass

from core.ids import ArtifactId
from core.interfaces.coder import Coder
from core.interfaces.llm_executor import LLMExecutor
from core.models.code_artifact import CodeArtifact
from core.models.plan import Plan


@dataclass(slots=True, frozen=True)
class LLMCoderAgent(Coder):
    """LLM-driven code implementation agent.

    Uses an LLM to generate code from a plan.
    """

    llm: LLMExecutor

    def implement(self, plan: Plan) -> CodeArtifact:
        prompt = (
            f"Implement the following plan:\n"
            f"Strategy: {plan.strategy}\n"
            f"Steps:\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(plan.steps))
        )
        response = self.llm.execute(prompt)
        file_name = f"{plan.task_id}.py"
        return CodeArtifact(
            id=ArtifactId(f"art-{plan.id}"),
            plan_id=plan.id,
            files=(file_name,),
            summary=response[:200] if response else f"Implemented plan: {plan.strategy}",
        )

    def get_artifact(self, artifact_id: str) -> CodeArtifact | None:
        return None
