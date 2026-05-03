"""Artifact rendering and protected writes."""
from __future__ import annotations

from pathlib import Path

try:
    from runtime_layout import relative_to_target, template_path
except ImportError:  # pragma: no cover
    from scripts.runtime_layout import relative_to_target, template_path  # type: ignore


def render(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


class ArtifactWriter:
    def __init__(self, target: Path, *, force: bool = False) -> None:
        self.target = target.resolve()
        self.force = force

    def read_template(self, name: str) -> str:
        return template_path(name).read_text(encoding="utf-8")

    def render_template(self, name: str, mapping: dict[str, str]) -> str:
        return render(self.read_template(name), mapping)

    def write(self, path: Path, content: str) -> bool:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not self.force:
            return False
        path.write_text(content, encoding="utf-8")
        return True

    def write_template(self, path: Path, template_name: str, mapping: dict[str, str]) -> bool:
        return self.write(path, self.render_template(template_name, mapping))

    def relative(self, path: Path) -> str:
        return relative_to_target(self.target, path)
