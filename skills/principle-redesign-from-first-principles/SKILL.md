---
name: principle-redesign-from-first-principles
description: "Apply when a new requirement has to fit into an existing design. Design as if the requirement had been known from day one, then deliver that design in small steps."
disable-model-invocation: true
---

# Redesign From First Principles

Do not bolt a new requirement onto the side of the current design. Ask what you would build if this requirement had been a founding assumption, then move toward that.

- Read every affected file first and understand why the current design looks the way it does.
- Sketch the from-scratch design that includes the new requirement. Compare it with the current one and name the gap.
- Carry the change through everything that refers to it: types, call sites, tests, docs, examples and comments.
- Plan the whole redesign, then deliver it in verifiable steps (verifiable-steps). If the gap is small, the bolt-on may be the right answer; say why.
