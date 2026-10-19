---
name: packaging-pyproject
description: Standards-compliant Python project packaging, build hooks, pyproject.toml, and distribution. Use when configuring modern Python project metadata, entrypoints, tool settings, and distribution builds.
---

# Modern Python Packaging with `pyproject.toml`

Configure standardized PEP 517/518/621 packaging for Python libraries and CLI tools.

## 1. Minimal Standards-Compliant `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "High performance developer utilities"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
    { name = "Developer", email = "dev@example.com" },
]
dependencies = [
    "pydantic>=2.0",
]

[project.scripts]
my-cli = "my_package.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --strict-markers"

[tool.ruff]
line-length = 100
target-version = "py310"
```

## 2. Building Distributions

```bash
# Build wheel and sdist
python -m build

# Inspect archive contents
tar -ztvf dist/*.tar.gz
```
