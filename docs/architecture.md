# Architecture

> High-level system architecture for OpenCode++.

## Overview

OpenCode++ is a continuously learning AI engineering platform that iteratively plans, executes, evaluates, and reflects on software tasks.

## Core Loop

```
Task → Plan → Execute → Evaluate → Reflect → Experience → Skill
```

## Packages

| Package | Purpose |
|---|---|
| `core/` | Domain models, interfaces, events, exceptions, config |
| `runtime/` | Execution orchestration |
| `agents/` | Agent definitions and behaviors |
| `memory/` | Experience and skill persistence |
| `skills/` | Skill discovery and composition |
| `evaluation/` | Scoring and benchmarking |
| `evolution/` | Learning loop and adaptation |
| `benchmarks/` | Standardized test suites |
| `applications/` | Entry points and CLI |
| `configs/` | Pydantic Settings configuration |

## Principles

- Immutable domain models (`frozen=True, slots=True`)
- Interface-driven design (ABCs in `core/interfaces/`)
- Event-sourced communication (`core/events/`)
- Dependency injection via `dependency_injector`
