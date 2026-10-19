# Changelog

All notable changes to the **Essentials** project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
