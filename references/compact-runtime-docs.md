# Compact runtime docs

Long-running Codex work needs external state, but each run should read the minimum useful state.

## Default

```text
LONGRUN.md = stable task contract, milestones, stop rules, validation gates
STATE.md   = current handoff snapshot
```

## Lazy

```text
REVIEW.md             created at review freeze
docs/reviews/pending created at review freeze
ReviewQueue.json      created after independent reviews
```

## Strict only

```text
STOP_RULES.md
VALIDATION_MATRIX.md
```

## File length budgets

- `LONGRUN.md`: target under 200 lines.
- `STATE.md`: target under 80 lines.
- `REVIEW.md`: target under 150 lines before reviewer reports.

If a file grows past its budget, compress it instead of creating another always-read file.
