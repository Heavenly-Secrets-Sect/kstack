---
name: principle-encode-lessons-in-structure
description: "Apply when you write the same instruction twice or see a recurring correction. Turn the rule into a type, lint, test, hook or script instead of more text."
disable-model-invocation: true
---

# Encode Lessons in Structure

A correction that keeps coming back belongs in the system, not in another instruction.

- Prefer, in order: make the wrong choice impossible (types, structure), then catch it automatically (lint, test, hook, CI), then write it down.
- If the fix is structural, remove the old instruction. The instruction was the symptom.
- If the rule needs judgment and cannot be automated, make it prominent and show an example of the failure.
