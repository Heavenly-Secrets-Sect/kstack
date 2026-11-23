---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Apply when replacing an internal API, function, module or data format while old callers still exist. Move every caller and delete the old version in the same change instead of keeping a compatibility layer."
disable-model-invocation: true
---

# Migrate Callers, Then Delete Legacy APIs

When you introduce a new internal API, finish the job in one wave:

- Find every caller with search, including strings, configs, docs and tests, not only imports.
- Move each caller to the new API.
- Delete the old API, its shims and its now-dead tests. Update tests to assert the new contract.
- Confirm no references remain, by search and by running the full checks.

No parallel old and new paths "for now", and no deprecated wrapper left behind.

This applies when nothing outside the repo depends on the old API. If external users do, keep the old API, mark it deprecated with a removal plan, and say so explicitly.
