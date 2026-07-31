#!/usr/bin/env python3
"""Validate the empty revision-decision evidence-intake packet."""

from __future__ import annotations

import json
from pathlib import Path

import validate_asset_provenance_evidence_intake
import validate_debrief_visual_evidence_intake
import validate_pilot_evidence_intake

ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
PACKET_PATH = ROOT / "docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json"
PACKET_FIELDS = {
  "schema_version",
  "status",
  "roadmap_item",
  "purpose",
  "source_contract",
  "input_sources",
  "target_catalog",
  "decision_boundary",
  "intake_boundary",
  "decision_contract",
  "records",
  "decision",
  "evidence_limits",
  "test_source",
}
SOURCE_FIELDS = {
  "revision_log",
  "evaluation_protocol",
  "feedback_instrument",
  "pilot_evidence_intake",
  "debrief_visual_evidence_intake",
  "asset_provenance_evidence_intake",
}
INPUT_FIELDS = {"id", "status"}
TARGET_FIELDS = {"pilot-task_ids", "debrief-case_ids", "asset_ids"}
BOUNDARY_FIELDS = {
  "technical_intake_complete",
  "source_parity_complete",
  "human_findings_present",
  "revision_decisions_present",
  "revision_implementation_present",
  "campaign_expansion_approval",
  "public_release_approval",
}
INTAKE_FIELDS = {
  "record_count",
  "human_findings_collected",
  "raw_notes_collected",
  "raw_media_collected",
  "private_game_state_collected",
  "browser_location_collected",
  "decision_status",
  "go_no_go",
}
CONTRACT_FIELDS = {
  "record_fields",
  "evidence_sources",
  "target_families",
  "decision_statuses",
  "finding_categories",
  "revision_dispositions",
  "priorities",
  "action_codes",
  "rationale_codes",
  "forbidden_fields",
}
DECISION_FIELDS = {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"}
RECORD_FIELDS = {
  "decision_id",
  "evidence_source",
  "target_id",
  "target_family",
  "decision_status",
  "finding_categories",
  "revision_disposition",
  "priority",
  "action_codes",
  "rationale_codes",
}
CANONICAL_RECORD_FIELDS = [
  "decision_id",
  "evidence_source",
  "target_id",
  "target_family",
  "decision_status",
  "finding_categories",
  "revision_disposition",
  "priority",
  "action_codes",
  "rationale_codes",
]
EXPECTED_SOURCE_CONTRACT = {
  "revision_log": "docs/evaluation/phase10.2-revision-log.md: Status: prepared; no participant findings have been collected or entered.",
  "evaluation_protocol": "docs/evaluation/phase10.2-evaluation-protocol.json: \"status\": \"ready-for-human-evaluation\"",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"status\": \"ready-for-authorized-human-pilot\"",
  "pilot_evidence_intake": "docs/evaluation/phase13.2-pilot-evidence-intake-packet.json: \"schema_version\": \"phase13.2-pilot-evidence-intake-v1\"",
  "debrief_visual_evidence_intake": "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json: \"schema_version\": \"phase13.2-debrief-visual-evidence-intake-v1\"",
  "asset_provenance_evidence_intake": "docs/evaluation/phase13.1-asset-provenance-evidence-intake-packet.json: \"schema_version\": \"phase13.1-asset-provenance-evidence-intake-v1\"",
}
EXPECTED_INPUT_SOURCES = [
  {"id": "pilot-evidence", "status": "empty-pending-human-evidence"},
  {"id": "debrief-visual-evidence", "status": "empty-pending-human-review"},
  {"id": "asset-provenance", "status": "empty-pending-human-review"},
]
EXPECTED_PURPOSE = "Provide a privacy-bounded, source-bound intake contract for authorized revision triage without recording human findings, revision decisions, or campaign-expansion approval in this preparation packet."
EXPECTED_EVIDENCE_LIMITS = [
  "This packet contains no human findings or revision decisions and does not approve a revision, campaign expansion, asset, or public release.",
  "The source packets and revision log remain empty preparation artifacts; automated parity and vocabulary checks are not human evaluation evidence.",
  "Decision records may use only bounded source IDs, target IDs, categories, dispositions, priorities, action codes, and rationale codes; free text, identity, private state, browser/session locations, and raw media are prohibited.",
  "Human evaluation, revision decisions, implementation verification, expansion approval, legal/provenance clearance, and public-release approval remain separate authorization gates.",
]
EXPECTED_TEST_SOURCE = "tests/test_phase13_2_revision_decision_evidence_intake.py"
EXPECTED_TARGET_FAMILIES = ["pilot-task", "debrief-case", "asset"]
EXPECTED_DECISION_STATUSES = ["proposed", "recorded"]
EXPECTED_DISPOSITIONS = ["revise", "retain", "defer", "reject"]
EXPECTED_PRIORITIES = ["critical", "high", "normal", "low"]
EXPECTED_ACTION_CODES = [
  "no-change",
  "copy",
  "layout",
  "accessibility",
  "audio",
  "visual",
  "asset",
  "provenance",
  "release",
  "scope",
  "additional-evidence",
]
EXPECTED_RATIONALE_CODES = [
  "evidence-confirmed",
  "insufficient-evidence",
  "privacy-boundary",
  "provenance-boundary",
  "accessibility-equivalent",
  "technical-defect",
  "scope-control",
  "release-safety",
]
EXPECTED_REVISION_LOG = """# Phase 10.2 evaluation revision log

Status: prepared; no participant findings have been collected or entered.

Use one row per anonymized finding after an authorized session. Do not add
names, contact details, health information, private game state, or identifying
recordings.

| Finding ID | Participant group | Task ID | Category (`defect` / `preference` / `scope-expansion`) | Observation | Evidence reference | Proposed revision | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | No findings recorded. | — | — | — | pending human evaluation |

## Decision record

- Go/no-go: pending human evidence.
- Authorized reviewer: —
- Decision date: —
- Rationale: —

Automated checks and this empty template do not establish participant
comprehension, accessibility quality, audio usefulness, educational benefit,
legal clearance, or policy validity.
"""
def _require(condition: bool, message: str) -> None:
  if not condition:
    raise ValueError(message)


def _load_json(path: Path) -> dict:
  value = json.loads(path.read_text(encoding="utf-8"))
  _require(isinstance(value, dict), f"canonical source is not an object: {path}")
  return value


def _source_contract_is_present(packet: dict) -> None:
  _require(packet["source_contract"] == EXPECTED_SOURCE_CONTRACT, "source contract is not canonical")
  for name, source in EXPECTED_SOURCE_CONTRACT.items():
    source_path, marker = source.split(": ", 1)
    path = (ROOT / source_path).resolve()
    _require(path == ROOT_RESOLVED / source_path, f"source path escaped repository root: {name}")
    _require(path.is_file(), f"source contract path is missing: {source_path}")
    _require(marker in path.read_text(encoding="utf-8"), f"source marker is missing: {name}")


def _require_empty_source(name: str, source: dict, status: str, decision_status: str) -> None:
  _require(source["status"] == status, f"{name} source status is not pending")
  _require(source.get("records") == [], f"{name} source must remain empty")
  _require(source.get("decision", {}).get("status") == decision_status, f"{name} decision must remain pending")


def _validate_revision_log_text(text: str) -> None:
  _require(text == EXPECTED_REVISION_LOG, "revision log empty boundary is not canonical")


def _validate_revision_log() -> None:
  path = ROOT / "docs/evaluation/phase10.2-revision-log.md"
  _require(path.is_file(), "revision log is missing")
  _validate_revision_log_text(path.read_text(encoding="utf-8"))


def _validate_source_packet(name: str, validator, source: dict) -> None:
  try:
    validator.validate_packet(source)
  except (KeyError, TypeError, ValueError) as error:
    raise ValueError(f"{name} source validation failed: {error}") from error


def _canonical_sources() -> tuple[dict, dict, dict]:
  feedback = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-feedback-instrument.json")
  pilot = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-evidence-intake-packet.json")
  debrief = _load_json(ROOT / "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json")
  asset = _load_json(ROOT / "docs/evaluation/phase13.1-asset-provenance-evidence-intake-packet.json")
  _validate_revision_log()
  _validate_source_packet("pilot-evidence", validate_pilot_evidence_intake, pilot)
  _validate_source_packet("debrief-visual-evidence", validate_debrief_visual_evidence_intake, debrief)
  _validate_source_packet("asset-provenance", validate_asset_provenance_evidence_intake, asset)
  _require_empty_source("pilot-evidence", pilot, "complete-technical-intake-pending-human-evidence", "pending-human-evidence")
  _require_empty_source("debrief-visual-evidence", debrief, "complete-technical-intake-pending-human-review", "pending-authorized-human-review")
  _require_empty_source("asset-provenance", asset, "complete-technical-intake-pending-human-review", "pending-human-review")
  pilot_ids = [task["id"] for task in feedback["tasks"]]
  debrief_ids = debrief["review_contract"]["case_ids"]
  debrief_review = _load_json(ROOT / "docs/evaluation/phase13.2-debrief-visual-review-packet.json")
  _require(debrief_ids == [case["id"] for case in debrief_review["cases"]], "debrief target IDs are not source-bound")
  _require(pilot["allowed_record_contract"]["task_ids"] == pilot_ids, "pilot task IDs are not source-bound")
  asset_ids = [
    *asset["inventory"]["visual_ids"],
    *asset["inventory"]["audio_ids"],
    *asset["inventory"]["portrait_preview_ids"],
  ]
  target_catalog = {
    "pilot-task_ids": pilot_ids,
    "debrief-case_ids": debrief_ids,
    "asset_ids": asset_ids,
  }
  target_families = {
    **{target_id: ("pilot-evidence", "pilot-task") for target_id in pilot_ids},
    **{target_id: ("debrief-visual-evidence", "debrief-case") for target_id in debrief_ids},
    **{target_id: ("asset-provenance", "asset") for target_id in asset_ids},
  }
  contract = {
    "record_fields": CANONICAL_RECORD_FIELDS,
    "evidence_sources": [source["id"] for source in EXPECTED_INPUT_SOURCES],
    "target_families": EXPECTED_TARGET_FAMILIES,
    "decision_statuses": EXPECTED_DECISION_STATUSES,
    "finding_categories": feedback["finding_categories"],
    "revision_dispositions": EXPECTED_DISPOSITIONS,
    "priorities": EXPECTED_PRIORITIES,
    "action_codes": EXPECTED_ACTION_CODES,
    "rationale_codes": EXPECTED_RATIONALE_CODES,
    "forbidden_fields": feedback["session_record"]["forbidden"],
  }
  return target_catalog, target_families, contract


def validate_record(record: object, contract: dict, target_families: dict) -> None:
  _require(isinstance(record, dict), "revision decision records must be objects")
  _require(set(record) == RECORD_FIELDS, "revision decision record fields are not exactly bounded")
  decision_id = record["decision_id"]
  _require(isinstance(decision_id, str), "decision ID must be a string")
  target_id = record["target_id"]
  _require(target_id in target_families, "target ID is not in the canonical catalog")
  expected_source, expected_family = target_families[target_id]
  _require(record["evidence_source"] == expected_source, "evidence source does not match target")
  _require(record["target_family"] == expected_family, "target family does not match target")
  _require(
    decision_id == f"revision-{expected_source}-{target_id}",
    "decision ID must be derived from the canonical source and target",
  )
  _require(record["decision_status"] in contract["decision_statuses"], "decision status is not allowed")
  _require(record["revision_disposition"] in contract["revision_dispositions"], "revision disposition is not allowed")
  _require(record["priority"] in contract["priorities"], "priority is not allowed")
  for field, allowed in (
    ("finding_categories", contract["finding_categories"]),
    ("action_codes", contract["action_codes"]),
    ("rationale_codes", contract["rationale_codes"]),
  ):
    values = record[field]
    _require(isinstance(values, list) and values, f"{field} must be a non-empty list")
    _require(all(isinstance(value, str) for value in values), f"{field} must contain only strings")
    _require(len(values) == len(set(values)), f"{field} must contain unique values")
    _require(set(values).issubset(allowed), f"{field} contains an unknown value")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "revision decision packet must be an object")
  _require(set(packet) == PACKET_FIELDS, "packet fields are not exactly bounded")
  _require(packet["schema_version"] == "phase13.2-revision-decision-evidence-intake-v1", "unexpected packet schema")
  _require(packet["status"] == "complete-technical-intake-pending-human-evidence", "packet status must remain pending")
  _require(packet["roadmap_item"] == "Record revision decisions", "roadmap item drifted")
  _require(packet["purpose"] == EXPECTED_PURPOSE, "packet purpose is not canonical")
  _require(packet["evidence_limits"] == EXPECTED_EVIDENCE_LIMITS, "evidence limits are not canonical")
  _require(packet["test_source"] == EXPECTED_TEST_SOURCE, "test source is not canonical")
  _source_contract_is_present(packet)

  _require(packet["input_sources"] == EXPECTED_INPUT_SOURCES, "input source boundary is not canonical")
  for source in packet["input_sources"]:
    _require(set(source) == INPUT_FIELDS, "input source fields are not exactly bounded")

  target_catalog, target_families, canonical_contract = _canonical_sources()
  _require(set(packet["target_catalog"]) == TARGET_FIELDS, "target catalog fields are not exactly bounded")
  _require(packet["target_catalog"] == target_catalog, "target catalog is not source-bound")

  boundary = packet["decision_boundary"]
  _require(set(boundary) == BOUNDARY_FIELDS, "decision boundary fields are not exactly bounded")
  _require(boundary["technical_intake_complete"] is True, "technical intake must be complete")
  _require(boundary["source_parity_complete"] is True, "source parity must be complete")
  for field in BOUNDARY_FIELDS - {"technical_intake_complete", "source_parity_complete"}:
    _require(boundary[field] is False, f"human or release boundary must remain open: {field}")

  intake = packet["intake_boundary"]
  _require(set(intake) == INTAKE_FIELDS, "intake boundary fields are not exactly bounded")
  _require(isinstance(intake["record_count"], int) and not isinstance(intake["record_count"], bool) and intake["record_count"] == 0, "preparation packet must contain integer zero records")
  for field in (
    "human_findings_collected",
    "raw_notes_collected",
    "raw_media_collected",
    "private_game_state_collected",
    "browser_location_collected",
  ):
    _require(intake[field] is False, f"intake boundary must keep {field} false")
  _require(intake["decision_status"] == "pending-human-evidence", "decision must remain pending")
  _require(intake["go_no_go"] is None, "go/no-go must remain unset")

  contract = packet["decision_contract"]
  _require(set(contract) == CONTRACT_FIELDS, "decision contract fields are not exactly bounded")
  for field, expected in canonical_contract.items():
    _require(contract[field] == expected, f"decision contract is not source-bound: {field}")

  records = packet["records"]
  _require(isinstance(records, list) and records == [], "preparation packet must contain no revision records")
  _require(len(records) == intake["record_count"], "record count does not match records")
  for record in records:
    validate_record(record, contract, target_families)

  decision = packet["decision"]
  _require(set(decision) == DECISION_FIELDS, "decision fields are not exactly bounded")
  _require(decision["status"] == "pending-human-evidence", "decision status must remain pending")
  for field in ("go_no_go", "authorized_reviewer", "recorded_at", "rationale"):
    _require(decision[field] is None, f"decision field must remain unset: {field}")


def main() -> int:
  try:
    packet = _load_json(PACKET_PATH)
    validate_packet(packet)
  except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
    print(json.dumps({"status": "fail", "errors": [str(error)]}, indent=2, sort_keys=True))
    return 1
  print(json.dumps({"status": "pass", "records": len(packet["records"])}, indent=2, sort_keys=True))
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
