# ADR 001: Use dataclasses for domain models

**Status:** Accepted

## Context

Domain models need to be immutable, lightweight, and type-safe.

## Decision

Use `@dataclass(slots=True, frozen=True)` for all domain models in `core/models/`.

## Consequences

- Immutability enforced at the type level
- Memory-efficient via `__slots__`
- No ORM or serialization coupling
- Validation via `__post_init__`
