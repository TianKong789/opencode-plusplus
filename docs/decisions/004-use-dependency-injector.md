# ADR 004: Use dependency_injector for DI

**Status:** Accepted

## Context

Components need loose coupling and testable wiring.

## Decision

Use `dependency_injector` containers in `core/container.py` with provider ABCs in `core/providers/`.

## Consequences

- Centralized wiring in `Container`
- Easy mocking via `override()`
- Singleton lifecycle for services
- Configuration injected alongside services
