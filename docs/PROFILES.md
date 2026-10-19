# Installation Profiles

Profiles in Essentials are curated, tested collections of skills designed for specific project archetypes and engineering disciplines.

Instead of hunting through individual skills, developers can install a cohesive profile with one command.

---

## 1. Available Profiles

### 🎨 `portfolio`
*For creative developers, agency websites, interactive 3D portfolios, and showcase sites.*
- **Focus**: High-fidelity art direction, Three.js 3D scenes, shaders, PBR materials, postprocessing, animation, and UI elegance.
- **Skills Included (30 total)**:
  - Three.js Core: `threejs-scene`, `threejs-materials`, `threejs-lighting`, `threejs-shaders`, `threejs-postprocessing`, `threejs-animation`, `threejs-geometry`, `threejs-particles`, `threejs-audio`, `threejs-interaction`, `threejs-performance`, `threejs-accessibility`, `threejs-html`, `threejs-r3f`, `threejs-web`, `threejs-product-viewer`, `threejs-assets`, `threejs-debugging`, `threejs-testing`, `threejs-deployment`
  - Design & Frontend: `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`, `apple-design`
  - Motion & Interaction: `emil-design-eng`, `animate`, `animation-performance`, `review-animations`, `design-motion-principles`
- **Installation Command**:
  ```bash
  ./scripts/essentials install portfolio --target ~/projects/portfolio-site
  ```

---

### 📊 `dashboard`
*For SaaS analytics platforms, internal admin tools, and data-dense dashboards.*
- **Focus**: Information hierarchy, visual clarity, data visualization, accessibility, and restrained motion.
- **Skills Included (6 total)**:
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

### 🐍 `python-dev`
*For backend services, CLI utilities, and data processing in Python.*
- **Focus**: Clean architecture, modern typing, test-driven development, and Python engineering standards.
- **Skills Included**:
  - `test-driven-development`: Red-Green-Refactor testing workflows and pytest patterns.
  - `code-review`: Static analysis, linting, code smells, and performance profiling.
  - `git-hygiene`: Atomic commits, branch workflows, and clean history maintenance.
- **Installation Command**:
  ```bash
  ./scripts/essentials install python-dev --target ~/projects/python-service
  ```

---

## 2. Safety & Profile Rules

1. **Only Static-Reviewed Skills**: All skills bundled into profiles must be approved in `resources/resources.json` with `securityReview.status = "static-reviewed"` and `safeForDefault = true`.
2. **Zero Arbitrary Code Execution**: No skill inside a default profile runs background code, network requests, or scripts.
3. **Held Items Excluded**: Tools like `oil-motion` (which runs a local HTTP credential server and spawns ffmpeg) are strictly excluded from profiles and require individual, manual installation.

