---
name: sharpen
description: "Rewrite a task prompt so it asks for a deeper result, not a bigger one. Use for /sharpen. It rewrites the prompt and does not do the task."
argument-hint: "<the task or prompt to sharpen>"
disable-model-invocation: true
---

# Sharpen

Here is a task I am about to hand to an agent:

$ARGUMENTS

If no task appears above, use my most recent request in this conversation.

I want this done more deeply, not more broadly. Do not start the task. First answer these briefly, specific to this task:

1. **Expert gap.** What would a top practitioner in this field do here that my prompt does not ask for?
2. **Raw material.** What primary source would they start from (the code, logs, data, spec or paper) instead of a summary or my description of it?
3. **Methods.** Which concrete methods, tools or commands would they reach for?
4. **Independent evidence.** What, other than the agent's word or mine, would show the result is right: a test, a measurement, a reproduction, a baseline?

Then rewrite my prompt to ask for exactly that. The rewritten prompt:

- Keeps my goal and scope. It adds depth, not features.
- Tells the agent to settle any choice an experiment can settle by trying it, then recommend from what it observed.
- Leaves product, taste and priority choices to me, listed as open questions.
- States how the agent will prove the work is done.

Reply with the four answers in a few lines, the rewritten prompt in a fenced block, then the open questions. Write in the language I used. Stop there and wait for me.
