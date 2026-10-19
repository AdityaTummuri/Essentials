---
name: pytest-workflow
description: Architect, write, and maintain deterministic unit and integration test suites using Pytest. Use when writing tests, fixtures, parametric testing, mocking, and coverage collection in Python projects.
---

# Pytest Workflow & Testing Standards

A disciplined guide to engineering robust, fast, deterministic test suites using `pytest`.

## 1. Test Architecture & Directory Structure

Organize tests mirroring the application package layout:

```text
my_project/
├── src/
│   └── my_pkg/
│       ├── core.py
│       └── service.py
├── tests/
│   ├── conftest.py          # Shared fixtures, hooks, and test configuration
│   ├── unit/
│   │   ├── test_core.py
│   │   └── test_service.py
│   └── integration/
│       └── test_api.py
└── pyproject.toml
```

## 2. Fixture Design Principles

- **Explicit Scoping**: Prefer `function` scope for test isolation. Use `module` or `session` strictly for expensive read-only resources (e.g. database client pools or test containers).
- **Yield Fixtures for Cleanup**: Always clean up resources using `yield`.
- **Avoid Fixture Duplication**: Place universal fixtures in `tests/conftest.py`.

```python
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_workspace():
    """Provide a clean temporary directory, cleaned up after test run."""
    tmp = tempfile.mkdtemp(prefix="test-workspace-")
    yield Path(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
```

## 3. Parametrization Patterns

Use `@pytest.mark.parametrize` to test boundary conditions, schemas, and edge cases:

```python
@pytest.mark.parametrize("input_val, expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase_conversion(input_val: str, expected: str):
    assert input_val.upper() == expected
```

## 4. Mocking & Monkeypatching

- Use `monkeypatch` for standard environment variable and attribute substitution.
- Use `unittest.mock.patch` for mocking external network calls or subprocesses.
- Never mock the code under test—only its external boundaries.

## 5. Execution Flags & Verification

```bash
# Run unit tests with verbosity and fail-fast
pytest tests/unit -v -x

# Run with coverage report
pytest --cov=src/my_pkg --cov-report=term-missing tests/
```
