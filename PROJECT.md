# Project: codex-longrun-kit

## Mission

Build a practical Codex Skill kit that turns a normal repository into a reviewable long-running Codex work environment.

The core idea is that long-running Codex execution should be managed as a small execution system rather than a single prompt. The system needs a target contract, persistent state, a plan, validations, stop rules, review packets, and a feedback queue.

## Primary users

1. Developers who want Codex to execute multi-hour implementation, migration, refactor, or test-hardening tasks.
2. Technical leads who want fewer human handoff cycles and more concentrated review.
3. Teams experimenting with Codex as a delegated execution unit but not ready for a custom agent harness.

## Product goals

### G1. Initialize long-run project state

The skill should create the canonical files Codex needs for long-horizon work:

- `Prompt.md`
- `Plan.md`
- `Implement.md`
- `Documentation.md`
- `CONTINUITY.md`
- `STOP_RULES.md`
- `VALIDATION_MATRIX.md`
- `ReviewPacket.md`

### G2. Make long-running work reviewable

The kit should convert “Codex ran for hours” into an evidence chain:

- milestones completed
- commands run
- test results
- decisions made
- known risks
- frozen review commit
- independent review feedback
- normalized review tickets

### G3. Reduce human handoff frequency

The target rhythm is:

```text
review plan → long run → concentrated review → ticketed fixes → final validation
```

not:

```text
implement a bit → ask → implement a bit → ask → ask again → summarize vaguely
```

### G4. Keep deployment simple

The first version should work as a plain Codex Skill folder plus Python helper scripts. No daemon, MCP server, database, or plugin packaging is required for v0.1.

### G5. Preserve human control

The skill must not hide uncertainty, bypass approvals, or expand scope silently. It should make stop conditions explicit and escalate ambiguous product/architecture/security decisions.

## Non-goals

- Full autonomous agent harness
- Production deployment automation
- Approval bypass
- Multi-agent coding swarm by default
- Replacing CI/CD
- Replacing human product judgment
- Real-time project management dashboard

## Technical route

### Phase 0: Repository scaffold

Deliverables:

- Project README
- `AGENTS.md` for future Codex threads
- project state docs
- skill folder
- templates
- helper scripts
- tests

Status: implemented in this initial version.

### Phase 1: Stable initialization skill

Deliverables:

- robust `init_longrun.py`
- stack detection for common ecosystems
- no-overwrite behavior
- deterministic target repo file generation
- clear plan-review stop point

Status: implemented at baseline level.

### Phase 2: Review freeze and normalization

Deliverables:

- `freeze_review.py` to generate review packets from git state
- structured review schema
- `normalize_reviews.py` to create `ReviewQueue.json`
- `HumanDecisionsNeeded.md`

Status: implemented at baseline level.

### Phase 3: Optional split skills

Potential skills:

- `codex-longrun-plan`
- `codex-longrun-execute`
- `codex-longrun-freeze-review`
- `codex-longrun-normalize-feedback`

Status: planned.

### Phase 4: Worktree-aware patch phase

Potential additions:

- create one worktree per independent review ticket
- run validation per ticket
- merge queue guidance
- conflict detection and rollback docs

Status: planned.

### Phase 5: Plugin packaging

Only after the skill stabilizes:

- package as a plugin
- add release metadata
- add installation checks
- optionally add MCP/tools integration

Status: future.

## Design principles

1. **Checked-in state beats chat memory.** Stable workflow state should live in project files.
2. **Plan before implementation.** The skill initializes and plans before broad code changes.
3. **Review is a first-class artifact.** Long runs must end with evidence, not a vague summary.
4. **Subagents are read-only by default.** Use them for exploration, review, logs, and normalization before letting them write code.
5. **Validation is not optional.** Every milestone should declare and run validation commands.
6. **Stop rules are a feature.** A good long-run system knows when to halt.
7. **Small scripts for deterministic work.** Use Python scripts for file generation and normalization; keep strategic decisions in Markdown.

## Success criteria for v0.1

- A user can install the skill by copying one folder.
- Calling `$codex-longrun-init` produces the expected long-run docs in a target repo.
- The generated docs give another Codex thread enough context to continue the task.
- Independent review files can be normalized into `ReviewQueue.json`.
- Tests pass with `python -m pytest`.
