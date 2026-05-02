# Sample long-running task brief

Migrate the legacy report generator to the new event schema.

Goals:

- Update the parser to read the new schema.
- Preserve the existing public report API.
- Add regression tests for old and new schema examples.
- Produce a review packet after implementation.

Non-goals:

- Do not change billing logic.
- Do not deploy.
- Do not introduce new dependencies without approval.
