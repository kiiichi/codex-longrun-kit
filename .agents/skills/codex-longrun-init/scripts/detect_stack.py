#!/usr/bin/env python3
"""Detect candidate validation commands for a repository.

The output is intentionally conservative. Commands are candidates until a human
or Codex runs and verifies them.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class CommandCandidate:
    category: str
    command: str
    reason: str
    confidence: str = "candidate"


@dataclass
class StackDetection:
    repo_root: str
    markers: list[str]
    commands: list[CommandCandidate]
    notes: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        data = asdict(self)
        data["commands"] = [asdict(c) for c in self.commands]
        return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
        return "bun"
    return "npm"


def _script_command(manager: str, script: str) -> str:
    if manager == "npm" and script == "test":
        return "npm test"
    if manager == "npm":
        return f"npm run {script}"
    if manager == "yarn":
        return f"yarn {script}"
    if manager == "pnpm":
        return f"pnpm {script}"
    if manager == "bun":
        return f"bun run {script}"
    return f"{manager} run {script}"


def _add(commands: list[CommandCandidate], category: str, command: str, reason: str) -> None:
    if not any(c.command == command for c in commands):
        commands.append(CommandCandidate(category=category, command=command, reason=reason))


def detect_stack(repo_root: str | Path) -> StackDetection:
    root = Path(repo_root).resolve()
    markers: list[str] = []
    commands: list[CommandCandidate] = []
    notes: list[str] = []

    if not root.exists():
        notes.append(f"Repository root does not exist yet: {root}")
        return StackDetection(str(root), markers, commands, notes)

    package_json = root / "package.json"
    if package_json.exists():
        markers.append("package.json")
        manager = _package_manager(root)
        pkg = _read_json(package_json)
        scripts = pkg.get("scripts", {}) if isinstance(pkg.get("scripts"), dict) else {}
        for category, names in [
            ("lint", ["lint"]),
            ("typecheck", ["typecheck", "type-check", "tsc"]),
            ("test", ["test", "test:unit", "test:ci"]),
            ("build", ["build"]),
            ("e2e", ["test:e2e", "e2e"]),
        ]:
            for name in names:
                if name in scripts:
                    _add(commands, category, _script_command(manager, name), f"package.json script `{name}`")
                    break
        if not scripts:
            notes.append("package.json exists but no scripts were detected.")

    if (root / "pyproject.toml").exists():
        markers.append("pyproject.toml")
    if (root / "requirements.txt").exists():
        markers.append("requirements.txt")
    if (root / "setup.py").exists():
        markers.append("setup.py")
    if any((root / name).exists() for name in ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"]):
        if (root / "tests").exists() or any(root.glob("test_*.py")):
            _add(commands, "test", "python -m pytest", "Python project with tests detected")
        if _file_contains(root / "pyproject.toml", r"\[tool\.ruff\]") or (root / "ruff.toml").exists():
            _add(commands, "lint", "python -m ruff check .", "Ruff configuration detected")
        if _file_contains(root / "pyproject.toml", r"\[tool\.mypy\]") or (root / "mypy.ini").exists():
            _add(commands, "typecheck", "python -m mypy .", "Mypy configuration detected")

    if (root / "Cargo.toml").exists():
        markers.append("Cargo.toml")
        _add(commands, "format", "cargo fmt --check", "Rust project detected")
        _add(commands, "lint", "cargo clippy -- -D warnings", "Rust project detected")
        _add(commands, "test", "cargo test", "Rust project detected")
        _add(commands, "build", "cargo build", "Rust project detected")

    if (root / "go.mod").exists():
        markers.append("go.mod")
        _add(commands, "test", "go test ./...", "Go module detected")
        _add(commands, "lint", "go vet ./...", "Go module detected")

    if (root / "pom.xml").exists():
        markers.append("pom.xml")
        _add(commands, "test", "mvn test", "Maven project detected")
        _add(commands, "build", "mvn package -DskipTests", "Maven project detected")

    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
        markers.append("Gradle build file")
        gradle = "./gradlew" if (root / "gradlew").exists() else "gradle"
        _add(commands, "test", f"{gradle} test", "Gradle project detected")
        _add(commands, "build", f"{gradle} build", "Gradle project detected")

    makefile = root / "Makefile"
    if makefile.exists():
        markers.append("Makefile")
        text = makefile.read_text(encoding="utf-8", errors="ignore")
        for target, category in [("test", "test"), ("lint", "lint"), ("typecheck", "typecheck"), ("build", "build")]:
            if re.search(rf"^{re.escape(target)}\s*:", text, flags=re.MULTILINE):
                _add(commands, category, f"make {target}", f"Makefile target `{target}`")

    if not commands:
        notes.append("No validation commands detected. Fill VALIDATION_MATRIX.md manually.")

    return StackDetection(str(root), markers, commands, notes)


def _file_contains(path: Path, pattern: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return re.search(pattern, text) is not None


def as_markdown(detection: StackDetection) -> str:
    lines: list[str] = []
    if detection.markers:
        lines.append("Detected markers:")
        for marker in detection.markers:
            lines.append(f"- `{marker}`")
    else:
        lines.append("Detected markers: none")
    lines.append("")
    if detection.commands:
        lines.append("Candidate validation commands:")
        for cmd in detection.commands:
            lines.append(f"- `{cmd.command}` — {cmd.category}; {cmd.reason}")
    else:
        lines.append("Candidate validation commands: none")
    if detection.notes:
        lines.append("")
        lines.append("Notes:")
        for note in detection.notes:
            lines.append(f"- {note}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect candidate validation commands for a repo.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    detection = detect_stack(args.repo_root)
    if args.format == "json":
        print(json.dumps(detection.to_jsonable(), indent=2, ensure_ascii=False))
    else:
        print(as_markdown(detection))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
