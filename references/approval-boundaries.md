# Approval boundaries

The skill does not configure Codex sandbox or approval settings.

## Usually safe without asking

- Read/search files in the current repo.
- Modify files inside the current repo according to the active milestone.
- Run local lint, tests, typecheck, and build commands.
- Generate review artifacts.

## Ask first

- Install dependencies.
- Use network access.
- Run database migrations.
- Modify CI/CD, auth, payment, permissions, encryption, or secrets handling.
- Delete many files.
- Change stop rules.

## Forbidden by default

- Commit secrets.
- Production deployment.
- Destructive git commands.
- Write outside the workspace.
- `curl | sh` installs.
