#!/usr/bin/env python3
"""Validate the empty full-campaign expansion-decision intake packet."""

from __future__ import annotations

import json
from pathlib import Path

import validate_asset_provenance_evidence_intake
import validate_debrief_visual_evidence_intake
import validate_pilot_evidence_intake
import validate_revision_decision_evidence_intake


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
PACKET_PATH = ROOT / "docs/evaluation/phase13.1-expansion-decision-evidence-intake-packet.json"
PACKET_FIELDS = {
  "schema_version",
  "status",
  "roadmap_item",
  "purpose",
  "source_contract",
  "input_sources",
  "scope_catalog",
  "decision_boundary",
  "intake_boundary",
  "decision_contract",
  "records",
  "decision",
  "evidence_limits",
  "test_source",
}
SOURCE_FIELDS = {
  "competitive_review_packet",
  "first_session_review_packet",
  "pilot_evidence_intake",
  "debrief_visual_evidence_intake",
  "asset_provenance_evidence_intake",
  "revision_decision_evidence_intake",
  "campaign_coverage_ledger",
  "evaluation_protocol",
  "feedback_instrument",
}
INPUT_FIELDS = {"id", "status"}
SCOPE_FIELDS = {"campaign_ids", "gate_catalog"}
GATE_FIELDS = {"gate_id", "source_id", "technical_status", "human_status"}
BOUNDARY_FIELDS = {
  "technical_intake_complete",
  "source_parity_complete",
  "human_evidence_present",
  "expansion_decision_present",
  "campaign_expansion_approved",
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
  "gate_statuses",
  "evidence_strengths",
  "decision_outcomes",
  "blocker_codes",
  "rationale_codes",
  "forbidden_fields",
}
DECISION_FIELDS = {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"}
RECORD_FIELDS = {
  "decision_id",
  "campaign",
  "gate_id",
  "gate_status",
  "evidence_strength",
  "blocker_codes",
  "decision_outcome",
  "rationale_codes",
}
CANONICAL_RECORD_FIELDS = [
  "decision_id",
  "campaign",
  "gate_id",
  "gate_status",
  "evidence_strength",
  "blocker_codes",
  "decision_outcome",
  "rationale_codes",
]
EXPECTED_SOURCE_CONTRACT = {
  "competitive_review_packet": "docs/evaluation/phase13.1-competitive-campaign-review-packet.json: \"schema_version\": \"phase13.1-competitive-campaign-review-packet-v1\"",
  "first_session_review_packet": "docs/evaluation/phase13.1-first-session-review-packet.json: \"schema_version\": \"phase13.1-first-session-review-packet-v1\"",
  "pilot_evidence_intake": "docs/evaluation/phase13.2-pilot-evidence-intake-packet.json: \"schema_version\": \"phase13.2-pilot-evidence-intake-v1\"",
  "debrief_visual_evidence_intake": "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json: \"schema_version\": \"phase13.2-debrief-visual-evidence-intake-v1\"",
  "asset_provenance_evidence_intake": "docs/evaluation/phase13.1-asset-provenance-evidence-intake-packet.json: \"schema_version\": \"phase13.1-asset-provenance-evidence-intake-v1\"",
  "revision_decision_evidence_intake": "docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json: \"schema_version\": \"phase13.2-revision-decision-evidence-intake-v1\"",
  "campaign_coverage_ledger": "docs/evaluation/phase11.1-campaign-coverage-ledger.json: \"status\": \"bounded-technical-ledger\"",
  "evaluation_protocol": "docs/evaluation/phase10.2-evaluation-protocol.json: \"status\": \"ready-for-human-evaluation\"",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"status\": \"ready-for-authorized-human-pilot\"",
}
EXPECTED_INPUT_SOURCES = [
  {"id": "competitive-review", "status": "technical-packet-pending-human-review"},
  {"id": "first-session-review", "status": "technical-packet-pending-human-review"},
  {"id": "pilot-evidence", "status": "empty-pending-human-evidence"},
  {"id": "debrief-visual-evidence", "status": "empty-pending-human-review"},
  {"id": "asset-provenance", "status": "empty-pending-human-review"},
  {"id": "revision-decisions", "status": "empty-pending-human-evidence"},
]
EXPECTED_CAMPAIGNS = [
  "competitive-regional-v1",
  "stabilization-v1",
  "regional-affiliation-v1",
]
EXPECTED_GATE_CATALOG = [
  {"gate_id": "first-session-workflow", "source_id": "first-session-review", "technical_status": "complete", "human_status": "pending"},
  {"gate_id": "competitive-campaign-coverage", "source_id": "competitive-review", "technical_status": "complete", "human_status": "pending"},
  {"gate_id": "debrief-visuals", "source_id": "debrief-visual-evidence", "technical_status": "complete", "human_status": "pending"},
  {"gate_id": "educational-usability", "source_id": "competitive-review", "technical_status": "not-established", "human_status": "pending"},
  {"gate_id": "accessibility", "source_id": "first-session-review", "technical_status": "not-established", "human_status": "pending"},
  {"gate_id": "audio-usefulness", "source_id": "competitive-review", "technical_status": "not-established", "human_status": "pending"},
  {"gate_id": "revision-decisions", "source_id": "revision-decisions", "technical_status": "complete", "human_status": "pending"},
  {"gate_id": "asset-provenance", "source_id": "asset-provenance", "technical_status": "complete", "human_status": "pending"},
  {"gate_id": "legal-public-release", "source_id": "asset-provenance", "technical_status": "not-established", "human_status": "pending"},
]
EXPECTED_GATE_STATUSES = ["technical-ready", "human-evidence-pending", "blocked", "pass", "fail", "not-observed"]
EXPECTED_EVIDENCE_STRENGTHS = ["technical-only", "human-evidence", "mixed", "not-observed"]
EXPECTED_DECISION_OUTCOMES = ["expand", "retain-bounded", "defer", "reject"]
EXPECTED_BLOCKER_CODES = [
  "missing-human-evidence",
  "first-session-review-pending",
  "campaign-review-pending",
  "visual-review-pending",
  "accessibility-review-pending",
  "educational-review-pending",
  "audio-listening-review-pending",
  "revision-decision-pending",
  "asset-provenance-pending",
  "legal-public-release-pending",
  "technical-gap",
]
EXPECTED_RATIONALE_CODES = [
  "evidence-confirmed",
  "insufficient-evidence",
  "scope-control",
  "accessibility-risk",
  "educational-risk",
  "audio-risk",
  "provenance-risk",
  "release-safety",
  "technical-gap",
]
EXPECTED_PURPOSE = "Provide a privacy-bounded, source-bound intake contract for an authorized full-campaign expansion decision without recording a go/no-go outcome or approving public release in this preparation packet."
EXPECTED_EVIDENCE_LIMITS = [
  "This packet contains no human findings or expansion decision and does not approve, reject, or expand the campaign scope.",
  "Technical campaign continuity and preparation packets do not establish comprehension, accessibility, educational usefulness, audio usefulness, provenance/legal clearance, or public-release readiness.",
  "Decision records may use only bounded campaign, gate, status, evidence-strength, blocker, outcome, and rationale codes; free text, identity, private state, browser/session locations, and raw media are prohibited.",
  "Human evaluation, revision decisions, expansion authorization, legal/provenance review, and public-release approval remain separate authorization gates.",
]
EXPECTED_TEST_SOURCE = "tests/test_phase13_1_expansion_decision_evidence_intake.py"


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


def _validate_packet_with(name: str, validator, packet: dict) -> None:
  try:
    validator.validate_packet(packet)
  except (KeyError, TypeError, ValueError) as error:
    raise ValueError(f"{name} source validation failed: {error}") from error


def _validate_pending_human_record(name: str, record: dict, fields: set[str], null_fields: tuple[str, ...]) -> None:
  _require(set(record) == fields, f"{name} human review record fields are not exactly bounded")
  _require(record["status"] == "pending-authorized-human-review", f"{name} human review must remain pending")
  _require(record["participant_results_present"] is False, f"{name} participant results must remain absent")
  for field in null_fields:
    _require(record[field] is None, f"{name} human review field must remain unset: {field}")


def _canonical_sources() -> tuple[list[str], list[dict], dict]:
  competitive = _load_json(ROOT / "docs/evaluation/phase13.1-competitive-campaign-review-packet.json")
  first_session = _load_json(ROOT / "docs/evaluation/phase13.1-first-session-review-packet.json")
  pilot = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-evidence-intake-packet.json")
  debrief = _load_json(ROOT / "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json")
  asset = _load_json(ROOT / "docs/evaluation/phase13.1-asset-provenance-evidence-intake-packet.json")
  revision = _load_json(ROOT / "docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json")
  ledger = _load_json(ROOT / "docs/evaluation/phase11.1-campaign-coverage-ledger.json")
  protocol = _load_json(ROOT / "docs/evaluation/phase10.2-evaluation-protocol.json")
  feedback = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-feedback-instrument.json")

  _validate_packet_with("pilot-evidence", validate_pilot_evidence_intake, pilot)
  _validate_packet_with("debrief-visual-evidence", validate_debrief_visual_evidence_intake, debrief)
  _validate_packet_with("asset-provenance", validate_asset_provenance_evidence_intake, asset)
  _validate_packet_with("revision-decisions", validate_revision_decision_evidence_intake, revision)
  _require(competitive["status"] == "complete-technical-packet-pending-human-review", "competitive review packet must remain pending")
  _require(first_session["status"] == "complete-technical-packet-pending-human-review", "first-session review packet must remain pending")
  _require(ledger["status"] == "bounded-technical-ledger", "campaign coverage ledger status drifted")
  _require(ledger["campaign"] == "competitive-regional-v1", "campaign coverage ledger campaign drifted")
  _require(protocol["status"] == "ready-for-human-evaluation", "evaluation protocol must remain ready and pending")
  _require(feedback["status"] == "ready-for-authorized-human-pilot", "feedback instrument status drifted")

  competitive_boundary = competitive["review_boundary"]
  _require(competitive_boundary["technical_packet_complete"] is True, "competitive technical packet must be complete")
  for field in (
    "participant_results_present",
    "full_campaign_human_review_complete",
    "human_visual_review_complete",
    "human_accessibility_review_complete",
    "educational_and_classroom_review_complete",
    "audio_listening_review_complete",
    "expansion_approval",
    "public_release_approval",
  ):
    _require(competitive_boundary[field] is False, f"competitive boundary must remain open: {field}")
  first_boundary = first_session["review_boundary"]
  _require(first_boundary["technical_packet_complete"] is True, "first-session technical packet must be complete")
  for field in (
    "participant_results_present",
    "structured_first_time_user_evaluation_complete",
    "human_accessibility_review_complete",
    "educational_usability_review_complete",
    "competitive_campaign_human_review_complete",
    "expansion_approval",
    "public_release_approval",
  ):
    _require(first_boundary[field] is False, f"first-session boundary must remain open: {field}")
  _validate_pending_human_record(
    "competitive",
    competitive["human_review_record"],
    {"status", "participant_results_present", "authorized_reviewer", "recorded_at", "decision", "expansion_go_no_go", "public_release_approval"},
    ("authorized_reviewer", "recorded_at", "decision", "expansion_go_no_go", "public_release_approval"),
  )
  _validate_pending_human_record(
    "first-session",
    first_session["human_review_record"],
    {"status", "participant_results_present", "authorized_reviewer", "recorded_at", "decision", "go_no_go"},
    ("authorized_reviewer", "recorded_at", "decision", "go_no_go"),
  )

  campaigns = pilot["allowed_record_contract"]["campaigns"]
  _require(campaigns == EXPECTED_CAMPAIGNS, "campaign catalog is not canonical")
  contract = {
    "record_fields": CANONICAL_RECORD_FIELDS,
    "gate_statuses": EXPECTED_GATE_STATUSES,
    "evidence_strengths": EXPECTED_EVIDENCE_STRENGTHS,
    "decision_outcomes": EXPECTED_DECISION_OUTCOMES,
    "blocker_codes": EXPECTED_BLOCKER_CODES,
    "rationale_codes": EXPECTED_RATIONALE_CODES,
    "forbidden_fields": feedback["session_record"]["forbidden"],
  }
  return campaigns, EXPECTED_GATE_CATALOG, contract


def validate_record(record: object, contract: dict, campaigns: list[str], gate_ids: set[str]) -> None:
  _require(isinstance(record, dict), "expansion decision records must be objects")
  _require(set(record) == RECORD_FIELDS, "expansion decision record fields are not exactly bounded")
  campaign = record["campaign"]
  gate_id = record["gate_id"]
  _require(campaign in campaigns, "campaign is not in the canonical catalog")
  _require(gate_id in gate_ids, "gate ID is not in the canonical catalog")
  _require(record["decision_id"] == f"expansion-{campaign}-{gate_id}", "decision ID must be derived from campaign and gate")
  _require(record["gate_status"] in contract["gate_statuses"], "gate status is not allowed")
  _require(record["evidence_strength"] in contract["evidence_strengths"], "evidence strength is not allowed")
  _require(record["decision_outcome"] in contract["decision_outcomes"], "decision outcome is not allowed")
  _require(
    isinstance(record["rationale_codes"], list) and record["rationale_codes"],
    "rationale codes are required",
  )
  if record["decision_outcome"] == "expand":
    _require(
      record["gate_status"] == "pass"
      and record["evidence_strength"] in {"human-evidence", "mixed"}
      and not record["blocker_codes"],
      "expand requires a passing gate, human or mixed evidence, and no blockers",
    )
  if record["gate_status"] in {"blocked", "fail"}:
    _require(record["blocker_codes"], "blocked or failed gates require blocker codes")
  for field, allowed in (
    ("blocker_codes", contract["blocker_codes"]),
    ("rationale_codes", contract["rationale_codes"]),
  ):
    values = record[field]
    _require(isinstance(values, list), f"{field} must be a list")
    _require(all(isinstance(value, str) for value in values), f"{field} must contain only strings")
    _require(len(values) == len(set(values)), f"{field} must contain unique values")
    _require(set(values).issubset(allowed), f"{field} contains an unknown value")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "expansion decision packet must be an object")
  _require(set(packet) == PACKET_FIELDS, "packet fields are not exactly bounded")
  _require(packet["schema_version"] == "phase13.1-expansion-decision-evidence-intake-v1", "unexpected packet schema")
  _require(packet["status"] == "complete-technical-intake-pending-human-evidence", "packet status must remain pending")
  _require(packet["roadmap_item"] == "Approve or reject expansion to full campaign coverage", "roadmap item drifted")
  _require(packet["purpose"] == EXPECTED_PURPOSE, "packet purpose is not canonical")
  _require(packet["evidence_limits"] == EXPECTED_EVIDENCE_LIMITS, "evidence limits are not canonical")
  _require(packet["test_source"] == EXPECTED_TEST_SOURCE, "test source is not canonical")
  _source_contract_is_present(packet)

  _require(packet["input_sources"] == EXPECTED_INPUT_SOURCES, "input source boundary is not canonical")
  for source in packet["input_sources"]:
    _require(set(source) == INPUT_FIELDS, "input source fields are not exactly bounded")
  campaigns, gate_catalog, canonical_contract = _canonical_sources()
  scope = packet["scope_catalog"]
  _require(set(scope) == SCOPE_FIELDS, "scope catalog fields are not exactly bounded")
  _require(scope["campaign_ids"] == campaigns, "campaign catalog is not source-bound")
  _require(scope["gate_catalog"] == gate_catalog, "gate catalog is not source-bound")
  for gate in scope["gate_catalog"]:
    _require(set(gate) == GATE_FIELDS, "gate catalog fields are not exactly bounded")

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
  _require(isinstance(records, list) and records == [], "preparation packet must contain no expansion records")
  _require(len(records) == intake["record_count"], "record count does not match records")
  gate_ids = {gate["gate_id"] for gate in gate_catalog}
  for record in records:
    validate_record(record, contract, campaigns, gate_ids)

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
