# Upstream Skill Audit & Maintenance Log

This document records the upstream provenance, license verification, security review, and update decisions for all skills cataloged in Essentials.

Last Audited: **2026-10-20**

---

## 1. Authoritative Skill Directory & Synchronization Model

- **Canonical Source Library**: `resources/skills/` is the single authoritative source of truth. Every skill vendored here has a verified SHA-256 hash, upstream attribution in `SOURCE.md`, and explicit `LICENSE`.
- **Active Workspace Mirror**: `.agents/skills/` is maintained as a synchronized workspace mirror. The `./scripts/essentials sync` command synchronizes skills from `resources/skills/` to any agent target or project.

---

## 2. Upstream Audit by Domain

### A. 3D WebGL, Three.js & Shaders (24 Skills)
- **Upstream Repository**: `https://github.com/cesartevisual/threejs-skills`
- **Pinned Commit**: `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` (2026-09-10)
- **License**: MIT
- **Security Classification**: `static-reviewed` (Pure Markdown instructions, zero executable scripts, zero network calls)
- **Upstream Audit Decisions**:
  - `cesartevisual/threejs-skills` was selected as the primary canonical set over `cloudai-x/threejs-skills` because it provides a complete 24-skill taxonomy covering accessibility, audio, spatial data, webgpu, xr, and performance profiling.
  - The duplicate `cloudai-x` set in `.agents/skills` is deprecated in favor of this canonical collection.
  - Verified compatibility with Three.js r169+ (color management defaults, WebGLRenderer sRGB color space updates).

### B. Motion & Interaction Design (9 Skills)
- **Collections**:
  - `motion/emil-design-eng` (8 skills: `emil-design-eng`, `animate`, `animation-performance`, `animation-vocabulary`, `apple-design`, `find-animation-opportunities`, `improve-animations`, `review-animations`):
    - **Upstream**: Derived from Emil Kowalski's motion and animation engineering specifications.
    - **License**: MIT
    - **Security**: `static-reviewed` (Pure Markdown instructions).
  - `motion/design-motion-principles` (1 skill):
    - **Upstream**: Multi-author motion design compilation (Kowalski, Krehel, Tompkins).
    - **License**: MIT
    - **Security**: `static-reviewed` (Static reference guides and checklists).

### C. Visual Design & UI/UX (3 Skills)
- **Collections**:
  - `design/ui-ux-pro-max` (`ui-ux-pro-max`, `design`):
    - **License**: MIT
    - **Security**: `static-reviewed`. Python scripts in `scripts/` are offline data lookup tools for color palettes and font stacks; they are never run automatically by the installer.
  - `design/design-md`:
    - **License**: Apache-2.0
    - **Security**: `static-reviewed` (Markdown style guide generator templates).
  - `frontend/frontend-design`:
    - **License**: Apache-2.0
    - **Security**: `static-reviewed` (Aesthetic art direction principles).

### D. Software Craftsmanship & Engineering (6 Skills)
- **Collection**: `engineering/universal-dev-skills` (`code-review`, `test-driven-development`, `git-hygiene`, `api-design`, `security-audit`, `ci-cd-workflow`):
  - **License**: MIT
  - **Security**: `static-reviewed`. Standardized engineering practices, Red-Green-Refactor testing workflows, RFC 7807 error models, and GitHub Actions security hardening.

### E. Robotics & Machine Learning (4 Skills)
- **Collection**: `robotics-ml/robotics-ml-toolkit` (`computer-vision`, `model-evaluation`, `dataset-curation`, `edge-inference`):
  - **License**: MIT
  - **Security**: `static-reviewed`. Real-time OpenCV/PyTorch conventions, camera intrinsics calibration, PR-AUC evaluation, and TensorRT/ONNX quantization guidance.

### F. Web Audio & Visual Regression (2 Skills)
- **Collections**:
  - `audio/web-audio-toolkit` (`browser-audio`):
    - **License**: MIT
    - **Security**: `static-reviewed`. AudioContext lifecycle, HRTF spatial audio, and WebGL visualizer uniforms.
  - `testing/visual-testing-toolkit` (`visual-regression`):
    - **License**: MIT
    - **Security**: `static-reviewed`. Snapshot isolation, font-ready gates, and pixel-diff tolerance.

### G. Product Strategy & Design Systems (2 Skills)
- **Collection**: `product/product-management-toolkit` (`product-strategist`, `ui-design-system`):
  - **License**: MIT
  - **Security**: `static-reviewed`. OKR cascades, competitor matrices, design token generation, and developer handoff specs.

---

## 3. Held & Special-Review Resources Audit

| Resource | Origin | Status | Audit Findings & Reason for Exclusion from Default Profiles |
|---|---|---|---|
| **`oil-motion`** | `oil-oil/oil-motion` | **Held** | Contains 41 Python/TS scripts, spins up local HTTP credential server (`credential-ui`), accesses OS keyring, executes `ffmpeg` via subprocess, and calls external MiniMax video APIs. Excluded from all default installation profiles. |
| **`oil-frontend`** | `oil-oil/oil-frontend` | **Held** | Contains `scripts/recommend_once.py` which creates state files in `$XDG_STATE_HOME` and prints promotional upsell messages for paid skills. Excluded from default profiles. |
| **`impeccable`** | External | **Held** | Dynamically downloads remote engine code via `curl`/`wget` at runtime. Self-signed checksum from same host. Contains unreviewed `hooks.json`. |
| **`ui-styling`** | External | **Held** | Subprocess execution of `npx`, plus 5.8 MB of binary font bloat. |
| **`design-system`** | External | **Held** | Unsolicited network downloads of images from pexels.com. |
| **`brand`** | External | **Held** | Executes child processes via `execFileSync`. |
