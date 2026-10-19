# Architecture of Essentials

## 1. Universal Skill Architecture

The core objective of Essentials is to provide a single, curated, security-reviewed library of developer capabilities and AI agent skills that can be deployed across multiple distinct AI coding agents without duplicating files or maintaining conflicting copies.

```text
                                  ┌─────────────────────────────┐
                                  │   Canonical Skill Library   │
                                  │   (resources/skills/ &      │
                                  │    authoritative manifest)  │
                                  └──────────────┬──────────────┘
                                                 │
                                                 │ essentials CLI /
                                                 │ setup-project.sh
                                                 ▼
                                  ┌─────────────────────────────┐
                                  │    Multi-Agent Adapters     │
                                  │   (symlink / copy / rule)   │
                                  └──────────────┬──────────────┘
                    ┌────────────────────────────┼───────────────────────────┐
                    ▼                            ▼                           ▼
          ┌──────────────────┐         ┌──────────────────┐        ┌──────────────────┐
          │   Claude Code    │         │  OpenAI Codex &  │        │   Cursor / MDC   │
          │ (.claude/skills) │         │  Universal Agent │        │ (.cursor/rules/) │
          │                  │         │ (.agents/skills) │        │                  │
          └──────────────────┘         └──────────────────┘        └──────────────────┘
```

### The Problem with Fragmented Agent Formats
Different AI coding assistants expect instructions in different directory layouts and metadata formats:
- **Claude Code**: Looks inside `.claude/skills/<skill-id>/SKILL.md` (or `~/.claude/skills/`).
- **OpenAI Codex & Standard Agent Skills**: Look inside `.agents/skills/<skill-id>/SKILL.md` or `.codex/skills/`.
- **Gemini CLI / Antigravity**: Discovers skills directly in `.agents/skills/<skill-id>/SKILL.md`.
- **Cursor**: Evaluates MDC rule files in `.cursor/rules/<skill-id>.mdc` with frontmatter `globs`, `description`, `alwaysApply`.
- **Windsurf**: Reads markdown rules in `.windsurf/rules/<skill-id>.md` or `.windsurfrules`.
- **GitHub Copilot**: Reads instructions from `.github/copilot-instructions.md` or prompt files.

### The Essentials Solution: Canonical Source + Adapters
Instead of manually copy-pasting or maintaining 5 diverging copies of every skill, Essentials stores **one canonical representation** of each skill (conforming to the Agent Skills standard with YAML frontmatter `name` and `description`). 

When an installation target is selected:
1. For directory-compatible agents (**Claude Code**, **Gemini CLI**, **Codex**), Essentials links or copies the canonical directory into the agent's expected path.
2. For format-differentiated agents (**Cursor**, **Windsurf**, **Copilot**), Essentials adapters generate the exact wrapper needed (e.g., adding Cursor MDC frontmatter: `globs: *`, `alwaysApply: false`).
3. Every operation is recorded in a project-local ledger (`.essentials-ledger.json` or `.resources-library.json`), enabling deterministic, collision-free uninstalls.

---

## 2. Manifest & Verification Model

All resources in Essentials are cataloged in `resources/resources.json`.
The manifest tracks:
- **Canonical ID**: Unique identifier across the entire system.
- **Category & Kind**: e.g., `threejs`, `motion`, `design`, `frontend`.
- **Status**: `vendored`, `held`, `not-vendored`, `app-dependency`.
- **Upstream Source**: Repository URL, pinned commit hash, and commit date.
- **License**: SPDX license identifier (e.g. `MIT`, `Apache-2.0`).
- **Security Review**: Review status (`static-reviewed`, `needs-review`), review date, audit notes.
- **Integrity Hashes**: SHA-256 hash of `SKILL.md` and whole-directory tree hash.
- **Agent Compatibility**: Supported agents and discovery paths.
- **Default Profile Safety**: Boolean indicating whether the skill is safe for unprompted default installation.

### Forbidden Artifacts Policy
To prevent supply-chain poisoning, the validator enforces that no vendored resource may include:
- `settings.json` or `settings.local.json`
- `hooks.json` (arbitrary command execution hooks)
- `.mcp.json` (unreviewed MCP server declarations)
- `plugin.json`
- Symlinks pointing outside the vendored directory

---

## 3. Installation Ledger Mechanics

When Essentials installs skills into a project:
1. **Safety Check**: Checks if the target path already exists. If an unmanaged file or directory is present, the transaction aborts with a clear conflict report before modifying anything.
2. **Ledger Record**: Writes metadata to `<project>/.essentials-ledger.json` (or `.claude/.resources-library.json` for Claude Code):
   ```json
   {
     "agent": "cursor",
     "mode": "copy",
     "source": "/path/to/resources/skills/...",
     "sha256": "6723003681...",
     "installedAt": "2026-10-20T00:00:00Z"
   }
   ```
3. **Safe Uninstall**: When uninstalling, Essentials verifies that:
   - For symlinks: the symlink still points to the Essentials source.
   - For copies: the file contents have not been modified by the developer since installation.
   - If a developer edited an installed skill, **Essentials refuses to delete it**, protecting user work.

---

## 4. Single Source of Truth & Synchronization

The repository maintains an explicit hierarchy between canonical sources and active mirrors:

1. **`resources/skills/` is Canonical**:
   All 51 reviewed skills reside under `resources/skills/`. This directory is strictly auditable: every collection contains an explicit `LICENSE` and `SOURCE.md`, and every `SKILL.md` is cryptographically hashed in `resources/resources.json`.
2. **`.agents/skills/` is a Synchronized Workspace Mirror**:
   For local agent tools (like Antigravity or Gemini CLI) operating directly inside the Essentials workspace, `.agents/skills/` provides the active toolset. Running `./scripts/essentials sync` verifies and synchronizes skills from the canonical library into any target project or workspace.
3. **Duplicate Resolution**:
   Duplicate sets (such as overlapping Three.js skills from older third-party dumps) are strictly resolved in favor of the canonical set (`cesartevisual-threejs-skills`), ensuring predictable precedence and deterministic discovery.

---

## 5. CLI Architecture & Operations

The Essentials CLI (`./scripts/essentials`) is implemented exclusively in the Python standard library with zero runtime pip dependencies.

### Command Execution Model:
- **`list`**: Scans the authoritative manifest and displays skills by category, presets, and supported agents.
- **`search <query>`**: Full-text keyword search across skill IDs, descriptions, categories, and use cases.
- **`inspect <skill-id>`**: Deep provenance viewer showing upstream commit, license, security review notes, and discovery paths.
- **`validate`**: Cryptographic hash integrity checker, forbidden file blocker, and schema validator.
- **`install <preset|skills>`**: Multi-agent installer with dry-run preview, conflict detection, and ledger recording.
- **`sync`**: Reconciles target project installations against the canonical library, updating unchanged skills while protecting local modifications.
- **`status`**: Audits project ledger integrity and flags missing or tampered files.
- **`uninstall`**: Safe atomic uninstaller protecting developer customizations.


