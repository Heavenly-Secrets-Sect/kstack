# Bug fix

You own the fix. Every line that ships traces to evidence you observed. A change that "might help" is a hypothesis, not a fix, and it does not ship.

1. **Reproduce** it yourself on the real surface: the project's `verify-*` skill, a test, a script or the running app. If it will not reproduce, tighten the conditions or add logging until it does. Ask the user only with a specific reason you cannot reach it.
2. **Find the cause** (fix-root-causes). List the candidate causes, then rule them out with runtime evidence, each time taking the check that eliminates the most. If two fixes on one assumption fail, stop and run attack-the-premise.
3. **Fix** with the smallest change the evidence justifies (smallest-change). Delegate to `kstack:kstack-worker` with a precise scope when the fix is more than a few lines.
4. **Verify** on the same surface as step 1. The original repro now passes. A unit test alone does not prove the bug is gone.
5. **Commit** the failing test or repro first, then the fix on top (verifiable-steps). The test asserts the behavior the user saw, not the internals you changed (test-behavior-not-implementation). Have a fresh `kstack:kstack-verifier` check the fix commit.

**Reply:** what was broken, the root cause, the fix, and the repro output before and after, pasted verbatim.
