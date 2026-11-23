---
name: principle-prove-it-works
description: "Apply before calling any task done. Check the real artifact (run it, read the actual value, inspect the diff), not a proxy such as 'it compiles' or a self-report."
disable-model-invocation: true
---

# Prove It Works

Done means you watched the real thing behave correctly: the feature ran, the value was read back, the diff says what you claim.

- Proxies do not count: "it compiles", a green unrelated test, a file timestamp, cached output, another agent's report.
- Exercise the path a user takes, not a test-only shortcut.
- When a check fails, doubt the check before the system. Confirm you observed the right thing.
- Script the check when you can, so anyone can rerun it. Say what you could not verify.
