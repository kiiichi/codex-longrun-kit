# codex-longrun-kit

`codex-longrun-kit` is a Codex skill for initializing compact, reviewable, long-running Codex work.

It does **not** make Codex fully autonomous or bypass approvals. It creates a small runtime scaffold so a multi-hour implementation, migration, refactor, or reviewable agent task can be planned, resumed, validated, frozen for review, and decomposed into follow-up tickets.

This v0.2 version uses **compact runtime docs** by default:

- `docs/agent/LONGRUN.md` — task contract, milestones, stop rules, validation gates.
- `docs/agent/STATE.md` — current handoff snapshot, kept short.
- `docs/agent/REVIEW.md` — created lazily only when review is frozen.

Strict mode can split out `STOP_RULES.md` and `VALIDATION_MATRIX.md`, but the default is intentionally small to reduce agent attention loss.

## Install

From a published GitHub repo:

```powershell
npx skills@latest add kiiichi/codex-longrun-kit -a codex -g
```

From a local checkout:

```powershell
npx skills@latest add ./codex-longrun-kit -a codex -g
```

## Use

Invoke the skill in Codex:

```text
Use $codex-longrun-kit to initialize this repository for a long-running Codex task.

Task brief:
<PRD / issue / migration goal / refactor goal>

Do not implement yet. Create the compact long-run docs, draft the plan, identify blockers, and stop at the plan review checkpoint.
```

Chinese:

```text
使用 $codex-longrun-kit 将当前仓库初始化为可长时间运行、可审查、可恢复的 Codex 长任务工作区。

任务说明：
<PRD / issue / migration goal / refactor goal>

先不要实现。请创建紧凑长任务文档、草拟计划、识别阻塞项，并停在计划审核点。
```

## Profiles

| Profile | Generated during init | Use when |
|---|---|---|
| `minimal` | `LONGRUN.md`, `STATE.md` | Small repos, one reviewer, short long-run tasks. |
| `standard` | `LONGRUN.md`, `STATE.md` | Default. Multi-hour tasks that need clear handoff and validation. |
| `strict` | `LONGRUN.md`, `STATE.md`, `STOP_RULES.md`, `VALIDATION_MATRIX.md` | High-risk tasks, teams, or tasks with strict audit requirements. |

Review docs are lazy. `REVIEW.md`, `docs/reviews/pending/`, and `docs/reviews/ReviewQueue.json` are created by the review/fix scripts when needed, not during normal initialization.

## Direct script use

Initialize a target repository:

```bash
python scripts/init_longrun.py --target /path/to/repo --profile standard --task-brief "Implement X"
```

Freeze a review packet:

```bash
python scripts/freeze_review.py --target /path/to/repo --base main
```

Normalize independent review reports into atomic fix tickets:

```bash
python scripts/normalize_reviews.py --target /path/to/repo
```

PowerShell wrappers are available:

```powershell
./scripts/init-longrun.ps1 -Target C:\path\to\repo -Profile standard -TaskBrief "Implement X"
./scripts/freeze-review.ps1 -Target C:\path\to\repo -Base main
./scripts/normalize-reviews.ps1 -Target C:\path\to\repo
```

## Runtime principle

Long-running Codex work needs external state, but each session should read the **minimum useful state**.

```text
Each run reads:       LONGRUN.md + STATE.md
Review reads:         REVIEW.md + review reports
Advanced topics read: references/*.md only when needed
Project maintenance:  docs/*.md for this repo itself
```

## Files

- `SKILL.md`: the skill consumed by Codex.
- `agents/openai.yaml`: UI metadata and default prompt.
- `assets/templates/`: compact runtime templates.
- `assets/schemas/`: JSON schemas for review reports and review queues.
- `scripts/`: deterministic initialization, review freeze, and review normalization helpers.
- `references/`: optional deep guidance; not meant to be read every run.
- `docs/`: project state and development plan for this skill repository.

## Safety

This skill must not change sandbox settings, approval policy, secrets, production systems, or deployment state. It creates docs and review artifacts only. Any high-risk action belongs in the target repo's stop rules and must be approved by the user.
