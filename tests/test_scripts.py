from __future__ import annotations

import json
import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from detect_stack import detect  # noqa: E402
from freeze_review import freeze  # noqa: E402
from init_longrun import init  # noqa: E402
from normalize_reviews import normalize  # noqa: E402

TEST_TMP = ROOT / ".codex_tmp_tests" / "unittest"
LONGRUN_DIR = Path("docs/agent/longrun")
REVIEWS_DIR = LONGRUN_DIR / "reviews"


class ScriptTests(unittest.TestCase):
    def make_target(self) -> Path:
        target = TEST_TMP / self._testMethodName
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        self.addCleanup(lambda: shutil.rmtree(target, ignore_errors=True))
        return target

    def test_init_standard_creates_compact_docs_only(self) -> None:
        target = self.make_target()
        (target / "package.json").write_text(
            json.dumps({"scripts": {"lint": "eslint .", "test": "vitest", "build": "vite build"}}),
            encoding="utf-8",
        )
        init(target, "standard", "Build X")
        self.assertTrue((target / LONGRUN_DIR / "LONGRUN.md").exists())
        self.assertTrue((target / LONGRUN_DIR / "STATE.md").exists())
        self.assertFalse((target / LONGRUN_DIR / "STRICT.md").exists())
        self.assertFalse((target / "docs/agent/STOP_RULES.md").exists())
        self.assertFalse((target / "docs/agent/VALIDATION_MATRIX.md").exists())
        self.assertFalse((target / "docs/agent/LONGRUN.md").exists())
        text = (target / LONGRUN_DIR / "LONGRUN.md").read_text(encoding="utf-8")
        self.assertIn("Build X", text)
        self.assertIn("npm run lint", text)
        self.assertIn("Scripts create artifacts", text)
        self.assertIn("plan -> longrun -> closeout", text)

    def test_init_strict_creates_one_appendix(self) -> None:
        target = self.make_target()
        init(target, "strict", "Strict task")
        self.assertTrue((target / LONGRUN_DIR / "STRICT.md").exists())
        self.assertFalse((target / "docs/agent/STOP_RULES.md").exists())
        self.assertFalse((target / "docs/agent/VALIDATION_MATRIX.md").exists())

    def test_detect_go_uses_non_mutating_gofmt(self) -> None:
        target = self.make_target()
        (target / "go.mod").write_text("module example.com/x\n", encoding="utf-8")
        data = detect(target)
        commands = "\n".join(data["commands"]["fast"])
        self.assertIn("gofmt -l .", commands)
        self.assertNotIn("gofmt -w", commands)

    def test_freeze_and_normalize(self) -> None:
        target = self.make_target()
        init(target, "standard", "Review task")
        freeze(target, "HEAD")
        pending = target / REVIEWS_DIR / "pending"
        self.assertTrue((target / LONGRUN_DIR / "REVIEW.md").exists())
        self.assertFalse((target / "docs/agent/REVIEW.md").exists())
        review_text = (target / LONGRUN_DIR / "REVIEW.md").read_text(encoding="utf-8")
        self.assertIn("defines the frozen version", review_text)
        self.assertIn("invoke $codex-longrun-kit normalize review feedback", review_text)
        self.assertNotIn("python scripts/normalize_reviews.py --target .", review_text)
        self.assertIn("docs/agent/longrun/reviews/pending", review_text)
        reviews_readme = (target / REVIEWS_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("invoke $codex-longrun-kit normalize review feedback", reviews_readme)
        self.assertNotIn("python scripts/normalize_reviews.py --target .", reviews_readme)
        self.assertIn("docs/agent/longrun/reviews/pending", reviews_readme)
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
        }), encoding="utf-8-sig")
        queue = normalize(target)
        self.assertEqual(len(queue["tickets"]), 1)
        self.assertEqual(queue["tickets"][0]["ticket_id"], "RQ-001")
        self.assertIn("draft", queue["notes"][0])
        self.assertTrue((target / REVIEWS_DIR / "ReviewQueue.json").exists())
        self.assertFalse((target / "docs/reviews/ReviewQueue.json").exists())


if __name__ == "__main__":
    unittest.main()
