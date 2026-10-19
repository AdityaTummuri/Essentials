---
name: ci-cd-workflow
description: "Architect secure, reproducible CI/CD pipelines using GitHub Actions, matrix testing, dependency caching, and least-privilege permissions."
---

# CI/CD Workflow & Pipeline Architecture

Use this skill when designing, reviewing, or hardening continuous integration and deployment pipelines.

## Core Security & Reliability Standards

### 1. Principle of Least Privilege
- Explicitly declare minimum required `permissions` at the top level of every GitHub Actions workflow:
  ```yaml
  permissions:
    contents: read
    pull-requests: write
  ```
- Never default to broad read/write repository permissions.

### 2. Supply-Chain Hardening
- **Pin Action Commit SHAs**: Do not rely on mutable version tags like `@v4`. Pin the full immutable 40-character commit SHA:
  ```yaml
  uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
  ```
- **Mask Secrets**: Ensure environment secrets are never echoed to console output or command parameters.

### 3. Caching & Deterministic Builds
- Cache package dependencies (`actions/cache` or built-in tool setup caching) keyed by lockfile hashes (`hashFiles('**/poetry.lock')`).
- Run tests against a matrix of supported runtime versions and operating systems (Linux, macOS, Windows where applicable).
- Separate fast validation gates (linters, formatters, unit tests) from slow integration/e2e stages to give developers rapid feedback.
