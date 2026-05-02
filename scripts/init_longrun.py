#!/usr/bin/env python3
"""Initialize compact long-running Codex runtime docs in a target repo."""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

try:
    from detect_stack import detect
except ImportError:  # pragma: no cover
    from scripts.detect_stack import detect  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"


def read_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def format_commands(commands: list[str] | None) -> str:
    if not commands:
        return "- UNCONFIRMED: add command."
    return "\n".join(f"- `{cmd}`" for cmd in commands)


def render(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_file(path: Path, content: str, *, force: bool) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def init(target: Path, profile: str, task_brief: str, force: bool = False) -> list[str]:
    target = target.resolve()
    target.mkdir(parents=True, exist_ok=True)
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
    docs_agent = target / "docs" / "agent"
    for name in ["LONGRUN.md", "STATE.md"]:
        content = render(read_template(f"{name}.template"), mapping)
        if write_file(docs_agent / name, content, force=force):
            written.append(str((docs_agent / name).relative_to(target)))

    artifacts = target / ".codex_artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    if write_file(artifacts / ".gitignore", "*\n!.gitignore\n", force=force):
        written.append(str((artifacts / ".gitignore").relative_to(target)))

    if profile == "strict":
        for name in ["STOP_RULES.md", "VALIDATION_MATRIX.md"]:
            content = render(read_template(f"{name}.template"), mapping)
            if write_file(docs_agent / name, content, force=force):
                written.append(str((docs_agent / name).relative_to(target)))

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", "--target-root", dest="target", default=".", help="Target repo root")
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
        print("No files written. Existing files preserved. Use --force to overwrite.")
    print("Next: inspect docs/agent/LONGRUN.md and docs/agent/STATE.md, then stop for plan review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
