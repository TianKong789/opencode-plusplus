# OpenCode++

OpenCode++ is a continuously learning AI engineering platform.

Unlike traditional coding assistants, OpenCode++ is designed to improve not only the software it builds, but also its own skills, workflows, prompts, memory, planning strategies, and evaluation methods.

The long-term goal is to create an AI engineering system that can accumulate experience across projects, learn from successes and failures, and continuously improve through benchmark-driven recursive self-improvement.

## Core Principle

Everything is an Experience.

Every engineering task follows the lifecycle:

Task → Plan → Execute → Evaluate → Reflect → Experience

Experiences become the foundation for memory, skill extraction, benchmarking, and future improvements.

## Major Components

Orchestrator
Agent Framework
Execution Engine Adapters
Memory System
Skill Library
Evaluation Framework
Evolution Lab
Benchmark Framework

## Project Structure

```
├── core/           # Core abstractions and base classes
├── runtime/        # Execution runtime and orchestration
├── agents/         # Agent implementations
├── memory/         # Memory and state management
├── skills/         # Skill definitions and loaders
├── evaluation/     # Evaluation and benchmarking
├── evolution/      # Self-improvement and adaptation
├── applications/   # End-user applications and interfaces
├── benchmarks/     # Benchmark datasets and runners
├── prompts/        # Prompt templates
├── configs/        # Configuration files
├── tests/          # Test suite
└── docs/           # Documentation
```
## Design Goals

Modular architecture
Execution engine independence
Long-term memory
Skill accumulation
Benchmark-driven evolution
Explainable decision making

## Setup

```bash
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
```

## Current Status

All 8 development phases complete (Phase 0–7).

See [docs/roadmap.md](docs/roadmap.md) for detailed progress per phase.

## License

See LICENSE for details.
