# Usage

## Install globally for Codex

```powershell
npx skills@latest add kiiichi/codex-longrun-kit -a codex -g
```

## Initialize a target repo through Codex

```text
Use $codex-longrun-kit to initialize this repository for a long-running Codex task.

Task brief:
<brief>

Do not implement yet. Stop at the plan review checkpoint.
```

## Initialize with script directly

```bash
python scripts/init_longrun.py --target /path/to/repo --profile standard --task-brief "<brief>"
```

## Review freeze

When implementation is complete enough for concentrated review:

```bash
python scripts/freeze_review.py --target /path/to/repo --base main
```

Then reviewers write independent reports under:

```text
docs/reviews/pending/<lane>.json
```

## Normalize feedback

```bash
python scripts/normalize_reviews.py --target /path/to/repo
```

Codex should fix `ReviewQueue.json` tickets one at a time.
