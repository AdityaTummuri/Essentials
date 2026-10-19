# Upstream Skill Audit & Maintenance Log

This document records the upstream provenance, license verification, security review, and update decisions for all 56 skills cataloged in Essentials.

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
