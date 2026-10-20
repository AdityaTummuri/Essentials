# Curated Profiles & Bundles

Essentials provides curated profiles—cohesive collections of skills designed for specific engineering disciplines, project archetypes, and developer workflows.

Because **skills are just folders**, you don't need a special installer to use a profile. You can inspect a profile's skills and copy them directly with standard shell commands.

```bash
# View skills in any profile and get the exact copy command:
./scripts/essentials inspect portfolio
./scripts/essentials inspect python-dev
./scripts/essentials inspect full-stack
```

---

## 1. Available Profiles

### 🎨 `portfolio` (31 skills)
*For creative developers, agency websites, interactive 3D portfolios, and showcase sites.*
- **Focus**: High-fidelity art direction, Three.js 3D scenes, shaders, PBR materials, postprocessing, animation, Web Audio API, and UI elegance.
- **Skills Included**:
  - **Three.js**: `threejs-scene`, `threejs-materials`, `threejs-lighting`, `threejs-shaders`, `threejs-postprocessing`, `threejs-animation`, `threejs-geometry`, `threejs-particles`, `threejs-audio`, `threejs-interaction`, `threejs-performance`, `threejs-accessibility`, `threejs-html`, `threejs-r3f`, `threejs-web`, `threejs-product-viewer`, `threejs-assets`, `threejs-debugging`, `threejs-testing`, `threejs-deployment`
  - **Design & Frontend**: `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`, `apple-design`
  - **Motion & Interaction**: `emil-design-eng`, `animate`, `animation-performance`, `review-animations`, `design-motion-principles`
  - **Audio**: `browser-audio`
- **Copy to `~/.agents/skills/`**:
  ```bash
  mkdir -p ~/.agents/skills
  cp -r skills/threejs/* ~/.agents/skills/
  cp -r skills/design/frontend-design skills/design/ui-ux-pro-max skills/design/design skills/design/design-md skills/design/apple-design ~/.agents/skills/
  cp -r skills/design/emil-design-eng skills/design/animate skills/design/animation-performance skills/design/review-animations skills/design/design-motion-principles ~/.agents/skills/
  cp -r skills/audio/browser-audio ~/.agents/skills/
  ```

---

### 🐍 `python-dev` (8 skills)
*For modern Python backend services, CLI utilities, and data processing.*
- **Focus**: Clean architecture, static typing with modern Python 3.10+ syntax, Pytest workflows, async patterns, pyproject.toml packaging, code reviews, and Git hygiene.
- **Skills Included**:
  - **Python**: `pytest-workflow`, `python-patterns`, `type-hints-modern`, `asyncio-patterns`, `packaging-pyproject`
  - **Engineering**: `code-review`, `git-hygiene`, `security-audit`
- **Copy to `~/.agents/skills/`**:
  ```bash
  mkdir -p ~/.agents/skills
  cp -r skills/python/* ~/.agents/skills/
  cp -r skills/engineering/code-review skills/engineering/git-hygiene skills/engineering/security-audit ~/.agents/skills/
  ```

---

### ⚙️ `engineering` (6 skills)
*Universal software engineering suite for backend, systems, and full-stack developers.*
- **Focus**: Craftsmanship, rigorous code review, TDD, Git hygiene, API schemas, security audits, and hardened CI/CD.
- **Skills Included**:
  - `code-review`, `test-driven-development`, `git-hygiene`, `api-design`, `security-audit`, `ci-cd-workflow`
- **Copy to `~/.agents/skills/`**:
  ```bash
  mkdir -p ~/.agents/skills
  cp -r skills/engineering/* ~/.agents/skills/
  ```

---

### 🌐 `full-stack` (10 skills)
*End-to-end web application suite covering backend, design, frontend, and visual testing.*
- **Focus**: Unified development from database APIs to frontend UI design and CI pipelines.
- **Skills Included**:
  - **Backend & Engineering**: `code-review`, `test-driven-development`, `git-hygiene`, `api-design`, `security-audit`, `ci-cd-workflow`
  - **Frontend & Design**: `frontend-design`, `ui-ux-pro-max`, `design-md`
  - **Visual Testing**: `visual-regression`
- **Copy to `~/.agents/skills/`**:
  ```bash
  mkdir -p ~/.agents/skills
  cp -r skills/engineering/* ~/.agents/skills/
  cp -r skills/design/frontend-design skills/design/ui-ux-pro-max skills/design/design-md ~/.agents/skills/
  cp -r skills/testing/visual-regression ~/.agents/skills/
  ```

---

### 📊 `dashboard` (6 skills)
*For SaaS analytics platforms, internal admin tools, and data-dense dashboards.*
- **Focus**: Information hierarchy, visual clarity, data visualization, accessibility, and restrained motion.
- **Skills Included**:
  - `frontend-design`, `ui-ux-pro-max`, `design`, `design-md`, `animation-performance`, `review-animations`
- **Copy to `~/.agents/skills/`**:
  ```bash
  mkdir -p ~/.agents/skills
  cp -r skills/design/frontend-design skills/design/ui-ux-pro-max skills/design/design skills/design/design-md skills/design/animation-performance skills/design/review-animations ~/.agents/skills/
  ```

---

### 🤖 `robotics-ml` (4 skills)
*For computer vision, robotics, edge AI, and machine learning practitioners.*
- **Focus**: Real-time vision pipelines, model evaluation, dataset curation, and edge quantization.
- **Skills Included**:
  - `computer-vision`, `model-evaluation`, `dataset-curation`, `edge-inference`
- **Copy to `~/.agents/skills/`**:
  ```bash
  mkdir -p ~/.agents/skills
  cp -r skills/robotics-ml/* ~/.agents/skills/
  ```

---

## 2. Safety Invariants

1. **100% Static-Reviewed Skills**: All skills in these profiles are strictly instructional markdown with zero arbitrary code execution, background daemons, or unsolicited network requests.
2. **Transparent Copying**: You choose exactly what gets copied into your environment. You can audit any skill's `SKILL.md` before copying.
3. **Easy Removal**: To remove any profile or skill, simply delete the folder from `~/.agents/skills/<skill-id>` or `~/.claude/skills/<skill-id>`.
