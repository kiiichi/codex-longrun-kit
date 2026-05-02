#!/usr/bin/env python3
"""Detect likely validation commands for compact Codex long-run docs.

The detector is intentionally conservative. It suggests commands from visible
project files; it does not install dependencies or execute project commands.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    return "npm"


def js_commands(root: Path) -> dict[str, list[str]]:
    pkg = root / "package.json"
    if not pkg.exists():
        return {}
    data = read_json(pkg)
    scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
    if not isinstance(scripts, dict):
        scripts = {}
    pm = package_manager(root)

    def cmd(name: str) -> list[str]:
        return [f"{pm} run {name}"] if name in scripts else []

    return {
        "fast": cmd("lint") + cmd("typecheck"),
        "targeted": cmd("test") or cmd("test:unit"),
        "full": cmd("test") + cmd("build"),
        "freeze": cmd("lint") + cmd("typecheck") + cmd("test") + cmd("build") + cmd("test:e2e"),
        "dev": cmd("dev"),
    }


def python_commands(root: Path) -> dict[str, list[str]]:
    markers = ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "tox.ini", "pytest.ini"]
    if not any((root / m).exists() for m in markers):
        return {}

    cmds: dict[str, list[str]] = {
        "fast": [],
        "targeted": ["python -m pytest -q"],
        "full": ["python -m pytest"],
        "freeze": ["python -m pytest"],
    }
    text = "\n".join((root / m).read_text(encoding="utf-8", errors="ignore") for m in markers if (root / m).exists())
    if "ruff" in text:
        cmds["fast"].append("python -m ruff check .")
        cmds["freeze"].insert(0, "python -m ruff check .")
    if "mypy" in text:
        cmds["fast"].append("python -m mypy .")
        cmds["freeze"].insert(0, "python -m mypy .")
    return cmds


def rust_commands(root: Path) -> dict[str, list[str]]:
    if not (root / "Cargo.toml").exists():
        return {}
    return {
        "fast": ["cargo fmt --check", "cargo clippy --all-targets -- -D warnings"],
        "targeted": ["cargo test"],
        "full": ["cargo test --all"],
        "freeze": ["cargo fmt --check", "cargo clippy --all-targets -- -D warnings", "cargo test --all"],
    }


def go_commands(root: Path) -> dict[str, list[str]]:
    if not (root / "go.mod").exists():
        return {}
    return {
        "fast": ["gofmt -w . # inspect diff before committing", "go vet ./..."],
        "targeted": ["go test ./..."],
        "full": ["go test ./..."],
        "freeze": ["go vet ./...", "go test ./..."],
    }


def makefile_commands(root: Path) -> dict[str, list[str]]:
    mf = root / "Makefile"
    if not mf.exists():
        return {}
    text = mf.read_text(encoding="utf-8", errors="ignore")
    targets = set()
    for line in text.splitlines():
        if line and not line.startswith((" ", "\t", "#")) and ":" in line:
            name = line.split(":", 1)[0].strip()
            if name and all(c.isalnum() or c in "_-" for c in name):
                targets.add(name)
    out = {"fast": [], "targeted": [], "full": [], "freeze": []}
    for target in ["lint", "typecheck", "check"]:
        if target in targets:
            out["fast"].append(f"make {target}")
    for target in ["test", "unit"]:
        if target in targets:
            out["targeted"].append(f"make {target}")
            out["full"].append(f"make {target}")
    for target in ["build", "e2e"]:
        if target in targets:
            out["full"].append(f"make {target}")
    out["freeze"] = list(dict.fromkeys(out["fast"] + out["full"]))
    return {k: v for k, v in out.items() if v}


def merge_commands(*groups: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {"fast": [], "targeted": [], "full": [], "freeze": [], "dev": []}
    for group in groups:
        for key, values in group.items():
            for value in values:
                if value not in merged.setdefault(key, []):
                    merged[key].append(value)
    return {k: v for k, v in merged.items() if v}


def detect(root: Path) -> dict[str, Any]:
    root = root.resolve()
    commands = merge_commands(
        js_commands(root),
        python_commands(root),
        rust_commands(root),
        go_commands(root),
        makefile_commands(root),
    )
    if not commands:
        commands = {
            "fast": ["UNCONFIRMED: add lint/typecheck command"],
            "targeted": ["UNCONFIRMED: add targeted test command"],
            "full": ["UNCONFIRMED: add full test/build command"],
            "freeze": ["UNCONFIRMED: add review-freeze validation command"],
        }
    return {"root": str(root), "commands": commands}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", "--target-root", dest="target", default=".", help="Repository root to inspect")
    args = parser.parse_args()
    print(json.dumps(detect(Path(args.target)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
