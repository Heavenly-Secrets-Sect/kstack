---
name: principle-foundational-thinking
description: "Apply before writing logic: choosing core types and data structures, ordering scaffolding before features, deciding what concurrent actors share. Get the data shape right so the code that follows is obvious."
disable-model-invocation: true
---

# Foundational Thinking

Get the data shape right before writing logic. Define the core types first, list every way the data is read and written, and pick structures that make the common paths simple. Remove duplication in the structure, not line by line.

Before two actors share state, ask what happens if the other one changes it at the same time. If the answer is not "nothing", give each its own (separate-before-serializing-shared-state).

Scaffold first: whatever helps every later step (tests, shared types, a way to run the thing) lands before features, right after dead code is removed.
