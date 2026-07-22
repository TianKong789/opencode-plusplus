from __future__ import annotations

from pathlib import Path

from dependency_injector import containers, providers

from agents.executor import ExecutorAgent
from agents.planner import PlannerAgent
from agents.reflector import ReflectorAgent
from applications.orchestrator import Orchestrator
from applications.services import ExperienceCapture
from benchmarks.metrics import MetricsTracker
from benchmarks.suite import BenchmarkSuite
from configs.application import ApplicationConfig
from configs.benchmark import BenchmarkConfig
from configs.git import GitConfig
from configs.llm import LLMConfig
from configs.memory import MemoryConfig
from configs.workspace import WorkspaceConfig
from core.null_objects import NullEventBus
from benchmarks.benchmark_runner import DefaultBenchmarkRunner
from evaluation.evaluator import LLMEvaluator
from evolution.engine import EvolutionEngine
from evolution.loop import EvolutionLoop
from evolution.skill_evolver import SkillEvolver
from memory.experience_store import ExperienceStore
from memory.file_reflection_repository import FileReflectionRepository
from memory.skill_repository import InMemorySkillRepository
from runtime.event_bus import SyncEventBus
from runtime.execution_engine import LocalExecutionEngine
from runtime.git_manager import LocalGitManager
from runtime.workflow_runner import LocalWorkflowRunner
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
    event_bus = providers.Singleton(SyncEventBus)
    null_event_bus = providers.Singleton(NullEventBus)
    planner = providers.Singleton(PlannerAgent)
    executor = providers.Singleton(ExecutorAgent)
    evaluator = providers.Singleton(LLMEvaluator)
    reflector = providers.Singleton(ReflectorAgent)
    experience_store = providers.Singleton(ExperienceStore)
    execution_engine = providers.Singleton(LocalExecutionEngine)
    workflow_runner = providers.Singleton(LocalWorkflowRunner, engine=execution_engine, event_bus=event_bus)
    workspace_manager = providers.Singleton(LocalWorkspaceManager)
    git_manager = providers.Singleton(LocalGitManager)
    experience_service = providers.Singleton(
        ExperienceCapture,
        experience_store=experience_store,
        event_bus=event_bus,
    )
    orchestrator = providers.Singleton(
        Orchestrator,
        planner=planner,
        workflow_runner=workflow_runner,
        workspace_manager=workspace_manager,
        evaluator=evaluator,
        reflector=reflector,
        experience_service=experience_service,
        git_manager=git_manager,
        event_bus=event_bus,
    )
    benchmark_runner = providers.Singleton(DefaultBenchmarkRunner)
    skill_repository = providers.Singleton(InMemorySkillRepository)
    reflection_path = providers.Callable(Path, memory.provided.path)
    reflection_repository = providers.Singleton(
        FileReflectionRepository,
        base_path=reflection_path,
    )
    benchmark_suite = providers.Singleton(BenchmarkSuite)
    metrics_tracker = providers.Singleton(MetricsTracker)
    evolution_loop = providers.Singleton(EvolutionLoop)
    skill_evolver = providers.Singleton(SkillEvolver)
    evolution_engine = providers.Singleton(
        EvolutionEngine,
        loop=evolution_loop,
        suite=benchmark_suite,
        evolver=skill_evolver,
        metrics=metrics_tracker,
        experience_store=experience_store,
        reflection_repository=reflection_repository,
        skill_repository=skill_repository,
    )
