# Agent instructions for codex-longrun-kit

Read `docs/PROJECT.md` before changing this repo.

## Purpose

This repo provides a Codex skill that initializes target repos for compact, reviewable long-running Codex work.

## Design constraints

- Keep `SKILL.md` short and agent-facing.
- Default generated runtime docs stay at `LONGRUN.md` + `STATE.md`.
- `REVIEW.md` is lazy, created only at freeze time.
- Strict mode creates one `STRICT.md` appendix, not multiple split files.
- Scripts are helpers; they must not make product decisions or touch product code.
- Do not add new default docs, scripts, or reference files without updating `docs/PROJECT.md`.

## Validation

```bash
python -m unittest discover -s tests
```

## Packaging

```bash
cd .. && python -m zipfile -c codex-longrun-kit.zip codex-longrun-kit
```
