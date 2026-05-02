---
name: codex-longrun-init
description: Initialize a repository for long-running, milestone-based Codex execution with durable task docs, validation, continuity, stop rules, review freeze, and feedback normalization. Use when the user wants Codex to run a multi-hour implementation, migration, refactor, or reviewable coding task. Do not use for small one-shot edits.
---

# Codex Long-Run Init Skill

You initialize a repository so Codex can perform a long-running coding task as a reviewable execution unit.

## Core boundary

Do **not** begin broad implementation by default.

Your default job is to create or update the long-run scaffold, draft the plan, identify validation commands, and stop for plan review. Implement only if the user explicitly asks you to execute after the scaffold is ready.

## When to use

Use this skill when the user asks for:

- overnight or multi-hour Codex work
- autonomous feature implementation
- large refactor or migration
- batch review and structured feedback repair
- fewer human handoff cycles
- a repository-level long-run prompt/runbook setup

Do not use this skill for:

- one small code edit
- one small bug fix
- a normal short chat answer
- tasks where there is no repository or no durable file system

## Required initialization steps

1. Read existing project guidance:
   - `AGENTS.md`
   - `README.md`
   - project docs if present
2. Inspect the repository structure.
3. Detect candidate validation commands.
4. Create long-run directories:
   - `docs/agent/`
   - `docs/reviews/pending/`
   - `docs/reviews/status/`
   - `.codex_artifacts/logs/`
   - `.codex_artifacts/review/`
5. Create missing long-run files:
   - `docs/agent/Prompt.md`
   - `docs/agent/Plan.md`
   - `docs/agent/Implement.md`
   - `docs/agent/Documentation.md`
   - `docs/agent/CONTINUITY.md`
   - `docs/agent/STOP_RULES.md`
   - `docs/agent/VALIDATION_MATRIX.md`
   - `docs/agent/ReviewPacket.md`
6. If available, use:

```bash
python .agents/skills/codex-longrun-init/scripts/init_longrun.py --repo-root . --task-brief-file <brief-file>
```

If the script is not available in the target repo, manually create the files from the templates in this skill.

7. Fill all unknowns explicitly. Do not silently invent product requirements.
8. Summarize:
   - generated files
   - candidate validation commands
   - open questions
   - proposed milestones
   - stop rules that may affect execution
9. Stop before implementation unless execution was explicitly requested.

## Generated file contract

### `Prompt.md`

The durable task contract. It must include:

- task brief
- goals
- non-goals
- hard constraints
- deliverables
- done-when criteria
- assumptions and unknowns

### `Plan.md`

The milestone plan. It must include:

- milestones
- acceptance criteria
- validation commands
- dependencies
- current status

### `Implement.md`

The long-running execution runbook. It must tell Codex to:

- work one milestone at a time
- keep diffs scoped
- run validation after each milestone
- repair validation failures before moving on
- update `Documentation.md` and `CONTINUITY.md`
- avoid foreground long-running processes
- stop under `STOP_RULES.md`

### `Documentation.md`

The audit log and project state. It must capture:

- changes made
- decisions
- validation results
- known issues
- next step

### `CONTINUITY.md`

The compaction-safe ledger. It must be concise and current enough for another Codex thread to resume without reading the entire chat.

### `STOP_RULES.md`

The escalation and halt conditions.

### `VALIDATION_MATRIX.md`

The validation plan and candidate commands.

### `ReviewPacket.md`

The frozen-review package template.

## Long-run execution discipline

When the user explicitly asks you to execute:

1. Read `docs/agent/Prompt.md`.
2. Read `docs/agent/Plan.md`.
3. Read `docs/agent/Implement.md`.
4. Read `docs/agent/Documentation.md`.
5. Read `docs/agent/CONTINUITY.md`.
6. Pick the next incomplete milestone.
7. Implement only that milestone.
8. Run the milestone validation commands.
9. If validation fails, repair before moving on.
10. Update `Documentation.md`.
11. Update `CONTINUITY.md`.
12. Commit or at least leave a clear diff summary when appropriate.
13. Continue to the next milestone unless a stop rule triggers.

## Approval and safety boundaries

Automatically allowed in normal workspace mode:

- inspect files
- search code
- edit files inside the workspace
- run local tests/lint/typecheck/build commands listed in `VALIDATION_MATRIX.md`
- generate logs, reports, and review packets

Require explicit approval or a human decision for:

- network access
- installing or upgrading dependencies
- database migrations
- changes to authentication, authorization, billing, secrets, CI/CD, deployment, or production config
- destructive file operations
- broad rewrites outside the planned scope
- anything involving secrets or external systems

Do not attempt to bypass sandbox, approval, or permission policy.

## Subagent policy

Default: subagents are read-only.

Appropriate subagent uses:

- codebase exploration
- test failure analysis
- log summarization
- security review
- architecture review
- UX/visual review
- feedback normalization

Do not use multiple write-capable subagents in the same working tree. Only use patch subagents when each ticket has an isolated branch/worktree and a narrow allowed scope.

## Review freeze discipline

When the long run reaches a review point:

1. Stop modifying product code.
2. Record base and head commits.
3. Generate or update `docs/agent/ReviewPacket.md`.
4. Put test logs and artifacts under `.codex_artifacts/review/`.
5. Ask reviewers to write independent files under `docs/reviews/pending/`.
6. Do not repair review feedback until `docs/reviews/ReviewQueue.json` exists.

## Feedback normalization discipline

After independent review files exist:

1. Read every file in `docs/reviews/pending/`.
2. Merge duplicates.
3. Identify conflicts and human decisions.
4. Split feedback into atomic tickets.
5. Write `docs/reviews/ReviewQueue.json`.
6. Write `docs/reviews/HumanDecisionsNeeded.md`.
7. Do not modify product code during normalization.

## Long-running process rule

Never block the agent on a foreground dev server such as:

- `npm run dev`
- `python -m http.server`
- `flask run`
- `rails server`

Use background execution, logs, health checks, and cleanup. Prefer commands with timeouts when available.

## Final response after initialization

After initialization, report:

- files created or skipped
- candidate validation commands
- milestone summary
- open questions
- whether implementation has started
- next recommended human action

Keep the response operational and concise.
