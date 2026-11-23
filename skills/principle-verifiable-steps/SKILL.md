---
name: principle-verifiable-steps
description: "Apply to multi-step work (migrations, sweeps, series of similar edits) and to how you split commits. Work in small steps that each end in a state you can check."
disable-model-invocation: true
---

# Verifiable Steps

Each step goes: known-good state, one change, run the check, move on. Do not start the next step while the current one is red.

- Run the per-step check even when a tool or script made the edit.
- Order the history so it proves itself: failing test before the fix, removal before the reshape, baseline before the treatment.
- Each commit stands on its own and leaves the project working.
