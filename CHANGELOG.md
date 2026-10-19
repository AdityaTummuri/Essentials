# Changelog

All notable changes to the **Essentials** project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-10-20

### Changed
- **"Skills Are Just Folders" Architecture**: Fundamentally simplified the skill distribution model. Removed all custom Python runtime installers, symlink daemons, installation ledgers, and format adapters. Users now simply copy skill folders directly into `~/.agents/skills/` (for OpenCode, VS Code Copilot, Gemini CLI, Cursor, Windsurf, Codex) or `~/.claude/skills/` (for Claude Code).
- **Top-Level `skills/` Directory**: Reorganized the entire canonical skill collection into a top-level `skills/` directory structured across 8 intuitive categories:
  - `skills/threejs/` (24 skills)
  - `skills/engineering/` (6 skills)
  - `skills/design/` (13 skills)
  - `skills/robotics-ml/` (4 skills)
  - `skills/python/` (5 skills)
  - `skills/audio/` (1 skill)
  - `skills/product/` (2 skills)
  - `skills/testing/` (1 skill)
- **Refactored CLI (`scripts/essentials`)**: Streamlined the CLI into a zero-dependency, pure standard library browsing and validation companion supporting:
  - `list`: Browse all 56 skills across 8 categories and curated profiles.
  - `search <query>`: Case-insensitive keyword search across skill names, categories, and descriptions.
  - `inspect <id|preset>`: Detailed view displaying metadata, YAML frontmatter, file trees, and ready-to-paste copy commands.
  - `validate`: Static integrity verifier checking YAML frontmatter, uniqueness, and absence of forbidden files.
- **Authoritative Manifest Updated**: Updated `resources/resources.json` to point all 56 skills directly to `skills/<category>/<skill-id>`.

### Added
- **5 New Modern Python Engineering Skills (`skills/python/`)**:
  - `pytest-workflow`: Robust pytest testing workflows, fixtures, parametrization, and coverage integration.
  - `python-patterns`: Clean architecture patterns, dependency injection, and idiomatic Pythonic design.
  - `type-hints-modern`: Python 3.10+ typing (`X | Y`, ParamSpec, TypeVarTuple, Self, Protocol).
  - `asyncio-patterns`: Modern Asyncio concurrency with `asyncio.TaskGroup` and cancellation semantics.
  - `packaging-pyproject`: Modern PEP 517/621 packaging with `pyproject.toml`, hatchling/flit, and pre-commit hooks.
- **Dedicated Test Suite (`tests/test_skills.py`)**: 9 automated unit and workflow tests verifying:
  - Category structure and license files.
  - Frontmatter validity and 100% unique skill names across all 56 skills.
  - Manual folder copying workflow in temporary isolation.
  - CLI `list`, `search`, `inspect`, and `validate` commands.

### Removed
- **Custom Installer & Symlink Machinery**: Deleted `scripts/global_manager.py`, `resources/scripts/setup-project.sh`, `resources/scripts/library.py`, and all 9 translation adapters in `adapters/`.
- **Legacy Duplication**: Deleted `resources/skills/` and removed tracked `.agents/` workspace copies, leaving top-level `skills/` as the single authoritative source of truth.

---

## [2.2.0] - 2026-10-20

### Added
- **System-Wide Personal Skill Management**:
  - Unified personal skill library on Linux shared across **OpenCode**, **Claude Code**, and **VS Code with GitHub Copilot**.
  - Symlink-first propagation ensures edits in canonical `resources/skills/` reflect in real-time across all three environments with zero manual file duplication.
- **New CLI Commands**:
  - `setup-global`: Installs selected presets or skills globally with `--strategy shared` (default: `~/.claude/skills` + `~/.agents/skills`), `--strategy dedicated`, or `--strategy all`. Supports `--dry-run`.
  - `global-status`: Audits system-wide installations, checks health of symlinks/copies, and reports unmanaged user skills.
  - `global-sync`: Synchronizes globally installed skills with canonical updates and automatically repairs broken symlinks.
  - `global-uninstall`: Safely uninstalls Essentials-managed global skills while guaranteeing unmanaged user skills and user-modified copies are untouched.
- **Dedicated Global Installation Ledger**: Tracks system-wide installations at `~/.config/essentials/global-ledger.json` (or `$XDG_CONFIG_HOME/essentials/global-ledger.json`), maintaining strict separation from project-level installations.
- **OpenCode Adapter (`adapters/opencode.py`)**: Added dedicated OpenCode adapter supporting both the universal Agent Skills standard (`.agents/skills/`) and OpenCode's dedicated config path (`.config/opencode/skills/`).
- **Global Integration Test Suite (`tests/test_global_manager.py`)**: 10 comprehensive tests covering dry-run safety, path resolution, YAML frontmatter compliance, multi-agent integrations, unmanaged user skill preservation, name collision prevention, link repair, and corrupted ledger recovery.

---

## [2.1.0] - 2026-10-20

### Added
- **Single Source of Truth Architecture**: Established `resources/skills/` as canonical reviewed source library and `.agents/skills/` as active synchronized workspace mirror.
- **11 New Curated Skills (51 Total)**:
  - Robotics & ML (`robotics-ml/`): `computer-vision`, `model-evaluation`, `dataset-curation`, `edge-inference`.
  - Web Audio (`audio/`): `browser-audio` (AudioContext lifecycle, HRTF spatial audio, WebGL visualizers).
  - Visual Testing (`testing/`): `visual-regression` (automated Playwright/pixelmatch snapshots).
  - Software Craftsmanship (`engineering/`): `api-design`, `security-audit`, `ci-cd-workflow`.
  - Product Strategy (`product/`): `product-strategist`, `ui-design-system`.
- **New Presets**: Added `robotics-ml` (4 skills), `engineering` (6 skills), and `full-stack` (10 skills). Expanded `portfolio` to 31 skills with `browser-audio`.
- **Enhanced CLI Subcommands (`scripts/essentials`)**:
  - `search`: Keyword and category search across skill metadata.
  - `inspect`: Detailed provenance, license, security review, and agent discovery viewer.
  - `sync`: Project-wide skill synchronization reconciling local installations with canonical library updates while protecting user customizations.
- **Extended Test Suite**: Added 5 new integration tests covering `search`, `inspect`, `sync`, paths containing spaces, and corrupted ledger recovery (35 total tests passing across test suites).
- **Upstream Maintenance Audit (`docs/UPSTREAM_AUDIT.md`)**: Complete provenance and audit record tracking commit pins, licenses, and review decisions for all cataloged skills.

---

## [2.0.0] - 2026-10-20

### Added
- **Universal Multi-Agent Architecture**: Established canonical skill storage with adapter generation for Claude Code, Gemini CLI / Antigravity, OpenAI Codex, Cursor, Windsurf, and GitHub Copilot.
- **Unified CLI Engine (`scripts/essentials`)**: Pure Python stdlib CLI for cross-agent installation, validation, dry-run previews, installation ledger tracking, and atomic uninstalls.
- **Agent Adapters (`adapters/`)**: Adapters for translating canonical `SKILL.md` into agent-specific formats, including Cursor MDC rules (`.cursor/rules/*.mdc`) and Windsurf rules.
- **Comprehensive Documentation**:
  - `docs/ARCHITECTURE.md`: Technical breakdown of canonical skill flow, ledger mechanics, and integrity verification.
  - `docs/AGENT_COMPATIBILITY.md`: Verified vs adapter-mediated support matrix across 6 AI agents.
  - `docs/PROFILES.md`: Detailed breakdown of `portfolio`, `dashboard`, and `python-dev` profiles.
  - `SECURITY.md`: Security policies, verification checks, and detailed findings on held resources.
  - `CONTRIBUTING.md`: Guidelines for skill vetting, contribution, and test verification.
  - Root `LICENSE`: Standard MIT license for Essentials with clear upstream attribution.
- **Developer Environment Configurations (`configs/`)**: Safe, non-destructive configurations for Bash, Zsh, Git, and EditorConfig.
- **Modern Project Starters (`templates/`)**: Production-ready starters for Python (`templates/python/`), Creative Web, and Data Dashboards.
- **Automated CI Workflow**: GitHub Actions workflow (`.github/workflows/test.yml`) running manifest validation, ledger tests, and cross-agent installation tests.

### Changed
- **Tracked Central Resource Library**: Staged and tracked the complete `resources/` library containing 37 vendored skills, manifest, and test suite.
- **Security Audit on `oil-motion` & `oil-frontend`**: Documented risks associated with `oil-motion` (local Node server, keyring access, ffmpeg subprocesses) and `oil-frontend` (marketing state script); strictly classified them as held/opt-in and excluded them from default installation profiles.
- **Migrated Python Baseline**: Elevated legacy root Python files (`main.py`, `requirements.txt`) into a clean, modern template under `templates/python/`.

### Removed
- **Static Binaries Cleanup**: Safely removed 30.6 MB of static Linux x86-64 binaries (`curl`, `git`, `git-receive-pack`, `git-shell`, `git-upload-pack`) from the repository root, preserving commit history while keeping checkouts lightweight and cross-platform.

---

## [1.1.0] - 2026-10-20

### Added
- Agent skills collection under `.agents/skills/` with `.skill-lock.json`.

---

## [1.0.1] - 2026-09-01

### Added
- Precompiled static Git and curl binary executables in root.

---

## [1.0.0] - 2026-09-01

### Added
- Initial scaffold: bare-minimum Python template with `.gitignore`, `main.py`, and `requirements.txt`.

