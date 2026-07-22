from __future__ import annotations

from dependency_injector import containers, providers

from agents.executor import ExecutorAgent
from agents.planner import PlannerAgent
from agents.reflector import ReflectorAgent
from configs.application import ApplicationConfig
from configs.benchmark import BenchmarkConfig
from configs.git import GitConfig
from configs.llm import LLMConfig
from configs.memory import MemoryConfig
from configs.workspace import WorkspaceConfig
from evaluation.benchmark_runner import DefaultBenchmarkRunner
from evaluation.evaluator import LLMEvaluator
from memory.experience_store import ExperienceStore
from memory.skill_repository import FileSkillRepository
from runtime.execution_engine import LocalExecutionEngine
from runtime.git_manager import LocalGitManager
from runtime.workspace_manager import LocalWorkspaceManager


class Container(containers.DeclarativeContainer):
    """Central dependency injection container.

    Configuration providers are loaded eagerly.
    Service providers are wired to their default implementations.
    Override any provider at startup via ``container.<service>.override(...)``.
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "core.providers",
            "applications.main",
        ],
    )

    # ── configuration ────────────────────────────────────────────────
    application = providers.Singleton(ApplicationConfig)
    llm = providers.Singleton(LLMConfig)
    memory = providers.Singleton(MemoryConfig)
    benchmark = providers.Singleton(BenchmarkConfig)
    git = providers.Singleton(GitConfig)
    workspace = providers.Singleton(WorkspaceConfig)

    # ── services ────────────────────────────────────────────────────
    planner = providers.Singleton(PlannerAgent)
    executor = providers.Singleton(ExecutorAgent)
    evaluator = providers.Singleton(LLMEvaluator)
    reflector = providers.Singleton(ReflectorAgent)
    memory_provider = providers.Singleton(ExperienceStore)
    execution_engine = providers.Singleton(LocalExecutionEngine)
    workspace_manager = providers.Singleton(LocalWorkspaceManager)
    git_manager = providers.Singleton(LocalGitManager)
    benchmark_runner = providers.Singleton(DefaultBenchmarkRunner)
    skill_repository = providers.Singleton(FileSkillRepository)
