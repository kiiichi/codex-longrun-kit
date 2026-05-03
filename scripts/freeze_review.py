#!/usr/bin/env python3
"""Create lazy review artifacts for a frozen long-running Codex result.

Writes review protocol files only. It does not freeze git itself, prevent future
edits, review the code, or make product decisions.
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"


def run_git(target: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=target, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "UNCONFIRMED"


def render(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def working_tree_status(target: Path) -> str:
    status = run_git(target, ["status", "--short"])
    if status == "UNCONFIRMED":
        return "- UNCONFIRMED: git status unavailable."
    if not status:
        return "- Clean working tree reported by git."
    lines = ["- WARNING: working tree has uncommitted changes. Review freeze is not stable until committed or explicitly recorded."]
    lines.extend(f"- `{line}`" for line in status.splitlines()[:30])
    if len(status.splitlines()) > 30:
        lines.append("- Additional changes omitted from this summary.")
    return "\n".join(lines)


def freeze(target: Path, base: str, force: bool = False) -> list[str]:
    target = target.resolve()
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    current_commit = run_git(target, ["rev-parse", "HEAD"])
    current_branch = run_git(target, ["branch", "--show-current"])
    current_ref = current_branch if current_branch != "UNCONFIRMED" and current_branch else current_commit
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
    docs_agent = target / "docs" / "agent"
    docs_reviews = target / "docs" / "reviews"
    review_artifacts = target / ".codex_artifacts" / "review"

    for path in [docs_agent, docs_reviews / "pending", docs_reviews / "status", review_artifacts]:
        path.mkdir(parents=True, exist_ok=True)

    review_text = render((TEMPLATES / "REVIEW.md.template").read_text(encoding="utf-8"), mapping)
    review_path = docs_agent / "REVIEW.md"
    if force or not review_path.exists():
        review_path.write_text(review_text, encoding="utf-8")
        written.append(str(review_path.relative_to(target)))

    readme_path = docs_reviews / "README.md"
    if force or not readme_path.exists():
        readme_path.write_text((TEMPLATES / "reviews_README.md.template").read_text(encoding="utf-8"), encoding="utf-8")
        written.append(str(readme_path.relative_to(target)))

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", "--target-root", dest="target", default=".", help="Target repo root")
    parser.add_argument("--base", default="main", help="Base ref to compare against")
    parser.add_argument("--force", action="store_true", help="Overwrite review files")
    args = parser.parse_args()

    written = freeze(Path(args.target), args.base, force=args.force)
    if written:
        print("Created/updated:")
        for item in written:
            print(f"- {item}")
    else:
        print("No files written. Existing review files preserved. Use --force only with explicit user approval.")
    print("Next: stop product-code changes; reviewers write independent JSON reports under docs/reviews/pending/.")
    print("Reminder: REVIEW.md is a protocol, not a review verdict.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
