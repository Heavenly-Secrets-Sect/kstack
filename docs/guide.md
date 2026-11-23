# Using kstack

A practical guide: which command to reach for, what a good run looks like, and how to extend kstack.

## Pick the command

| Situation | Command |
|---|---|
| Any real task you want done carefully | `/kstack:kstack-mode <task>` |
| The task is vague and you want a better prompt before anything runs | `/kstack:sharpen <task>` |
| You want the agent to show it understood before it starts | `/kstack:in-your-own-words <task>` |
| You want one specific lens on the current work | `/kstack:principle-<name>` |

`kstack-mode` stays active for the rest of the session once invoked, so follow-up requests in the same session are handled the same way.

## What kstack-mode does

1. **Restates the goal** and the smallest change that meets it, and names the playbook it picked.
2. **Routes** the task to one of five playbooks:

   | Playbook | Use when | Produces |
   |---|---|---|
   | investigation | "How/why does X work?" | A cited answer. No code changes |
   | bug-fix | Something behaves wrong | A failing repro first, then the fix |
   | feature | New or changed behavior | Design, small commits, verification |
   | refactoring | Structure changes, behavior must not (including replacing an internal API) | A behavior pin, then subtraction, then reshape |
   | multi-phase-plan | A migration or rewrite too big for one change | A plan file. No code until you say go |

3. **Reads the principles** the playbook names before applying them, and tells you which principle changed which decision.
4. **Delegates** code to `kstack-worker` agents (separate worktrees when two would touch the same files) and has a fresh `kstack-verifier` check the result. The verifier is read-only and never fixes anything.
5. **Proves the result** on the real artifact (tests, a repro, a run) and pastes the evidence.
6. **Commits small, never pushes** without asking.

## Principles

| Group | Principles |
|---|---|
| Core | `smallest-change`, `attack-the-premise` |
| Design | `foundational-thinking`, `model-the-domain`, `type-system-discipline`, `boundary-discipline`, `minimize-reader-load`, `redesign-from-first-principles`, `exhaust-the-design-space` |
| Operations and migration | `make-operations-idempotent`, `separate-before-serializing-shared-state`, `migrate-callers-then-delete-legacy-apis`, `outcome-oriented-execution` |
| Verification | `prove-it-works`, `fix-root-causes`, `test-behavior-not-implementation`, `verifiable-steps`, `explain-the-number` |
| Delegation | `guard-the-context-window`, `build-the-lever`, `proceed-on-reversible-work` |
| Meta | `encode-lessons-in-structure` |

Calling one directly is useful as a review lens, for example:

- `/kstack:principle-explain-the-number` before reporting an F1 score or a speedup.
- `/kstack:principle-make-operations-idempotent` while designing a cron job or webhook handler.
- `/kstack:principle-test-behavior-not-implementation` on a test file you are about to keep.

## Autonomy

- Reversible work (editing, local commits) proceeds without asking.
- Pushing, deploying, deleting data and messaging people always wait for your yes.
- Say "run until done" or "I'm going to bed" to keep it going until one of those gates.

## Good habits

- Start a fresh session per task. Long sessions dilute the mode's instructions.
- If a repo has a way to drive the real app, wrap it in a project skill named `verify-<app>`. The mode uses it automatically for proof.
- When you correct the agent twice the same way, encode the lesson: a test, lint, hook or a sharper rule in kstack. Do not just repeat yourself.

## Extending kstack

1. Add `skills/principle-<name>/SKILL.md` with `disable-model-invocation: true`, a `# Title` line and a description that says when it applies.
2. Add one line to the index in `skills/kstack-mode/SKILL.md`, and mention it in the playbook steps where it matters.
3. Add a scenario to `scripts/check_routing.py` that should route to it, then run:

   ```bash
   python3 scripts/check_routing.py --only <scenario>
   python3 scripts/check_routing.py          # all scenarios, before committing
   ```

4. If the change affects `sharpen`, rerun `claude plugin eval . --runs 2 --no-publish`.
5. If it affects agents, `worker.md`, commits or the verifier rule, run `python3 scripts/check_e2e.py`.

## The three test layers

| Layer | What it checks | Command |
|---|---|---|
| Evals | A skill's output meets its criteria, compared with no plugin | `claude plugin eval . --runs 2 --no-publish` |
| Routing | The mode picks the right playbook and reads the right principles (plan only) | `python3 scripts/check_routing.py` |
| End to end | Real edits and commits; the outcome is checked by running the code; verifier rule; no git changes by subagents; no push | `python3 scripts/check_e2e.py` |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `/kstack:...` not found | Run `/reload-plugins`; check `claude plugin list` shows `kstack@skills-dir ✔ loaded` |
| The model does not see kstack skills | Expected: they are hand-invoked only (`disable-model-invocation: true`) |
| The mode skips principles | Run `scripts/check_routing.py`; if a scenario fails, inspect its stream with `--keep` |
| A verifier changed git state | It must not. Report it and tighten `agents/kstack-verifier.md` |
| The mode skipped the verifier | Allowed only for one file and about 20 lines, and the reply must say so |
