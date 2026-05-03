"""Longrun runtime paths.

One namespace. One source of path truth.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
SCHEMAS = ROOT / "assets" / "schemas"

LONGRUN_DIR = Path("docs") / "agent" / "longrun"
REVIEWS_DIR = LONGRUN_DIR / "reviews"
PENDING_REVIEWS_DIR = REVIEWS_DIR / "pending"
REVIEW_STATUS_DIR = REVIEWS_DIR / "status"
CODEX_ARTIFACTS_DIR = Path(".codex_artifacts")
REVIEW_ARTIFACTS_DIR = CODEX_ARTIFACTS_DIR / "review"


def target_root(target: Path) -> Path:
    return target.resolve()


def longrun_dir(target: Path) -> Path:
    return target_root(target) / LONGRUN_DIR


def reviews_dir(target: Path) -> Path:
    return target_root(target) / REVIEWS_DIR


def pending_reviews_dir(target: Path) -> Path:
    return target_root(target) / PENDING_REVIEWS_DIR


def review_status_dir(target: Path) -> Path:
    return target_root(target) / REVIEW_STATUS_DIR


def codex_artifacts_dir(target: Path) -> Path:
    return target_root(target) / CODEX_ARTIFACTS_DIR


def review_artifacts_dir(target: Path) -> Path:
    return target_root(target) / REVIEW_ARTIFACTS_DIR


def template_path(name: str) -> Path:
    return TEMPLATES / name


def schema_path(name: str) -> Path:
    return SCHEMAS / name


def relative_to_target(target: Path, path: Path) -> str:
    return str(path.relative_to(target_root(target)))
