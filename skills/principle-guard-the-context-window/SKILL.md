---
name: principle-guard-the-context-window
description: "Apply when context is filling up or about to: large outputs, long files, repeated reads, many search results, planning a fan-out. Send bulk work to subagents and keep only conclusions in the main thread."
disable-model-invocation: true
---

# Guard the Context Window

A full context degrades reasoning, triggers lossy compaction and stalls progress. Treat it as a budget.

- Read the part you need: search first, then read a line range, not the whole file. Do not reread a file you already have.
- Cap command output with filters, `head`, `tail` or counts. Write large output to a file and read only what you need from it.
- Send wide searches, log dives and bulk reading to a subagent and ask for a conclusion of bounded length, not the raw material.
- Hand subagents file paths, not pasted contents.
- Size phases of long work so each fits comfortably, and write durable state (plans, findings) to files rather than relying on the conversation.
