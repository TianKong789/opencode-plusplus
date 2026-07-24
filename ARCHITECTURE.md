# OpenCode++ Architecture Specification v0.1

## Vision
OpenCode++ is a continuously learning AI engineering platform.
The system improves not only the software it builds, but also its
own prompts, workflows, skills, memory, planning strategies,
and evaluation methods through benchmark-driven recursive
self-improvement.

## Core Principle

Everything is an Experience.

Task
    ↓
Plan
    ↓
Execute
    ↓
Evaluate
    ↓
Reflect
    ↓
Experience

Everything either creates, consumes, or improves experiences.

## High-Level Architecture

User
↓
Orchestrator
↓
Planner
↓
Execution Engine
↓
Evaluator
↓
Reflector
↓
Memory
↓
Experience Store

## Primary Domain Objects

* Task
* Plan
* Execution
* Evaluation
* Reflection
* Experience
* Skill
* Benchmark
* Workspace

## Design Principles

1. Experience-centric architecture
2. Interface-first design
3. Benchmark-driven improvement
4. Execution-engine independence
5. Version everything
6. Human oversight for promotions

## Development Phases

Phase 0  Foundation

Phase 1  Execution Runtime

Phase 2  Model Intelligence

Phase 3  Experience Memory

Phase 4  Skill System

Phase 5  Multi-Agent Collaboration

Phase 6  Evolution Lab

Phase 7  Recursive Self-Improvement

## Three-Layer Architecture

The system is organized into three layers with strict unidirectional dependencies:

```
Runtime (ephemeral)  →  Knowledge (derived)  →  Assets (persistent, versioned)
```

### Dependency Matrix

| Layer      | May depend on         | Must NOT depend on |
|------------|----------------------|--------------------|
| **Runtime**  | core/interfaces       | Knowledge, Assets  |
| **Knowledge**| core/interfaces       | Runtime, Assets    |
| **Assets**   | core/interfaces       | Runtime, Knowledge |

**Rule:** Layers communicate through `core/interfaces` (ports) and may not import another layer's implementation directory. Implementations may import the `core` type definitions they operate on, such as domain models, IDs, events, and null objects. "Ports-only" constrains cross-layer communication, not use of shared core types required to implement a port.

| Layer | Components | Port Contracts |
|-------|-----------|----------------|
| **Runtime** | WorkflowRunner, ExecutionEngine, WorkspaceManager, GitManager, EventBus | workflow_runner, execution_engine, workspace_manager, git_manager, event_bus |
| **Knowledge** | CapabilityAssessor, ModelRouter, Profiler, Evaluator, Reflector, SkillExtractor, PromptEvolver, SkillEvolver | capability_assessor, model_router, evaluator, reflector, skill_repository, reflection_repository |
| **Assets** | AssetRepository, BenchmarkRunner, SkillRepository, ExperienceStore, ReflectionRepository | asset_repository, benchmark_runner, skill_repository, experience_store, reflection_repository |

### Data Flow

```
Runtime produces       →  ExecutionResult, Evaluation
Knowledge derives      →  Skills, Reflections, Capability Profiles, Evolved Prompts
Assets persists        →  Skills, Experiences, Benchmarks, Prompts, Workflows
```

### Port Usage

Each layer exposes interfaces in `core/interfaces/`. Implementations live in their respective layer directories. The DI container (`applications/container.py`) wires implementations to ports.

`applications/` and `configs/` are composition-root support, not a fourth domain layer. They may import concrete Runtime, Knowledge, and Assets implementations only to assemble the application graph and inject those implementations behind `core/interfaces` ports.

### Architecture Exceptions

The following are exempt from the "depend only on core/interfaces" rule:

- `core/ids.py`: Typed ID wrappers (WorkflowId, SkillId, etc.) are shared across all layers to prevent ID confusion.
- `core/assets/`: Asset value types (Benchmark, Prompt, Skill, Template, Workflow) are shared domain types used by all layers.
- `core/events/`: Domain event types (TaskReceived, WorkflowStarted, ExperienceStored, etc.) are shared across all layers for the event bus.
