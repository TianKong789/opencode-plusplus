from agents.llm_coder import LLMCoderAgent
from core.ids import PlanId, TaskId
from core.models.plan import Plan, PlanStatus
from core.stub_llm import StubLLMExecutor


def _make_plan(plan_id: str = "p1", task_id: str = "t1") -> Plan:
    return Plan(
        id=PlanId(plan_id),
        task_id=TaskId(task_id),
        strategy="sequential",
        steps=("step1",),
        status=PlanStatus.APPROVED,
    )


class TestLLMCoderAgent:
    def test_implement_uses_llm(self) -> None:
        llm = StubLLMExecutor(response="generated code here")
        agent = LLMCoderAgent(llm=llm)
        plan = _make_plan()
        artifact = agent.implement(plan)
        assert artifact.plan_id == plan.id
        assert "generated code" in artifact.summary

    def test_implement_empty_llm_response(self) -> None:
        llm = StubLLMExecutor(response="")
        agent = LLMCoderAgent(llm=llm)
        plan = _make_plan()
        artifact = agent.implement(plan)
        assert artifact.files[0] == "t1.py"
