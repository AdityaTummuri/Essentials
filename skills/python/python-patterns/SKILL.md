---
name: python-patterns
description: Idiomatic modern Python design patterns, dataclasses, protocols, and clean architecture conventions. Use when designing object models, interfaces, exception hierarchies, and data pipelines in Python 3.10+.
---

# Modern Python Patterns & Clean Architecture

Design robust, type-safe, and idiomatic Python applications.

## 1. Data Modeling: Dataclasses & Immutability

Prefer `@dataclass(frozen=True, slots=True)` for immutable value objects and domain entities:

```python
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True, slots=True)
class Coordinate:
    x: float
    y: float
    z: float = 0.0

    def translate(self, dx: float, dy: float) -> Self:
        return self.__class__(self.x + dx, self.y + dy, self.z)
```

## 2. Structural Subtyping: Protocols

Decouple interfaces from concrete implementations using `typing.Protocol`:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class StorageBackend(Protocol):
    def read(self, key: str) -> bytes: ...
    def write(self, key: str, data: bytes) -> None: ...
```

## 3. Pattern Matching (Python 3.10+)

Decompose complex polymorphic data structures with structural pattern matching:

```python
def handle_event(event: dict) -> None:
    match event:
        case {"type": "login", "user": str(username)}:
            print(f"User {username} logged in")
        case {"type": "logout", "user": str(username), "reason": str(reason)}:
            print(f"User {username} logged out: {reason}")
        case _:
            raise ValueError(f"Unsupported event payload: {event}")
```

## 4. Custom Exception Hierarchies

Always derive domain exceptions from a package-level root base exception:

```python
class AppError(Exception):
    """Base exception for all domain errors."""

class ValidationError(AppError):
    """Raised when input payload fails validation."""

class ResourceNotFoundError(AppError):
    """Raised when requested resource does not exist."""
```

