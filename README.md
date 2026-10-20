# Essentials

**The Universal, All-in-One AI Developer Toolkit & Portable Skills Library.**

Essentials is a curated collection of **ready-to-use AI agent skills**, developer environment configurations, and production-ready project templates.

Designed for developers working across **OpenCode**, **Claude Code**, **VS Code with GitHub Copilot**, **Cursor**, **Windsurf**, and **Gemini CLI / Antigravity**.

---

## 1. Philosophy: Skills Are Just Folders

You should never need a custom Python program, installer, symlink manager, manifest-processing tool, or special setup procedure just to use AI skills.

In Essentials, **every skill is an ordinary, self-contained directory** containing a standard `SKILL.md` (with YAML frontmatter `name` and `description`) and any required reference docs or templates.

### The 30-Second Workflow

```bash
# 1. Clone or download Essentials
git clone https://github.com/AdityaTummuri/Essentials.git
cd Essentials

# 2. Browse skills/ and copy what you need into your agent's skills directory
mkdir -p ~/.agents/skills
cp -r skills/engineering/code-review ~/.agents/skills/

# 3. Refresh or restart your agent — the skill is instantly active!
```

> **Prefer ZIP downloads?** You don't even need Git. Click **Code → Download ZIP** on GitHub, unzip it, copy the skill folders you want into `~/.agents/skills/`, and delete the download when finished.

---

## 2. What Essentials Contains

Essentials is a complete developer toolkit, not just a skills library:

```text
Essentials/
├── skills/                      # 82 portable, self-contained Agent Skills across 8 categories
│   ├── audio/                   # Web Audio API soundscapes, spatial 3D audio, WebGL visualizers
│   ├── design/                  # UI/UX Pro Max, DESIGN.md, Apple design language, motion principles
│   ├── engineering/             # Code review, Git hygiene, TDD, REST/RPC API design, security, CI/CD
│   ├── product/                 # Product strategy, OKR cascades, UI design systems
│   ├── python/                  # Pytest testing, modern patterns, static typing, Asyncio, pyproject
│   ├── robotics-ml/             # Computer vision, dataset curation, model evaluation, edge inference
│   ├── testing/                 # Visual regression testing, Playwright & pixel-diff snapshots
│   └── threejs/                 # Complete 3D suite: scenes, PBR materials, shaders, postprocessing
├── configs/                     # Modular, non-destructive developer environment configurations
│   ├── editor/                  # Universal EditorConfig (.editorconfig)
│   ├── git/                     # Safe Git settings (.gitconfig.template, .gitignore.template)
│   └── shell/                   # Productive Bash and Zsh aliases and navigation helpers
├── templates/                   # Clean, production-ready project starter baselines
│   ├── python/                  # Python 3.10+, pyproject.toml, pytest, ruff baseline
│   ├── portfolio/               # Vite + Three.js creative portfolio starter
│   └── dashboard/               # Semantic CSS data dashboard with responsive metric cards
├── docs/                        # Architecture guides, agent compatibility, and security audits
├── scripts/                     # Optional lightweight terminal companion (list, search, inspect)
├── tests/                       # Automated validation test suite
├── README.md                    # This guide
├── CONTRIBUTING.md              # Guidelines for contributing new skills or templates
├── SECURITY.md                  # Security policies and audit findings
├── CHANGELOG.md                 # Version and release history
└── LICENSE                      # MIT License
```

---

## 3. Supported Agents & Discovery Paths

Essentials adheres strictly to the open **Agent Skills** specification (`SKILL.md` with YAML frontmatter). Different AI coding agents discover personal skills from specific user directories on Linux/macOS:

| Tool | Recommended Personal Skills Directory | Format & Notes |
| :--- | :--- | :--- |
| **OpenCode** | `~/.agents/skills/<skill-name>/` | Native Agent Skills standard. Also scans `~/.config/opencode/skills/`. |
| **VS Code Copilot** | `~/.agents/skills/<skill-name>/` | Native personal Agent Skills (GitHub Copilot Chat). Also scans `~/.copilot/skills/`. |
| **Claude Code** | `~/.claude/skills/<skill-name>/` | Native personal skills directory for Claude Code. |
| **Gemini CLI / Antigravity** | `~/.agents/skills/<skill-name>/` | Native Agent Skills standard in personal or workspace scope. |
| **OpenAI Codex** | `~/.agents/skills/<skill-name>/` | Standard Agent Skills open convention. |
| **Cursor / Windsurf** | `<project>/.agents/skills/<skill-name>/` | Workspace-level discovery under the Agent Skills standard. |

### Copying to Multiple Agents

- **OpenCode & VS Code with GitHub Copilot** share `~/.agents/skills/`. Copying a skill there powers both tools simultaneously with zero duplicate files.
- **Claude Code** looks in `~/.claude/skills/`. Copy skills there, or create a symlink:
  ```bash
  mkdir -p ~/.claude
  ln -s ~/.agents/skills ~/.claude/skills
  ```

---

## 4. Skills Catalog by Category

Essentials includes **82 portable skills** organized into 8 domain directories. The complete list with licences, upstream sources, and bundled-code flags is in [docs/SKILL_CATALOG.md](docs/SKILL_CATALOG.md).

### 🛠️ Engineering (`skills/engineering/`)
- **`code-review`**: Structured, rigorous code reviews for correctness, performance, edge cases, and maintainability.
- **`git-hygiene`**: Atomic commits, conventional commit formatting, clean branch topology, and safe rebasing.
- **`test-driven-development`**: Red-Green-Refactor workflows, test boundary design, and mocking discipline.
- **`api-design`**: Clean, scalable, backward-compatible REST and RPC API schemas with error envelopes.
- **`security-audit`**: OWASP Top 10 vulnerability checks, dependency supply-chain auditing, and secret scanning.
- **`ci-cd-workflow`**: Hardened, reproducible GitHub Actions workflows with caching and security gates.
- **`writing-plans`**, **`brainstorming`**, **`executing-plans`**, **`subagent-driven-development`**: Requirements clarification, implementation plans, and plan execution (Superpowers).
- **`systematic-debugging`**, **`verification-before-completion`**, **`requesting-code-review`**, **`receiving-code-review`**: Root-cause debugging and review workflows (Superpowers).
- **`acquire-codebase-knowledge`**: Maps an unfamiliar codebase into architecture and convention documents.
- **`threat-model-analyst`**, **`secret-scanning`**, **`github-actions-hardening`**, **`dependabot`**: Threat modelling, secrets detection, Actions security review, and dependency updates.
- **`refactor`**: Behaviour-preserving refactoring for maintainability.
- **`mcp-builder`**, **`skill-creator`**: Building MCP servers and authoring or evaluating skills.
- **`reverse-engineer-anything`**: Binary, package, and runtime analysis with REA evidence tools (rea-agents, MIT).
- **`ollama-local-models`**: Sizing, running, and benchmarking local Ollama models.
- **`caveman`**: Terse response style. Lightweight skill only; copy it when you want that style.

### 🐍 Python Development (`skills/python/`)
- **`pytest-workflow`**: Deterministic unit and integration testing, fixtures, parametrization, and coverage.
- **`python-patterns`**: Modern Python 3.10+ dataclasses, protocols, structural pattern matching, and exceptions.
- **`type-hints-modern`**: Static type annotations, `TypeAlias`, `Self`, `ParamSpec`, and strict Mypy verification.
- **`asyncio-patterns`**: Structured concurrency with `TaskGroup`, deterministic timeouts, and semaphore throttling.
- **`packaging-pyproject`**: Standards-compliant PEP 517/518/621 packaging with `pyproject.toml` and build hooks.

### 🎨 Design & Motion (`skills/design/`)
- **`frontend-design`**: Distinctive, intentional UI design principles avoiding generic AI boilerplate.
- **`ui-ux-pro-max`**: Design intelligence for responsive web layouts, color palettes, and component hierarchy.
- **`design`**: Comprehensive design tokens, typography scales, spacing units, and brand styling.
- **`design-md`**: Authoring single-document design specifications capturing design tokens and system architecture.
- **`apple-design`**: Fluid, physical motion curves, spatial hierarchy, and refined Apple HIG aesthetics.
- **`emil-design-eng`**: Emil Kowalski's philosophy on interaction polish, physics-based springs, and feedback.
- **`animate`**: Crafting purposeful, natural animations ordered by cognitive hierarchy.
- **`animation-performance`**: Keeping animations inside the 60/120fps budget via composite-only transforms.
- **`review-animations`**: High-bar auditing of animation code against frame budgets and ease curves.
- **`design-motion-principles`**: Motion recipes, accessibility guards (`prefers-reduced-motion`), and choreography.
- **`animation-vocabulary`**: Reverse-lookup glossary translating visual motion concepts into code.
- **`find-animation-opportunities`**: Pinpointing micro-interactions that elevate UI feel without distraction.
- **`improve-animations`**: Upgrading existing clunky transitions into smooth, spring-driven interactions.
- **`web-design-reviewer`**: Visually inspects a running site, finds layout, accessibility, and consistency problems, and fixes them.

### 🌐 Three.js & WebGL (`skills/threejs/`)
A complete 24-skill suite covering every facet of modern 3D web graphics:
- **`threejs-scene`**, **`threejs-materials`**, **`threejs-lighting`**, **`threejs-shaders`**
- **`threejs-postprocessing`**, **`threejs-animation`**, **`threejs-geometry`**, **`threejs-particles`**
- **`threejs-audio`**, **`threejs-interaction`**, **`threejs-performance`**, **`threejs-accessibility`**
- **`threejs-html`**, **`threejs-r3f`**, **`threejs-web`**, **`threejs-product-viewer`**
- **`threejs-assets`**, **`threejs-debugging`**, **`threejs-testing`**, **`threejs-deployment`**
- **`threejs-webgpu`**, **`threejs-physics`**, **`threejs-xr`**, **`threejs-spatial-data`**

### 🤖 Robotics & Machine Learning (`skills/robotics-ml/`)
- **`computer-vision`**: Real-time OpenCV pipelines, camera calibration, feature extraction, and optical flow.
- **`model-evaluation`**: Rigorous validation metrics, leakage prevention, and calibration curves.
- **`dataset-curation`**: Data validation, stratified sampling, split integrity, and dataset versioning.
- **`edge-inference`**: ONNX Runtime, TensorRT quantization, pruning, and low-latency edge deployment.
- **`ros2-debugging`**: ROS 2 discovery, topic and QoS mismatches, launch and colcon failures (original).
- **`esp32-embedded-debugging`**: ESP32 boot loops, brownouts, watchdog resets, serial and flashing problems (original).
- **`pytorch-experiments`**: Reproducible training, leakage-safe splits, GPU benchmarking, and ONNX export verification (original).

### 🔊 Browser Audio (`skills/audio/`)
- **`browser-audio`**: Interactive Web Audio API soundscapes, HRTF spatial audio, user-gesture unlock lifecycles, and audio-reactive WebGL visualizers.

### 📐 Product Strategy (`skills/product/`)
- **`product-strategist`**: OKR cascade generation, product vision formulation, and competitive roadmaps.
- **`ui-design-system`**: Design token generation, component documentation, and developer handoff specs.

### 🧪 Visual Testing (`skills/testing/`)
- **`visual-regression`**: Automated visual regression testing, pixel-diff snapshots with Playwright, and thresholding.
- **`webapp-testing`**: Native Playwright Python scripts for local web apps: server lifecycle, element discovery, console logs.
- **`playwright-generate-test`**: Generates a Playwright test from a scenario using the Playwright MCP tools.
- **`test-gap-audit`**: Read-only audit of missing, weak, or stale test coverage.

---

## 5. Curated Presets (Copy Shortcuts)

If you are setting up an environment for a specific project type, use these recommended skill combinations:

### Portfolio / Creative Web
```bash
mkdir -p ~/.agents/skills
cp -r skills/threejs/* ~/.agents/skills/
cp -r skills/design/frontend-design skills/design/ui-ux-pro-max skills/design/apple-design ~/.agents/skills/
cp -r skills/audio/browser-audio ~/.agents/skills/
```

### Full-Stack & Engineering
```bash
mkdir -p ~/.agents/skills
cp -r skills/engineering/* ~/.agents/skills/
cp -r skills/python/* ~/.agents/skills/
cp -r skills/testing/visual-regression ~/.agents/skills/
```

### Data Dashboard
```bash
mkdir -p ~/.agents/skills
cp -r skills/design/frontend-design skills/design/ui-ux-pro-max skills/design/design-md ~/.agents/skills/
cp -r skills/design/animation-performance skills/design/review-animations ~/.agents/skills/
```

### Robotics & ML
```bash
mkdir -p ~/.agents/skills
cp -r skills/robotics-ml/* ~/.agents/skills/
cp -r skills/engineering/code-review skills/engineering/test-driven-development ~/.agents/skills/
```

---

## 6. Managing Copied Skills

### How to Update a Skill
When Essentials receives updates, simply copy the updated skill directory over the old one:
```bash
cp -r skills/engineering/code-review ~/.agents/skills/
```

### How to Remove a Skill
Because skills are ordinary folders, removing a skill is completely safe and standard:
```bash
rm -rf ~/.agents/skills/code-review
```
It leaves no hidden registry entries, dangling symlinks, or orphaned records.

### How to Add Your Own Custom Skills
To add your own skills to `~/.agents/skills/`, create a new folder with a `SKILL.md`:
```bash
mkdir -p ~/.agents/skills/my-custom-skill
cat << 'EOF' > ~/.agents/skills/my-custom-skill/SKILL.md
---
name: my-custom-skill
description: Brief summary of what this skill does and when the agent should trigger it.
---

# My Custom Skill

Detailed procedural instructions for your AI agent...
EOF
```

---

## 7. Optional Companion CLI

Essentials includes an optional zero-dependency Python script to help you browse, search, and inspect skills directly in your terminal:

```bash
# List all skills by category and view curated profiles
./scripts/essentials list

# Search skills by keyword
./scripts/essentials search "vision"
./scripts/essentials search "audio" --category audio

# Inspect skill metadata and copy instructions
./scripts/essentials inspect code-review
./scripts/essentials inspect portfolio

# Validate that all skills have valid frontmatter and unique IDs
./scripts/essentials validate
```

*Note: The CLI is purely informative. It never installs or deletes files in your home directory.*

---

## 8. Safety & Security

Essentials follows strict security principles:

1. **Passive Guidance by Default**: All skills are instructional Markdown documents (`SKILL.md`). They do not run silent background scripts, make unsolicited network requests, or modify system settings.
2. **Transparent Code**: You can read every line of every skill before copying it.
3. **Quarantined Third-Party Tools**: Complex tools that require active background daemons or credential management (such as `oil-motion`) are held outside the default collection in `resources/docs/` with explicit security audit notes.
4. **No Lock-In**: Essentials does not modify your shell profiles or global environment variables.

> Read the complete security policy in [SECURITY.md](SECURITY.md).

---

## 9. License & Attribution

- **Essentials Core & Toolkit**: Licensed under the [MIT License](LICENSE).
- **Curated Skills**: Maintained with upstream licenses (predominantly MIT and Apache-2.0) preserved in each category's `LICENSE` and `SOURCE.md` files.

Contributions and community skill additions are warmly welcomed! Please read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.
