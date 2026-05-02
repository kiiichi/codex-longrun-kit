#!/usr/bin/env python3
"""Initialize a target repository for long-running Codex work."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from detect_stack import as_markdown, detect_stack


TEMPLATE_MAP = {
    "Prompt.md.template": "docs/agent/Prompt.md",
    "Plan.md.template": "docs/agent/Plan.md",
    "Implement.md.template": "docs/agent/Implement.md",
    "Documentation.md.template": "docs/agent/Documentation.md",
    "CONTINUITY.md.template": "docs/agent/CONTINUITY.md",
    "STOP_RULES.md.template": "docs/agent/STOP_RULES.md",
    "VALIDATION_MATRIX.md.template": "docs/agent/VALIDATION_MATRIX.md",
    "ReviewPacket.md.template": "docs/agent/ReviewPacket.md",
    "ReviewQueue.json.template": "docs/reviews/ReviewQueue.json",
    "HumanDecisionsNeeded.md.template": "docs/reviews/HumanDecisionsNeeded.md",
}

COPY_ONLY = {
    "review-item.schema.yaml": "docs/reviews/review-item.schema.yaml",
}


def _run_git(root: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def _repo_name(root: Path) -> str:
    top = _run_git(root, ["rev-parse", "--show-toplevel"])
    if top:
        return Path(top).name
    return root.name


def _read_task_brief(args: argparse.Namespace) -> str:
    if args.task_brief_file:
        return Path(args.task_brief_file).read_text(encoding="utf-8")
    if args.task_brief:
        return args.task_brief
    return "TODO: Paste the task brief, PRD, issue, migration brief, or refactor goal here."


def _compact(text: str, limit: int = 400) -> str:
    compact = " ".join(text.strip().split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _render(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def init_longrun(
    repo_root: str | Path,
    task_brief: str,
    force: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    root.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    template_dir = script_dir.parent / "assets" / "templates"
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    detection = detect_stack(root)
    validation_markdown = as_markdown(detection)

    values = {
        "CREATED_AT": created_at,
        "REPO_NAME": _repo_name(root),
        "TASK_BRIEF": task_brief.strip(),
        "TASK_BRIEF_COMPACT": _compact(task_brief),
        "VALIDATION_COMMANDS_MARKDOWN": validation_markdown,
        "RUN_ID": f"RUN-{created_at.replace(':', '').replace('-', '')}",
        "BASE_COMMIT": "not captured yet",
        "HEAD_COMMIT": _run_git(root, ["rev-parse", "--short", "HEAD"]) or "not captured yet",
        "BRANCH": _run_git(root, ["branch", "--show-current"]) or "not captured yet",
        "WORKTREE_STATUS": "not captured yet",
        "DIFFSTAT": "not captured yet",
        "CHANGED_FILES_MARKDOWN": "- not captured yet",
    }

    dirs = [
        root / "docs" / "agent",
        root / "docs" / "reviews" / "pending",
        root / "docs" / "reviews" / "status",
        root / ".codex_artifacts" / "logs",
        root / ".codex_artifacts" / "review",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []

    for template_name, dest_rel in TEMPLATE_MAP.items():
        src = template_dir / template_name
        dest = root / dest_rel
        content = _render(src.read_text(encoding="utf-8"), values)
        if dest.exists() and not force:
            skipped.append(dest_rel)
            continue
        if dest.exists() and force:
            overwritten.append(dest_rel)
        else:
            created.append(dest_rel)
        dest.write_text(content, encoding="utf-8")

    for template_name, dest_rel in COPY_ONLY.items():
        src = template_dir / template_name
        dest = root / dest_rel
        content = _render(src.read_text(encoding="utf-8"), values)
        if dest.exists() and not force:
            skipped.append(dest_rel)
            continue
        if dest.exists() and force:
            overwritten.append(dest_rel)
        else:
            created.append(dest_rel)
        dest.write_text(content, encoding="utf-8")

    result = {
        "repo_root": str(root),
        "created": created,
        "skipped": skipped,
        "overwritten": overwritten,
        "directories": [str(d.relative_to(root)) for d in dirs],
        "detection": detection.to_jsonable(),
        "next_step": "Review docs/agent/Plan.md before broad implementation.",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a repo for long-running Codex work.")
    parser.add_argument("--repo-root", default=".", help="Target repository root.")
    parser.add_argument("--task-brief", default="", help="Task brief text.")
    parser.add_argument("--task-brief-file", default="", help="Path to a file containing the task brief.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files.")
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    args = parser.parse_args()

    task_brief = _read_task_brief(args)
    result = init_longrun(args.repo_root, task_brief, force=args.force)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Long-run scaffold initialized.")
        print(f"Repository: {result['repo_root']}")
        if result["created"]:
            print("Created:")
            for path in result["created"]:
                print(f"- {path}")
        if result["overwritten"]:
            print("Overwritten:")
            for path in result["overwritten"]:
                print(f"- {path}")
        if result["skipped"]:
            print("Skipped existing files:")
            for path in result["skipped"]:
                print(f"- {path}")
        print("\nCandidate validation commands:")
        for cmd in result["detection"]["commands"]:
            print(f"- {cmd['command']} ({cmd['category']})")
        if not result["detection"]["commands"]:
            print("- none detected; fill docs/agent/VALIDATION_MATRIX.md manually")
        print(f"\nNext step: {result['next_step']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
