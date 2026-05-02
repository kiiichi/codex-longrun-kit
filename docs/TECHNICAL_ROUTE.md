# Technical route

## v0.1 baseline

- Root-level Codex skill.
- Templates for task contract, plan, implementation, continuity, stop rules, validation, review packet.
- Scripts for initialization, review freeze, and review normalization.

## v0.2 route

Reduce default runtime docs:

```text
LONGRUN.md = task contract + milestones + execution rules + stop rules + validation gates
STATE.md   = compact handoff ledger
REVIEW.md  = lazy review freeze artifact
```

Add profiles:

```text
minimal  -> LONGRUN.md + STATE.md
standard -> LONGRUN.md + STATE.md, review docs lazy
strict   -> standard + STOP_RULES.md + VALIDATION_MATRIX.md
```

## Future route

v0.3 candidates:

- `--update-agents` option to add a short `## Codex long-run` block to target repo `AGENTS.md`.
- `--ticket RQ-001` patch-worker prompt generator.
- Better semantic conflict detection in review normalization.
- Optional GitHub issue creation for ReviewQueue tickets.
- Optional worktree command generation for parallel patch workers.

## Constraints

- Python scripts must use only the standard library.
- Generated files must be safe to commit.
- Default templates must avoid secrets, external network, and approval changes.
- The skill must be useful even when GitHub CLI is unavailable.
