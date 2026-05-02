# Long-run runbook

## Initialize

- Read task brief.
- Explore repo briefly.
- Create compact scaffold.
- Draft milestones as vertical slices.
- Stop for plan review.

## Execute

Loop:

1. Read `LONGRUN.md` and `STATE.md`.
2. Select the next unfinished milestone.
3. Implement only that milestone.
4. Run the listed validation gate.
5. Repair focused failures.
6. Update `STATE.md`.
7. Continue unless a stop rule triggers.

## Avoid foreground servers

Do not run commands like `npm run dev`, `python -m http.server`, or `flask run` in the foreground when the agent must continue working.

Use background process + log + PID + cleanup.
