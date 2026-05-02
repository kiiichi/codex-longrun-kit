from pathlib import Path

from detect_stack import detect_stack


def test_detects_package_json_scripts(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        '{"scripts":{"lint":"eslint .","typecheck":"tsc --noEmit","test":"vitest","build":"vite build"}}',
        encoding="utf-8",
    )
    result = detect_stack(tmp_path)
    commands = {cmd.command for cmd in result.commands}
    assert "npm run lint" in commands
    assert "npm run typecheck" in commands
    assert "npm test" in commands
    assert "npm run build" in commands


def test_detects_python_pytest(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.ruff]\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    result = detect_stack(tmp_path)
    commands = {cmd.command for cmd in result.commands}
    assert "python -m pytest" in commands
    assert "python -m ruff check ." in commands
