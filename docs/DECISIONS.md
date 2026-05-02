# Design decisions

## D1 — Compact runtime docs by default

Decision: default generated target docs are `LONGRUN.md` and `STATE.md`.

Reason: many separate process files can reduce agent attention, create stale-state conflicts, and make handoff harder rather than easier.

Consequence: stop rules and validation gates live inside `LONGRUN.md` unless `--profile strict` is used.

## D2 — Lazy review docs

Decision: `REVIEW.md`, `docs/reviews/pending/`, and ReviewQueue files are created during review freeze, not during initialization.

Reason: review artifacts are irrelevant before implementation and add noise if created too early.

Consequence: `freeze_review.py` is the transition point from implementation to review.

## D3 — No default write-code subagents

Decision: the skill recommends read-only subagents by default and patch subagents only after ReviewQueue tickets exist.

Reason: parallel write-code agents increase merge conflicts and semantic coupling unless tickets are isolated.

Consequence: subagent/worktree guidance lives in references, not runtime docs.

## D4 — Deterministic scripts, not generated code

Decision: file generation and review normalization are scripts.

Reason: deterministic operations are safer, shorter, and easier to test than asking the model to regenerate boilerplate each time.

Consequence: scripts use only Python standard library and are covered by basic tests.
