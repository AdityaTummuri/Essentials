---
name: test-driven-development
description: "Design and implement comprehensive automated test suites following Red-Green-Refactor, boundary testing, and regression prevention."
---

# Test-Driven Development (TDD) & Testing Methodology

Use this skill when designing test plans, writing unit/integration tests, or implementing bug fixes.

## Core Rules

1. **Write the Failing Test First**:
   - Write a test demonstrating the bug or desired behavior.
   - Run the test to confirm it fails for the expected reason (Red).
2. **Minimal Implementation**:
   - Implement only the code necessary to pass the test cleanly (Green).
3. **Refactor**:
   - Clean up duplicates, improve readability, and verify tests still pass (Refactor).

## Testing Pyramid & Boundaries

- **Unit Tests**: Test pure business logic in isolation. Fast, deterministic, zero I/O or network dependency.
- **Integration Tests**: Test interactions across real component boundaries (e.g., database queries, filesystem operations, CLI arguments). Use temporary directories (`tempfile.TemporaryDirectory()`).
- **Regression Tests**: Every bug fix MUST have an accompanying regression test replicating the failure case.

## Test Code Quality

- **Arrange-Act-Assert**: Structure every test clearly into setup, execution, and verification.
- **Independent Tests**: Tests must never rely on execution order or shared mutable global state.
- **Descriptive Names**: Name tests after the requirement: `test_empty_input_raises_value_error()`.
