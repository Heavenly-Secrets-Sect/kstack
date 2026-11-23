<p align="center"><img src="assets/icon.png" width="128" alt="kstack"></p>

# kstack

**English** · [Tiếng Việt](README.vi.md)

A workflow for coding with agents in Claude Code, packaged as a plugin: small skills you invoke by hand, principles as leaf skills, a mode skill that routes work by task type, and the habit of proving every change works before calling it done.

Inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan ([@poteto](https://github.com/poteto)). pstack is written for Cursor; kstack learns from its ideas and rewrites them in its own words for Claude Code rather than copying them.

> **Status:** the shared workflow (A1–A5) is in place. Per-project integration is next.

## Usage

| Command | What it does |
|---|---|
| `/kstack:kstack-mode <task>` | Work in kstack style: restate the goal, pick a playbook (investigation, bug fix, feature, refactoring, multi-phase plan), apply the principles, delegate to `kstack-worker`, have a fresh `kstack-verifier` check the result, commit in small steps, never push without asking |
| `/kstack:sharpen <task>` | Rewrite a prompt so the task goes deeper, not bigger, then stop for your review |
| `/kstack:in-your-own-words <task>` | Play back the goal, problem, scope and plan before starting |
| `/kstack:principle-<name>` | Apply a single principle, e.g. `principle-explain-the-number` before reporting a number |

22 principles in six groups (core, design, operations and migration, verification, delegation, meta). See the [guide](docs/guide.md) for the full list, when each applies and how to extend kstack.

## Core ideas

- **Go deep first, then go fast.** Less code, higher quality.
- **Agents must prove their own work.** Without a way to verify, the human becomes the bottleneck.
- **Encode lessons in structure.** When you correct an agent, prefer a type, lint, test or hook over another line of instructions.
- **Trust before parallelism.** Raise autonomy only once verification is solid.

## Layout

Two layers:

| Layer | Contains | Written as |
|---|---|---|
| Core | `in-your-own-words`, `sharpen`, `principle-*` | Agent-neutral: no tool names or agent-specific paths, so other agents can reuse them |
| Orchestration | `kstack-mode`, playbooks, `worker.md`, agents, hooks | Specific to Claude Code |

Almost every skill sets `disable-model-invocation: true`: it runs only when you call it (`/kstack:<name>`), never on the model's initiative.

```
kstack/
├── .claude-plugin/plugin.json   # plugin manifest
├── skills/
│   ├── in-your-own-words/       # core
│   ├── sharpen/                 # core
│   ├── principle-*/             # core: 22 principles as leaf skills
│   └── kstack-mode/             # orchestration
│       ├── SKILL.md             #   non-negotiables, principle index, autonomy, subagents
│       ├── worker.md            #   rules every subagent brief makes it read first
│       └── playbooks/           #   investigation, bug-fix, feature, refactoring, multi-phase-plan
├── agents/
│   ├── kstack-worker.md         # writes code from a brief
│   └── kstack-verifier.md       # independent, read-only check (no Edit/Write)
├── hooks/                       # PreToolUse guard: asks before any `git push`
├── tests/                       # unit tests for the hook
├── evals/                       # skill evals, run with `claude plugin eval`
├── scripts/check_routing.py     # checks the mode routes tasks to the right playbook and principles
├── scripts/check_e2e.py         # runs the mode for real and checks the outcome independently
├── docs/guide.md                # how to use and extend kstack
├── assets/                      # icon and the script that draws it
└── CLAUDE.md                    # rules for editing kstack itself
```

## Install

**Local development** (current setup): the repo lives at `~/Desktop/Workspace/kstack` and `~/.claude/skills/kstack` is a symlink to it. Claude Code loads it automatically as `kstack@skills-dir`.

```bash
ln -s ~/Desktop/Workspace/kstack ~/.claude/skills/kstack
```

Edit files in the repo, then run `/reload-plugins` in a Claude Code session.

**Try it once without installing:**

```bash
claude --plugin-dir /path/to/kstack
```

Marketplace installation will be available once the repo adds `.claude-plugin/marketplace.json`.

## Checks

```bash
claude plugin validate .                  # plugin structure is valid
claude plugin list                        # should show kstack@skills-dir ✔ loaded
claude plugin details kstack@skills-dir   # components and per-session token cost
claude plugin eval . --runs 2 --no-publish   # evals, with a no-plugin baseline
python3 scripts/check_routing.py          # routing: 8 scenarios, playbook and principles read
python3 scripts/check_e2e.py              # end to end: real edits and commits, outcome checked by running the code
python3 -m unittest discover -s tests     # hook unit tests
```

## Enforced, not just asked

kstack ships one hook. Any Bash call that runs `git push` gets a permission prompt, so "never push without a yes" no longer depends on the model remembering it. Measured headless: without the hook a push in bypass mode reached the remote; with it, the push was stopped in both default and bypass mode. The verifier's lack of Edit and Write tools is the other structural guard.

## Roadmap

- [x] **A1.** Hand-invoked skills: `in-your-own-words`, `sharpen`
- [x] **A2.** 8 principles as leaf skills
- [x] **A3.** `kstack-mode`: non-negotiables, principle index, playbooks (bug-fix, feature, investigation)
- [x] **A4.** `worker.md` and two agents, `kstack-worker` and `kstack-verifier`
- [x] **A5.** Evals for `sharpen`: 1.00 with kstack versus 0.43 and 0.67 without (2 cases, 2 runs each)
- [x] **A6.** 14 more principles (design, operations and migration, delegation, testing), refactoring and multi-phase-plan playbooks, a routing check (8/8 scenarios) and an end-to-end check (2/2)
- [x] **A7.** Push guard hook with unit tests and a controlled experiment; the verifier now refuses to work without `worker.md`

Next is per-project integration: verification skills, lint/typecheck hooks, a fresh verifier per PR, then gradually more autonomy.

## Credits

Ideas and structure come from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, released under the MIT License. Any passage in kstack copied or adapted from pstack's text must keep pstack's original MIT copyright notice.
