# Contributing to Essentials

Thank you for contributing to Essentials! Our goal is to maintain a polished, maintainable, secure, and cross-agent developer toolkit.

Every addition must solve a real problem, have a clear purpose, and justify its maintenance cost.

---

## 1. Principles & Quality Bar

- **Zero Arbitrary Execution in Default Skills**: Default skills are instructional Markdown guides (`SKILL.md`). We do not accept skills that execute unsolicited background scripts, download runtime binaries, or tamper with user environments.
- **Reproducibility**: All vendored skills must be pinned to an immutable upstream commit hash and include upstream attribution.
- **Strict Licensing**: Vendored resources must have open, permissible licenses (e.g. MIT, Apache-2.0, BSD). Collections without explicit license files will be rejected.
- **Standard Library First**: Tooling in `scripts/` and `adapters/` relies exclusively on the Python standard library. Do not introduce heavy runtime pip dependencies for core features.

---

## 2. Adding a New Skill

### Step 1: Check Suitability
Before creating a PR, check whether the skill is already covered by existing resources (`./scripts/essentials list`). Compare it against the standards in `resources/docs/SECURITY-REVIEW.md`.

### Step 2: Place Vendored Files
Create a collection folder under `resources/skills/<category>/<collection>/<skill-id>/`:
```text
resources/skills/design/my-collection/
├── LICENSE                 # Upstream license
├── SOURCE.md                # Pinned repo, commit hash, date
└── my-skill/
    └── SKILL.md             # Canonical skill instructions
```

Ensure `SKILL.md` contains valid YAML frontmatter:
```markdown
---
name: my-skill
description: "Clear, concise explanation of when and how the agent should activate this skill."
---

# My Skill Content
```

### Step 3: Register in `resources/resources.json`
Add an entry to the `resources` array in `resources/resources.json`:
- `id`: Unique identifier (must match frontmatter `name`).
- `kind`: `"skill"`.
- `status`: `"vendored"`.
- `installable`: `true`.
- `category`: Category name.
- `collection`: Collection path.
- `path`: Path to skill directory relative to `resources/`.
- `source`: Upstream URL, commit hash, commit date.
- `license`: SPDX identifier.
- `securityReview`: Status (`"static-reviewed"`), date, and audit notes.
- `skillMd.sha256`: SHA-256 hash of `SKILL.md`.
- `supportedAgents`: `["claude-code", "gemini-cli", "codex", "cursor", "windsurf", "copilot"]`.
- `safeForDefault`: `true` (if static-reviewed).

### Step 4: Validate
Run the validation suite:
```bash
./scripts/essentials validate
```
This checks for hash drift, duplicate IDs, forbidden files (`settings.json`, `hooks.json`), and schema conformity.

---

## 3. Running Tests Locally

Run both test suites before submitting a pull request:
```bash
# Run multi-agent CLI test suite
python3 -m unittest discover -s tests -v

# Run resource library core test suite
python3 -m unittest discover -s resources/scripts/tests -v
```

All tests execute inside temporary directories and will never modify your real projects or home directory.

---

## 4. Commit Message Guidelines

We follow Conventional Commits:
- `feat: add <feature>`
- `fix: resolve <issue>`
- `docs: update <documentation>`
- `test: add tests for <module>`
- `chore: maintain <component>`
