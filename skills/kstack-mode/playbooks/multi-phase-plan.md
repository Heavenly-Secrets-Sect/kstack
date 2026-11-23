# Multi-phase plan

You own the plan, not the code. Use this for a migration, rewrite or feature too large for one change. The plan is the deliverable; do not implement until the operator says go.

1. If the change is one or two files with an obvious approach, skip the plan, say so and use another playbook.
2. Read the affected code and settle open technical questions by small experiments (exhaust-the-design-space). Ask the operator only about product or priority choices.
3. Write the target end state and how it will be verified (outcome-oriented-execution, redesign-from-first-principles).
4. Write the plan to a file, `docs/plans/<name>.md` unless the project has a convention. Open with the target, the phases in landing order and which phases are independent. Then one section per phase with checkboxes for: what it depends on, the files it may touch, the single change it makes, where temporary breakage is allowed, and how it is verified on the real surface (verifiable-steps, prove-it-works).
5. Call out operations that must survive crashes and retries (make-operations-idempotent), actors that may write the same state (separate-before-serializing-shared-state), and APIs to migrate and delete (migrate-callers-then-delete-legacy-apis).
6. Hand back the plan path and stop.

**Reply:** the plan path, the phases with their dependencies, what remains unproven, and the decisions waiting on the operator.
