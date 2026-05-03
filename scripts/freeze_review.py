#!/usr/bin/env python3
"""Create review-freeze artifacts.

Record frozen-version metadata and review protocol. Git remains mutable; approval stays external.
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

try:
    from artifacts import ArtifactWriter
    from runtime_layout import (
        longrun_dir,
        review_artifacts_dir,
        review_status_dir,
        reviews_dir,
        target_root,
    )
except ImportError:  # pragma: no cover
    from scripts.artifacts import ArtifactWriter  # type: ignore
    from scripts.runtime_layout import (  # type: ignore
        longrun_dir,
        review_artifacts_dir,
        review_status_dir,
        reviews_dir,
        target_root,
    )


def run_git(target: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=target,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "UNCONFIRMED"


def working_tree_status(target: Path) -> str:
    status = run_git(target, ["status", "--short"])
    if status == "UNCONFIRMED":
        return "- UNCONFIRMED: git status unavailable."
    if not status:
        return "- Clean working tree reported by git."
    lines = [
        "- WARNING: working tree has uncommitted changes. "
        "Stable review needs commit or explicit record."
    ]
    lines.extend(f"- `{line}`" for line in status.splitlines()[:30])
    if len(status.splitlines()) > 30:
        lines.append("- Additional changes omitted from this summary.")
    return "\n".join(lines)


def freeze(target: Path, base: str, force: bool = False) -> list[str]:
    target = target_root(target)
    writer = ArtifactWriter(target, force=force)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    current_commit = run_git(target, ["rev-parse", "HEAD"])
    current_branch = run_git(target, ["branch", "--show-current"])
    current_ref = (
        current_branch
        if current_branch != "UNCONFIRMED" and current_branch
        else current_commit
    )
    diff_stat = run_git(target, ["diff", "--stat", f"{base}...HEAD"])
    if diff_stat == "UNCONFIRMED" or not diff_stat:
        diff_stat = "UNCONFIRMED: no diff stat available."

    mapping = {
        "BASE_REF": base,
        "CURRENT_REF": current_ref,
        "CURRENT_COMMIT": current_commit,
        "CURRENT_BRANCH": current_branch,
        "CREATED_AT": now,
        "DIFF_STAT": diff_stat,
        "WORKTREE_STATUS": working_tree_status(target),
    }

    written: list[str] = []
    docs_agent = longrun_dir(target)
    docs_reviews = reviews_dir(target)
    review_artifacts = review_artifacts_dir(target)

    for path in [docs_agent, docs_reviews / "pending", review_status_dir(target), review_artifacts]:
        path.mkdir(parents=True, exist_ok=True)

    review_path = docs_agent / "REVIEW.md"
    if writer.write_template(review_path, "REVIEW.md.template", mapping):
        written.append(writer.relative(review_path))

    readme_path = docs_reviews / "README.md"
    if writer.write_template(readme_path, "reviews_README.md.template", {}):
        written.append(writer.relative(readme_path))

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target", "--target-root", dest="target", default=".", help="Target repo root"
    )
    parser.add_argument("--base", default="main", help="Base ref to compare against")
    parser.add_argument("--force", action="store_true", help="Overwrite review files")
    args = parser.parse_args()

    written = freeze(Path(args.target), args.base, force=args.force)
    if written:
        print("Created/updated:")
        for item in written:
            print(f"- {item}")
    else:
        print(
            "No files written. Existing review files preserved. "
            "Use --force only with explicit user approval."
        )
    print(
        "Next: stop product-code changes; reviewers write independent JSON reports under "
        "docs/agent/longrun/reviews/pending/."
    )
    print("Then invoke: $codex-longrun-kit normalize review feedback")
    print(
        "Reminder: REVIEW.md defines review protocol. Approval comes from reports or user sign-off."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
