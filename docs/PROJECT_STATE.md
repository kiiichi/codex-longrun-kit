# Project state

Last updated: 2026-05-02

## Current phase

Initial v0.1 scaffold is ready.

The repository is designed as a Codex Skill kit. The primary skill is:

```text
.agents/skills/codex-longrun-init/
```

## What exists

### Skill

- `.agents/skills/codex-longrun-init/SKILL.md`
- templates in `.agents/skills/codex-longrun-init/assets/templates/`
- references in `.agents/skills/codex-longrun-init/references/`
- helper scripts in `.agents/skills/codex-longrun-init/scripts/`

### Helper scripts

- `detect_stack.py`: detects candidate validation commands from common project files.
- `init_longrun.py`: creates long-run docs in a target repository.
- `freeze_review.py`: generates a frozen review packet from git state.
- `normalize_reviews.py`: turns independent review files into `ReviewQueue.json`.

### Project docs

- `README.md`: installation and use.
- `PROJECT.md`: mission, goals, technical route.
- `AGENTS.md`: instructions for future Codex threads.
- `docs/ARCHITECTURE.md`: system design.
- `docs/TECHNICAL_ROUTE.md`: phased development route.
- `docs/USAGE.md`: detailed usage.
- `docs/REVIEW_WORKFLOW.md`: review and feedback normalization flow.

### Tests

- `tests/test_detect_stack.py`
- `tests/test_init_longrun.py`
- `tests/test_normalize_reviews.py`

## Important design decisions

1. The skill is explicit-invocation only by convention. It should not be used implicitly for small edits.
2. Initialization stops before broad implementation unless the user explicitly requests execution.
3. Subagents are read-only by default.
4. Review feedback must be normalized before Codex repairs it.
5. Scripts perform deterministic file operations; Markdown files hold workflow intent.
6. Generated long-run state belongs in the target repository, not only in chat context.

## Known limitations

- `normalize_reviews.py` has simple duplicate and potential-conflict detection. It is intentionally conservative.
- `detect_stack.py` returns candidate commands; a human or Codex should verify them before relying on them for unattended runs.
- The project is not packaged as a plugin yet.
- Worktree-based patch execution is documented but not automated.
- The skill does not change Codex sandbox or approval policy.

## Validation to run after changes

```bash
python -m pytest
python .agents/skills/codex-longrun-init/scripts/detect_stack.py --repo-root . --format markdown
python .agents/skills/codex-longrun-init/scripts/init_longrun.py --repo-root /tmp/codex-longrun-smoke --task-brief "Smoke test" --force
```

## Recommended next development tasks

1. Validate the generated docs inside a real software repository.
2. Add a second skill for `codex-longrun-freeze-review` if repeated use shows that separate skills are clearer.
3. Improve review schema validation.
4. Add optional worktree ticket scaffolding.
5. Add release instructions once the first public repo commit exists.
