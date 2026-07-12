from __future__ import annotations

from dependency_injector import containers, providers

from configs.application import ApplicationConfig
from configs.benchmark import BenchmarkConfig
from configs.git import GitConfig
from configs.llm import LLMConfig
from configs.memory import MemoryConfig
from configs.workspace import WorkspaceConfig


class Container(containers.DeclarativeContainer):
    """Central dependency injection container.

    Configuration providers are loaded eagerly.
    Service providers are declared as ``Singleton`` stubs —
    call ``container.<service>().wire(...)`` or override via
    ``container.<service>.override(providers.Singleton(RealImpl))`` at startup.
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "core.providers",
        ],
    )

    # ── configuration ────────────────────────────────────────────────
    application = providers.Singleton(ApplicationConfig)
    llm = providers.Singleton(LLMConfig)
    memory = providers.Singleton(MemoryConfig)
    benchmark = providers.Singleton(BenchmarkConfig)
    git = providers.Singleton(GitConfig)
    workspace = providers.Singleton(WorkspaceConfig)

    # ── services (override at startup) ──────────────────────────────
    planner = providers.Singleton(object)
    executor = providers.Singleton(object)
    evaluator = providers.Singleton(object)
    reflector = providers.Singleton(object)
    memory_provider = providers.Singleton(object)
    execution_engine = providers.Singleton(object)
    workspace_manager = providers.Singleton(object)
    git_manager = providers.Singleton(object)
    benchmark_runner = providers.Singleton(object)
    skill_repository = providers.Singleton(object)
