---
name: principle-exhaust-the-design-space
description: "Apply to a design decision with no precedent in the codebase (a new architecture, data model, API or interaction) where several approaches are plausible. Build 2-3 small competing prototypes and compare them before committing."
disable-model-invocation: true
---

# Exhaust the Design Space

When the codebase has no precedent and more than one approach is plausible, do not pick by intuition. Build two or three small prototypes of genuinely different approaches and compare them side by side.

- Keep each prototype the smallest thing that exposes the difference: a spike, a script, a throwaway branch.
- Decide the comparison criteria before building (simplicity, performance, how invalid states are prevented, how it feels to use).
- Compare on evidence from running them, and record why the losers lost.
- Throw the prototypes away and build the winner properly.

Skip this when the codebase already has an established pattern for the problem; follow the pattern.
