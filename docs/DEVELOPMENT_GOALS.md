# Development goals

## Primary objective

Create a Codex skill that turns a target repo into a compact long-run workspace with enough state, validation, review, and recovery structure for multi-hour Codex tasks.

## Non-goals

- Build a full autonomous agent runtime.
- Bypass approval or sandbox policy.
- Replace human architectural/product review.
- Generate large process manuals in every target repo.
- Force one workflow on all projects.

## Success criteria

- The skill can be installed via `npx skills@latest add kiiichi/codex-longrun-kit -a codex -g`.
- A user can invoke `$codex-longrun-kit` and receive a small, readable long-run scaffold.
- New Codex threads can resume by reading `LONGRUN.md` and `STATE.md`.
- Review feedback can be collected independently and normalized into atomic tickets.
- Default generated docs remain small enough to actually read.

## Design pressure

The project balances two opposing needs:

1. Long-running Codex needs external state, stop rules, validation, and reviewability.
2. Too many files and too much text reduce effective agent attention.

v0.2 resolves this by defaulting to compact runtime docs and using lazy expansion for review and strict audit modes.
