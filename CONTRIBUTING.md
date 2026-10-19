# Contributing to Essentials

Thank you for contributing to Essentials! Our goal is to maintain a polished, maintainable, secure, and cross-agent developer toolkit.

Every addition must solve a real problem, have a clear purpose, and justify its maintenance cost.

---

## 1. Principles & Quality Bar

- **Skills Are Just Folders**: Skills must be self-contained directories with a `SKILL.md` (and any required supporting assets). They must never require runtime installers, symlink daemons, or translation adapters.
- **Zero Arbitrary Execution**: Skills are instructional Markdown guides (`SKILL.md`). We do not accept skills that execute unsolicited background scripts, download runtime binaries, or tamper with user environments.
- **Strict Licensing**: All skills must include an open, permissible license (e.g. MIT, Apache-2.0, BSD) and upstream attribution in `SOURCE.md`.
- **Zero Pip Dependencies**: Maintenance tooling in `scripts/` relies exclusively on the Python standard library.

---

## 2. Adding a New Skill

### Step 1: Check Suitability
Before creating a PR, check whether the skill is already covered (`./scripts/essentials list`). Review our security standards in `SECURITY.md`.

### Step 2: Place Skill Folder
Create a folder under the appropriate category in `skills/<category>/<skill-id>/`:
```text
skills/engineering/my-new-skill/
└── SKILL.md             # Canonical skill instructions
```

Ensure `SKILL.md` contains valid YAML frontmatter:
```markdown
---
name: my-new-skill
description: "Clear, concise explanation of when and how the agent should activate this skill."
---

# My New Skill Content
...
```

If adding a new category, ensure it includes a `LICENSE` and `SOURCE.md` file.

### Step 3: Register in `resources/resources.json`
Add an entry to the `resources` array in `resources/resources.json`:
- `id`: Unique identifier (must match frontmatter `name`).
- `kind`: `"skill"`.
- `category`: Category name (e.g. `"engineering"`).
- `path`: Path relative to repository root (`skills/engineering/my-new-skill`).
- `license`: SPDX identifier (e.g. `"MIT"`).
- `securityReview`: Status (`"static-reviewed"`), date, and audit notes.
- `skillMd.sha256`: SHA-256 hash of `SKILL.md`.

### Step 4: Validate and Test
Run the static validator and unit test suite:
```bash
# Validate library integrity and frontmatter
./scripts/essentials validate

# Run unit tests
python3 -m unittest discover -s tests -v
```

All checks must pass before opening a pull request.

---

## 3. Commit Message Guidelines

We follow Conventional Commits:
- `feat: add <feature>`
- `fix: resolve <issue>`
- `docs: update <documentation>`
- `test: add tests for <module>`
- `chore: maintain <component>`
