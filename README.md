# codex-longrun-kit

`codex-longrun-kit` is a Codex Skill kit for initializing a repository so Codex can run long, reviewable coding tasks with less human handoff overhead.

It does **not** try to make Codex magically autonomous. It creates the durable project scaffold that long-running Codex work needs:

- a task contract (`Prompt.md`)
- a milestone plan (`Plan.md`)
- an implementation runbook (`Implement.md`)
- a continuity ledger (`CONTINUITY.md`)
- stop rules and approval boundaries (`STOP_RULES.md`)
- a validation matrix (`VALIDATION_MATRIX.md`)
- a review freeze packet (`ReviewPacket.md`)
- independent review files and a normalized review queue

The default behavior is conservative: the skill initializes and plans first, then stops before broad implementation unless the user explicitly asks to execute.

## Status

`v0.1.0` initial scaffold.

Implemented in this repository:

- `codex-longrun-init` skill
- templates for long-running task docs
- scripts for initialization, stack detection, review freeze, and feedback normalization
- project docs for future Codex threads
- basic pytest coverage for the scripts

Read [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md) before continuing development.

## Install

### User-level install

Copy or symlink the skill folder into your user skills directory:

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/.agents/skills/codex-longrun-init" ~/.agents/skills/codex-longrun-init
```

Or copy it instead of symlinking:

```bash
mkdir -p ~/.agents/skills/codex-longrun-init
cp -R .agents/skills/codex-longrun-init/* ~/.agents/skills/codex-longrun-init/
```

### Repo-level install

For a target project, copy the skill into that repository:

```bash
mkdir -p /path/to/project/.agents/skills
cp -R .agents/skills/codex-longrun-init /path/to/project/.agents/skills/
```

A user-level install is usually better for personal use. A repo-level install is better when the whole team should use the same workflow.

## Use in Codex

Invoke the skill explicitly:

```text
$codex-longrun-init

Initialize this repository for a long-running Codex task.
Task brief:
<put PRD, migration brief, refactor goal, issue, or feature request here>

Do not implement yet. Generate the long-run scaffold and stop after Plan.md.
```

The skill should create or update:

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
.codex_artifacts/
```

## Script usage outside Codex

The skill can also be used directly from a shell:

```bash
python .agents/skills/codex-longrun-init/scripts/init_longrun.py \
  --repo-root . \
  --task-brief-file examples/sample-task-brief.md
```

Detect candidate validation commands:

```bash
python .agents/skills/codex-longrun-init/scripts/detect_stack.py --repo-root . --format markdown
```

Freeze a review packet:

```bash
python .agents/skills/codex-longrun-init/scripts/freeze_review.py --repo-root .
```

Normalize independent review files into a review queue:

```bash
python .agents/skills/codex-longrun-init/scripts/normalize_reviews.py --repo-root .
```

## Recommended long-run flow

```text
1. Human writes or pastes a task brief.
2. $codex-longrun-init creates the scaffold.
3. Human reviews Plan.md once.
4. Codex executes one milestone at a time using Implement.md.
5. Codex updates Documentation.md and CONTINUITY.md after each milestone.
6. Codex freezes a ReviewPacket.md.
7. Reviewers independently write docs/reviews/pending/*.yaml.
8. normalize_reviews.py creates ReviewQueue.json and HumanDecisionsNeeded.md.
9. Codex fixes one review ticket at a time, preferably one worktree per independent ticket.
10. Human performs final validation from the evidence chain.
```

## Design stance

This kit favors reliability over maximum autonomy.

Default choices:

- Main Codex thread writes code.
- Subagents are read-only by default.
- Human review is batched around a frozen commit.
- Feedback is normalized before repair.
- Long-running foreground processes are avoided.
- Risky actions are escalated instead of silently executed.

## Repository map

```text
.agents/skills/codex-longrun-init/  # The actual Codex Skill
  SKILL.md                          # Skill instructions and operating contract
  assets/templates/                 # Files copied into target repos
  references/                       # Long-form workflow guidance for Codex
  scripts/                          # Deterministic helper scripts

docs/                               # Project docs for this kit
examples/                           # Example task brief and review file
tests/                              # Pytest coverage for helper scripts
```

## Development

```bash
python -m pytest
```

The scripts are intentionally small and mostly standard-library based. `PyYAML` is optional but recommended for review normalization.

## Non-goals

This project does not:

- bypass Codex sandbox or approval policies
- guarantee unattended completion
- replace CI/CD
- deploy production changes
- force parallel coding subagents
- make product decisions without a human decision point

## License

MIT. See [`LICENSE`](LICENSE).
