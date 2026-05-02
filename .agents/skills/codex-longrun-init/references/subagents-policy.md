# Subagents policy reference

## Default

Use subagents only for read-only work unless the user explicitly requests isolated patch workers.

## Good subagent tasks

- codebase exploration
- log analysis
- test failure triage
- security review
- architecture review
- UX/visual review
- performance review
- feedback normalization

## Risky subagent tasks

- multiple agents editing the same files
- broad refactors
- product decisions
- changes that require approvals
- work that cannot be validated independently

## Patch subagents

Only use patch subagents when:

- each ticket is atomic
- each ticket has acceptance criteria
- each ticket has validation commands
- each worker has an isolated branch or worktree
- merge order is explicit
