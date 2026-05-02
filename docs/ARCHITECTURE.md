# Architecture

## Overview

`codex-longrun-kit` is a small workflow layer around Codex. It uses a Codex Skill plus deterministic scripts to create project files that survive context compaction, thread changes, and long execution windows.

```text
User task brief
  ↓
$codex-longrun-init
  ↓
Target repo long-run docs
  ↓
Milestone execution
  ↓
Review freeze packet
  ↓
Independent review files
  ↓
ReviewQueue.json
  ↓
Ticketed fixes
```

## Components

### 1. Skill instructions

Path:

```text
.agents/skills/codex-longrun-init/SKILL.md
```

The skill defines when to use the workflow, the default stop point, the generated file contract, and the rules for execution, review, subagents, and approvals.

### 2. Templates

Path:

```text
.agents/skills/codex-longrun-init/assets/templates/
```

Templates are copied into the target repo and rendered with basic placeholders. They become the target repo's durable long-run state.

### 3. Scripts

Path:

```text
.agents/skills/codex-longrun-init/scripts/
```

Scripts are used for deterministic operations:

- file generation
- stack detection
- review packet generation
- review feedback normalization

Scripts should not make product decisions.

### 4. References

Path:

```text
.agents/skills/codex-longrun-init/references/
```

References contain long-form workflow guidance. Keeping them separate avoids making `SKILL.md` too large while still giving Codex detailed instructions when needed.

### 5. Generated target-repo docs

The skill creates:

```text
docs/agent/
  Prompt.md
  Plan.md
  Implement.md
  Documentation.md
  CONTINUITY.md
  STOP_RULES.md
  VALIDATION_MATRIX.md
  ReviewPacket.md

docs/reviews/
  pending/
  status/
  ReviewQueue.json
  HumanDecisionsNeeded.md
```

These generated files are meant to be committed to the target repo or at least kept in the working tree during the long task.

## Data flow

### Initialization

1. Read user task brief.
2. Inspect target repo.
3. Detect candidate validation commands.
4. Render templates into `docs/agent/`.
5. Create review directories.
6. Stop for plan review.

### Execution

1. Main Codex thread reads `Prompt.md`, `Plan.md`, `Implement.md`, `Documentation.md`, and `CONTINUITY.md`.
2. It executes one milestone at a time.
3. It runs milestone validation.
4. It updates state docs.
5. It stops only under `STOP_RULES.md` or after completing the planned run.

### Review freeze

1. Stop modifying code.
2. Capture git commit, diffstat, changed files, and validation status.
3. Generate `ReviewPacket.md`.
4. Give reviewers a frozen base commit.

### Feedback normalization

1. Each reviewer writes an independent YAML/JSON file under `docs/reviews/pending/`.
2. `normalize_reviews.py` merges duplicate items.
3. It marks potential conflicts and human decisions.
4. It writes `ReviewQueue.json` and `HumanDecisionsNeeded.md`.

### Patch phase

Initial recommendation:

- main thread fixes one ticket at a time

Future recommendation:

- one independent ticket per git worktree
- validate each ticket independently
- merge after CI passes

## Why not one giant prompt?

A long prompt does not preserve state across compaction, thread changes, review cycles, or interrupted runs. This kit converts the prompt into files Codex can repeatedly read and update.

## Why not default parallel coding subagents?

Parallel code-writing agents increase merge conflicts and semantic drift. This kit defaults subagents to read-only roles such as exploration, log analysis, security review, and feedback normalization.
