# Agent instructions

Project goal: compact Codex skill for long-running, reviewable work.

Read first:

- `SKILL.md`
- `docs/PROJECT.md`

Style:

- High-density operational language.
- Prefer positive contracts over defensive caveats.
- Use negative rules only for hard stops or observed failure modes.
- Every hard stop needs the replacement action or HITL route.

Development rules:

- Keep default target output small: `LONGRUN.md` + `STATE.md`.
- Create review artifacts lazily.
- Keep helper scripts standard-library Python.
- Scripts create artifacts. Humans or Codex decide next actions from those artifacts.
- Target repo docs use `invoke $codex-longrun-kit normalize review feedback`; they never assume target-local skill scripts.

Validation:

```bash
python -m unittest discover -s tests
```
