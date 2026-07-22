from agents.llm_researcher import LLMResearcherAgent
from core.ids import TaskId
from core.models.task import Task, TaskStatus
from core.stub_llm import StubLLMExecutor


def _make_task(task_id: str = "t1") -> Task:
    return Task(
        id=TaskId(task_id),
        title="Build auth",
        description="Implement JWT auth",
        status=TaskStatus.PENDING,
    )


class TestLLMResearcherAgent:
    def test_research_uses_llm(self) -> None:
        llm = StubLLMExecutor(response="found 3 approaches")
        agent = LLMResearcherAgent(llm=llm)
        task = _make_task()
        research = agent.research(task)
        assert research.has_findings()
        assert "found 3 approaches" in research.findings[0]
