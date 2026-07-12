# Python Style Guide

You write clean, idiomatic Python 3.12+ code.

## Formatting

- Line length: 100 characters
- Use ruff for linting and formatting
- Follow PEP 8 conventions

## Type Hints

- Annotate all function signatures
- Use `from __future__ import annotations`
- Prefer `X | None` over `Optional[X]`
- Use `tuple` and `frozenset` for immutable collections

## Dataclasses

- Always use `slots=True`
- Always use `frozen=True` unless mutation is required
- Validate in `__post_init__`, not in constructors
- Use `field(default_factory=...)` for mutable defaults

## Naming

- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes: `_leading_underscore`

## Imports

- Group: stdlib → third-party → local
- Sort with ruff (`isort`)
- Never use wildcard imports

## Docstrings

- Google style for public methods
- Skip docstrings for obvious properties
- Document Args, Returns, and Raises sections
