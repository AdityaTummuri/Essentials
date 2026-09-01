# Bare Minimum

A minimal baseline repository template.

## Getting Started

### Prerequisites
- Python 3.10+

### Installation & Setup

#### Option 1: Using pip and virtualenv

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using Poetry

```bash
# Install dependencies
poetry install

# Spawn a shell within the virtual environment
poetry shell
```

## Usage

```bash
python main.py
```
