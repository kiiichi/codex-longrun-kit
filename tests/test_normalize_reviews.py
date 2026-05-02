from pathlib import Path
import json

from normalize_reviews import normalize_reviews


def test_normalize_reviews_creates_queue(tmp_path: Path) -> None:
    pending = tmp_path / "docs" / "reviews" / "pending"
    pending.mkdir(parents=True)
    (pending / "security.yaml").write_text(
        """
reviewer_lane: security
base_commit: abc123
items:
  - id: SEC-001
    severity: P1
    claim: Auth missing
    affected_files:
      - src/api.py
    acceptance_criteria:
      - returns 401 when unauthenticated
    validation_commands:
      - pytest tests/test_auth.py
    requires_human_decision: false
""".strip(),
        encoding="utf-8",
    )
    result = normalize_reviews(tmp_path)
    assert result["ticket_count"] == 1
    queue = json.loads((tmp_path / "docs" / "reviews" / "ReviewQueue.json").read_text(encoding="utf-8"))
    assert queue["tickets"][0]["ticket_id"] == "RQ-001"
    assert queue["tickets"][0]["source_review_ids"] == ["SEC-001"]
