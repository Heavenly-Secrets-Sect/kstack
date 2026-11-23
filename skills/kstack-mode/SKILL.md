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
- **A choice an experiment can settle:** try it and recommend from what you observed instead of asking.
- **Every subagent brief** starts with `Read ${CLAUDE_SKILL_DIR}/worker.md before anything else.`, then the goal, the scope and how to check the result.
- **Commits:** small and ordered so the history proves itself (Verifiable Steps). Never push without a yes.

## Principles

Each principle is a skill file at `${CLAUDE_SKILL_DIR}/../principle-<name>/SKILL.md`. Read the file in full before you apply it; do not invoke it as a skill. In your reply, name each principle that changed a decision and what it changed.

- **prove-it-works.** Before calling anything done.
- **fix-root-causes.** Debugging.
- **attack-the-premise.** Two or more fixes on the same assumption failed the same check.
- **smallest-change.** Sizing a diff, refactoring, tempted to add a layer or option.
- **verifiable-steps.** Multi-step work and splitting commits.
- **explain-the-number.** Before measuring, and before reporting or acting on a number.
- **encode-lessons-in-structure.** The same correction comes up twice.
- **proceed-on-reversible-work.** Tempted to ask "should I do X?" about something reversible.

## Playbooks

Match the task to one playbook in `${CLAUDE_SKILL_DIR}/playbooks/`, read it, and copy its steps into your todo list.

- `investigation.md`: a question about how or why something works. Read-only.
- `bug-fix.md`: something behaves wrong.
- `feature.md`: new behavior or a change in behavior.

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
