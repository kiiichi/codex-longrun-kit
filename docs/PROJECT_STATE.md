# Project state

Status: v0.2 scaffold generated.

## Current goal

Build `codex-longrun-kit` as a deployable Codex skill that initializes target repositories for compact, reviewable long-running Codex tasks.

## Current design

The project intentionally separates:

- **Skill entrypoint**: root `SKILL.md`, short and agent-facing.
- **Deterministic helpers**: `scripts/*.py` and PowerShell wrappers.
- **Runtime templates**: `assets/templates/`, used in target repos.
- **Optional references**: `references/*.md`, read only when needed.
- **Project docs**: `docs/*.md`, for maintaining this repo itself.

## Important v0.2 change

Default target output was reduced from many files to compact runtime docs:

```text
docs/agent/LONGRUN.md
docs/agent/STATE.md
```

Review docs are created lazily by `freeze_review.py`.

Strict mode can still generate:

```text
docs/agent/STOP_RULES.md
docs/agent/VALIDATION_MATRIX.md
```

## Validation run

Run before release:

```bash
python -m unittest discover -s tests
```

## Next useful tasks

- Add richer conflict detection in `normalize_reviews.py`.
- Add optional GitHub issue export for ReviewQueue tickets.
- Add real-world smoke test against a small JS/Python repo.
- Tune templates after first Codex dry run.

## Known limitations

- Scripts do not validate JSON schemas without an optional schema dependency.
- Review normalizer deduplicates by simple claim/files key, not semantic equivalence.
- The skill does not configure Codex sandbox or approval policy.
- The skill does not push to GitHub or create PRs.
