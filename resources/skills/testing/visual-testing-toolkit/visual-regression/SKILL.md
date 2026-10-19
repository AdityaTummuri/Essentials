---
name: visual-regression
description: "Implement automated visual regression testing, pixel-diffing thresholds, headless browser consistency, and screenshot snapshot baselines."
---

# Visual Regression Testing Protocol

Use this skill when implementing automated UI regression tests, visual snapshot comparisons, or catching unintended CSS and WebGL layout shifts.

## Methodology & Tooling

### 1. Snapshot Isolation & Flakiness Prevention
- **Disable Animations & Carets**:
  - Inject CSS to disable transitions, animations, and blinking carets before taking snapshots:
    ```css
    *, *::before, *::after {
      transition: none !important;
      animation: none !important;
      caret-color: transparent !important;
    }
    ```
- **Consistent Viewports**: Always lock fixed viewport dimensions (e.g. `1280x720` desktop, `375x812` mobile) and explicit device scale factors (`deviceScaleFactor: 2` for Retina).
- **Web Font Readiness**: Never capture screenshots until `document.fonts.ready` resolves, preventing font-swap layout shifts.

### 2. Difference Thresholds & Anti-Aliasing
- Render engines on different OS platforms (Linux CI vs macOS dev) produce minor anti-aliasing variations.
- Use threshold-aware diffing algorithms (such as `pixelmatch` or Playwright's built-in `toHaveScreenshot`):
  - Set `maxDiffPixelRatio: 0.01` (allows up to 1% difference).
  - Set `threshold: 0.2` (per-pixel color distance sensitivity).
  - Mask dynamic elements (timestamps, random user avatars, live video feeds) using test locators.

### 3. CI Baseline Management
- Store reference snapshots in Git LFS or object storage.
- When intentional UI redesigns occur, update baselines via a dedicated `--update-snapshots` CI run with peer review approval.
