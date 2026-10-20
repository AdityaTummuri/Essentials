# Skill Catalog

Generated 2026-10-20 from `resources/resources.json` (82 vendored skills). Each row is a skill folder under `skills/<category>/`. The catalog is the provenance record; this table is a readable view of it.

- **Licence**: SPDX identifier from the catalog. Upstream `LICENSE.txt` is kept in the skill folder when the upstream ships one.
- **Bundled code**: `Yes` means the folder contains scripts (`.py`, `.sh`, `.js`, `.cjs`, `.mjs`, `.ts`, `.ps1`, or any executable non-document file). Scripts run only when the agent is asked to use them.
- **Safe by default**: `Yes` means the skill has no code, or every bundled script was audited as local-only (see `docs/UPSTREAM_AUDIT.md`). `No` means the skill bundles code that runs on request, or its instructions direct the agent to download or run packages or write client configuration. Code-bearing skills must be `No` unless audited; `tests/test_catalog.py` enforces this.
- **Install**: copy the folder into `~/.agents/skills/` or `~/.claude/skills/` as a real copy, not a symlink. See `docs/INSTALLATION_STATUS.md` for what is installed where.

Not vendored (excluded, see `docs/UPSTREAM_AUDIT.md`): `finishing-a-development-branch`, `using-git-worktrees` (Superpowers). Two adopted skills reference them; Claude Code gets them from the Superpowers plugin, other agents do not.

## audio

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `browser-audio` | MIT | Essentials (original) | Web Audio API, spatial audio, sound effects, audio visualizers, AudioContext lifecycle | No | Yes |

## design

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `animate` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Building an animation from scratch in a decision order | No | Yes |
| `animation-performance` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Keeping animations inside the frame budget (composite-only props) | No | Yes |
| `animation-vocabulary` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Turning vague animation descriptions into precise terms | No | Yes |
| `apple-design` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Apple-style interface design and fluid physical motion | No | Yes |
| `design` | MIT | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) @ `56ea9cf174ed86786187daa9de0e6247cb0747e4` | Design-generation workflow with references | Yes | No |
| `design-md` | Apache-2.0 | [moesuito/claude-skill-design-md](https://github.com/moesuito/claude-skill-design-md) @ `aeddb0d588f8ded1cc4d431c3532dbb76cb12678` | Authoring DESIGN.md token and brand documents for agents | No | Yes |
| `design-motion-principles` | MIT | [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles) @ `4a9ca879f24a361f4dca4174fe2da0f67b5ddee3` | Motion and interaction design guidance with reference workflows | No | Yes |
| `emil-design-eng` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | UI polish and component craft (Emil Kowalski's approach) | No | Yes |
| `find-animation-opportunities` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Finding static UI that should animate | No | Yes |
| `frontend-design` | Apache-2.0 | [anthropics/skills](https://github.com/anthropics/skills) @ `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Distinctive, production-grade frontend aesthetics that avoid generic AI-looking UI | No | Yes |
| `improve-animations` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Auditing a codebase's motion system and planning fixes | No | Yes |
| `review-animations` | MIT | [emilkowalski/skills](https://github.com/emilkowalski/skills) @ `2d228630ba1446365f614a108cb8252f1feda202` | Reviewing animation code against a craft bar | No | Yes |
| `ui-ux-pro-max` | MIT | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) @ `56ea9cf174ed86786187daa9de0e6247cb0747e4` | Searchable UI/UX rules, palettes, typography and style data | Yes | Yes |
| `web-design-reviewer` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Visual QA, design review, frontend debugging | No | Yes |

## engineering

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `acquire-codebase-knowledge` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Codebase onboarding and mapping | Yes | No |
| `api-design` | MIT | Essentials (original) | REST API design, idempotency keys, cursor pagination, error formatting, schema design | No | Yes |
| `brainstorming` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Requirements clarification, design exploration | Yes | No |
| `caveman` | Apache-2.0 | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) @ `bad48a0` | Lower-token responses | No | Yes |
| `ci-cd-workflow` | MIT | Essentials (original) | CI/CD workflows, GitHub Actions, matrix testing, artifact caching, pipeline security | No | Yes |
| `code-review` | MIT | Essentials (original) | Code review, pull request audits, correctness and security checks | No | Yes |
| `dependabot` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Dependency auditing, update automation | No | Yes |
| `executing-plans` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Inline plan execution | Yes | No |
| `git-hygiene` | MIT | Essentials (original) | Git branching, atomic conventional commits, rebase workflows, repo maintenance | No | Yes |
| `github-actions-hardening` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | CI/CD security review | No | Yes |
| `mcp-builder` | Apache-2.0 | [anthropics/skills](https://github.com/anthropics/skills) @ `dbd4588` | MCP server development and evaluation | Yes | No |
| `ollama-local-models` | MIT | Essentials (original) | Local LLMs, Ollama benchmarking | No | Yes |
| `receiving-code-review` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Handling review comments | No | Yes |
| `refactor` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Refactoring, maintainability | No | Yes |
| `requesting-code-review` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Pre-merge review, review briefs | No | Yes |
| `reverse-engineer-anything` | MIT | [morluto/rea](https://github.com/morluto/rea) (rea-agents 6.5.0) | Binary and package analysis with REA | No | No |
| `secret-scanning` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Secrets detection, push protection | No | Yes |
| `security-audit` | MIT | Essentials (original) | Security review, vulnerability audits, OWASP Top 10, dependency auditing, secret scanning | No | Yes |
| `skill-creator` | Apache-2.0 | [anthropics/skills](https://github.com/anthropics/skills) @ `dbd4588` | Skill authoring and evaluation | Yes | No |
| `subagent-driven-development` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Subagent-driven implementation with review gates | Yes | No |
| `systematic-debugging` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Debugging, root-cause analysis, flaky tests | No | Yes |
| `test-driven-development` | MIT | Essentials (original) | Unit testing, TDD methodology, test automation, regression testing | No | Yes |
| `threat-model-analyst` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Threat analysis, security design review | No | Yes |
| `verification-before-completion` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Verified completion, pre-commit checks | No | Yes |
| `writing-plans` | MIT | [obra/superpowers](https://github.com/obra/superpowers) @ `bb92a77` | Implementation planning, task decomposition | No | Yes |

## product

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `product-strategist` | MIT | Essentials (original) | Product strategy, OKR cascades, product vision documents, quarterly roadmap planning | No | Yes |
| `ui-design-system` | MIT | Essentials (original) | Design systems, design tokens, typography scales, color palettes, developer handoff | No | Yes |

## python

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `asyncio-patterns` | MIT | Essentials (original) | Production asynchronous programming with Asyncio, TaskGroups, timeouts, and concurrency throttling. | No | Yes |
| `packaging-pyproject` | MIT | Essentials (original) | Standards-compliant Python project packaging, build hooks, pyproject.toml, and distribution. | No | Yes |
| `pytest-workflow` | MIT | Essentials (original) | Architect, write, and maintain deterministic unit and integration test suites using Pytest. | No | Yes |
| `python-patterns` | MIT | Essentials (original) | Idiomatic modern Python design patterns, dataclasses, protocols, and clean architecture conventions. | No | Yes |
| `type-hints-modern` | MIT | Essentials (original) | Python 3.10+ static type hinting, TypeAlias, TypeVar, Self, ParamSpec, and static verification. | No | Yes |

## robotics-ml

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `computer-vision` | MIT | Essentials (original) | Computer vision, OpenCV, camera calibration, object detection, optical flow, PyTorch vision | No | Yes |
| `dataset-curation` | MIT | Essentials (original) | Dataset preparation, data validation, schema enforcement, class imbalance, DVC versioning | No | Yes |
| `edge-inference` | MIT | Essentials (original) | Edge AI, ONNX Runtime, TensorRT, INT8 quantization, Jetson embedded deployment | No | Yes |
| `esp32-embedded-debugging` | MIT | Essentials (original) | ESP32 and serial debugging | No | Yes |
| `model-evaluation` | MIT | Essentials (original) | Machine learning validation, PR-AUC, metrics, data leakage prevention, latency benchmarking | No | Yes |
| `pytorch-experiments` | MIT | Essentials (original) | PyTorch training, benchmarking, ONNX export | No | Yes |
| `ros2-debugging` | MIT | Essentials (original) | ROS 2 debugging | No | Yes |

## testing

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `playwright-generate-test` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | E2E test generation | No | Yes |
| `test-gap-audit` | MIT | [github/awesome-copilot](https://github.com/github/awesome-copilot) @ `613efc8` | Test coverage gap analysis | Yes | No |
| `visual-regression` | MIT | Essentials (original) | Visual testing, snapshot testing, Playwright, pixelmatch, UI regression prevention | No | Yes |
| `webapp-testing` | Apache-2.0 | [anthropics/skills](https://github.com/anthropics/skills) @ `dbd4588` | Browser testing of local web apps | Yes | No |

## threejs

| Skill | Licence | Upstream | Intended use | Bundled code | Safe by default |
| --- | --- | --- | --- | --- | --- |
| `threejs-accessibility` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Keyboard and assistive-technology access to 3D interactions | No | Yes |
| `threejs-animation` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Animation clips, skeletal animation, transitions | No | Yes |
| `threejs-assets` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Loading, validating and compressing glTF models and textures | No | Yes |
| `threejs-audio` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Spatial audio with user-controlled playback | No | Yes |
| `threejs-debugging` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Black canvases, missing meshes, wrong colors, flicker | No | Yes |
| `threejs-deployment` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Web build preparation, asset hosting, decoder paths | No | Yes |
| `threejs-geometry` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | BufferGeometry, procedural meshes, instancing | No | Yes |
| `threejs-html` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Responsive HTML and framework integration | No | Yes |
| `threejs-interaction` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Pointer picking, orbit controls, dragging | No | Yes |
| `threejs-lighting` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Environment maps, direct lights, baked lighting | No | Yes |
| `threejs-materials` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | PBR materials, texture mapping, transparency, color-management fixes | No | Yes |
| `threejs-particles` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Particle systems, point clouds, large repeated datasets | No | Yes |
| `threejs-performance` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Frame time, GPU workload, memory profiling and optimization | No | Yes |
| `threejs-physics` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Rapier physics integration | No | Yes |
| `threejs-postprocessing` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Bloom, antialiasing, ambient occlusion, depth effects | No | Yes |
| `threejs-product-viewer` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Product viewers with material variants and camera presets | No | Yes |
| `threejs-r3f` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | React Three Fiber scenes, Drei helpers, Suspense loading | No | Yes |
| `threejs-scene` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Scene hierarchy, camera framing, coordinate conventions | No | Yes |
| `threejs-shaders` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Custom GLSL shaders, uniforms, material effects | No | Yes |
| `threejs-spatial-data` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | BIM/IFC, GIS and CAD data, measurements, clipping | No | Yes |
| `threejs-testing` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Browser checks and deterministic visual fixtures | No | Yes |
| `threejs-web` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | Planning complete Three.js web experiences | No | Yes |
| `threejs-webgpu` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | WebGPURenderer and TSL node materials | No | Yes |
| `threejs-xr` | MIT | [cesartevisual/threejs-skills](https://github.com/cesartevisual/threejs-skills) @ `84f9bcb4bea1f7a28d57fe7f0af78f7f9c3dc467` | VR and AR sessions and XR input | No | Yes |
