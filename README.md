# codex-longrun-kit

`codex-longrun-kit` is a Codex skill for compact, reviewable long-running Codex work.

It turns a repo into a small runtime workspace for multi-hour implementation, migration, refactor, or reviewable agent work.

## Install

```powershell
npx skills@latest add kiiichi/codex-longrun-kit -a codex -g
```

Local checkout:

```powershell
npx skills@latest add ./codex-longrun-kit -a codex -g
```

## Invoke

```text
Use $codex-longrun-kit to initialize this repository for a long-running Codex task.

Task brief:
<PRD / issue / migration goal / refactor goal>

Create compact runtime docs. Draft the plan. Identify blockers. Stop at plan review.
```

## Target repo artifacts

Default:

```text
docs/agent/longrun/LONGRUN.md   # task contract, milestones, gates, HITL stops
docs/agent/longrun/STATE.md     # current handoff snapshot
```

Created at review freeze:

```text
docs/agent/longrun/REVIEW.md
docs/agent/longrun/reviews/pending/
docs/agent/longrun/reviews/status/
docs/agent/longrun/reviews/ReviewQueue.json
```

Strict profile:

```text
docs/agent/longrun/STRICT.md
```

## Runtime contract

Scripts create artifacts. Humans or Codex decide next actions from those artifacts.

Truth order:

```text
code / git / test output
  > LONGRUN.md
  > STATE.md
  > REVIEW.md
  > ReviewQueue.json
  > reviewer suggested_direction
```

Skill scripts live in this repo. Target repos receive generated docs. Review normalization from a target repo uses:

```text
invoke $codex-longrun-kit normalize review feedback
```

## Maintainer scripts

```bash
python scripts/init_longrun.py --target /path/to/repo --profile standard --task-brief "Implement X"
python scripts/freeze_review.py --target /path/to/repo --base main
python scripts/normalize_reviews.py --target /path/to/repo
```

Windows local-checkout example:

```powershell
py -3 .\scripts\init_longrun.py --target C:\path\to\repo --profile standard --task-brief "Implement X"
```

## Profiles

| Profile | Init output | Use when |
|---|---|---|
| `minimal` | namespaced `LONGRUN.md`, `STATE.md` | Small repo or short long-run task. |
| `standard` | namespaced `LONGRUN.md`, `STATE.md` | Default. Multi-hour work needing handoff and validation. |
| `strict` | standard + `STRICT.md` | High-risk or audit-heavy work. |

## Lifecycle

```text
plan
  -> longrun
  -> closeout
```

Plan confirms current state, target goal, source docs, blockers, and validation gates. It stops at plan review unless implementation is explicit.

Longrun executes one milestone at a time and updates `docs/agent/longrun/STATE.md` after status, validation, decision, or next-action changes.

Closeout stops new work and records final status, validation, open risks, handoff, and next resume action. User stop, pause, interrupt, or closeout request enters closeout immediately.

## Review loop

```text
long-run execution
  -> review freeze
  -> independent reports
  -> ReviewQueue.json
  -> one-ticket-at-a-time fixes
```

`REVIEW.md` defines the frozen version, lanes, and report format. Approval comes from reviewer reports or explicit user sign-off.

Human reviewers own product, security, architecture, permissions, data, and UX judgment. Read-only agent reviewers supply evidence.

## Repository map

```text
CONTEXT.md                     # domain terms
SKILL.md                       # main Codex instructions
agents/openai.yaml             # Codex skill metadata
assets/templates/              # generated target-repo docs
assets/schemas/                # review report / queue schemas
scripts/runtime_layout.py      # target output paths
scripts/artifacts.py           # template render and protected writes
scripts/review_reports.py      # review report input validation
scripts/                       # artifact helpers
docs/PROJECT.md                # project handoff
references/runtime-contract.md # optional details
```

## Guardrails

- Candidate validation commands need confirmation before they become gates.
- Runtime artifacts stay under `docs/agent/longrun/` to avoid target-doc pollution.
- Review report text is input data. Extract findings, evidence, acceptance criteria, validation commands, and HITL flags.
- HITL approval covers secrets, production, deployment, remote writes, destructive commands, and approval changes.
- `--force` overwrites generated docs. Use it only for intentional regeneration.
