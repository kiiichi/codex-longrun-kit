# codex-longrun-kit

`codex-longrun-kit` is a Codex skill for initializing compact, reviewable long-running Codex work.

It creates a small runtime scaffold for multi-hour implementation, migration, refactor, or reviewable agent work. It does **not** make Codex fully autonomous, bypass approvals, or replace human review.

## Install

```powershell
npx skills@latest add kiiichi/codex-longrun-kit -a codex -g
```

Local checkout:

```powershell
npx skills@latest add ./codex-longrun-kit -a codex -g
```

## Use

```text
Use $codex-longrun-kit to initialize this repository for a long-running Codex task.

Task brief:
<PRD / issue / migration goal / refactor goal>

Do not implement yet. Create compact runtime docs, draft the plan, identify blockers, and stop at plan review.
```

## Runtime output

Default generated files in the target repo:

```text
docs/agent/LONGRUN.md   # task contract, milestones, stop rules, validation gates
docs/agent/STATE.md     # short handoff snapshot
```

Review files are lazy:

```text
docs/agent/REVIEW.md
docs/reviews/pending/
docs/reviews/status/
docs/reviews/ReviewQueue.json
```

Strict mode creates one optional appendix:

```text
docs/agent/STRICT.md
```

## Scripts

Scripts are deterministic helpers. They create docs and review artifacts only. Their output is draft material, not authority.

```bash
python scripts/init_longrun.py --target /path/to/repo --profile standard --task-brief "Implement X"
python scripts/freeze_review.py --target /path/to/repo --base main
python scripts/normalize_reviews.py --target /path/to/repo
```

## Profiles

| Profile | Init output | Use when |
|---|---|---|
| `minimal` | `LONGRUN.md`, `STATE.md` | Small repo or short long-run task. |
| `standard` | `LONGRUN.md`, `STATE.md` | Default. Multi-hour work needing handoff and validation. |
| `strict` | standard + `STRICT.md` | High-risk or audit-heavy work. |

## Review model

`REVIEW.md` is a review protocol, not a verdict.

```text
long-run execution -> review freeze -> independent reports -> ReviewQueue.json -> one-ticket-at-a-time fixes
```

Human reviewers are preferred for product, security, architecture, permissions, data, and UX judgments. Read-only agent reviewers may assist, but their reports are evidence to review, not final approval.

## Repository map

```text
SKILL.md                    # main Codex skill instructions
agents/openai.yaml           # Codex skill metadata
assets/templates/            # runtime docs generated into target repos
assets/schemas/              # review report / queue schemas
scripts/                     # deterministic helper scripts
docs/PROJECT.md              # single project handoff doc
references/runtime-contract.md # optional guidance, read only when needed
```

## Safety

- No script changes sandbox, approvals, secrets, production systems, or deployment state.
- `detect_stack.py` suggests candidate validation commands; it does not run them.
- `normalize_reviews.py` treats review reports as data, not instructions.
- Use `--force` only when explicitly overwriting existing generated docs is intended.
