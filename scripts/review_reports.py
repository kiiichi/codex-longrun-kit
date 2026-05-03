"""Review report input normalization.

Reports are data. Schema errors become HITL tickets.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from runtime_layout import schema_path
except ImportError:  # pragma: no cover
    from scripts.runtime_layout import schema_path  # type: ignore


def load_report_schema() -> dict[str, Any]:
    return json.loads(schema_path("review-report.schema.json").read_text(encoding="utf-8"))


def invalid_report(path: Path, reason: str) -> dict[str, Any]:
    return {
        "reviewer_lane": "invalid-report",
        "_source_path": str(path),
        "findings": [{
            "id": f"INVALID-{path.stem}",
            "severity": "P1",
            "claim": f"Invalid review report in {path}: {reason}",
            "requires_human_decision": True,
        }],
    }


def required_fields(schema: dict[str, Any], key: str | None = None) -> list[str]:
    if key is None:
        return list(schema.get("required", []))
    items = schema.get("properties", {}).get(key, {}).get("items", {})
    return list(items.get("required", []))


def severity_values(schema: dict[str, Any]) -> set[str]:
    finding_props = (
        schema.get("properties", {})
        .get("findings", {})
        .get("items", {})
        .get("properties", {})
    )
    return set(finding_props.get("severity", {}).get("enum", []))


def validate_report(data: Any, schema: dict[str, Any]) -> list[str]:
    if not isinstance(data, dict):
        return ["report must be an object"]

    errors: list[str] = []
    for field in required_fields(schema):
        if field not in data:
            errors.append(f"missing report field {field}")

    if "reviewer_lane" in data and not isinstance(data["reviewer_lane"], str):
        errors.append("reviewer_lane must be a string")
    if "base_commit" in data and not isinstance(data["base_commit"], str):
        errors.append("base_commit must be a string")

    findings = data.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be an array")
        return errors

    required_finding = required_fields(schema, "findings")
    allowed_severities = severity_values(schema)
    list_fields = ["affected_files", "acceptance_criteria", "validation_commands"]
    for idx, finding in enumerate(findings, start=1):
        if not isinstance(finding, dict):
            errors.append(f"finding {idx} must be an object")
            continue
        for field in required_finding:
            if field not in finding:
                errors.append(f"finding {idx} missing field {field}")
        severity = finding.get("severity")
        if severity is not None and severity not in allowed_severities:
            errors.append(f"finding {idx} severity must be one of {sorted(allowed_severities)}")
        for field in list_fields:
            if field in finding and not isinstance(finding[field], list):
                errors.append(f"finding {idx} {field} must be an array")
        if "requires_human_decision" in finding and not isinstance(
            finding["requires_human_decision"], bool
        ):
            errors.append(f"finding {idx} requires_human_decision must be boolean")

    return errors


def load_report(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return invalid_report(path, f"invalid JSON: {exc}")

    errors = validate_report(data, schema)
    if errors:
        return invalid_report(path, "; ".join(errors))

    data["_source_path"] = str(path)
    return data
