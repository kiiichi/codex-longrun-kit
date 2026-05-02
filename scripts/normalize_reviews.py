#!/usr/bin/env python3
"""Normalize independent review reports into atomic ReviewQueue tickets.

This script is read-only with respect to product code. It only reads
`docs/reviews/pending/*.json` and writes review queue artifacts.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"

SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "info": 4}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80]


def load_reports(pending: Path) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    if not pending.exists():
        return reports
    for path in sorted(pending.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["_source_path"] = str(path)
            reports.append(data)
        except json.JSONDecodeError as exc:
            reports.append({
                "reviewer_lane": "invalid-json",
                "_source_path": str(path),
                "findings": [{
                    "id": f"INVALID-{path.stem}",
                    "severity": "P1",
                    "claim": f"Invalid JSON in {path}: {exc}",
                    "requires_human_decision": True,
                }],
            })
    return reports


def finding_key(finding: dict[str, Any]) -> str:
    claim = slug(str(finding.get("claim", "")))
    files = finding.get("affected_files") or []
    if not isinstance(files, list):
        files = []
    return claim + "|" + ",".join(sorted(map(str, files)))


def normalize(target: Path) -> dict[str, Any]:
    target = target.resolve()
    pending = target / "docs" / "reviews" / "pending"
    outdir = target / "docs" / "reviews"
    outdir.mkdir(parents=True, exist_ok=True)

    reports = load_reports(pending)
    groups: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    base_commit = "UNCONFIRMED"
    for report in reports:
        if report.get("base_commit") and base_commit == "UNCONFIRMED":
            base_commit = str(report["base_commit"])
        for finding in report.get("findings", []) or []:
            if not isinstance(finding, dict):
                continue
            groups.setdefault(finding_key(finding), []).append((report, finding))

    tickets: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    human_decisions: list[dict[str, Any]] = []

    for idx, (_key, items) in enumerate(sorted(groups.items()), start=1):
        findings = [f for _r, f in items]
        severity = min((str(f.get("severity", "P3")) for f in findings), key=lambda s: SEVERITY_ORDER.get(s, 99))
        first = findings[0]
        source_ids = []
        affected_files: list[str] = []
        acceptance: list[str] = []
        commands: list[str] = []
        requires_human = False

        for report, finding in items:
            rid = str(finding.get("id") or f"{report.get('reviewer_lane', 'review')}-{idx}")
            source_ids.append(rid)
            for value in finding.get("affected_files") or []:
                if str(value) not in affected_files:
                    affected_files.append(str(value))
            for value in finding.get("acceptance_criteria") or []:
                if str(value) not in acceptance:
                    acceptance.append(str(value))
            for value in finding.get("validation_commands") or []:
                if str(value) not in commands:
                    commands.append(str(value))
            requires_human = requires_human or bool(finding.get("requires_human_decision"))

        ticket = {
            "ticket_id": f"RQ-{idx:03d}",
            "title": str(first.get("claim", "Untitled review finding"))[:120],
            "severity": severity,
            "source_review_ids": source_ids,
            "affected_files": affected_files,
            "acceptance_criteria": acceptance or ["Reviewer finding is addressed and validated."],
            "validation_commands": commands,
            "requires_human_decision": requires_human,
            "parallelizable": not requires_human and len(affected_files) <= 5,
            "status": "open",
        }
        tickets.append(ticket)
        if len(items) > 1:
            duplicates.append({"ticket_id": ticket["ticket_id"], "source_review_ids": source_ids})
        if requires_human:
            human_decisions.append({"ticket_id": ticket["ticket_id"], "reason": ticket["title"]})

    queue = {
        "schema_version": "1.0",
        "base_commit": base_commit,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "tickets": tickets,
        "duplicates": duplicates,
        "conflicts": [],
        "human_decisions_needed": human_decisions,
    }

    (outdir / "ReviewQueue.json").write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

    if human_decisions:
        lines = ["# Human decisions needed", ""]
        for item in human_decisions:
            lines.append(f"- {item['ticket_id']}: {item['reason']}")
        (outdir / "HumanDecisionsNeeded.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        (outdir / "HumanDecisionsNeeded.md").write_text((TEMPLATES / "HumanDecisionsNeeded.md.template").read_text(encoding="utf-8"), encoding="utf-8")

    return queue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", "--target-root", dest="target", default=".", help="Target repo root")
    args = parser.parse_args()
    queue = normalize(Path(args.target))
    print(f"Wrote docs/reviews/ReviewQueue.json with {len(queue['tickets'])} tickets.")
    if queue["human_decisions_needed"]:
        print("Human decisions are required before fixing some tickets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
