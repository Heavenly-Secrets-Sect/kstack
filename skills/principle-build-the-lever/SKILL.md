---
name: principle-build-the-lever
description: "Apply to non-trivial edits, migrations, analyses or checks. Build the small tool that does or proves the work (a script, codemod, generator or rerunnable check) instead of doing it by hand."
disable-model-invocation: true
---

# Build the Lever

When work is not trivial, write the tool that does it or proves it, rather than doing it by hand. The bar is triviality, not repetition: skip the tool only for a couple of obvious edits.

- Do the first unit by hand, then write the tool and prove it by rerunning it on that unit. Make it safe to run twice.
- A deterministic script beats fanning out to many agents. When you do fan out, write the recipe and its verification check down once, as a file every delegate reads.
- Applying this leaves a file in the diff: a script, codemod, generator or check. If there is none, you did not apply it. Commit it if the work outlives the session.
- Build the smallest script that does the job, never a framework.
