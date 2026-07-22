# Python Dataclass Modeling

> Skill for creating immutable, validated domain models using Python dataclasses.

## Description

Ability to design and implement clean domain models using `@dataclass(slots=True, frozen=True)` with:
- Typed identifiers (`BaseEntityId` str subclasses)
- Comprehensive docstrings (module, class, field, method level)
- Validation in `__post_init__`
- Immutable collections (`tuple` instead of `list`)
- Enum status fields
- Query helper methods

## When to Use

- Creating new domain entities
- Adding fields to existing models
- Refactoring models for better type safety
- Reviewing model designs

## Key Patterns

### Model Template
```python
from dataclasses import dataclass
from core.ids import SomeId

@dataclass(slots=True, frozen=True)
class ModelName:
    """One-line description."""

    id: SomeId
    """Unique identifier."""

    name: str
    """Human-readable name."""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("ModelName id must not be empty")
```

### Typed ID Pattern
```python
from core.ids import BaseEntityId

class ModelId(BaseEntityId):
    """Unique identifier for ModelName."""
```

### Status Enum Pattern
```python
from enum import Enum, unique

@unique
class ModelStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
```

## Proficiency Indicators

| Level | Score | Indicators |
|---|---|---|
| Novice | 0.0–0.3 | Can create basic dataclasses with type hints |
| Competent | 0.3–0.6 | Uses typed IDs, validation, docstrings consistently |
| Proficient | 0.6–0.9 | Designs model hierarchies, uses enums, immutable collections |
| Mastered | 0.9–1.0 | Creates models that are self-documenting and type-safe end-to-end |
