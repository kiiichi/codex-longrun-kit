# Review workflow reference

## Batch review principle

Human review should happen against a frozen artifact, not while Codex is still changing the code.

## Independent review principle

Reviewers should independently produce review files. Codex should not merge or summarize feedback until all reviewers have submitted.

## Normalization principle

Codex should normalize feedback into atomic repair tickets before writing code.

## Ticket repair principle

Each ticket should have:

- source review ids
- affected files
- acceptance criteria
- validation commands
- allowed scope
- dependencies
- human-decision flag

Do not ask Codex to repair a vague pile of feedback.
