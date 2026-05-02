# Subagents and worktrees

## Default

No write-code subagents during the main implementation loop.

## Good subagent uses

- Read-only codebase exploration.
- Test failure analysis.
- Log summarization.
- Security review.
- Architecture review.
- UX / visual review.
- Feedback normalization.

## Patch subagents

Use patch subagents only after review feedback is normalized into independent tickets.

Recommended shape:

```text
one ReviewQueue ticket -> one worktree -> one patch worker
```

Never let multiple write-code agents modify the same working tree unless the changes are read-only or explicitly coordinated.
