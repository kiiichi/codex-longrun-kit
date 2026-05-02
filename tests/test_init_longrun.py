from pathlib import Path

from init_longrun import init_longrun


def test_init_creates_expected_files(tmp_path: Path) -> None:
    result = init_longrun(tmp_path, "Build a sample feature", force=False)
    assert (tmp_path / "docs" / "agent" / "Prompt.md").exists()
    assert (tmp_path / "docs" / "agent" / "Plan.md").exists()
    assert (tmp_path / "docs" / "agent" / "Implement.md").exists()
    assert (tmp_path / "docs" / "agent" / "CONTINUITY.md").exists()
    assert (tmp_path / "docs" / "reviews" / "pending").is_dir()
    assert ".codex_artifacts/logs" in result["directories"]


def test_init_does_not_overwrite_without_force(tmp_path: Path) -> None:
    init_longrun(tmp_path, "First", force=False)
    prompt = tmp_path / "docs" / "agent" / "Prompt.md"
    prompt.write_text("custom", encoding="utf-8")
    result = init_longrun(tmp_path, "Second", force=False)
    assert prompt.read_text(encoding="utf-8") == "custom"
    assert "docs/agent/Prompt.md" in result["skipped"]
