# Known limits

- The skill cannot guarantee Codex will run indefinitely.
- The skill cannot bypass sandbox or approval prompts.
- The skill cannot ensure validation commands are correct; it detects candidates from files.
- The review normalizer does not yet do deep semantic conflict detection.
- Strict mode can still create too much text if teams overfill split files.
- `STATE.md` can become misleading if not updated after meaningful state changes.

Mitigation: keep runtime docs short, mark uncertain items as `UNCONFIRMED`, and treat validation output and git history as higher authority than summaries.
