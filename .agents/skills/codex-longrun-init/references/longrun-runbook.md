# Long-run runbook reference

## Purpose

A long-running Codex task should be treated as a delegated execution unit with an explicit operating contract.

## Minimal operating system

The target repository should contain:

- task contract
- milestone plan
- implementation runbook
- continuity ledger
- validation matrix
- stop rules
- review packet
- review queue

## Good long-run behavior

- Work one milestone at a time.
- Keep diffs scoped.
- Validate after each milestone.
- Repair validation failures before moving on.
- Record decisions and validation evidence.
- Stop at human decision points.
- Prepare a review packet before repair feedback.

## Bad long-run behavior

- Editing broadly without a milestone.
- Treating a vague chat message as the only source of truth.
- Running a dev server in the foreground and blocking.
- Saying validation passed without running it.
- Fixing all review comments as one coupled task.
- Using parallel writers in the same worktree.
