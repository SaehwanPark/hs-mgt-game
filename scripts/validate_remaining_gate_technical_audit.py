#!/usr/bin/env python3
"""Validate the source-bound audit of remaining visual/audio roadmap gates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
AUDIT_PATH = ROOT / "docs/evaluation/phase13-remaining-gate-technical-audit.json"
AUDIT_FIELDS = {
  "schema_version",
  "status",
  "package_version",
  "roadmap_item",
  "purpose",
  "roadmap_contract",
  "technical_checks",
  "gates",
  "decision_boundary",
  "evidence_limits",
  "test_source",
}
ROADMAP_CONTRACT_FIELDS = {"path", "open_item_markers"}
MARKER_FIELDS = {"id", "text"}
CHECK_FIELDS = {"id", "status", "command", "sources"}
GATE_FIELDS = {
  "id",
  "roadmap_marker_ids",
  "technical_status",
  "human_status",
  "required_authority",
  "next_action",
  "blocking_promotion",
  "sources",
}
DECISION_FIELDS = {
  "technical_implementation_gaps_remaining",
  "human_or_runtime_gates_remaining",
  "promotion_blocked",
  "status",
  "go_no_go",
  "authorized_reviewer",
  "recorded_at",
  "rationale",
}
EXPECTED_SCHEMA = "phase13-remaining-gate-technical-audit-v1"
EXPECTED_STATUS = "complete-technical-audit-pending-human-gates"
EXPECTED_PACKAGE_VERSION = "0.14.2"
EXPECTED_TEST_SOURCE = "tests/test_phase13_remaining_gate_technical_audit.py"
EXPECTED_TECHNICAL_CHECKS = {
  "current-release-coverage",
  "asset-and-attribution-boundary",
  "evaluation-and-review-intakes",
  "browser-device-boundary",
  "runtime-boundary-evidence",
  "durable-checkpoint-archive",
  "checkpoint-discovery",
  "checkpoint-reference-transfer",
  "checkpoint-artifact-download",
  "automatic-resume-policy",
  "firefox-browser-refresh-resume-smoke",
  "firefox-multi-campaign-launch-smoke",
  "firefox-competitive-full-campaign-smoke",
  "firefox-all-campaign-full-transition-smoke",
}
EXPECTED_GATES = {
  "asset-provenance-and-portrait-review",
  "audio-and-first-session-evaluation",
  "debrief-and-educational-review",
  "content-resemblance-and-clinical-review",
  "competitive-campaign-human-coverage",
  "browser-device-certification",
  "revision-decisions",
  "campaign-expansion-approval",
}
EXPECTED_ROADMAP_MARKERS = {
  "portrait-prompt-seed": "Prompt and seed recorded.",
  "portrait-crop-derivative": "Crop and release derivative completed.",
  "portrait-identity": "Identity consistency reviewed.",
  "portrait-resemblance": "Real-person resemblance reviewed.",
  "portrait-artifact": "Anatomy and artifact review completed.",
  "portrait-marks": "No protected marks present.",
  "portrait-registry": "Registry entry approved.",
  "portrait-small-size": "Small-size rendering tested.",
  "portrait-grayscale": "Grayscale rendering tested.",
  "audio-feedback": "Audio preference feedback collected.",
  "audio-ratings": "Quantitative ratings collected.",
  "audio-interviews": "Qualitative interviews completed.",
  "audio-findings": "Findings classified as defect, preference, or scope expansion.",
  "audio-go-no-go": "Go/no-go decision recorded.",
  "educational-review": "Educational usability reviewed.",
  "first-session-evaluation": "First-session workflow complete.",
  "competitive-human-coverage": "Competitive campaign coverage complete.",
  "content-institution": "No real institution accidentally represented.",
  "content-public-figure": "No public-figure resemblance remains.",
  "content-clinical": "No unsupported clinical implication introduced.",
  "ai-metadata": "AI-generation metadata complete.",
  "debrief-visuals": "Debrief visuals reviewed.",
  "asset-provenance": "Complete asset provenance review.",
  "pilot-evaluation": "Run structured first-time-user evaluation.",
  "revision-decisions": "Record revision decisions.",
  "expansion-decision": "Approve or reject expansion to full campaign coverage.",
  "browser-device-certification": "coverage, durable persistence, cross-browser/device certification, and human educational/accessibility gates remain open.",
}
NON_CHECKBOX_ROADMAP_MARKERS = {"browser-device-certification"}
ALLOWED_HUMAN_STATUSES = {
  "pending-authorized-human-review",
  "pending-authorized-human-evidence",
  "pending-runtime-certification",
}
ALLOWED_TECHNICAL_STATUSES = {
  "prepared-source-bound",
  "pass-bounded-source-qa-only",
  "partial-source-bound-technical-preparation",
}


def _require(condition: bool, message: str) -> None:
  if not condition:
    raise ValueError(message)


def _load_json(path: Path) -> dict:
  value = json.loads(path.read_text(encoding="utf-8"))
  _require(isinstance(value, dict), f"JSON object required: {path}")
  return value


def _repository_path(value: object, label: str) -> Path:
  _require(isinstance(value, str), f"{label} must be a string")
  candidate = Path(value)
  _require(not candidate.is_absolute(), f"{label} must be relative")
  resolved = (ROOT / candidate).resolve()
  try:
    resolved.relative_to(ROOT_RESOLVED)
  except ValueError as error:
    raise ValueError(f"{label} escapes repository root") from error
  return resolved


def _source_marker_is_valid(source: object) -> None:
  _require(isinstance(source, str), "source marker must be a string")
  source_path, marker = source.split(": ", 1)
  path = _repository_path(source_path, "source path")
  _require(path.is_file(), f"source path is missing: {source_path}")
  _require(marker in path.read_text(encoding="utf-8"), f"source marker is missing: {source}")


def validate_audit(audit: object) -> None:
  _require(isinstance(audit, dict), "audit must be an object")
  _require(set(audit) == AUDIT_FIELDS, "audit fields are not exactly bounded")
  _require(audit["schema_version"] == EXPECTED_SCHEMA, "audit schema drifted")
  _require(audit["status"] == EXPECTED_STATUS, "audit status must remain pending human gates")
  _require(audit["package_version"] == EXPECTED_PACKAGE_VERSION, "audit package version drifted")
  _require(audit["roadmap_item"] == "Remaining visual/audio roadmap gates", "roadmap item drifted")
  _require(isinstance(audit["purpose"], str) and audit["purpose"], "audit purpose is required")
  _require(isinstance(audit["test_source"], str), "test source must be a string")
  _require(audit["test_source"] == EXPECTED_TEST_SOURCE, "test source drifted")

  roadmap_contract = audit["roadmap_contract"]
  _require(isinstance(roadmap_contract, dict), "roadmap contract must be an object")
  _require(set(roadmap_contract) == ROADMAP_CONTRACT_FIELDS, "roadmap contract fields are not bounded")
  roadmap_path = _repository_path(roadmap_contract["path"], "roadmap path")
  _require(roadmap_path.is_file(), "roadmap source is missing")
  roadmap_text = roadmap_path.read_text(encoding="utf-8")
  markers = roadmap_contract["open_item_markers"]
  _require(isinstance(markers, list) and markers, "open roadmap markers are required")
  marker_ids = set()
  for marker in markers:
    _require(isinstance(marker, dict) and set(marker) == MARKER_FIELDS, "roadmap marker fields are not bounded")
    _require(isinstance(marker["id"], str) and marker["id"] not in marker_ids, "roadmap marker IDs must be unique")
    _require(isinstance(marker["text"], str) and marker["text"], "roadmap marker text is required")
    _require(EXPECTED_ROADMAP_MARKERS.get(marker["id"]) == marker["text"], f"roadmap marker contract drifted: {marker['id']}")
    if marker["id"] in NON_CHECKBOX_ROADMAP_MARKERS:
      normalized_roadmap = " ".join(roadmap_text.split())
      normalized_marker = " ".join(marker["text"].split())
      _require(normalized_marker in normalized_roadmap, f"roadmap marker is missing: {marker['id']}")
    else:
      checkbox_marker = f"- [ ] {marker['text']}"
      _require(
        any(line.startswith(checkbox_marker) for line in roadmap_text.splitlines()),
        f"unchecked roadmap marker is missing: {marker['id']}",
      )
    marker_ids.add(marker["id"])
  _require(
    {marker["id"]: marker["text"] for marker in markers} == EXPECTED_ROADMAP_MARKERS,
    "roadmap marker inventory drifted",
  )

  checks = audit["technical_checks"]
  _require(isinstance(checks, list), "technical checks must be a list")
  check_ids = set()
  for check in checks:
    _require(isinstance(check, dict) and set(check) == CHECK_FIELDS, "technical check fields are not bounded")
    _require(isinstance(check["id"], str) and check["id"] not in check_ids, "technical check IDs must be unique")
    _require(
      check["status"] in {"pass-source-bound-technical-preparation", "partial-source-bound-technical-preparation"},
      f"unsupported technical check status: {check['id']}",
    )
    _require(isinstance(check["command"], str) and check["command"], f"command is required: {check['id']}")
    _require(isinstance(check["sources"], list) and check["sources"], f"sources are required: {check['id']}")
    for source in check["sources"]:
      source_path = _repository_path(source, "check source")
      _require(source_path.is_file(), f"check source is missing: {source}")
    check_ids.add(check["id"])
  _require(check_ids == EXPECTED_TECHNICAL_CHECKS, "technical check inventory drifted")

  gates = audit["gates"]
  _require(isinstance(gates, list), "gates must be a list")
  gate_ids = set()
  mapped_markers = set()
  for gate in gates:
    _require(isinstance(gate, dict) and set(gate) == GATE_FIELDS, "gate fields are not bounded")
    _require(isinstance(gate["id"], str) and gate["id"] not in gate_ids, "gate IDs must be unique")
    _require(gate["technical_status"] in ALLOWED_TECHNICAL_STATUSES, f"technical status is not allowed: {gate['id']}")
    _require(gate["human_status"] in ALLOWED_HUMAN_STATUSES, f"human status is not pending: {gate['id']}")
    _require(isinstance(gate["required_authority"], str) and gate["required_authority"], f"authority is required: {gate['id']}")
    _require(isinstance(gate["next_action"], str) and gate["next_action"], f"next action is required: {gate['id']}")
    _require(gate["blocking_promotion"] is True, f"open gate must block promotion: {gate['id']}")
    marker_list = gate["roadmap_marker_ids"]
    _require(isinstance(marker_list, list) and marker_list, f"roadmap mapping is required: {gate['id']}")
    _require(all(isinstance(marker_id, str) and marker_id in marker_ids for marker_id in marker_list), f"gate marker mapping drifted: {gate['id']}")
    _require(len(marker_list) == len(set(marker_list)), f"gate markers must be unique: {gate['id']}")
    mapped_markers.update(marker_list)
    _require(isinstance(gate["sources"], list) and gate["sources"], f"gate sources are required: {gate['id']}")
    for source in gate["sources"]:
      _source_marker_is_valid(source)
    gate_ids.add(gate["id"])
  _require(gate_ids == EXPECTED_GATES, "gate inventory drifted")
  _require(mapped_markers == marker_ids, "every open roadmap marker must map to one gate")

  decision = audit["decision_boundary"]
  _require(isinstance(decision, dict) and set(decision) == DECISION_FIELDS, "decision boundary fields are not bounded")
  _require(decision["technical_implementation_gaps_remaining"] is False, "technical implementation gaps must be explicitly closed")
  _require(decision["human_or_runtime_gates_remaining"] is True, "human/runtime gates must remain open")
  _require(decision["promotion_blocked"] is True, "promotion must remain blocked")
  _require(decision["status"] == "awaiting-authorized-human-evidence-or-runtime-certification", "decision status must remain pending")
  for field in ("go_no_go", "authorized_reviewer", "recorded_at", "rationale"):
    _require(decision[field] is None, f"decision field must remain unset: {field}")

  limits = audit["evidence_limits"]
  _require(isinstance(limits, list) and all(isinstance(limit, str) and limit for limit in limits), "evidence limits are required")
  limits_text = " ".join(limits)
  for marker in ("human comprehension", "accessibility quality", "legal clearance", "public-release approval", "authorized human evidence"):
    _require(marker in limits_text, f"evidence limit is missing: {marker}")
  test_source = _repository_path(audit["test_source"], "test source")
  _require(test_source.is_file(), "audit test source is missing")


def main() -> int:
  try:
    validate_audit(_load_json(AUDIT_PATH))
  except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
    print(json.dumps({"status": "fail", "error": str(error)}))
    return 1
  print(json.dumps({"status": "pass", "schema_version": EXPECTED_SCHEMA, "gate_count": len(_load_json(AUDIT_PATH)["gates"])}))
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
