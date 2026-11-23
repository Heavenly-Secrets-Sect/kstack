---
name: principle-explain-the-number
description: "Apply before you measure, and before you report or act on a measured number: a speedup, latency, accuracy, F1 or eval score. Know what limits it and rule out that it measured something else."
disable-model-invocation: true
---

# Explain the Number

- Before running, write the decision the number feeds, the result that would change it, and the noise level. An effect smaller than run-to-run spread is not a result.
- Ask why it is not twice as good. Name what bounds it, from evidence gathered during the run, not from reading code.
- List what else it could be measuring (errors, skipped or cached work, code that never ran, data leakage, an untuned baseline, a lucky seed) and rule each out.
- Report the number with its run count, spread and limiting factor.
