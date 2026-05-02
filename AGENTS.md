# Agent instructions for codex-longrun-kit

This repository is itself a Codex Skill kit. Future Codex threads should treat project documentation as the source of truth.

## Start here

Before changing code, read these files in order:

1. `README.md`
2. `docs/PROJECT_STATE.md`
3. `PROJECT.md`
4. `docs/ARCHITECTURE.md`
5. `.agents/skills/codex-longrun-init/SKILL.md`
6. `docs/TECHNICAL_ROUTE.md`

## Current objective

Improve a skill named `codex-longrun-init` that initializes target repositories for long-running Codex tasks. The skill should create a durable scaffold around task contract, milestone plan, execution runbook, continuity ledger, validation matrix, stop rules, review packet, and feedback normalization.

## Development rules

- Keep v0.1 simple: skill folder + templates + Python scripts + docs.
- Do not introduce a daemon, database, MCP server, or plugin packaging unless explicitly requested.
- Prefer standard-library Python. `PyYAML` may be used when available for YAML review files.
- Do not change the generated file contract without updating:
  - `.agents/skills/codex-longrun-init/SKILL.md`
  - templates in `assets/templates/`
  - `README.md`
  - `docs/PROJECT_STATE.md`
  - tests
- Do not make the skill auto-implement by default. It should stop after initialization and planning unless the user explicitly asks for execution.
- Keep subagents read-only by default in the skill instructions.
- Maintain no-overwrite behavior in `init_longrun.py` unless `--force` is passed.

## Validation commands

Run these after script or template changes:

```bash
python -m pytest
python .agents/skills/codex-longrun-init/scripts/detect_stack.py --repo-root . --format markdown
python .agents/skills/codex-longrun-init/scripts/init_longrun.py --repo-root /tmp/codex-longrun-smoke --task-brief "Smoke test" --force
```

The smoke command creates files in `/tmp/codex-longrun-smoke`, not in this repository.

## Project status update rule

After meaningful work, update `docs/PROJECT_STATE.md` with:

- what changed
- validation performed
- remaining risks
- recommended next step

## Style

- Documentation should be direct and operational.
- Scripts should have clear CLI help, typed functions where practical, and deterministic output.
- Templates should be useful immediately after generation and should not rely on hidden chat context.
