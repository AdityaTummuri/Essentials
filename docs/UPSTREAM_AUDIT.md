# Upstream Skill Audit & Maintenance Log

This document records the upstream provenance, license verification, security review, and update decisions for all 82 skills cataloged in Essentials (`resources/resources.json`, 2026-10-20).

Last Audited: **2026-10-20**

---

## 1. Authoritative Skill Directory Architecture

- **Canonical Library**: The top-level `skills/` directory is the single authoritative source of truth. Every category contains an explicit `LICENSE` and `SOURCE.md` file, and every skill `SKILL.md` is fingerprinted with a SHA-256 hash in `resources/resources.json`.
- **Zero-Machinery Portability**: Skills are distributed as plain, self-contained directories. Users can inspect, copy, or symlink them directly without requiring background daemons or installer scripts.

---

## 2. Upstream Audit by Domain

### A. 3D WebGL, Three.js & Shaders (24 Skills)
- **Directory**: `skills/threejs/`
- **Upstream Repository**: `https://github.com/cesartevisual/threejs-skills`
- **Pinned Commit**: `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467`
- **License**: MIT
- **Security Classification**: `static-reviewed` (Pure Markdown instructions, zero executable scripts, zero network calls).
- **Audit Decision**: `cesartevisual/threejs-skills` was chosen as the canonical Three.js library because it provides a complete 24-skill taxonomy covering accessibility, audio, spatial data, webgpu, xr, and performance profiling. Verified compatibility with Three.js r169+ color management defaults.

### B. Motion & Interaction Design (9 Skills)
- **Directory**: `skills/design/`
- **Skills**: `emil-design-eng`, `animate`, `animation-performance`, `animation-vocabulary`, `apple-design`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `design-motion-principles`
- **Upstream Sources**: Emil Kowalski motion engineering specifications; multi-author motion design compilation (Kowalski, Krehel, Tompkins).
- **License**: MIT
- **Security Classification**: `static-reviewed`.

### C. Visual Design & UI/UX (4 Skills)
- **Directory**: `skills/design/`
- **Skills**: `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`
- **Upstream Sources**: Anthropic frontend design guidelines, UI/UX Pro Max system, and style guide templates.
- **Licenses**: MIT and Apache-2.0.
- **Security Classification**: `static-reviewed`. Standalone offline lookup scripts in `ui-ux-pro-max` are strictly local utilities and never run automatically.

### D. Universal Software Engineering (6 Skills)
- **Directory**: `skills/engineering/`
- **Skills**: `code-review`, `test-driven-development`, `git-hygiene`, `api-design`, `security-audit`, `ci-cd-workflow`
- **License**: MIT
- **Security Classification**: `static-reviewed`. Standardized engineering practices, Red-Green-Refactor testing workflows, RFC 7807 error models, and GitHub Actions security hardening.

### E. Modern Python Engineering (5 Skills)
- **Directory**: `skills/python/`
- **Skills**: `pytest-workflow`, `python-patterns`, `type-hints-modern`, `asyncio-patterns`, `packaging-pyproject`
- **License**: MIT
- **Security Classification**: `static-reviewed`. Modern Python 3.10+ conventions, pytest parametrization/fixtures, PEP 604 union types, TaskGroup structured concurrency, and pyproject.toml packaging with hatchling/flit.

### F. Robotics & Machine Learning (4 Skills)
- **Directory**: `skills/robotics-ml/`
- **Skills**: `computer-vision`, `model-evaluation`, `dataset-curation`, `edge-inference`
- **License**: MIT
- **Security Classification**: `static-reviewed`. Real-time OpenCV/PyTorch conventions, camera intrinsics calibration, PR-AUC evaluation, and TensorRT/ONNX quantization guidance.

### G. Web Audio & Visual Testing (2 Skills)
- **Directories**: `skills/audio/` and `skills/testing/`
- **Skills**: `browser-audio` (AudioContext lifecycle, HRTF spatial audio, WebGL visualizer uniforms), `visual-regression` (automated Playwright/pixelmatch snapshots).
- **License**: MIT
- **Security Classification**: `static-reviewed`.

### H. Product Strategy & Design Systems (2 Skills)
- **Directory**: `skills/product/`
- **Skills**: `product-strategist`, `ui-design-system`
- **License**: MIT
- **Security Classification**: `static-reviewed`. OKR cascades, competitor matrices, design token generation, and developer handoff specs.

---

## 3. Held & Special-Review Resources Audit

The following third-party resources were evaluated and classified as **held** (not included in the canonical `skills/` library):

| Resource | Origin | Status | Audit Findings & Reason for Exclusion |
|---|---|---|---|
| **`oil-motion`** | `oil-oil/oil-motion` | **Held** | Contains 41 Python/TS scripts, spins up local HTTP credential server (`credential-ui`), accesses OS keyring, executes `ffmpeg` via subprocess, and calls external MiniMax video APIs. Excluded from clean library. |
| **`oil-frontend`** | `oil-oil/oil-frontend` | **Held** | Contains `scripts/recommend_once.py` which touches `$XDG_STATE_HOME` and outputs promotional messages for paid external skills. Excluded. |
| **`impeccable`** | External | **Held** | Dynamically downloads remote engine code via `curl`/`wget` at runtime. Contains unreviewed `hooks.json`. |
| **`ui-styling`** | External | **Held** | Subprocess execution of `npx`, plus 5.8 MB of binary font bloat. |
| **`design-system`** | External | **Held** | Unsolicited network downloads of images from external websites. |
| **`brand`** | External | **Held** | Executes child processes via `execFileSync`. |

---

## 2026-10-20 Acquisition Decisions

Superpowers and Anthropic skills were re-cloned on 2026-10-20 and matched the pinned revisions below. awesome-copilot and caveman were cloned the same day in an earlier pass. Licences were read from each repository. The `rea` revision was resolved from the upstream tag.

| Upstream | Revision | Licence | Adopted | Excluded and why |
| --- | --- | --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | `bb92a77` (2026-10-09) | MIT | `writing-plans`, `brainstorming`, `executing-plans`, `subagent-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review`, `receiving-code-review` | `finishing-a-development-branch` merges, pushes, force-deletes branches, and removes worktrees. `using-git-worktrees` runs `npm install`, `pip install`, and similar automatically in each new worktree. Both are referenced by adopted skills and are provided by the Superpowers plugin in Claude Code. Not vendored. |
| [anthropics/skills](https://github.com/anthropics/skills) | `dbd4588` (2026-10-09) | Apache-2.0 (per-skill `LICENSE.txt`) | `webapp-testing`, `mcp-builder`, `skill-creator` | `frontend-design` already vendored under `skills/design/`. `skill-creator` is also provided by the platform in Claude Code, so it is not copied to personal directories. |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | `bad48a0` (2026-10-17) | Apache-2.0 | `caveman` (skill only) | Proxy, middleware, shell hooks, and installer. |
| [morluto/rea](https://github.com/morluto/rea) (npm `rea-agents` 6.5.0) | tag `rea-agents-6.5.0` = `3b79af28` | MIT | `reverse-engineer-anything` (moved from untracked `skills/` into `engineering/`, content unchanged, byte-identical to the npm bundle) | None. |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | `613efc8` (2026-10-20) | MIT | 9 skills (see `docs/SKILL_CATALOG.md`) | `conventional-commit` duplicates `git-hygiene`. `security-review` overlaps `security-audit`. `diagnose` is an AI-workflow tool, not a code skill. |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | not vendored | Sustainable Use License 1.0 (not MIT; third-party components keep their own licences) | None | Installer-driven, enables anonymous telemetry by default, and imports API keys, MCP servers, and model settings from other tools. Its licence limits use to internal or non-commercial purposes. Not installed. See `docs/INSTALLATION_STATUS.md`. |

### Safety flag (`safeForDefault`)

`safeForDefault: true` means the skill has no code, or every bundled script was audited and recorded as local-only. `false` means the skill bundles code that runs on request, or its instructions direct the agent to download or run packages or write client configuration. The test suite enforces this for code-bearing skills (`tests/test_catalog.py`). Two audits are on record:

- `ui-ux-pro-max`: stdlib-only scripts, no network, subprocess, or credential access, writes only with `--persist` to a chosen directory. Kept `true`.
- `design`: image generators call external APIs (Gemini, AtlasCloud, MuAPI) with keys from the environment, read `.env` files from several home-directory paths, and write downloads. Changed to `false`. The held-resource rule would exclude these generators. Decision pending.
