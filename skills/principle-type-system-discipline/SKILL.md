---
name: principle-type-system-discipline
description: "Apply when designing types or function signatures, in typed languages or typed Python. Make illegal states unrepresentable, give distinct meanings distinct types, parse external data at the boundary, handle every variant."
disable-model-invocation: true
---

# Type System Discipline

Let the type checker reject impossible states, mixed-up values and unhandled cases.

- **Illegal states unrepresentable.** Prefer a tagged union or enum with per-variant data over optional fields that are only valid together.
- **Distinct meanings, distinct types.** If two values share a primitive type but mean different things (user id vs order id, seconds vs milliseconds), give each its own type and validate it once when it is created.
- **External data is untyped until parsed.** JSON, API responses, CLI arguments, config, environment variables and database rows pass through one parse function at the boundary that returns the typed model.
- **One source for each shape.** When a schema (OpenAPI, protobuf, SQL, pydantic) owns a shape, derive the type from it instead of writing a parallel one by hand.
- **Exhaustive handling.** Match on every variant and make the checker fail when a new one is added.
