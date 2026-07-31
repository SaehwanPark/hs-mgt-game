#!/usr/bin/env python3
"""Validate the empty educational-usability evidence-intake packet."""

from __future__ import annotations

import json
from pathlib import Path

import validate_debrief_visual_evidence_intake
import validate_pilot_evidence_intake
import validate_revision_decision_evidence_intake


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
PACKET_PATH = ROOT / "docs/evaluation/phase13.2-educational-usability-evidence-intake-packet.json"
PACKET_FIELDS = {
  "schema_version",
  "status",
  "roadmap_item",
  "purpose",
  "review_questions",
  "source_contract",
  "review_boundary",
  "intake_boundary",
  "review_contract",
  "records",
  "decision",
  "evidence_limits",
  "test_source",
}
SOURCE_FIELDS = {
  "evaluation_protocol",
  "first_session_review_packet",
  "competitive_campaign_review_packet",
  "feedback_instrument",
  "pilot_preparation",
  "pilot_evidence_intake",
  "debrief_visual_evidence_intake",
  "revision_decision_evidence_intake",
}
REVIEW_BOUNDARY_FIELDS = {
  "technical_intake_complete",
  "source_parity_complete",
  "human_results_present",
  "educational_usability_review_complete",
  "classroom_review_complete",
  "accessibility_review_complete",
  "audio_listening_review_complete",
  "revision_decisions_present",
  "expansion_approval",
  "public_release_approval",
}
INTAKE_BOUNDARY_FIELDS = {
  "record_count",
  "reviewer_identity_collected",
  "raw_notes_collected",
  "raw_media_collected",
  "raw_transcripts_collected",
  "browser_location_collected",
  "private_game_state_collected",
  "decision_status",
  "go_no_go",
}
REVIEW_CONTRACT_FIELDS = {
  "record_fields",
  "task_ids",
  "reviewer_categories",
  "review_statuses",
  "rating_dimensions",
  "rating_values",
  "accommodation_categories",
  "finding_categories",
  "forbidden_fields",
}
DECISION_FIELDS = {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"}
RECORD_FIELDS = {
  "review_id",
  "task_id",
  "reviewer_category",
  "review_status",
  "ratings",
  "accommodations",
  "finding_categories",
}
CANONICAL_RECORD_FIELDS = [
  "review_id",
  "task_id",
  "reviewer_category",
  "review_status",
  "ratings",
  "accommodations",
  "finding_categories",
]
EXPECTED_SOURCE_CONTRACT = {
  "evaluation_protocol": "docs/evaluation/phase10.2-evaluation-protocol.json: \"status\": \"ready-for-human-evaluation\"",
  "first_session_review_packet": "docs/evaluation/phase13.1-first-session-review-packet.json: \"educational_usability_review_complete\": false",
  "competitive_campaign_review_packet": "docs/evaluation/phase13.1-competitive-campaign-review-packet.json: \"educational_and_classroom_review_complete\": false",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"status\": \"ready-for-authorized-human-pilot\"",
  "pilot_preparation": "docs/evaluation/phase13.2-pilot-preparation-boundary.json: \"feedback\": \"Tasks, rating dimensions, response states, finding categories, and pending decision fields are structured in a checked-in instrument.\"",
  "pilot_evidence_intake": "docs/evaluation/phase13.2-pilot-evidence-intake-packet.json: \"schema_version\": \"phase13.2-pilot-evidence-intake-v1\"",
  "debrief_visual_evidence_intake": "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json: \"schema_version\": \"phase13.2-debrief-visual-evidence-intake-v1\"",
  "revision_decision_evidence_intake": "docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json: \"schema_version\": \"phase13.2-revision-decision-evidence-intake-v1\"",
}
EXPECTED_PURPOSE = "Provide a privacy-bounded, source-bound intake contract for authorized educational and classroom usability review without recording human findings in this preparation packet."
EXPECTED_EVIDENCE_LIMITS = [
  "This packet contains no human findings and does not perform or represent educational, classroom, accessibility, or audio-listening review.",
  "The bounded record vocabulary does not establish comprehension, learning, classroom effectiveness, universal accessibility, audio usefulness, legal/provenance clearance, or policy validity.",
  "Technical source parity and an empty intake are preparation evidence only; they do not substitute for authorized participant review or a decision.",
  "Human review, revision decisions, expansion approval, legal/provenance clearance, and public-release approval remain separate authorization gates.",
]
EXPECTED_TEST_SOURCE = "tests/test_phase13_2_educational_usability_evidence_intake.py"
EXPECTED_FIRST_SESSION_REVIEW_BOUNDARY = {
  "technical_packet_complete": True,
  "participant_results_present": False,
  "structured_first_time_user_evaluation_complete": False,
  "human_accessibility_review_complete": False,
  "educational_usability_review_complete": False,
  "competitive_campaign_human_review_complete": False,
  "expansion_approval": False,
  "public_release_approval": False,
}
EXPECTED_FIRST_SESSION_HUMAN_REVIEW = {
  "status": "pending-authorized-human-review",
  "participant_results_present": False,
  "authorized_reviewer": None,
  "recorded_at": None,
  "decision": None,
  "go_no_go": None,
}
EXPECTED_COMPETITIVE_REVIEW_BOUNDARY = {
  "technical_packet_complete": True,
  "participant_results_present": False,
  "full_campaign_human_review_complete": False,
  "human_visual_review_complete": False,
  "human_accessibility_review_complete": False,
  "educational_and_classroom_review_complete": False,
  "audio_listening_review_complete": False,
  "expansion_approval": False,
  "public_release_approval": False,
}
EXPECTED_COMPETITIVE_HUMAN_REVIEW = {
  "status": "pending-authorized-human-review",
  "participant_results_present": False,
  "authorized_reviewer": None,
  "recorded_at": None,
  "decision": None,
  "expansion_go_no_go": None,
  "public_release_approval": None,
}


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


def _validate_source_packet(name: str, validator, source: dict) -> None:
  try:
    validator.validate_packet(source)
  except (KeyError, TypeError, ValueError) as error:
    raise ValueError(f"{name} source validation failed: {error}") from error


def _require_pending_source(
  name: str,
  source: dict,
  expected_boundary: dict,
  expected_human_review: dict,
) -> None:
  _require(source["status"] == "complete-technical-packet-pending-human-review", f"{name} source status is not pending")
  _require(source.get("review_boundary") == expected_boundary, f"{name} source boundary is not canonical")
  _require(source.get("human_review_record") == expected_human_review, f"{name} human review record is not pending")


def _canonical_sources() -> tuple[list[str], list[str], dict]:
  protocol = _load_json(ROOT / "docs/evaluation/phase10.2-evaluation-protocol.json")
  first_session = _load_json(ROOT / "docs/evaluation/phase13.1-first-session-review-packet.json")
  competitive = _load_json(ROOT / "docs/evaluation/phase13.1-competitive-campaign-review-packet.json")
  feedback = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-feedback-instrument.json")
  preparation = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-preparation-boundary.json")
  pilot = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-evidence-intake-packet.json")
  debrief = _load_json(ROOT / "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json")
  revision = _load_json(ROOT / "docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json")

  _require(protocol["status"] == "ready-for-human-evaluation", "evaluation protocol is not ready")
  _require(feedback["status"] == "ready-for-authorized-human-pilot", "feedback instrument is not ready")
  _require(preparation["status"] == "complete-preparation-only", "pilot preparation is not preparation-only")
  _validate_source_packet("pilot-evidence", validate_pilot_evidence_intake, pilot)
  _validate_source_packet("debrief-visual-evidence", validate_debrief_visual_evidence_intake, debrief)
  _validate_source_packet("revision-decision-evidence", validate_revision_decision_evidence_intake, revision)
  _require(pilot["records"] == [], "pilot evidence source must remain empty")
  _require(debrief["records"] == [], "debrief evidence source must remain empty")
  _require(revision["records"] == [], "revision evidence source must remain empty")
  _require(pilot["decision"]["status"] == "pending-human-evidence", "pilot decision must remain pending")
  _require(debrief["decision"]["status"] == "pending-authorized-human-review", "debrief decision must remain pending")
  _require(revision["decision"]["status"] == "pending-human-evidence", "revision decision must remain pending")
  _require_pending_source(
    "first-session",
    first_session,
    EXPECTED_FIRST_SESSION_REVIEW_BOUNDARY,
    EXPECTED_FIRST_SESSION_HUMAN_REVIEW,
  )
  _require_pending_source(
    "competitive-campaign",
    competitive,
    EXPECTED_COMPETITIVE_REVIEW_BOUNDARY,
    EXPECTED_COMPETITIVE_HUMAN_REVIEW,
  )

  task_ids = [task["id"] for task in protocol["tasks"]]
  _require(all(isinstance(task_id, str) for task_id in task_ids), "protocol task IDs must be strings")
  review_questions = [
    *first_session["review_questions"],
    *competitive["review_questions"],
    *debrief["review_questions"],
  ]
  review_statuses = debrief["review_contract"]["review_statuses"]
  _require(review_statuses == ["reviewed", "skipped", "not-observed"], "review statuses drifted")
  contract = {
    "record_fields": CANONICAL_RECORD_FIELDS,
    "task_ids": task_ids,
    "reviewer_categories": protocol["participant_groups"],
    "review_statuses": review_statuses,
    "rating_dimensions": protocol["rating_dimensions"],
    "rating_values": [1, 2, 3, 4, 5, "not-observed"],
    "accommodation_categories": pilot["allowed_record_contract"]["accommodation_categories"],
    "finding_categories": feedback["finding_categories"],
    "forbidden_fields": feedback["session_record"]["forbidden"],
  }
  return task_ids, review_questions, contract


def validate_record(record: object, contract: dict) -> None:
  _require(isinstance(record, dict), "educational review records must be objects")
  _require(set(record) == RECORD_FIELDS, "educational review record fields are not exactly bounded")
  task_id = record["task_id"]
  reviewer_category = record["reviewer_category"]
  _require(task_id in contract["task_ids"], "task ID is not allowed")
  _require(reviewer_category in contract["reviewer_categories"], "reviewer category is not allowed")
  _require(
    record["review_id"] == f"educational-{task_id}-{reviewer_category}",
    "review ID must be the deterministic task/category identifier",
  )
  _require(record["review_status"] in contract["review_statuses"], "review status is not allowed")

  ratings = record["ratings"]
  _require(isinstance(ratings, dict), "ratings must be an object")
  _require(set(ratings).issubset(contract["rating_dimensions"]), "rating dimension is not allowed")
  for value in ratings.values():
    if value == "not-observed":
      continue
    _require(
      isinstance(value, int) and not isinstance(value, bool) and value in contract["rating_values"],
      "rating value must be an integer from 1 to 5 or not-observed",
    )

  for field, allowed in (
    ("accommodations", contract["accommodation_categories"]),
    ("finding_categories", contract["finding_categories"]),
  ):
    values = record[field]
    _require(isinstance(values, list), f"{field} must be a list")
    _require(all(isinstance(item, str) for item in values), f"{field} must contain strings")
    _require(len(values) == len(set(values)), f"{field} must be unique")
    _require(all(item in allowed for item in values), f"{field} contains an unsupported value")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "educational usability intake packet must be an object")
  _require(set(packet) == PACKET_FIELDS, "packet fields are not exactly bounded")
  _require(packet.get("schema_version") == "phase13.2-educational-usability-evidence-intake-v1", "unexpected packet schema")
  _require(packet.get("status") == "complete-technical-intake-pending-human-review", "packet status must remain pending")
  _require(packet.get("roadmap_item") == "Educational usability reviewed", "roadmap item drifted")
  _require(packet.get("purpose") == EXPECTED_PURPOSE, "packet purpose is not canonical")
  _require(packet.get("evidence_limits") == EXPECTED_EVIDENCE_LIMITS, "evidence limits are not canonical")
  _require(packet.get("test_source") == EXPECTED_TEST_SOURCE, "test source is not canonical")

  _source_contract_is_present(packet)
  task_ids, review_questions, canonical = _canonical_sources()
  _require(packet["review_questions"] == review_questions, "review questions are not source-bound")

  review_boundary = packet["review_boundary"]
  _require(set(review_boundary) == REVIEW_BOUNDARY_FIELDS, "review boundary fields are not exactly bounded")
  _require(review_boundary["technical_intake_complete"] is True, "technical intake must be complete")
  _require(review_boundary["source_parity_complete"] is True, "source parity must be complete")
  for field in REVIEW_BOUNDARY_FIELDS - {"technical_intake_complete", "source_parity_complete"}:
    _require(review_boundary[field] is False, f"review boundary must remain open: {field}")

  intake_boundary = packet["intake_boundary"]
  _require(set(intake_boundary) == INTAKE_BOUNDARY_FIELDS, "intake boundary fields are not exactly bounded")
  _require(
    isinstance(intake_boundary["record_count"], int)
    and not isinstance(intake_boundary["record_count"], bool)
    and intake_boundary["record_count"] == 0,
    "preparation packet must contain zero records",
  )
  for field in (
    "reviewer_identity_collected",
    "raw_notes_collected",
    "raw_media_collected",
    "raw_transcripts_collected",
    "browser_location_collected",
    "private_game_state_collected",
  ):
    _require(intake_boundary[field] is False, f"intake boundary must keep {field} false")
  _require(intake_boundary["decision_status"] == "pending-authorized-human-review", "decision must remain pending")
  _require(intake_boundary["go_no_go"] is None, "go/no-go must remain unset")

  contract = packet["review_contract"]
  _require(set(contract) == REVIEW_CONTRACT_FIELDS, "review contract fields are not exactly bounded")
  for field, expected in canonical.items():
    _require(contract[field] == expected, f"review contract is not source-bound: {field}")
  _require(contract["task_ids"] == task_ids, "task IDs are not source-bound")
  _require(set(contract["record_fields"]) == RECORD_FIELDS, "record field contract drifted")

  records = packet["records"]
  _require(isinstance(records, list), "records must be a list")
  _require(records == [], "preparation packet must contain no human records")
  _require(len(records) == intake_boundary["record_count"], "record count does not match records")

  decision = packet["decision"]
  _require(set(decision) == DECISION_FIELDS, "decision fields are not exactly bounded")
  _require(decision["status"] == "pending-authorized-human-review", "decision status must remain pending")
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
