---
name: type-hints-modern
description: Python 3.10+ static type hinting, TypeAlias, TypeVar, Self, ParamSpec, and static verification. Use when annotating functions, classes, generics, decorators, and configuring Mypy or Pyright.
---

# Modern Python Type Hinting (Python 3.10+)

Strict, readable static typing guidelines for modern Python codebases.

## 1. Union Types & Builtin Generics

- Use `|` instead of `typing.Union` or `typing.Optional`.
- Use standard collection types (`list[T]`, `dict[K, V]`, `set[T]`, `tuple[T, ...]`) instead of `typing.List`, `typing.Dict`.

```python
def fetch_metadata(resource_id: str | int) -> dict[str, list[str]] | None:
    ...
```

## 2. The `Self` Type

Use `typing.Self` for fluent APIs, builders, and alternative constructors:

```python
from typing import Self

class QueryBuilder:
    def __init__(self) -> None:
        self._filters: list[str] = []

    def filter(self, condition: str) -> Self:
        self._filters.append(condition)
        return self
```

## 3. Preserving Function Signatures with `ParamSpec`

Wrap functions and preserve decorator signatures accurately:

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
import functools

P = ParamSpec("P")
R = TypeVar("R")

def log_invocation(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## 4. Static Type Verification

Verify typing without runtime overhead:

```bash
mypy src/ --strict
```

