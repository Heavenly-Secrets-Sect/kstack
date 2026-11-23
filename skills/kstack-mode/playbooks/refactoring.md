# Refactoring

You own the contract. The structure changes; observable behavior does not. If the work uncovers a bug or a missing feature, split it out and route it to bug fix or feature.

1. **Pin the behavior** before moving anything: a characterization test, snapshot or script that records current outputs (test-behavior-not-implementation). Type checks and lint are not a pin.
2. **Name the target shape**: the types, module layout and call graph you would build today (foundational-thinking, model-the-domain, redesign-from-first-principles). It must remove branches, layers or invalid states (minimize-reader-load), not add indirection.
3. **Subtract first**: delete dead code, one-caller wrappers and redundant checks before adding the new shape (smallest-change).
4. **Move in small steps**, keeping the pin green after each (verifiable-steps). When replacing an internal API, move every caller and delete the old one in the same wave (migrate-callers-then-delete-legacy-apis). For many similar edits, write a script or codemod and rerun it (build-the-lever). Search for leftover names in strings, configs and docs, not only code.
5. **Prove behavior is unchanged** on the real artifact: rerun the pin, then the full test suite (prove-it-works). Have a fresh `kstack:kstack-verifier` compare before and after.
6. **Keep it only if it pays**: if no reader-facing complexity went down, revert it.
7. **Commit** the pin first, then subtraction, then the reshape.

**Reply:** what changed in structure, the pin it was held against, the evidence that behavior is unchanged, and what got simpler.
