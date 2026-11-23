# kstack

A Claude Code plugin holding a workflow for coding with agents, learned from Lauren Tan's pstack (reference: `github.com/cursor/plugins/tree/main/pstack`). This file holds the rules for **editing kstack itself**; it does not ship to plugin users.

`~/.claude/skills/kstack` is a symlink to this repo, so Claude Code loads kstack as `kstack@skills-dir`. Run `/reload-plugins` after editing.

## Language

Write everything in English: skills, agents, playbooks, docs, code comments and commit messages. `README.vi.md` is the one Vietnamese file; update it whenever `README.md` changes. Eval prompts may be in Vietnamese on purpose, to test Vietnamese input.

## Two layers

- **Core** (`in-your-own-words`, `sharpen`, `principle-*`): agent-neutral, with no tool names or agent-specific paths.
- **Orchestration** (`kstack-mode` with its `worker.md` and `playbooks/`, plus `agents/`): written for Claude Code, using real tool names.

## Writing skills

- One idea per skill, kept short: about 10 lines for a principle, under 25 for a playbook.
- Default to `disable-model-invocation: true`. The Skill tool refuses such skills, so the mode reads them by path: `${CLAUDE_SKILL_DIR}/../<name>/SKILL.md`.
- `${CLAUDE_SKILL_DIR}` and `$ARGUMENTS` are substituted only in `SKILL.md`, not in playbooks or `worker.md`.
- Rewrite ideas in your own words; do not copy pstack text. Anything copied must carry pstack's MIT notice.
- A new principle needs a `# Title` line, a line in the index in `skills/kstack-mode/SKILL.md`, a mention in the playbook steps where it matters, and a routing scenario in `scripts/check_routing.py`.
- When an agent repeats a mistake, fix it with structure first (tool limits, a specific rule with an alternative), then wording. Example: the verifier once ran `git checkout`, so it now has an explicit ban with the alternative spelled out.

## Checks before committing

```bash
claude plugin validate .                        # structure is valid
claude plugin details kstack@skills-dir         # components; hand-invoked skills are not shown to the model
claude -p "/kstack:<skill> <sample task>"       # try a skill from a scratch directory
claude plugin eval . --runs 2 --no-publish      # evals, with a no-plugin baseline
python3 scripts/check_routing.py                # every scenario must route to its playbook and principles
python3 scripts/check_e2e.py                    # real runs; outcome, verifier rule and git safety checked
python3 -m unittest discover -s tests           # hook unit tests
```

Which layer to run: `sharpen` changes need the evals; mode, playbook or principle changes need the routing check; agent, `worker.md`, commit or verifier rule changes need the end-to-end check. LLM runs vary, so run a check twice before trusting a pass. When a check fails, first confirm the check itself is right by re-grading a kept run (`--keep`) offline.

After changing a skill that has evals, rerun them (`--case <name>`). The with-plugin score must not drop.

## Hooks

`hooks/hooks.json` registers `hooks/guard_push.py` (PreToolUse, Bash): a command that runs `git push` gets "ask". Only modes that show prompts (default, acceptEdits, plan) actually ask; bypassPermissions and auto approve it silently, measured. Denying in those modes worked (commit 5f0d7a1) but is off until it is wanted globally. A changed script takes effect on its next call; a changed `hooks.json` needs a new session. It applies in every session where kstack is enabled, not only during kstack-mode. Change the detector only with a unit test in `tests/test_guard_push.py` for the new case.

## Commits

Small commits, one step each, each leaving the repo working. The repo identity is `KiRzEa <kietnt0603@gmail.com>`, set in the local git config. Never push without a yes.
