# Worktree strategy reference

Use worktrees only after review feedback has been normalized into independent tickets.

## Recommended flow

```text
ReviewQueue.json
  ↓
select independent tickets
  ↓
one worktree per ticket
  ↓
patch + validate
  ↓
merge queue
```

## Avoid

- many patch agents in the same worktree
- parallel changes to the same files
- repairing unrelated tickets in one patch
- merging before validation evidence exists

## Ticket status files

Each ticket can write:

```text
docs/reviews/status/RQ-001.md
```

Include:

- files changed
- validation run
- result
- residual risk
- source review ids addressed
