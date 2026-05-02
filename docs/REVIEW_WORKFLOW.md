# Review workflow

## Goal

Move human review from frequent interruptions to a concentrated, independent, structured batch.

## Flow

```text
long run
  ↓
freeze commit
  ↓
ReviewPacket.md
  ↓
independent review files
  ↓
ReviewQueue.json
  ↓
ticketed fixes
```

## Review freeze rules

When review starts:

- stop modifying product code
- record the commit SHA
- record diffstat and changed files
- record validation results
- give every reviewer the same frozen artifact

## Independent review lanes

Suggested lanes:

- security
- architecture
- tests
- UX / visual behavior
- performance
- maintainability
- product behavior
- documentation

Each reviewer should write only one file under `docs/reviews/pending/`.

## Review item schema

See:

```text
.agents/skills/codex-longrun-init/assets/templates/review-item.schema.yaml
```

Every item should include:

- stable id
- severity
- claim
- evidence
- affected files
- acceptance criteria
- validation commands
- whether a human decision is required

## Normalization rules

The normalizer should:

- merge obvious duplicates
- preserve source review ids
- flag human decisions
- flag potential conflicts
- split broad review feedback into atomic tickets when possible
- avoid modifying code

## Repair rules

Do not ask Codex to “fix all review feedback” as one task.

Use one ticket at a time:

```text
Address exactly one review ticket: RQ-001.
```

For independent tickets, use one branch/worktree per ticket.
