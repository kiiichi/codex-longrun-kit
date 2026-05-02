# Approval boundaries reference

## Low-risk actions

Usually safe inside the workspace:

- read files
- search files
- edit planned files
- run local validation commands
- generate logs and reports

## Requires approval or explicit human decision

- network access
- dependency install or upgrade
- database migration
- authentication or authorization change
- billing/payment change
- secret handling
- production deployment
- CI/CD change
- destructive git or file operations
- broad scope expansion

## Forbidden by default

- accessing secrets
- writing outside the workspace
- production deployment
- destructive operations without approval
- bypassing sandbox or approval policy
