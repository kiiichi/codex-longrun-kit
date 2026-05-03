# Project handoff

## Version

v0.3.2 language compact.

## Goal

Deployable Codex skill for compact long-run scaffolding.

Outcome: target repos get enough structure for long execution, recovery, validation, and review freeze without document bloat.

## Architecture

```text
SKILL.md                  # compact agent-facing workflow
assets/templates/         # generated runtime docs
scripts/                  # artifact helpers
references/               # optional detail, loaded on demand
docs/PROJECT.md           # this handoff
```

## Target repo output

Default:

```text
docs/agent/LONGRUN.md
docs/agent/STATE.md
```

Review freeze creates `REVIEW.md` and `docs/reviews/*`. Strict profile adds one `STRICT.md` appendix.

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
- v0.4: optional review-report schema validation.
- v0.5: optional worktree patch-ticket workflow.

## Validation

```bash
python -m unittest discover -s tests
```

## Known limits

- Stack detection is heuristic.
- Review normalization is heuristic.
- Freeze metadata records state; git remains mutable.
- Plan review still gates long execution.
