from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from detect_stack import detect  # noqa: E402
from freeze_review import freeze  # noqa: E402
from init_longrun import init  # noqa: E402
from normalize_reviews import normalize  # noqa: E402


class ScriptTests(unittest.TestCase):
    def test_init_standard_creates_compact_docs_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "package.json").write_text(
                json.dumps({"scripts": {"lint": "eslint .", "test": "vitest", "build": "vite build"}}),
                encoding="utf-8",
            )
            init(target, "standard", "Build X")
            self.assertTrue((target / "docs/agent/LONGRUN.md").exists())
            self.assertTrue((target / "docs/agent/STATE.md").exists())
            self.assertFalse((target / "docs/agent/STRICT.md").exists())
            self.assertFalse((target / "docs/agent/STOP_RULES.md").exists())
            self.assertFalse((target / "docs/agent/VALIDATION_MATRIX.md").exists())
            text = (target / "docs/agent/LONGRUN.md").read_text(encoding="utf-8")
            self.assertIn("Build X", text)
            self.assertIn("npm run lint", text)
            self.assertIn("Scripts may generate or update docs", text)

    def test_init_strict_creates_one_appendix(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            init(target, "strict", "Strict task")
            self.assertTrue((target / "docs/agent/STRICT.md").exists())
            self.assertFalse((target / "docs/agent/STOP_RULES.md").exists())
            self.assertFalse((target / "docs/agent/VALIDATION_MATRIX.md").exists())

    def test_detect_go_uses_non_mutating_gofmt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "go.mod").write_text("module example.com/x\n", encoding="utf-8")
            data = detect(target)
            commands = "\n".join(data["commands"]["fast"])
            self.assertIn("gofmt -l .", commands)
            self.assertNotIn("gofmt -w", commands)

    def test_freeze_and_normalize(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            init(target, "standard", "Review task")
            freeze(target, "HEAD")
            pending = target / "docs/reviews/pending"
            self.assertTrue((target / "docs/agent/REVIEW.md").exists())
            review_text = (target / "docs/agent/REVIEW.md").read_text(encoding="utf-8")
            self.assertIn("review protocol, not a review verdict", review_text)
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
            queue = normalize(target)
            self.assertEqual(len(queue["tickets"]), 1)
            self.assertEqual(queue["tickets"][0]["ticket_id"], "RQ-001")
            self.assertIn("draft", queue["notes"][0])


if __name__ == "__main__":
    unittest.main()
