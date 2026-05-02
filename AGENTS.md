# Agent instructions for codex-longrun-kit

Read `docs/PROJECT_STATE.md` before making changes. Then read `docs/DEVELOPMENT_GOALS.md` and `docs/TECHNICAL_ROUTE.md` if the task affects design.

## Project purpose

This repo provides a Codex skill that initializes target repositories for compact, reviewable long-running Codex work.

The main design choice in v0.2 is **compact runtime docs**:

- Default target output: `docs/agent/LONGRUN.md` + `docs/agent/STATE.md`.
- Review output is lazy: `REVIEW.md` and `docs/reviews/` are created at freeze time.
- Strict split files are optional: `STOP_RULES.md` and `VALIDATION_MATRIX.md` are generated only in `--profile strict`.

## Development rules

- Keep `SKILL.md` concise and agent-facing.
- Prefer scripts for deterministic file generation and normalization.
- Prefer references for optional deep guidance.
- Do not increase the number of default generated runtime docs without updating `docs/DECISIONS.md`.
- Tests must pass before packaging.

## Validation

```bash
python -m unittest discover -s tests
python scripts/init_longrun.py --target /tmp/longrun-smoke --profile standard --task-brief "Smoke task" --force
python scripts/freeze_review.py --target /tmp/longrun-smoke --base HEAD
python scripts/normalize_reviews.py --target /tmp/longrun-smoke
```

## Packaging

```bash
python -m zipfile -c ../codex-longrun-kit.zip .
```
