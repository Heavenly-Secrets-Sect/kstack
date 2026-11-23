---
name: principle-minimize-reader-load
description: "Apply when writing, reviewing or reshaping code that is hard to follow. Cut the layers a reader must trace and the hidden or mutable state they must keep in their head."
disable-model-invocation: true
---

# Minimize Reader Load

Reader load is the work needed to understand code. It has two axes: how many layers sit between a question and its answer, and how much hidden or mutable state the reader must track.

- Collapse layers that only forward: wrappers with one caller, interfaces with one implementation, pass-through methods.
- Shrink the scope of state: return values over mutation, locals over fields, fields over module globals. Derive values instead of keeping copies in sync.
- State an invariant once, where it is established, not in every consumer.

The test: can a new reader answer "where does X come from?" and "what can change X?" within about thirty seconds? If not, remove a layer or remove state.
