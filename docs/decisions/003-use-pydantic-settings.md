# ADR 003: Use Pydantic Settings for configuration

**Status:** Accepted

## Context

Configuration must support `.env` files, typed fields, and validation.

## Decision

Use `pydantic-settings` `BaseSettings` with per-module config classes in `configs/`.

## Consequences

- Type-safe configuration with defaults
- Automatic `.env` loading
- Validation at import time
- Environment variable prefixing per config class
