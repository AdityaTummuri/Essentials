# Security Policy

## 1. Security Philosophy & Boundaries

Essentials is a developer toolkit designed to distribute AI agent skills, environment configurations, and project templates across multiple coding agents (OpenCode, Claude Code, Gemini CLI, Cursor, OpenAI Codex, Windsurf, GitHub Copilot).

Because agent skills provide system prompts and instructions to autonomous AI coding models, security integrity is a first-class requirement.

### Core Security Rules

1. **Passive Guidance by Default**: Skills in `skills/` are instructional markdown (`SKILL.md`). Some bundle scripts that run only when the agent is asked to use them. Every such skill is marked `safeForDefault: false` in `resources/resources.json` unless its scripts were audited as local-only. No skill starts background processes or makes network requests on install.
2. **Strict File Restrictions in Library**: The central skills library enforces strict checks. No skill directory may contain hidden configurations or executable hooks such as `settings.json`, `settings.local.json`, `hooks.json`, `.mcp.json`, or `.claude-plugin/`.
3. **Cryptographic Verification**: Every vendored `SKILL.md` is fingerprinted with SHA-256 in `resources/resources.json`. Any drift or tampering triggers validation failure during `./scripts/essentials validate`.
4. **Transparent, User-Controlled Installation**: Skills are distributed as plain directories. Developers copy only the skills they want into their agent's skills directory (e.g. `~/.agents/skills/` or `~/.claude/skills/`). There are no background installers, hidden daemon processes, or system modification scripts.
5. **Supply Chain Defense**: All third-party skills are audited, pinned to immutable commit hashes, and stripped of tracking scripts or upsell mechanisms.

---

## 2. Review Record & Approved Skills

A rigorous security audit of all candidate resources was performed. The repository maintains an explicit distinction between approved static guidance and held resources:

### Approved Collections in `skills/` (82 Total Skills)
- `skills/threejs/` (24 skills): Pure markdown instructions covering 3D WebGL, shaders, PBR materials, WebGPU, and performance.
- `skills/design/` (14 skills): Frontend design, UI/UX Pro Max design reasoning, motion principles, Apple design guidelines, and web design review. The `design` skill bundles image-generation scripts that call external APIs and is marked not safe by default (see the note below).
- `skills/engineering/` (25 skills): Code review, TDD, Git hygiene, API design, security and threat analysis, CI/CD hardening, planning and debugging workflows, MCP server and skill authoring, and reverse engineering with REA.
- `skills/python/` (5 skills): Modern Python 3.10+ typing, Pytest workflows, clean architecture, Asyncio, and pyproject.toml packaging.
- `skills/robotics-ml/` (7 skills): Computer vision, model evaluation, dataset curation, edge quantization, and ROS 2, ESP32, and PyTorch debugging.
- `skills/audio/` (1 skill): Web Audio API, spatial soundscapes, and audio visualizer shaders.
- `skills/product/` (2 skills): Executive product strategy, OKR cascades, and UI design systems.
- `skills/testing/` (4 skills): Automated visual regression testing, web app testing, Playwright test generation, and test-gap audits.

**Note on `design`.** Its logo, icon, and CIP generators call Gemini, AtlasCloud, or MuAPI with the user's keys, read `.env` files, and write downloads. Section 2 of this policy would hold resources like this. It is kept in the library and marked `safeForDefault: false` pending a decision.

### Held Resources (Excluded from Canonical Library)
The following resources contain executable code, subprocesses, or network calls and are **held** (not included in `skills/`):

| Resource | Findings & Risk Factors | Decision |
|---|---|---|
| **`oil-motion`** | Contains 41 Python and TypeScript scripts. Accesses OS keyring (`keyring`), spawns subprocesses (`ffmpeg`), makes outbound network calls to external video APIs, and spins up a local Node.js HTTP server (`credential-ui`). | **HELD & EXCLUDED**. Must not be distributed in clean library. |
| **`oil-frontend`** | Contains `scripts/recommend_once.py`, which touches `$XDG_STATE_HOME` to track display state and outputs promotional text for a paid skill. | **HELD & EXCLUDED**. Upsell tracking violates clean toolkit policy. |
| **`impeccable`** | Script fetches remote engine code via `curl`/`wget` at runtime. Self-fetches checksum without independent verification. Contains `hooks.json`. | **HELD**. Remote execution violates zero-remote-execution policy. |
| **`ui-styling`** | Contains scripts executing `npx` via subprocess, plus 5.8 MB of binary fonts. | **HELD**. Subprocess execution and binary bloat. |
| **`design-system`** | Contains `fetch-background.py` downloading images from external sources. | **HELD**. Unsolicited network access. |
| **`brand`** | Uses `child_process.execFileSync`. | **HELD**. Arbitrary process execution. |

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability, compromised upstream skill, or prompt injection vector in any resource:

1. **Do not open a public issue.**
2. Email the maintainer directly at: `adityatummuri@gmail.com`
3. Include:
   - Skill identifier and path (`skills/<category>/<skill-id>`).
   - Specific lines of code, network calls, or prompt injection vectors identified.
   - Steps to reproduce or verify.

Reports will be acknowledged within 48 hours, and compromised skills will be immediately revoked from the repository.
