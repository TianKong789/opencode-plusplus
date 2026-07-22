from agents.researcher import ResearcherAgent
from core.ids import TaskId
from core.models.task import Task, TaskStatus


def _make_task(
    task_id: str = "t1",
    title: str = "Build auth",
    description: str = "Implement JWT auth",
) -> Task:
    return Task(
        id=TaskId(task_id),
        title=title,
        description=description,
        status=TaskStatus.PENDING,
    )


class TestResearcherAgent:
    def test_research_with_description(self) -> None:
        agent = ResearcherAgent()
        task = _make_task()
        research = agent.research(task)
        assert research.task_id == task.id
        assert research.has_findings()
        assert "JWT auth" in research.findings[0]

    def test_research_without_description(self) -> None:
        agent = ResearcherAgent()
        task = _make_task(description="")
        research = agent.research(task)
        assert not research.has_findings()

    def test_research_includes_summary(self) -> None:
        agent = ResearcherAgent()
        task = _make_task(title="Build auth")
        research = agent.research(task)
        assert "Build auth" in research.summary

    def test_get_research_returns_none(self) -> None:
        agent = ResearcherAgent()
        assert agent.get_research("any") is None
