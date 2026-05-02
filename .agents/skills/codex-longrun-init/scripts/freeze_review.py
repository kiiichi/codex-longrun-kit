#!/usr/bin/env python3
"""Generate or update docs/agent/ReviewPacket.md from git state."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _run(root: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as exc:
        return exc.output.strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def _safe_run(root: Path, args: list[str]) -> str:
    out = _run(root, args)
    return out if out else "not available"


def _git_branch(root: Path) -> str:
    return _safe_run(root, ["branch", "--show-current"])


def _git_head(root: Path) -> str:
    return _safe_run(root, ["rev-parse", "HEAD"])


def _default_base(root: Path) -> str:
    for ref in ["origin/main", "main", "origin/master", "master"]:
        out = _run(root, ["merge-base", "HEAD", ref])
        if out and not out.startswith("fatal") and not out.startswith("ERROR"):
            return out
    return "HEAD~1"


def _markdown_list(text: str) -> str:
    if not text or text == "not available":
        return "- not available"
    return "\n".join(f"- `{line}`" for line in text.splitlines() if line.strip())


def generate_review_packet(repo_root: str | Path, base: str | None = None) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = f"RUN-{created_at.replace(':', '').replace('-', '')}"
    base_ref = base or _default_base(root)
    head = _git_head(root)
    branch = _git_branch(root)
    status = _safe_run(root, ["status", "--short"])
    diffstat = _safe_run(root, ["diff", "--stat", base_ref, "HEAD"])
    changed_files = _safe_run(root, ["diff", "--name-only", base_ref, "HEAD"])
    log = _safe_run(root, ["log", "--oneline", f"{base_ref}..HEAD"])

    review_dir = root / ".codex_artifacts" / "review" / run_id
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "git-status.txt").write_text(status + "\n", encoding="utf-8")
    (review_dir / "diffstat.txt").write_text(diffstat + "\n", encoding="utf-8")
    (review_dir / "changed-files.txt").write_text(changed_files + "\n", encoding="utf-8")
    (review_dir / "git-log.txt").write_text(log + "\n", encoding="utf-8")

    packet = f"""# ReviewPacket.md — Concentrated review packet

Created: {created_at}
Run id: {run_id}

## Review status

Status: frozen-for-review

## Frozen version

- Base commit/ref: {base_ref}
- Head commit: {head}
- Branch: {branch}
- Working tree status: {'clean' if status == 'not available' or status == '' else 'has changes; inspect git-status.txt'}

## Artifact directory

`{review_dir.relative_to(root)}`

## What changed

Fill this summary from `docs/agent/Documentation.md` before sending to reviewers.

## Commit log

```text
{log}
```

## Diff summary

```text
{diffstat}
```

## Changed files

{_markdown_list(changed_files)}

## Validation evidence

Fill from `docs/agent/Documentation.md` and logs under `.codex_artifacts/`.

| Command | Result | Evidence/log path | Notes |
|---|---|---|---|
| not recorded | n/a | n/a | Add validation evidence before final review |

## Decisions made

Fill with important decisions from `docs/agent/Documentation.md`.

## Known issues and risks

Fill with known issues before review.

## Reviewer lanes

Suggested independent review files:

- `docs/reviews/pending/security.yaml`
- `docs/reviews/pending/architecture.yaml`
- `docs/reviews/pending/tests.yaml`
- `docs/reviews/pending/ux.yaml`
- `docs/reviews/pending/performance.yaml`
- `docs/reviews/pending/maintainability.yaml`

## Review instructions

All reviewers should inspect the same frozen commit and produce independent review files. Do not repair feedback until `docs/reviews/ReviewQueue.json` exists.
"""

    target = root / "docs" / "agent" / "ReviewPacket.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(packet, encoding="utf-8")

    return {
        "run_id": run_id,
        "review_packet": str(target),
        "artifact_dir": str(review_dir),
        "base": base_ref,
        "head": head,
        "branch": branch,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a concentrated review packet from git state.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--base", default=None, help="Base commit/ref for diff. Defaults to merge-base with main/master when possible.")
    args = parser.parse_args()
    result = generate_review_packet(args.repo_root, args.base)
    print("Review packet generated.")
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
