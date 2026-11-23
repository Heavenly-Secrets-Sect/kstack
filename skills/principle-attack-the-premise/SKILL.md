---
name: principle-attack-the-premise
description: "Apply when two or more fixes built on the same assumption have failed the same check. Write the assumption down and test it before trying another fix."
disable-model-invocation: true
---

# Attack the Premise

When several fixes fail the same way, suspect what they all assumed, not each fix.

- Write the shared assumption as one sentence.
- Find an observation that would come out differently if it were false, and make it. Look at where failures cluster, not only how big they are.
- If the evidence breaks the assumption, look for what the failures share that it did not predict.

No new fix until the premise is written down and tested.
