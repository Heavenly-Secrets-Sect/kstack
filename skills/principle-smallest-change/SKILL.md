---
name: principle-smallest-change
description: "Apply when sizing a diff, refactoring, or tempted to add an abstraction, layer, option or guard. Remove before adding, and ship the smallest change that solves the problem."
disable-model-invocation: true
---

# Smallest Change

- Subtract first. Remove dead code, stale options and redundant checks, then build on the simpler base.
- Ship the smallest diff that solves the problem. Fewer lines beat elegant scaffolding.
- Design for observed use, not imagined edge cases. No speculative validators, flags or layers.
- Keep each decision in one place and pass its result along, instead of repeating it.
- Leave the code slightly simpler than you found it.
