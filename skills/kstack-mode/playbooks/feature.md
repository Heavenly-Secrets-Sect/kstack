# Feature

You own the design. Delegate the typing, not the thinking.

1. **Trace** the code the feature touches and name the data shape that changes. If the task is vague, read `sharpen/SKILL.md` in the sibling skills folder and answer its four questions for yourself before designing.
2. **Design** the smallest shape that delivers it (smallest-change). If two designs are both plausible and an experiment can decide, prototype both briefly and pick from what you observed.
3. **Plan** the work as verifiable steps. Mark which steps are independent: those can go to parallel `kstack:kstack-worker` agents in separate worktrees. Steps that touch the same files stay serial.
4. **Build** by delegating each step with file paths, the data shape and the success check. Read every diff that comes back.
5. **Verify** on the real surface (prove-it-works). Then have a fresh `kstack:kstack-verifier` check the result against the original goal.
6. **Commit** in small ordered commits, each leaving the project working (verifiable-steps).

**Reply:** what you built, what you chose and why (a table if there were alternatives), the evidence, and open decisions.
