# Essentials

**A Universal AI Developer Toolkit & Cross-Agent Resource Library.**

Essentials provides a curated, security-reviewed, canonical collection of AI agent skills, environment configurations, and project templates that install cleanly across **Claude Code**, **Cursor**, **Gemini CLI / Antigravity**, **OpenAI Codex**, **Windsurf**, and **GitHub Copilot**.

---

## 1. Overview & Purpose

### What is Essentials?
Essentials is a modular toolkit designed to give developers and their AI coding agents consistent, high-leverage capabilities across different IDEs, terminals, and workflows.

Instead of hunting for prompts, manually copying `.cursorrules` or `.claude/skills` across dozens of projects, or trusting unreviewed scripts from the internet, Essentials gives you:
- **Canonical Skill Library**: 51 curated, security-reviewed skills spanning 3D WebGL (Three.js), UI/UX art direction, motion principles, software craftsmanship, robotics/ML, browser audio, and data dashboards.
- **Universal Multi-Agent Adapters**: Write a skill once; deploy it natively to Claude Code, Cursor MDC rules, Gemini CLI, Codex, Windsurf, or Copilot.
- **Safe Installation & Sync Engine**: Project-local, non-destructive CLI with dry-run previews, synchronization, conflict protection, and an installation ledger that protects user edits.
- **Developer Environment Configurations**: Modular, opt-in configurations for Git, Bash, Zsh, and EditorConfig.
- **Production Starters**: Clean baselines for modern Python, interactive 3D portfolios, and metric dashboards.

### Who is it for?
- **Full-Stack & Frontend Engineers** building high-craft web apps, creative portfolios, and data dashboards.
- **Robotics & ML Practitioners** implementing real-time computer vision, model validation, and edge quantization.
- **AI-Native Developers** working across multiple AI coding agents who need consistent instructions and tools.
- **Engineering Teams** seeking safe, auditable agent skills without remote script execution or prompt injection risks.

---

## 2. Supported Agents & Environments

Essentials separates **Native Verified** integration from **Adapter-Mediated** compatibility:

| Agent / Tool | Target Location | Format | Integration |
|---|---|---|---|
| **Claude Code** | `<project>/.claude/skills/<id>/` | Canonical `SKILL.md` | Native Verified |
| **Gemini CLI / Antigravity** | `<project>/.agents/skills/<id>/` | Canonical `SKILL.md` | Native Verified |
| **OpenAI Codex** | `<project>/.agents/skills/<id>/` | Canonical `SKILL.md` | Native Verified (Agent Skills spec) |
| **Cursor IDE** | `<project>/.cursor/rules/<id>.mdc` | Cursor MDC (`globs`, `alwaysApply`) | Verified via Adapter |
| **Windsurf** | `<project>/.windsurf/rules/<id>.md` | Markdown Cascade Rule | Verified via Adapter |
| **GitHub Copilot** | `<project>/.github/prompts/<id>.prompt.md` | Copilot Prompts / Instructions | Compatible via Adapter |

> See [docs/AGENT_COMPATIBILITY.md](docs/AGENT_COMPATIBILITY.md) for detailed platform notes and verification details.

---

## 3. Quickstart

Essentials requires **Python 3.10+** and standard command-line tools. Zero third-party `pip` packages are required for core operations.

```bash
# 1. Clone the repository
git clone https://github.com/AdityaTummuri/Essentials.git
cd Essentials

# 2. Browse available skills, presets, and supported agents
./scripts/essentials list

# 3. Search for specific skills by keyword
./scripts/essentials search vision

# 4. Inspect skill provenance, security status, and license
./scripts/essentials inspect computer-vision

# 5. Validate library integrity and cryptographic hashes
./scripts/essentials validate

# 6. Preview installing a curated profile into your project (dry run)
./scripts/essentials install portfolio --target ~/projects/my-portfolio --dry-run

# 7. Install for your preferred agent (e.g., Cursor)
./scripts/essentials install portfolio --target ~/projects/my-portfolio --agent cursor --yes
```

---

## 4. Browsing, Installing & Synchronizing Skills

### Presets
Essentials provides 6 curated bundles designed for specific project archetypes:

- **`portfolio`** (31 skills): High-end creative web engineering — Three.js scenes, PBR materials, shaders, postprocessing, animation budgeting, Web Audio API, and visual design systems.
- **`dashboard`** (6 skills): Data-dense internal tools and analytics platforms — UI reasoning, typography, responsive grids, and restrained motion.
- **`python-dev`** (5 skills): Modern Python development — test-driven development, code review protocols, Git hygiene, API design, and security review.
- **`engineering`** (6 skills): Software craftsmanship — TDD, code review, atomic Git commits, REST/RPC API schemas, security audits, and hardened CI/CD.
- **`robotics-ml`** (4 skills): Robotics, computer vision, data leakage prevention, dataset curation, and edge ONNX/TensorRT quantization.
- **`full-stack`** (10 skills): Comprehensive full-stack engineering, design systems, visual regression testing, and architecture.

### Targeted CLI Commands

```bash
# Search available skills across categories
./scripts/essentials search "audio"
./scripts/essentials search "testing" --category testing

# Inspect provenance and license of any skill or preset
./scripts/essentials inspect browser-audio
./scripts/essentials inspect robotics-ml

# Install a curated profile into a project
./scripts/essentials install dashboard --target ~/projects/analytics-ui

# Install for a specific agent (e.g. Cursor, Claude, Codex, Gemini, Windsurf, Copilot)
./scripts/essentials install robotics-ml --target ~/projects/robot-vision --agent cursor

# Install specific individual skills
./scripts/essentials install --skills code-review,api-design --target ~/projects/api-service --agent claude

# Choose symlink (default for local development) or copy mode (for shared repos)
./scripts/essentials install portfolio --target ~/projects/showcase --mode copy --yes

# Synchronize installed project skills with canonical updates
./scripts/essentials sync --target ~/projects/my-portfolio

# Inspect installation status and file integrity in a project
./scripts/essentials status --target ~/projects/my-portfolio

# Safely uninstall skills managed by Essentials (preserves user-edited files)
./scripts/essentials uninstall --target ~/projects/my-portfolio --yes
```

---

## 5. Developer Environment Configurations

Essentials includes modular, non-destructive configurations under `configs/`:

- **EditorConfig** (`configs/editor/.editorconfig`): Universal whitespace, newline, and indentation rules.
- **Git Defaults** (`configs/git/.gitconfig.template`): Safe Git settings (`pull.rebase = true`, `push.autoSetupRemote = true`, conflict markers).
- **Git Ignore** (`configs/git/.gitignore.template`): Multi-language ignore rules (Python, Node, Rust, OS junk, secrets).
- **Shell Helpers** (`configs/shell/`): Clean aliases and navigation shortcuts for Bash and Zsh.

> All configurations are opt-in. Essentials will **never** overwrite your home directory dotfiles automatically. See [configs/README.md](configs/README.md).

---

## 6. Project Starter Templates

Clean, production-ready baselines are available under `templates/`:

- **Python Baseline** (`templates/python`): Python 3.10+, `pyproject.toml`, `pytest`, `ruff`.
- **Creative Portfolio** (`templates/portfolio`): Vite + Three.js starter with camera framing, responsive canvas, and basic animation loop.
- **Data Dashboard** (`templates/dashboard`): Semantic CSS dashboard starter with responsive grid metric cards.

---

## 7. Safety, Verification & Ledger

Essentials takes security seriously:

1. **Passive Guidance by Default**: All default skills are instructional Markdown (`SKILL.md`). They execute zero background scripts, make no unsolicited network requests, and cannot tamper with system environments.
2. **Cryptographic Fingerprinting**: Every vendored `SKILL.md` is fingerprinted with SHA-256 in `resources/resources.json`. Tampering triggers validation failure.
3. **No Supply-Chain Hooks**: Vendored skills are forbidden from including `settings.json`, `hooks.json`, or `.mcp.json`.
4. **Non-Destructive Uninstall**: An installation ledger (`.essentials-ledger.json`) tracks managed files. If a developer edits an installed file, **Essentials will refuse to delete it** during uninstallation.
5. **Audited Held Resources**: Complex tools with active scripts or credential management (such as `oil-motion`) are strictly audited and held outside default profiles.

> Read the complete security policy in [SECURITY.md](SECURITY.md) and review records in [resources/docs/SECURITY-REVIEW.md](resources/docs/SECURITY-REVIEW.md).

---

## 8. Repository Structure

```text
Essentials/
├── .agents/                     # Canonical agent skills and lockfile
├── resources/                   # Central audited resource library
│   ├── skills/                  # Vendored skills (design, motion, threejs, engineering)
│   ├── docs/                    # Security audit records and held decisions
│   ├── catalogues/              # Source lists and alternatives comparisons
│   ├── scripts/                 # Core engine and library validation
│   └── resources.json           # Authoritative manifest
├── adapters/                    # Multi-agent adapters (Claude, Cursor, Gemini, Codex, Windsurf, Copilot)
├── configs/                     # Modular developer environment configs (Git, shell, editor)
├── templates/                   # Clean starter templates (Python, portfolio, dashboard)
├── scripts/
│   ├── essentials               # Unified CLI executable
│   └── essentials_cli.py        # CLI engine (pure Python stdlib)
├── tests/                       # End-to-end integration test suite
├── docs/                        # Architecture, agent matrix, and profile guides
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contributor onboarding
├── SECURITY.md                  # Security policy and audit findings
└── LICENSE                      # MIT License
```

---

## 9. Contributing & License

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting skills, adapters, or templates.

- **Essentials Core**: Licensed under the [MIT License](LICENSE).
- **Vendored Skills**: Retain their respective upstream licenses (predominantly MIT and Apache-2.0), documented in `resources/resources.json` and each collection's `LICENSE` file.
