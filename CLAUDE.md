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
- A new principle also needs a line in the index in `skills/kstack-mode/SKILL.md`.
- When an agent repeats a mistake, fix it with structure first (tool limits, a specific rule with an alternative), then wording. Example: the verifier once ran `git checkout`, so it now has an explicit ban with the alternative spelled out.

## Checks before committing

```bash
claude plugin validate .                        # structure is valid
claude plugin details kstack@skills-dir         # per-session token cost (about 850 now)
claude -p "/kstack:<skill> <sample task>"       # try a skill from a scratch directory
claude plugin eval . --runs 2 --no-publish      # evals, with a no-plugin baseline
```

After changing a skill that has evals, rerun them (`--case <name>`). The with-plugin score must not drop.

## Commits

Small commits, one step each, each leaving the repo working. The repo identity is `KiRzEa <kietnt0603@gmail.com>`, set in the local git config. Never push without a yes.
