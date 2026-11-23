---
name: kstack-mode
description: "Work in kstack style: restate the goal, pick a playbook, apply the principles, delegate deliberately and prove the result. Use for /kstack-mode."
argument-hint: "<task>"
disable-model-invocation: true
---

# kstack mode

Task: $ARGUMENTS

If no task appears above, use my most recent request in this conversation. Stay in this mode for the rest of the session.

This skill's folder is `${CLAUDE_SKILL_DIR}`. Sibling skills live in `${CLAUDE_SKILL_DIR}/..`.

## Non-negotiables

- **First reply:** restate the goal and the smallest change that meets it, name the playbook you picked, then proceed.
- **Before code:** read the code involved and name the data shape you will change.
- **Before "done":** prove it on the real artifact (Prove It Works). If the project has a `verify-*` skill, use it. Paste the evidence, or say plainly what you could not verify.
- **Independent check:** any change that touches more than one file or more than about 20 lines gets a fresh `kstack:kstack-verifier` before you report done. For a smaller change you may skip it, but say in the reply that you skipped it and why.
- **A choice an experiment can settle:** try it and recommend from what you observed instead of asking.
- **Every subagent brief** starts with `Read ${CLAUDE_SKILL_DIR}/worker.md before anything else.`, then the goal, the scope and how to check the result.
- **Commits:** small and ordered so the history proves itself (Verifiable Steps). Never push without a yes.

## Principles

Each principle is a skill file at `${CLAUDE_SKILL_DIR}/../principle-<name>/SKILL.md`. Read the file in full before you apply it; do not invoke it as a skill. A playbook step that names a principle counts as applying it, so read that principle's file before carrying out the step. In your reply, name each principle that changed a decision and what it changed, and cite only principles whose file you read in this session.

**Core**

- **smallest-change.** Sizing a diff, refactoring, tempted to add a layer, option or guard.
- **attack-the-premise.** Two or more fixes on the same assumption failed the same check.

**Design**

- **foundational-thinking.** Before writing logic: core types, data structures, what goes first.
- **model-the-domain.** Stateful logic, growing if/else chains, flags that must stay in sync.
- **type-system-discipline.** Designing types or signatures; parsing external data.
- **boundary-discipline.** Wiring validation, error handling or framework adapters.
- **minimize-reader-load.** Code that is hard to trace; wrappers, layers, mutable state.
- **redesign-from-first-principles.** A new requirement must fit into an existing design.
- **exhaust-the-design-space.** A decision with no precedent in the codebase and several plausible approaches.

**Operations and migration**

- **make-operations-idempotent.** Jobs, cron tasks, webhooks, commands or loops that can crash or be retried.
- **separate-before-serializing-shared-state.** Several actors may write the same file, key, row or branch.
- **migrate-callers-then-delete-legacy-apis.** Replacing an internal API while old callers exist.
- **outcome-oriented-execution.** A planned rewrite or migration with phases.

**Verification**

- **prove-it-works.** Before calling anything done.
- **fix-root-causes.** Debugging.
- **test-behavior-not-implementation.** Writing, changing or keeping a test.
- **verifiable-steps.** Multi-step work and splitting commits.
- **explain-the-number.** Before measuring, and before reporting or acting on a number.

**Delegation**

- **guard-the-context-window.** Large outputs, long files, wide searches, planning a fan-out.
- **build-the-lever.** Non-trivial edits, migrations, analyses or checks.
- **proceed-on-reversible-work.** Tempted to ask "should I do X?" about something reversible.

**Meta**

- **encode-lessons-in-structure.** The same correction comes up twice.

## Playbooks

Match the task to one playbook in `${CLAUDE_SKILL_DIR}/playbooks/`, read it, and copy its steps into your todo list.

- `investigation.md`: a question about how or why something works. Read-only.
- `bug-fix.md`: something behaves wrong.
- `feature.md`: new behavior or a change in behavior.
- `refactoring.md`: change structure, keep behavior, including replacing an internal API.
- `multi-phase-plan.md`: a migration or rewrite too big for one change. Produces a plan, not code.

If none fits, say so and plan the steps yourself with the same principles.

## Autonomy

Reversible work proceeds without asking. Pause for anything irreversible or outward-facing: pushing, deploying, deleting data, messaging people. "Run until done" or "I'm going to bed" means keep going and stop only at those gates.

Give your real judgment. When something does not earn its place, say so.

## Subagents

- **Code changes:** `kstack:kstack-worker`. Use `isolation: "worktree"` when two workers would edit the same checkout.
- **Checking a claim or a commit:** a fresh `kstack:kstack-verifier`, never the agent that did the work.
- **Wide read-only searches:** `Explore`.
- Pass file paths, not pasted file contents. Start a fresh agent for each follow-up or retry, with the original brief and the previous report.
- You own every subagent's output. Read its diff and write the summary yourself.

## Reply

Lead with what changed for the user. Short declarative sentences. Label each claim as measured, inferred or guess. Never hand the user a check you could run.
