# Security Policy

## 1. Security Philosophy & Boundaries

Essentials is a developer toolkit designed to distribute AI agent skills, environment configurations, and project templates across multiple coding agents (Claude Code, Gemini CLI, Cursor, OpenAI Codex, Windsurf, GitHub Copilot).

Because agent skills provide system prompts and context to autonomous AI coding models, security integrity is a first-class requirement.

### Core Security Rules

1. **Passive Guidance by Default**: Canonical and installable skills in default profiles are strictly instructional markdown (`SKILL.md`). They do not execute background scripts, make unsolicited network requests, or tamper with system environments.
2. **Strict File Restrictions in Library**: The central resource library enforces strict checks. No skill directory may contain hidden configurations or executable hooks such as `settings.json`, `settings.local.json`, `hooks.json`, `.mcp.json`, or `.claude-plugin/`.
3. **Cryptographic Verification**: Every vendored `SKILL.md` is fingerprinted with SHA-256 in `resources/resources.json`. Any drift or tampering triggers validation failure during `essentials validate`.
4. **Project-Local & Non-Destructive**: Essentials installs only into project-scoped directories (e.g. `<project>/.claude/skills/`, `<project>/.cursor/rules/`, `<project>/.agents/skills/`). It **never** modifies global system settings or existing unmanaged files.
5. **Installation Ledger Integrity**: All installed files are recorded in an installation ledger (`.essentials-ledger.json` or `.resources-library.json`). The uninstaller verifies file hashes before removal and refuses to delete user-modified files.

---

## 2. Review Record & Held Resources

A full audit of all candidate resources was performed. The following resources have specific security classifications:

### Security Classification Tiers

- **Level 1 (Static Instructions Reviewed)**: Pure markdown instructions (`SKILL.md`). Zero runtime scripts, zero network access, zero hook execution. Completely safe for default project installations.
- **Level 2 (Offline Tooling Reviewed)**: Contains standalone local scripts for dataset validation or data lookup that never execute automatically during installation.
- **Level 3 (Runtime / Script Execution)**: Contains scripts that make network calls, spawn subprocesses, or access system keyrings. Strictly held and excluded from default profiles.

### Audited & Approved Collections for Default Profiles
- `threejs/cesartevisual-threejs-skills` (24 skills): Pure markdown instructions, no scripts or hooks.
- `motion/emil-design-eng` (8 skills): Pure markdown animation instructions.
- `motion/design-motion-principles`: Static reference guides.
- `frontend/frontend-design`: Static interface aesthetic guidelines.
- `design/design-md`: Static design system documentation templates.
- `design/ui-ux-pro-max`: Static UI reasoning catalogs and styling rules.
- `engineering/universal-dev-skills` (6 skills): Rigorous code review, TDD, Git hygiene, API design, security audit, CI/CD hardening.
- `robotics-ml/robotics-ml-toolkit` (4 skills): Computer vision, model evaluation, dataset curation, and edge quantization guidance.
- `audio/web-audio-toolkit` (1 skill): Web Audio API, spatial soundscapes, and audio visualizer shaders.
- `testing/visual-testing-toolkit` (1 skill): Automated visual regression testing and snapshot baselines.
- `product/product-management-toolkit` (2 skills): Executive product strategy, OKR cascades, and UI design systems.

### Held Resources (Excluded from Default Installation)
The following resources contain executable code, subprocesses, or network calls and are **held** (not installable in default profiles):

| Resource | Findings & Risk Factors | Decision |
|---|---|---|
| **`oil-motion`** | Contains 41 Python and TypeScript scripts. Accesses OS keyring (`keyring`), spawns subprocesses (`ffmpeg`), makes outbound network calls to MiniMax/video generation APIs, and spins up a local Node.js HTTP server (`credential-ui`). CI workflow uses `sudo`. | **HELD & EXCLUDED FROM DEFAULTS**. Must not be installed in project default profiles. Requires explicit manual opt-in and local review. |
| **`oil-frontend`** | Contains `scripts/recommend_once.py`, which touches `$XDG_STATE_HOME` to track display state and outputs promotional text for a paid skill. | **HELD FROM VENDORED DEFAULTS**. Script must be neutralized or removed before vendoring into clean libraries. |
| **`impeccable`** | Script fetches remote engine code via `curl`/`wget` at runtime. Self-fetches checksum without independent verification. Contains `hooks.json`. | **HELD**. Runtime remote execution violates Essentials zero-remote-execution policy. |
| **`ui-styling`** | Contains scripts executing `npx` via subprocess, plus 5.8 MB of binary fonts. | **HELD**. Subprocess execution and binary bloat. |
| **`design-system`** | Contains `fetch-background.py` downloading images from external sources. | **HELD**. Unsolicited network access. |
| **`brand`** | Uses `child_process.execFileSync`. | **HELD**. Arbitrary process execution. |

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability, compromised upstream skill, or malicious pattern in any resource:

1. **Do not open a public issue.**
2. Email the maintainer directly at: `adityatummuri@gmail.com`
3. Include:
   - Resource identifier (`id` in `resources.json`).
   - Upstream commit hash or source URL.
   - Specific lines of code, network calls, or prompt injection vectors identified.
   - Steps to reproduce or verify.

Reports will be acknowledged within 48 hours, and compromised skills will be immediately revoked from the manifest and held.

