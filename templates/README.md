# Project Starter Templates

Essentials provides minimal, production-grade starter templates to quickly scaffold new projects with sensible defaults.

## Available Templates

| Template | Path | Description | Stack |
|---|---|---|---|
| **Python Starter** | `templates/python` | Clean modern Python baseline with `pyproject.toml`, pytest, and ruff | Python 3.10+, Pytest, Ruff |
| **Creative Portfolio** | `templates/portfolio` | Interactive 3D web experience with canvas framing and lighting | Vite, Three.js, Vanilla JS |
| **Data Dashboard** | `templates/dashboard` | Clean, accessible data-dense metric cards with CSS variables | Vite, Semantic CSS |

## Usage

Copy any template into your new project directory:
```bash
cp -r templates/python ~/projects/my-new-service
cd ~/projects/my-new-service
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```
