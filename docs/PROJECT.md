# Project handoff

## Current version

v0.3 compact architecture.

## Goal

Create a deployable Codex skill that initializes repositories for long-running, reviewable Codex tasks while avoiding document bloat.

## Architecture

```text
SKILL.md                  # compact agent-facing workflow
assets/templates/         # generated runtime docs
scripts/                  # deterministic helpers
references/               # optional detail, loaded on demand
docs/PROJECT.md           # this project handoff doc
```

## Runtime output

Default generated files in a target repo:

```text
docs/agent/LONGRUN.md
docs/agent/STATE.md
```

Review files are created only at review freeze. Strict detail is one optional `STRICT.md` appendix.

## Boundaries

Scripts may create docs, inspect visible project files, read git metadata, and normalize review JSON. They must not run project tests, install dependencies, access secrets, deploy, or modify product code.

`REVIEW.md` is a protocol for frozen-version review. It is written for human reviewers and optional read-only review agents. It is not Codex self-approval.

## Roadmap

- v0.3: compact default output, safer script language, one project handoff doc.
- v0.4: optional schema validation for review reports.
- v0.5: optional worktree patch-ticket workflow.

## Validation

```bash
python -m unittest discover -s tests
```

## Known limits

- Stack detection is heuristic.
- Review normalization is heuristic.
- Freeze scripts record metadata but cannot truly prevent later code changes.
- Generated docs still require plan review before long execution.
