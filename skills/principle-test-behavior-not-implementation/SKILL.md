---
name: principle-test-behavior-not-implementation
description: "Apply when writing, changing or keeping a test. Assert what users of the code can observe, so the test fails when behavior breaks and keeps passing when only internals change."
disable-model-invocation: true
---

# Test Behavior, Not Implementation

A test is a claim about what callers can observe: return values, raised errors, state they can read back, and effects on outside systems. Private helpers, call order and intermediate data are implementation.

Judge each test against two imagined edits:

- **Break the behavior** (wrong value, skipped or doubled effect). If the test still passes, it proves nothing. Usual causes: a loose assertion, an expected value computed by the code under test, asserting on data the test built itself.
- **Change the internals** but keep every observable result. If the test fails, it is pinned to the implementation.

Keep tests that catch the first and survive the second; rewrite or delete the rest. Drive the code through its public interface with concrete inputs, and derive expected values from the requirement, not from the code. What an external service receives is behavior; a call to an internal helper is not. Assert the error type callers branch on, not the message text.
