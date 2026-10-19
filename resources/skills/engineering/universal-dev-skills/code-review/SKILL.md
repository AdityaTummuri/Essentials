---
name: code-review
description: "Perform structured, rigorous code reviews focusing on correctness, edge cases, error handling, security, performance, and architecture."
---

# Code Review Protocol

Use this skill when auditing, reviewing, or critiquing code changes, pull requests, or modules.

## Review Dimensions

### 1. Correctness & Logic
- Check invariants, boundary conditions (empty collections, 0, null/nil/None, off-by-one errors).
- Verify control flow handles unexpected early returns and exceptions properly.
- Ensure state mutations cannot violate domain constraints or lead to race conditions.

### 2. Security & Input Sanitization
- Never trust external inputs: enforce strict schema validation, type checking, and boundary limits.
- Check for SQL injection, command execution, path traversal, and SSRF patterns.
- Ensure secrets, authentication headers, or sensitive user PII are never logged or exposed.

### 3. Error Handling & Observability
- Avoid catch-all exception swallowers (`except: pass` or `catch (e) {}`).
- Ensure errors provide actionable debugging context while concealing sensitive internal details from clients.
- Verify logging is balanced: informative on failures, quiet on normal paths.

### 4. Performance & Resource Management
- Look out for $O(N^2)$ loops, N+1 query patterns, and unbounded memory allocations.
- Ensure file descriptors, database connections, sockets, and subprocesses are properly closed via context managers (`with` / `try-finally`).

### 5. Architectural Cleanliness & Maintainability
- Keep functions single-responsibility and concise.
- Preserve existing codebase conventions and documentation integrity.
