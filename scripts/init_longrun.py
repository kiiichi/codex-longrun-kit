#!/usr/bin/env python3
"""Initialize compact long-run runtime docs.

Create artifacts only. Product code, dependencies, approvals, secrets, deployments,
and remote state stay untouched.
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

try:
    from artifacts import ArtifactWriter
    from detect_stack import detect
    from runtime_layout import codex_artifacts_dir, longrun_dir, target_root
except ImportError:  # pragma: no cover
    from scripts.artifacts import ArtifactWriter  # type: ignore
    from scripts.detect_stack import detect  # type: ignore
    from scripts.runtime_layout import codex_artifacts_dir, longrun_dir, target_root  # type: ignore


def format_commands(commands: list[str] | None) -> str:
    if not commands:
        return "- UNCONFIRMED: add command."
    return "\n".join(f"- `{cmd}`" for cmd in commands)


def init(target: Path, profile: str, task_brief: str, force: bool = False) -> list[str]:
    target = target_root(target)
    target.mkdir(parents=True, exist_ok=True)
    writer = ArtifactWriter(target, force=force)
    detected = detect(target)["commands"]
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    mapping = {
        "TASK_BRIEF": task_brief.strip() or "UNCONFIRMED: task brief not provided.",
        "CREATED_AT": now,
        "FAST_VALIDATION": format_commands(detected.get("fast")),
        "TARGETED_VALIDATION": format_commands(detected.get("targeted")),
        "FULL_VALIDATION": format_commands(detected.get("full")),
        "FREEZE_VALIDATION": format_commands(detected.get("freeze")),
    }

    written: list[str] = []
    docs_agent = longrun_dir(target)
    for name in ["LONGRUN.md", "STATE.md"]:
        path = docs_agent / name
        if writer.write_template(path, f"{name}.template", mapping):
            written.append(writer.relative(path))

    artifacts = codex_artifacts_dir(target)
    artifacts.mkdir(parents=True, exist_ok=True)
    gitignore = artifacts / ".gitignore"
    if writer.write(gitignore, "*\n!.gitignore\n"):
        written.append(writer.relative(gitignore))

    if profile == "strict":
        path = docs_agent / "STRICT.md"
        if writer.write_template(path, "STRICT.md.template", mapping):
            written.append(writer.relative(path))

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target", "--target-root", dest="target", default=".", help="Target repo root"
    )
    parser.add_argument("--profile", choices=["minimal", "standard", "strict"], default="standard")
    parser.add_argument("--task-brief", default="", help="Task brief to place in LONGRUN.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files")
    args = parser.parse_args()

    written = init(Path(args.target), args.profile, args.task_brief, force=args.force)
    if written:
        print("Created/updated:")
        for item in written:
            print(f"- {item}")
    else:
        print(
            "No files written. Existing files preserved. "
            "Use --force only with explicit user approval."
        )
    print(
        "Next: inspect docs/agent/longrun/LONGRUN.md and docs/agent/longrun/STATE.md, "
        "then stop for plan review."
    )
    print("Reminder: validation commands are candidates. Confirm gates during M1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
