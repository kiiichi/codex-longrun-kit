# Long-running process reference

Foreground dev servers can block Codex. Avoid commands that do not return.

## Risky foreground commands

- `npm run dev`
- `vite --host`
- `python -m http.server`
- `flask run`
- `rails server`
- `uvicorn app:app`

## Safer pattern

- start in background
- write logs to `.codex_artifacts/logs/`
- store pid
- wait with bounded health check
- run tests
- kill process

Example:

```bash
mkdir -p .codex_artifacts/logs
nohup npm run dev > .codex_artifacts/logs/devserver.log 2>&1 &
echo $! > .codex_artifacts/logs/devserver.pid

for i in {1..30}; do
  curl -sf http://localhost:3000/health && break
  sleep 1
done

npm run test:e2e

kill "$(cat .codex_artifacts/logs/devserver.pid)" || true
```
