from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScriptTests(unittest.TestCase):
    def run_script(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=cwd or ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def test_init_standard_creates_compact_docs_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "package.json").write_text(
                json.dumps({"scripts": {"lint": "eslint .", "test": "vitest", "build": "vite build"}}),
                encoding="utf-8",
            )
            self.run_script("scripts/init_longrun.py", "--target", str(target), "--profile", "standard", "--task-brief", "Build X")
            self.assertTrue((target / "docs/agent/LONGRUN.md").exists())
            self.assertTrue((target / "docs/agent/STATE.md").exists())
            self.assertFalse((target / "docs/agent/STOP_RULES.md").exists())
            self.assertFalse((target / "docs/agent/VALIDATION_MATRIX.md").exists())
            text = (target / "docs/agent/LONGRUN.md").read_text(encoding="utf-8")
            self.assertIn("Build X", text)
            self.assertIn("npm run lint", text)

    def test_init_strict_creates_split_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            self.run_script("scripts/init_longrun.py", "--target", str(target), "--profile", "strict", "--task-brief", "Strict task")
            self.assertTrue((target / "docs/agent/STOP_RULES.md").exists())
            self.assertTrue((target / "docs/agent/VALIDATION_MATRIX.md").exists())

    def test_freeze_and_normalize(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            self.run_script("scripts/init_longrun.py", "--target", str(target), "--task-brief", "Review task")
            self.run_script("scripts/freeze_review.py", "--target", str(target), "--base", "HEAD")
            pending = target / "docs/reviews/pending"
            self.assertTrue((target / "docs/agent/REVIEW.md").exists())
            pending.mkdir(parents=True, exist_ok=True)
            (pending / "security.json").write_text(json.dumps({
                "reviewer_lane": "security",
                "base_commit": "abc123",
                "findings": [{
                    "id": "SEC-001",
                    "severity": "P1",
                    "claim": "Auth check missing",
                    "affected_files": ["src/api.ts"],
                    "acceptance_criteria": ["Unauthenticated request returns 401"],
                    "validation_commands": ["npm test -- auth"],
                    "requires_human_decision": False,
                }],
            }), encoding="utf-8")
            self.run_script("scripts/normalize_reviews.py", "--target", str(target))
            queue = json.loads((target / "docs/reviews/ReviewQueue.json").read_text(encoding="utf-8"))
            self.assertEqual(len(queue["tickets"]), 1)
            self.assertEqual(queue["tickets"][0]["ticket_id"], "RQ-001")


if __name__ == "__main__":
    unittest.main()
