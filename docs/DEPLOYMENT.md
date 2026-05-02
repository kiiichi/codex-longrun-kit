# Deployment

## GitHub release path

1. Commit this repo to `kiiichi/codex-longrun-kit`.
2. Validate tests.
3. Install through skills CLI:

```powershell
npx skills@latest add kiiichi/codex-longrun-kit -a codex -g
```

## Local development install

```powershell
npx skills@latest add ./codex-longrun-kit -a codex -g
```

## Manual install

Copy or symlink this repo to a user-level skills directory supported by the Codex skill runtime.

## Smoke test

In any low-risk target repo, invoke:

```text
Use $codex-longrun-kit to initialize this repository for a long-running Codex task.

Task brief:
Add a tiny smoke-testable feature.

Do not implement yet.
```

Expected result: `docs/agent/LONGRUN.md` and `docs/agent/STATE.md` are created; implementation has not started.
