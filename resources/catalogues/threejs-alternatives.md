# Three.js skill collections: comparison

Compared on 2026-10-19 from shallow clones of the default branches.

| | cesartevisual/threejs-skills (**installed**) | CloudAI-X/threejs-skills (catalogue only) |
|---|---|---|
| License | MIT | MIT |
| Pinned commit | `84f9bcb` (2026-09-10) | `0e18186` (2026-10-19) |
| Skills | 24 | 13 |
| Size per skill | ~2 KB, principle-based | ~20–30 KB, reference-style with code |
| Version targeting | Uses the project's installed three.js; no pin | Targets three.js r186 (`three@0.186.0`) |
| Breadth | Accessibility, audio, XR, WebGPU, physics, testing, debugging, product viewers, spatial data, deployment | Geometry, fundamentals, postprocessing, animation, asset pipeline, shaders, loaders, materials, performance, React Three Fiber, textures, interaction, lighting |

## Overlap

Both cover scene, materials, lighting, shaders, postprocessing, animation, geometry, performance, interaction, and r3f. Installing both would give two competing answers on the same topics.

## What CloudAI-X has that the primary set does not go deep on

- **`threejs-asset-pipeline`**: `gltf-transform` inspect, validate, and compress workflow.
- **`threejs-loaders`**: concrete Draco, meshopt, and KTX2 setup.
- **`threejs-textures`**: color spaces, UV channels, and texture transforms in detail.

`cesartevisual` has `threejs-assets` and `threejs-materials`, which cover these at a higher level.

## Recommendation

1. Keep `cesartevisual-threejs-skills` as the primary collection. It is in the portfolio preset.
2. If the portfolio hits a loader or asset-pipeline problem that the primary set does not answer, copy only `threejs-asset-pipeline` or `threejs-loaders` from CloudAI-X into `skills/threejs/`, with a SOURCE.md that records the commit. Check first that the project's three.js version matches r186, or that the advice still applies to it.
3. Do not install both collections into the same project.
