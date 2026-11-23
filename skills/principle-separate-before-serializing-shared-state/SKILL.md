---
name: principle-separate-before-serializing-shared-state
description: "Apply when concurrent actors (processes, jobs, agents, workers) might write the same file, branch, key, row or object. Remove the sharing first; add locking only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate Before Serializing Shared State

When several actors might write the same target, first ask whether they truly need one shared object or are each publishing independent facts.

- Default to giving each actor its own file, key, row, branch or worktree, and combine results only where they are read.
- Two workers writing different fields of one JSON file or document is still shared mutation.
- Only when a single shared target is a real invariant, serialize access with structure: one writer, sequential phases, a lock, or compare-and-swap.

Instructions such as "be careful not to overwrite" are not concurrency control. "We need a lock" is a signal to check whether the sharing can go away instead.
