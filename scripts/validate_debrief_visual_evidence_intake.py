#!/usr/bin/env python3
"""Validate the privacy-bounded terminal debrief review intake packet."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
PACKET_PATH = ROOT / "docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json"
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
  "review_packet",
  "technical_boundary",
  "feedback_instrument",
  "evaluation_protocol",
  "facilitator_guide",
  "accommodations",
}
REVIEW_BOUNDARY_FIELDS = {
  "technical_intake_complete",
  "human_review_records_present",
  "human_visual_review_complete",
  "human_accessibility_review_complete",
  "educational_and_classroom_review_complete",
  "audio_listening_review_complete",
  "public_release_approval",
}
INTAKE_BOUNDARY_FIELDS = {
  "record_count",
  "reviewer_identity_collected",
  "raw_notes_collected",
  "raw_media_collected",
  "browser_location_collected",
  "private_game_state_collected",
  "decision_status",
  "go_no_go",
}
REVIEW_CONTRACT_FIELDS = {
  "record_fields",
  "case_ids",
  "reviewer_categories",
  "review_statuses",
  "review_dimensions",
  "rating_values",
  "accommodation_categories",
  "finding_categories",
  "forbidden_fields",
}
DECISION_FIELDS = {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"}
RECORD_FIELDS = {
  "case_id",
  "reviewer_category",
  "review_status",
  "ratings",
  "accommodations",
  "finding_categories",
}
CANONICAL_RECORD_FIELDS = [
  "case_id",
  "reviewer_category",
  "review_status",
  "ratings",
  "accommodations",
  "finding_categories",
]
EXPECTED_DIMENSIONS = [
  "history-debrief-distinction",
  "consequence-sequence-reconstruction",
  "terminal-status-and-control-legibility",
  "accessibility-fallback-equivalence",
  "actor-visible-and-uncertainty-boundary",
]
DIMENSION_MARKERS = [
  "distinguish committed campaign history",
  "reconstruct the visible consequence sequence",
  "terminal status, and absence of further decision controls",
  "preserve decision-relevant meaning",
  "actor-visible observations, uncertainty, written fallbacks",
]
EXPECTED_REVIEW_STATUSES = ["reviewed", "skipped", "not-observed"]
EXPECTED_ACCOMMODATIONS = [
  "keyboard-navigation",
  "large-text",
  "reduced-motion",
  "audio-off",
  "cues-only",
  "reduced-notifications",
  "written-equivalent",
  "skip-review",
  "extra-time",
  "no-accommodation-observed",
]
EXPECTED_SOURCE_CONTRACT = {
  "review_packet": "docs/evaluation/phase13.2-debrief-visual-review-packet.json: \"status\": \"complete-technical-packet-pending-human-review\"",
  "technical_boundary": "docs/evaluation/phase13.2-debrief-visual-boundary.json: \"status\": \"complete-current-technical-debrief-visual-boundary-only\"",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"status\": \"ready-for-authorized-human-pilot\"",
  "evaluation_protocol": "docs/evaluation/phase10.2-evaluation-protocol.json: \"status\": \"ready-for-human-evaluation\"",
  "facilitator_guide": "docs/guides/phase10.2-structured-evaluation.md: explicit consent",
  "accommodations": "docs/evaluation/phase13.2-pilot-preparation-boundary.json: \"accessibility\": \"Reduced motion, Large text, written equivalents, mute/reduced notifications, keyboard, skip/review, and extra-time accommodations are written.\"",
}
EXPECTED_PURPOSE = "Provide a privacy-bounded, source-bound intake contract for authorized human review of the three terminal debrief cases without recording human findings in this preparation packet."
EXPECTED_EVIDENCE_LIMITS = [
  "This packet contains no human findings and does not perform or represent visual, accessibility, educational, classroom, or audio-listening review.",
  "The bounded record vocabulary does not establish pixel quality, comprehension, learning, classroom effectiveness, audio usefulness, legal/provenance clearance, or policy validity.",
  "Existing rasters and transcripts remain evaluation-only; this slice adds no screenshot, recording, asset, or release artifact.",
  "Human review, revision decisions, expansion approval, legal/provenance clearance, and public-release approval remain separate authorization gates.",
]
EXPECTED_TEST_SOURCE = "tests/test_phase13_2_debrief_visual_evidence_intake.py"


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
    _require(path == (ROOT_RESOLVED / source_path), f"source path escaped repository root: {name}")
    _require(path.is_file(), f"source contract path is missing: {source_path}")
    _require(marker in path.read_text(encoding="utf-8"), f"source marker is missing: {name}")


def _canonical_review_contract() -> dict:
  review_packet = _load_json(ROOT / "docs/evaluation/phase13.2-debrief-visual-review-packet.json")
  feedback = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-feedback-instrument.json")
  protocol = _load_json(ROOT / "docs/evaluation/phase10.2-evaluation-protocol.json")
  questions = review_packet["review_questions"]
  for marker in DIMENSION_MARKERS:
    _require(any(marker in question for question in questions), f"review dimension source marker is missing: {marker}")
  return {
    "record_fields": CANONICAL_RECORD_FIELDS,
    "case_ids": [case["id"] for case in review_packet["cases"]],
    "reviewer_categories": protocol["participant_groups"],
    "review_statuses": EXPECTED_REVIEW_STATUSES,
    "review_dimensions": EXPECTED_DIMENSIONS,
    "rating_values": [1, 2, 3, 4, 5, "not-observed"],
    "accommodation_categories": EXPECTED_ACCOMMODATIONS,
    "finding_categories": feedback["finding_categories"],
    "forbidden_fields": feedback["session_record"]["forbidden"],
    "review_questions": questions,
  }


def validate_record(record: object, contract: dict) -> None:
  _require(isinstance(record, dict), "debrief review records must be objects")
  _require(set(record) == RECORD_FIELDS, "debrief review record fields are not exactly bounded")
  _require(record["case_id"] in contract["case_ids"], "case ID is not allowed")
  _require(record["reviewer_category"] in contract["reviewer_categories"], "reviewer category is not allowed")
  _require(record["review_status"] in contract["review_statuses"], "review status is not allowed")

  ratings = record["ratings"]
  _require(isinstance(ratings, dict), "ratings must be an object")
  _require(set(ratings).issubset(contract["review_dimensions"]), "review dimension is not allowed")
  for value in ratings.values():
    if value == "not-observed":
      continue
    _require(
      isinstance(value, int) and not isinstance(value, bool) and value in contract["rating_values"],
      "rating value must be an integer from 1 to 5 or not-observed",
    )

  accommodations = record["accommodations"]
  _require(isinstance(accommodations, list), "accommodations must be a list")
  _require(all(isinstance(item, str) for item in accommodations), "accommodations must be strings")
  _require(len(accommodations) == len(set(accommodations)), "accommodations must be unique")
  for accommodation in accommodations:
    _require(accommodation in contract["accommodation_categories"], "accommodation is not allowed")

  findings = record["finding_categories"]
  _require(isinstance(findings, list), "finding categories must be a list")
  _require(all(isinstance(item, str) for item in findings), "finding categories must be strings")
  _require(len(findings) == len(set(findings)), "finding categories must be unique")
  for finding in findings:
    _require(finding in contract["finding_categories"], "finding category is not allowed")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "debrief intake packet must be an object")
  _require(set(packet) == PACKET_FIELDS, "packet fields are not exactly bounded")
  _require(packet.get("schema_version") == "phase13.2-debrief-visual-evidence-intake-v1", "unexpected packet schema")
  _require(packet.get("status") == "complete-technical-intake-pending-human-review", "packet status must remain pending")
  _require(packet.get("roadmap_item") == "Debrief visuals reviewed", "roadmap item drifted")
  _require(packet.get("purpose") == EXPECTED_PURPOSE, "packet purpose is not canonical")
  _require(packet.get("evidence_limits") == EXPECTED_EVIDENCE_LIMITS, "evidence limits are not canonical")
  _require(packet.get("test_source") == EXPECTED_TEST_SOURCE, "test source is not canonical")

  _source_contract_is_present(packet)
  canonical = _canonical_review_contract()
  _require(packet["review_questions"] == canonical["review_questions"], "review questions are not source-bound")

  review_boundary = packet["review_boundary"]
  _require(set(review_boundary) == REVIEW_BOUNDARY_FIELDS, "review boundary fields are not exactly bounded")
  _require(review_boundary["technical_intake_complete"] is True, "technical intake must be complete")
  for field in REVIEW_BOUNDARY_FIELDS - {"technical_intake_complete"}:
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
    "browser_location_collected",
    "private_game_state_collected",
  ):
    _require(intake_boundary[field] is False, f"intake boundary must keep {field} false")
  _require(intake_boundary["decision_status"] == "pending-authorized-human-review", "decision must remain pending")
  _require(intake_boundary["go_no_go"] is None, "go/no-go must remain unset")

  contract = packet["review_contract"]
  _require(set(contract) == REVIEW_CONTRACT_FIELDS, "review contract fields are not exactly bounded")
  for field, expected in canonical.items():
    if field != "review_questions":
      _require(contract[field] == expected, f"review contract is not source-bound: {field}")
  _require(set(contract["record_fields"]) == RECORD_FIELDS, "record field contract drifted")

  records = packet["records"]
  _require(isinstance(records, list), "records must be a list")
  _require(len(records) == intake_boundary["record_count"], "record count does not match records")
  for record in records:
    validate_record(record, contract)

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
