---
name: git-hygiene
description: "Maintain clean, atomic, conventional commit histories, branch workflows, and safe conflict resolution strategies."
---

# Git Hygiene & Repository Maintenance

Use this skill when staging changes, writing commit messages, branching, rebasing, or maintaining Git repositories.

## Commit Philosophy

1. **Atomic Commits**:
   - Each commit should represent one logical unit of work that passes tests independently.
   - Never bundle unrelated refactors, formatting sweeps, and feature additions into one massive commit.
2. **Conventional Commit Formatting**:
   - Structure: `<type>(<scope>): <short imperative description>`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`.
   - Example: `fix(auth): handle expired token redirect correctly`
3. **Commit Body**:
   - Explain *why* the change was made, what trade-offs were considered, and any non-obvious details.

## Branching & Rebase Workflow

- **Clean Linear History**: Prefer `git pull --rebase` to avoid cluttering main branches with unnecessary merge commits.
- **Pre-Commit Verification**: Always run `git diff` and relevant tests before creating commits.
- **Never Force-Push Public Branches**: Protect shared team history. Use revert commits when amending public branches.
- **Zero Secrets**: Ensure `.env`, local tokens, and keys are guarded by `.gitignore` before every stage.

