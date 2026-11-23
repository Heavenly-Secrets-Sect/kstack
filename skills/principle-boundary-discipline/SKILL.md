---
name: principle-boundary-discipline
description: "Apply when wiring validation, error handling or framework adapters. Validate and handle errors where data enters the system; trust types inside; keep business logic in pure functions behind a thin shell."
disable-model-invocation: true
---

# Boundary Discipline

Validate, convert and handle errors where data crosses into the system: CLI arguments, config files, HTTP requests, external APIs, queues, the database. Inside, trust the types. No re-validation and no defensive null checks on values that cannot be null.

Convert raw input into domain types at the edge, and keep framework and transport types (request objects, ORM rows, SDK responses) out of the core. Business logic lives in pure functions with no framework imports; the handler, job or CLI command that calls them stays thin.

Two questions for any check or try/except: is this data crossing a boundary right now? If not, the check is noise. Could this logic be a pure function the shell just calls? If so, extract it.
