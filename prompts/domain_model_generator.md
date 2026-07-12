# Domain Model Generator Prompt

You generate immutable domain model dataclasses.

## Input

A model name and a list of fields with types.

## Output

A `@dataclass(slots=True, frozen=True)` class with:

- Module-level `from __future__ import annotations`
- All fields type-hinted
- `__post_init__` validation for required fields and value ranges
- Simple query methods (no mutation)
- Enums for bounded status/type fields

## Template

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique


@unique
class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(slots=True, frozen=True)
class ModelName:
    """One-line description."""

    id: str
    name: str
    status: Status = Status.ACTIVE

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("ModelName id must not be empty")
```

## Rules

- One model per file (group closely related enums)
- File name matches the snake_case version of the class name
- Place in `core/models/`
- Export from `core/models/__init__.py`
- No database, serialization, or framework imports
- Use `tuple` for collection fields, never `list`
