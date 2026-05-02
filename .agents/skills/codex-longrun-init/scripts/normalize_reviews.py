#!/usr/bin/env python3
"""Normalize independent review files into docs/reviews/ReviewQueue.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - exercised only when PyYAML missing
    yaml = None


SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}


def _load_review(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if yaml is None:
        raise RuntimeError("PyYAML is required for YAML review files. Use JSON or install PyYAML.")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Review file must contain an object: {path}")
    return data


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _affected_files(item: dict[str, Any]) -> list[str]:
    files = _as_list(item.get("affected_files"))
    evidence = item.get("evidence")
    if isinstance(evidence, dict):
        files.extend(_as_list(evidence.get("files")))
    clean: list[str] = []
    for file in files:
        if not isinstance(file, str):
            continue
        clean.append(file.split(":", 1)[0])
    return sorted(set(clean))


def _fingerprint(item: dict[str, Any]) -> str:
    claim = str(item.get("claim", "")).strip().lower()
    files = "|".join(_affected_files(item))
    criteria = "|".join(str(x).strip().lower() for x in _as_list(item.get("acceptance_criteria")))
    raw = f"{claim}|{files}|{criteria}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def _best_severity(a: str | None, b: str | None) -> str:
    a = a or "P3"
    b = b or "P3"
    return a if SEVERITY_ORDER.get(a, 99) <= SEVERITY_ORDER.get(b, 99) else b


def normalize_reviews(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    pending = root / "docs" / "reviews" / "pending"
    out_dir = root / "docs" / "reviews"
    out_dir.mkdir(parents=True, exist_ok=True)

    review_files = sorted(
        [p for p in pending.glob("*") if p.suffix.lower() in {".yaml", ".yml", ".json"}]
    )

    grouped: dict[str, dict[str, Any]] = {}
    human_decisions: list[dict[str, Any]] = []
    file_to_ticket_ids: dict[str, list[str]] = {}
    base_commit = ""

    for path in review_files:
        review = _load_review(path)
        lane = str(review.get("reviewer_lane") or path.stem)
        base_commit = base_commit or str(review.get("base_commit") or "")
        for item in _as_list(review.get("items")):
            if not isinstance(item, dict):
                continue
            source_id = str(item.get("id") or f"{lane}-{len(grouped) + 1:03d}")
            fp = _fingerprint(item)
            files = _affected_files(item)
            severity = str(item.get("severity") or "P3")
            ticket = grouped.get(fp)
            if ticket is None:
                ticket = {
                    "fingerprint": fp,
                    "source_review_ids": [],
                    "reviewer_lanes": [],
                    "title": str(item.get("claim") or "Untitled review item"),
                    "severity": severity,
                    "affected_files": files,
                    "acceptance_criteria": [],
                    "validation_commands": [],
                    "suggested_directions": [],
                    "requires_human_decision": False,
                    "parallelizable": True,
                    "dependencies": [],
                    "raw_items": [],
                }
                grouped[fp] = ticket
            ticket["source_review_ids"].append(source_id)
            if lane not in ticket["reviewer_lanes"]:
                ticket["reviewer_lanes"].append(lane)
            ticket["severity"] = _best_severity(ticket.get("severity"), severity)
            ticket["affected_files"] = sorted(set(ticket.get("affected_files", []) + files))
            ticket["acceptance_criteria"] = sorted(
                set(ticket.get("acceptance_criteria", []) + [str(x) for x in _as_list(item.get("acceptance_criteria"))])
            )
            ticket["validation_commands"] = sorted(
                set(ticket.get("validation_commands", []) + [str(x) for x in _as_list(item.get("validation_commands"))])
            )
            direction = item.get("suggested_direction")
            if direction and str(direction) not in ticket["suggested_directions"]:
                ticket["suggested_directions"].append(str(direction))
            if bool(item.get("requires_human_decision")):
                ticket["requires_human_decision"] = True
                human_decisions.append(
                    {
                        "source_review_id": source_id,
                        "reviewer_lane": lane,
                        "claim": item.get("claim"),
                        "affected_files": files,
                    }
                )
            ticket["raw_items"].append({"review_file": str(path.relative_to(root)), "item": item})

    tickets = []
    for index, ticket in enumerate(sorted(grouped.values(), key=lambda t: (SEVERITY_ORDER.get(t.get("severity", "P3"), 99), t.get("title", ""))), start=1):
        ticket_id = f"RQ-{index:03d}"
        ticket["ticket_id"] = ticket_id
        for file in ticket.get("affected_files", []):
            file_to_ticket_ids.setdefault(file, []).append(ticket_id)
        tickets.append(ticket)

    potential_conflicts = []
    for file, ticket_ids in sorted(file_to_ticket_ids.items()):
        if len(ticket_ids) > 1:
            potential_conflicts.append(
                {
                    "affected_file": file,
                    "ticket_ids": ticket_ids,
                    "reason": "Multiple normalized tickets affect the same file. Review merge order and semantic compatibility.",
                }
            )
            for ticket in tickets:
                if ticket["ticket_id"] in ticket_ids:
                    ticket["parallelizable"] = False

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    queue = {
        "base_commit": base_commit,
        "generated_at": generated_at,
        "tickets": tickets,
        "human_decisions_needed": human_decisions,
        "potential_conflicts": potential_conflicts,
    }

    queue_path = out_dir / "ReviewQueue.json"
    queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

    decisions_path = out_dir / "HumanDecisionsNeeded.md"
    decisions_path.write_text(_human_decisions_markdown(queue), encoding="utf-8")

    return {
        "review_files": [str(p.relative_to(root)) for p in review_files],
        "ticket_count": len(tickets),
        "human_decision_count": len(human_decisions),
        "potential_conflict_count": len(potential_conflicts),
        "queue_path": str(queue_path),
        "human_decisions_path": str(decisions_path),
    }


def _human_decisions_markdown(queue: dict[str, Any]) -> str:
    lines = ["# HumanDecisionsNeeded.md", "", f"Generated: {queue['generated_at']}", ""]
    if not queue["human_decisions_needed"] and not queue["potential_conflicts"]:
        lines.append("No human decisions or potential conflicts were detected.")
        return "\n".join(lines) + "\n"

    if queue["human_decisions_needed"]:
        lines.append("## Explicit human decisions")
        lines.append("")
        for item in queue["human_decisions_needed"]:
            lines.append(f"- `{item['source_review_id']}` ({item['reviewer_lane']}): {item.get('claim')}")
            for file in item.get("affected_files", []):
                lines.append(f"  - affected: `{file}`")
        lines.append("")

    if queue["potential_conflicts"]:
        lines.append("## Potential conflicts")
        lines.append("")
        for conflict in queue["potential_conflicts"]:
            lines.append(f"- `{conflict['affected_file']}`: {', '.join(conflict['ticket_ids'])}")
            lines.append(f"  - {conflict['reason']}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize independent review files into ReviewQueue.json.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = normalize_reviews(args.repo_root)
    print("Review feedback normalized.")
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
