# Installation Profiles

Profiles in Essentials are curated, tested collections of skills designed for specific project archetypes and engineering disciplines.

Instead of hunting through individual skills, developers can install a cohesive profile with one command.

---

## 1. Available Profiles

### 🎨 `portfolio` (31 skills)
*For creative developers, agency websites, interactive 3D portfolios, and showcase sites.*
- **Focus**: High-fidelity art direction, Three.js 3D scenes, shaders, PBR materials, postprocessing, animation, Web Audio API, and UI elegance.
- **Skills Included**:
  - Three.js Core: `threejs-scene`, `threejs-materials`, `threejs-lighting`, `threejs-shaders`, `threejs-postprocessing`, `threejs-animation`, `threejs-geometry`, `threejs-particles`, `threejs-audio`, `threejs-interaction`, `threejs-performance`, `threejs-accessibility`, `threejs-html`, `threejs-r3f`, `threejs-web`, `threejs-product-viewer`, `threejs-assets`, `threejs-debugging`, `threejs-testing`, `threejs-deployment`
  - Design & Frontend: `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`, `apple-design`
  - Motion & Interaction: `emil-design-eng`, `animate`, `animation-performance`, `review-animations`, `design-motion-principles`
  - Audio: `browser-audio`
- **Installation Command**:
  ```bash
  ./scripts/essentials install portfolio --target ~/projects/portfolio-site
  ```

---

### 📊 `dashboard` (6 skills)
*For SaaS analytics platforms, internal admin tools, and data-dense dashboards.*
- **Focus**: Information hierarchy, visual clarity, data visualization, accessibility, and restrained motion.
- **Skills Included**:
  - `frontend-design`: Layout balance, high-contrast usability, responsive grid alignment.
  - `ui-ux-pro-max`: UI reasoning, color harmony, typography systems, chart palettes.
  - `design`: General interface design principles.
  - `design-md`: Automated design token and style guide documentation.
  - `animation-performance`: 60fps interaction budgeting, minimizing DOM thrashing.
  - `review-animations`: Eliminating unnecessary UI animations.
- **Installation Command**:
  ```bash
  ./scripts/essentials install dashboard --target ~/projects/analytics-dashboard
  ```

---

### 🐍 `python-dev` (5 skills)
*For backend services, CLI utilities, and data processing in Python.*
- **Focus**: Clean architecture, modern typing, test-driven development, and Python engineering standards.
- **Skills Included**:
  - `code-review`: Static analysis, linting, code smells, and performance profiling.
  - `test-driven-development`: Red-Green-Refactor testing workflows and pytest patterns.
  - `git-hygiene`: Atomic commits, branch workflows, and clean history maintenance.
  - `api-design`: RESTful conventions, idempotency keys, cursor pagination.
  - `security-audit`: Dependency vulnerability scanning and OWASP security review.
- **Installation Command**:
  ```bash
  ./scripts/essentials install python-dev --target ~/projects/python-service
  ```

---

### ⚙️ `engineering` (6 skills)
*Universal software engineering suite for backend, systems, and full-stack developers.*
- **Focus**: Craftsmanship, rigorous code review, TDD, Git hygiene, API schemas, security audits, and hardened CI/CD.
- **Skills Included**:
  - `code-review`, `test-driven-development`, `git-hygiene`, `api-design`, `security-audit`, `ci-cd-workflow`
- **Installation Command**:
  ```bash
  ./scripts/essentials install engineering --target ~/projects/core-service
  ```

---

### 🤖 `robotics-ml` (4 skills)
*For computer vision, robotics, edge AI, and machine learning practitioners.*
- **Focus**: Real-time vision pipelines, model evaluation, dataset curation, and edge quantization.
- **Skills Included**:
  - `computer-vision`: Camera intrinsics calibration, OpenCV/PyTorch pipelines, optical flow, object detection.
  - `model-evaluation`: Data leakage prevention, PR-AUC, group cross-validation, inference benchmarking.
  - `dataset-curation`: Labeling schema, class imbalance mitigation, data validation.
  - `edge-inference`: ONNX Runtime, TensorRT quantization (INT8/FP16), embedded deployment.
- **Installation Command**:
  ```bash
  ./scripts/essentials install robotics-ml --target ~/projects/robot-vision
  ```

---

### 🌐 `full-stack` (10 skills)
*End-to-end web application suite covering backend, design, frontend, and visual testing.*
- **Focus**: Unified development from database APIs to frontend UI design and CI pipelines.
- **Skills Included**:
  - `code-review`, `test-driven-development`, `git-hygiene`, `api-design`, `security-audit`
  - `frontend-design`, `ui-ux-pro-max`, `design-md`, `visual-regression`, `ci-cd-workflow`
- **Installation Command**:
  ```bash
  ./scripts/essentials install full-stack --target ~/projects/web-app
  ```

---

## 2. Safety & Profile Rules

1. **Only Static-Reviewed Skills**: All skills bundled into profiles must be approved in `resources/resources.json` with `securityReview.status = "static-reviewed"` and `safeForDefault = true`.
2. **Zero Arbitrary Code Execution**: No skill inside a default profile runs background code, network requests, or scripts.
3. **Held Items Excluded**: Tools like `oil-motion` (which runs a local HTTP credential server and spawns ffmpeg) are strictly excluded from profiles and require individual, manual installation.
