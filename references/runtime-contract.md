# Runtime contract

Default generated docs are intentionally small.

## `LONGRUN.md`

Canonical task contract:

- goal
- done criteria
- non-goals
- hard constraints
- milestones
- stop rules
- validation gates

## `STATE.md`

Current handoff snapshot:

- current milestone
- current status
- next action
- decisions
- last validation
- open questions
- working set

Keep `STATE.md` under about 80 lines. It is a snapshot, not a log.

## `REVIEW.md`

Created only at review freeze. It describes the frozen version and review protocol. It is not a review verdict.

## `STRICT.md`

Created only in strict profile. It adds extra stop guidance and validation cost policy without splitting into multiple files.
