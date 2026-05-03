# Project handoff

## Version

v0.3.4 architecture deepening.

## Goal

Deployable Codex skill for compact long-run scaffolding.

Outcome: target repos get enough structure for planning, long execution, recovery, closeout, validation, and review freeze without document bloat or doc pollution.

## Architecture

```text
CONTEXT.md                 # domain glossary
SKILL.md                   # compact agent-facing workflow
assets/templates/          # generated runtime docs
scripts/runtime_layout.py  # target output paths
scripts/artifacts.py       # template render and protected writes
scripts/review_reports.py  # review report input validation
scripts/                   # artifact helpers
references/                # optional detail, loaded on demand
docs/PROJECT.md            # this handoff
```

## Target repo output

Default:

```text
docs/agent/longrun/LONGRUN.md
docs/agent/longrun/STATE.md
```

Review freeze creates `docs/agent/longrun/REVIEW.md` and `docs/agent/longrun/reviews/*`. Strict profile adds one `docs/agent/longrun/STRICT.md` appendix.

## Lifecycle

```text
plan -> longrun -> closeout
```

Plan owns current state, target goal, source docs, blockers, and validation gates.

Longrun owns milestone execution and current `STATE.md`.

Closeout owns final status, validation, open risks, handoff, and next resume action. User stop, pause, interrupt, or closeout request enters closeout immediately.

## Boundaries

Scripts create artifacts. Humans or Codex decide next actions from those artifacts.

Scripts may:

- create compact runtime docs
- inspect visible project files
- read git metadata
- normalize review JSON

HITL owns:

- secrets, production, deployment, remote writes
- sandbox and approval changes
- destructive commands
- product, security, data, architecture, UX judgment

Script location: skill repo owns scripts. Target repo owns generated docs. Target-repo docs use:

```text
invoke $codex-longrun-kit normalize review feedback
```

## Roadmap

- v0.3: compact default output, one project handoff doc.
- v0.3.1: fix target-repo / script-location mismatch.
- v0.3.2: rewrite language layer for dense operational instructions.
- v0.3.3: namespace runtime docs under `docs/agent/longrun/`; add plan / longrun / closeout lifecycle.
- v0.3.4: deepen runtime layout, artifact writing, and review report input modules.
- v0.4: optional review-report schema validation.
- v0.5: optional worktree patch-ticket workflow.

## Validation

```bash
python -m unittest discover -s tests
```

## Known limits

- Stack detection is heuristic.
- Review normalization is heuristic.
- Review report validation covers schema required fields and severity enum.
- Freeze metadata records state; git remains mutable.
- Plan review still gates long execution.
