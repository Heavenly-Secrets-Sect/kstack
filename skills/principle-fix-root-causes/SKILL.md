---
name: principle-fix-root-causes
description: "Apply when debugging. Trace the symptom back to the first wrong decision and fix it there. A guard is a fix only when the state it handles is legitimate."
disable-model-invocation: true
---

# Fix Root Causes

Fix where the system first went wrong, not where the symptom showed up.

- Reproduce first. Keep asking why until the answer is a wrong decision in the code. Read real state; do not guess.
- Is the triggering state legitimate? If yes, handle it where the code broke. If it should never exist, find what produced it. Guards, retries, swallowed errors and clamped values usually hide the bug instead.
- Fix the pattern: find every place with the same fault.
- If finding the cause took a deep dig, propose the cheap signal that would have shown it at first glance.
