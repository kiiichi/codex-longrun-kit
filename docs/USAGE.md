# Usage guide

## 1. Install the skill

Use a user-level install for personal use:

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/.agents/skills/codex-longrun-init" ~/.agents/skills/codex-longrun-init
```

Use a repo-level install when the target repository should carry the skill:

```bash
mkdir -p /path/to/project/.agents/skills
cp -R .agents/skills/codex-longrun-init /path/to/project/.agents/skills/
```

## 2. Invoke in Codex

```text
$codex-longrun-init

Task brief:
We need to migrate the legacy billing report generator to the new event schema.
Do not implement yet. Initialize the long-run scaffold and stop after producing Plan.md.
```

Expected output in the target repository:

```text
docs/agent/Prompt.md
docs/agent/Plan.md
docs/agent/Implement.md
docs/agent/Documentation.md
docs/agent/CONTINUITY.md
docs/agent/STOP_RULES.md
docs/agent/VALIDATION_MATRIX.md
docs/agent/ReviewPacket.md
docs/reviews/pending/
docs/reviews/status/
.codex_artifacts/
```

## 3. Review the plan

Before implementation, review:

- scope
- non-goals
- milestone boundaries
- validation commands
- stop rules
- approval boundaries

## 4. Execute the long run

A follow-up instruction can be:

```text
Proceed with the long-run execution using docs/agent/Implement.md.
Work one milestone at a time.
Update docs/agent/Documentation.md and docs/agent/CONTINUITY.md after each milestone.
Stop only if docs/agent/STOP_RULES.md is triggered.
```

## 5. Freeze for review

At the end of the run:

```bash
python .agents/skills/codex-longrun-init/scripts/freeze_review.py --repo-root .
```

Then give reviewers the frozen commit and `docs/agent/ReviewPacket.md`.

## 6. Independent review

Each reviewer writes one file:

```text
docs/reviews/pending/security.yaml
docs/reviews/pending/architecture.yaml
docs/reviews/pending/tests.yaml
docs/reviews/pending/ux.yaml
```

They should not read each other's files until all review files are submitted.

## 7. Normalize feedback

```bash
python .agents/skills/codex-longrun-init/scripts/normalize_reviews.py --repo-root .
```

Outputs:

```text
docs/reviews/ReviewQueue.json
docs/reviews/HumanDecisionsNeeded.md
```

## 8. Repair one ticket at a time

Recommended prompt:

```text
Address exactly one review ticket: RQ-001.
Read docs/reviews/ReviewQueue.json.
Keep the diff minimal.
Do not fix other tickets.
Run the ticket validation commands.
Update docs/reviews/status/RQ-001.md.
```

Use a separate worktree when tickets are independent and can be safely parallelized.
