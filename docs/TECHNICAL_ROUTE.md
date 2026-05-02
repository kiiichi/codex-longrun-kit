# Technical route

## v0.1: Single initialization skill

Target:

- one skill: `codex-longrun-init`
- one initialization script
- one stack detection script
- review freeze script
- review normalization script
- stable documentation

Rationale:

The user value comes first from reducing setup friction and making long-run state durable. Complex automation can wait.

## v0.2: Better validation and schema checks

Potential work:

- JSON Schema for `ReviewQueue.json`
- stricter validation for review YAML
- template snapshot tests
- richer stack detection
- clearer generated `Plan.md` milestone examples

## v0.3: Split workflow skills

Potential separate skills:

- `codex-longrun-plan`
- `codex-longrun-execute`
- `codex-longrun-freeze-review`
- `codex-longrun-normalize-feedback`

Rationale:

A single init skill is easier to install. Separate skills may be clearer once the workflow is used often.

## v0.4: Worktree-aware repair flow

Potential work:

- create a branch/worktree for each independent review ticket
- track ticket status under `docs/reviews/status/`
- generate merge guidance
- detect changed-file overlap before patching

## v0.5: Plugin packaging

Potential work:

- package skill set as a plugin
- add release metadata
- document install/update lifecycle
- optionally integrate with richer tools

## Explicit deferrals

- No autonomous deployment.
- No automatic sandbox/approval modification.
- No background daemon.
- No database.
- No default write-capable subagents.
