#!/usr/bin/env python3
"""Detect candidate validation gates.

Read visible project files. Return candidates. Leave repo state unchanged.
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
    text = "\n".join((root / m).read_text(encoding="utf-8", errors="ignore") for m in markers if (root / m).exists())
    fast: list[str] = []
    if "ruff" in text:
        fast.append("python -m ruff check .")
    if "mypy" in text:
        fast.append("python -m mypy .")
    return {
        "fast": fast,
        "targeted": ["python -m pytest -q"],
        "full": ["python -m pytest"],
        "freeze": fast + ["python -m pytest"],
    }


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
        "fast": ["gofmt -l .", "go vet ./..."],
        "targeted": ["go test ./..."],
        "full": ["go test ./..."],
        "freeze": ["gofmt -l .", "go vet ./...", "go test ./..."],
    }


def make_commands(root: Path) -> dict[str, list[str]]:
    makefile = root / "Makefile"
    if not makefile.exists():
        return {}
    text = makefile.read_text(encoding="utf-8", errors="ignore")
    cmds: dict[str, list[str]] = {"fast": [], "targeted": [], "full": [], "freeze": []}
    for target, bucket in [("lint", "fast"), ("typecheck", "fast"), ("test", "targeted"), ("build", "full")]:
        if f"{target}:" in text:
            cmds[bucket].append(f"make {target}")
            if bucket != "freeze":
                cmds["freeze"].append(f"make {target}")
    return cmds


def merge(target: dict[str, list[str]], source: dict[str, list[str]]) -> None:
    for key, values in source.items():
        target.setdefault(key, [])
        for value in values:
            if value not in target[key]:
                target[key].append(value)


def detect(root: Path) -> dict[str, Any]:
    root = root.resolve()
    commands: dict[str, list[str]] = {"fast": [], "targeted": [], "full": [], "freeze": []}
    for detector in [js_commands, python_commands, rust_commands, go_commands, make_commands]:
        merge(commands, detector(root))
    if not any(commands.values()):
        commands = {
            "fast": ["UNCONFIRMED: add lint/typecheck command"],
            "targeted": ["UNCONFIRMED: add targeted test command"],
            "full": ["UNCONFIRMED: add full test/build command"],
            "freeze": ["UNCONFIRMED: add review-freeze validation command"],
        }
    return {
        "root": str(root),
        "notes": ["Detected commands are candidates. Confirm before promoting to validation gates."],
        "commands": commands,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", "--target-root", dest="target", default=".", help="Repository root to inspect")
    args = parser.parse_args()
    print(json.dumps(detect(Path(args.target)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
