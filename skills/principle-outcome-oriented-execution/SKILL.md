---
name: principle-outcome-oriented-execution
description: "Apply to planned rewrites and migrations that have explicit phases. Aim for the target end state and prove it at checkpoints, instead of writing throwaway compatibility code to keep every intermediate step perfect."
disable-model-invocation: true
---

# Outcome-Oriented Execution

In a planned rewrite or migration, optimize for a correct end state, not for every intermediate state being fully polished. Temporary compatibility code tends to outlive the migration and become debt.

- Write the target state and how it will be verified before starting.
- Declare where temporary breakage is acceptable and for how long, for example "the old importer is broken between phase 2 and phase 3 on this branch".
- Keep fast, high-signal checks on the areas you are actively touching during the migration.
- At the end, run the full verification: every test, type check and real-surface check.

Planned breakage must stay on a branch or behind a boundary. The shared main line always works.
