# Review workflow

## Freeze

Stop modifying product code. Generate `docs/agent/REVIEW.md` and `docs/reviews/pending/`.

## Independent review

Each reviewer writes one report:

```text
docs/reviews/pending/security.json
docs/reviews/pending/architecture.json
docs/reviews/pending/tests.json
```

Reviewers should not read each other's reports before the review window closes.

## Normalize

Run:

```bash
python scripts/normalize_reviews.py --target .
```

This produces `ReviewQueue.json`.

## Fix

Fix one ticket at a time. Do not fix unrelated tickets in the same patch.
