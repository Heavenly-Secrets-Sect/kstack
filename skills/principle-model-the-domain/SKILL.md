---
name: principle-model-the-domain
description: "Apply when writing stateful logic, or when code branches a lot or repeats the same shape assumption across files. Encode the domain in a structure instead of scattered conditionals."
disable-model-invocation: true
---

# Model the Domain

Put the rules of the domain into a data structure instead of spreading them across if/else chains. The right structure removes branches and makes invalid states impossible to build.

- A state machine (an enum of states plus allowed transitions) instead of several booleans that must stay in sync.
- A typed model (dataclass, struct, interface) instead of loose dicts or long parameter lists.
- A lookup table or registry instead of the same switch repeated in several files.
- A reducer or single update function instead of mutations scattered around.

Do not force it. Keep plain code when the shape is clear, local and unlikely to grow, and distrust an abstraction that adds a layer without removing a branch or an invalid state.

Signs you skipped this: each new feature adds one more branch to the same chain, or a second flag appears that must stay consistent with the first.
