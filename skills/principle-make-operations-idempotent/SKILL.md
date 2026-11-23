---
name: principle-make-operations-idempotent
description: "Apply when designing commands, jobs, cron tasks, webhooks, lifecycle steps or processing loops that can crash, restart or be retried. Every run must converge to the same correct end state."
disable-model-invocation: true
---

# Make Operations Idempotent

A state-changing operation must reach the correct end state no matter how many times it runs or where the previous run stopped.

- Derive each step from the state that exists now, not from what the last run meant to do: read current state, compare with the goal, apply only the difference.
- Give side effects a natural key (an idempotency key, a unique constraint, an upsert) so a repeat is a no-op instead of a duplicate.
- Anything a run leaves behind (lock, temp file, half-written record, claimed job) must be recognizable as stale by the next run. Write to a temporary path and rename into place.

The test: what happens if this runs twice? What if the previous run died at each possible point? If the answer depends on what was left behind, add a reconciliation step.
