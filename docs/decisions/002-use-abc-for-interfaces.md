# ADR 002: Use ABC for interface contracts

**Status:** Accepted

## Context

The system needs pluggable implementations for each component (planner, executor, etc.).

## Decision

Define all interfaces as abstract base classes in `core/interfaces/` using `abc.ABC`.

## Consequences

- Clear contract for implementors
- Runtime enforcement of interface compliance
- IDE support for method signatures
- No framework dependency
