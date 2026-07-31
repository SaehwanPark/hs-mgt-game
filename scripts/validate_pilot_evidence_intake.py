#!/usr/bin/env python3
"""Validate the privacy-bounded first-time-user evidence intake packet."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-pilot-evidence-intake-packet.json"
ROOT_RESOLVED = ROOT.resolve()
PACKET_FIELDS = {
  "schema_version",
  "status",
  "roadmap_item",
  "purpose",
  "source_contract",
  "intake_boundary",
  "allowed_record_contract",
  "records",
  "decision",
  "evidence_limits",
  "test_source",
}
SOURCE_FIELDS = {
  "first_session_packet",
  "feedback_instrument",
  "evaluation_protocol",
  "facilitator_guide",
  "supported_campaigns",
  "difficulties",
  "accommodations",
  "feedback_fields",
}
BOUNDARY_FIELDS = {
  "participant_results_present",
  "record_count",
  "participant_identity_collected",
  "raw_media_collected",
  "raw_transcripts_collected",
  "private_game_state_collected",
  "browser_location_collected",
  "decision_status",
  "go_no_go",
}
CONTRACT_FIELDS = {
  "record_fields",
  "participant_categories",
  "campaigns",
  "difficulties",
  "consent_fields",
  "task_ids",
  "task_responses",
  "rating_dimensions",
  "rating_values",
  "accommodation_categories",
  "finding_categories",
  "forbidden_fields",
}
DECISION_FIELDS = {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"}
RECORD_FIELDS = {
  "participant_category",
  "campaign",
  "seed",
  "difficulty",
  "consent",
  "tasks",
  "ratings",
  "accommodations",
  "finding_categories",
}
CONSENT_FIELDS = {"feedback", "screenshot", "recording"}
CANONICAL_RECORD_FIELDS = [
  "participant_category",
  "campaign",
  "seed",
  "difficulty",
  "consent",
  "tasks",
  "ratings",
  "accommodations",
  "finding_categories",
]
EXPECTED_CAMPAIGNS = [
  "competitive-regional-v1",
  "stabilization-v1",
  "regional-affiliation-v1",
]
EXPECTED_DIFFICULTIES = ["easy", "normal", "hard", "expert"]
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
  "first_session_packet": "docs/evaluation/phase13.1-first-session-review-packet.json: \"status\": \"complete-technical-packet-pending-human-review\"",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"status\": \"ready-for-authorized-human-pilot\"",
  "evaluation_protocol": "docs/evaluation/phase10.2-evaluation-protocol.json: \"status\": \"ready-for-human-evaluation\"",
  "facilitator_guide": "docs/guides/phase10.2-structured-evaluation.md: explicit consent",
  "supported_campaigns": "docs/guides/reproducible-distribution.md: The live GUI supports `competitive-regional-v1`, `stabilization-v1`, and",
  "difficulties": "src/model/campaign.rs: pub enum Difficulty",
  "accommodations": "docs/evaluation/phase13.2-pilot-preparation-boundary.json: \"accessibility\": \"Reduced motion, Large text, written equivalents, mute/reduced notifications, keyboard, skip/review, and extra-time accommodations are written.\"",
  "feedback_fields": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"forbidden\": [",
}
EXPECTED_PURPOSE = "Provide a privacy-bounded, source-bound intake contract for an authorized first-time-user pilot without recording participant results in this preparation packet."
EXPECTED_EVIDENCE_LIMITS = [
  "This packet contains no participant results and does not perform a human evaluation.",
  "The bounded record vocabulary does not establish comprehension, accessibility, educational effectiveness, audio usefulness, or classroom readiness.",
  "Consent status is metadata only; names, contact details, raw media, raw transcripts, browser URLs, session IDs, and private game state remain prohibited.",
  "Human review, revision decisions, expansion approval, legal/provenance clearance, and public-release approval remain separate authorization gates.",
]
EXPECTED_TEST_SOURCE = "tests/test_phase13_2_pilot_evidence_intake.py"


def _require(condition: bool, message: str) -> None:
  if not condition:
    raise ValueError(message)


def _load_json(path: Path) -> dict:
  value = json.loads(path.read_text(encoding="utf-8"))
  _require(isinstance(value, dict), f"canonical source is not an object: {path}")
  return value


def _split_choices(value: str) -> list[str]:
  return [choice.strip() for choice in value.split(" | ")]


def _source_contract_is_present(packet: dict) -> None:
  _require(packet["source_contract"] == EXPECTED_SOURCE_CONTRACT, "source contract is not canonical")
  for name, source in EXPECTED_SOURCE_CONTRACT.items():
    _require(": " in source, f"source contract entry is malformed: {name}")
    source_path, marker = source.split(": ", 1)
    path = (ROOT / source_path).resolve()
    _require(path == ROOT_RESOLVED / source_path, f"source path escaped repository root: {name}")
    _require(path.is_file(), f"source contract path is missing: {source_path}")
    _require(marker in path.read_text(encoding="utf-8"), f"source marker is missing: {name}")


def _canonical_record_contract() -> dict:
  feedback = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-feedback-instrument.json")
  protocol = _load_json(ROOT / "docs/evaluation/phase10.2-evaluation-protocol.json")
  task_responses = []
  for task in feedback["tasks"]:
    for response in _split_choices(task["response"]):
      if response not in task_responses:
        task_responses.append(response)
  return {
    "record_fields": CANONICAL_RECORD_FIELDS,
    "participant_categories": protocol["participant_groups"],
    "campaigns": EXPECTED_CAMPAIGNS,
    "difficulties": EXPECTED_DIFFICULTIES,
    "consent_fields": {
      field: _split_choices(feedback["consent_record"][field])
      for field in ("feedback", "screenshot", "recording")
    },
    "task_ids": [task["id"] for task in feedback["tasks"]],
    "task_responses": task_responses,
    "rating_dimensions": feedback["rating_dimensions"],
    "rating_values": [1, 2, 3, 4, 5, "not-observed"],
    "accommodation_categories": EXPECTED_ACCOMMODATIONS,
    "finding_categories": feedback["finding_categories"],
    "forbidden_fields": feedback["session_record"]["forbidden"],
  }


def validate_record(record: object, contract: dict) -> None:
  _require(isinstance(record, dict), "pilot evidence records must be objects")
  _require(set(record) == RECORD_FIELDS, "pilot evidence record fields are not exactly bounded")
  _require(record["participant_category"] in contract["participant_categories"], "participant category is not allowed")
  _require(record["campaign"] in contract["campaigns"], "campaign is not allowed")
  _require(
    isinstance(record["seed"], int) and not isinstance(record["seed"], bool) and record["seed"] >= 0,
    "seed must be a non-negative integer",
  )
  _require(record["difficulty"] in contract["difficulties"], "difficulty is not allowed")

  consent = record["consent"]
  _require(isinstance(consent, dict) and set(consent) == CONSENT_FIELDS, "consent fields are not exactly bounded")
  for field, values in contract["consent_fields"].items():
    _require(consent[field] in values, f"consent value is not allowed: {field}")

  tasks = record["tasks"]
  _require(isinstance(tasks, list), "task observations must be a list")
  task_ids = set()
  for task in tasks:
    _require(isinstance(task, dict) and set(task) == {"id", "response"}, "task observations are not exactly bounded")
    _require(isinstance(task["id"], str), "task ID must be a string")
    _require(task["id"] in contract["task_ids"], "task ID is not allowed")
    _require(task["id"] not in task_ids, "task IDs must be unique")
    _require(task["response"] in contract["task_responses"], "task response is not allowed")
    task_ids.add(task["id"])

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
  _require(isinstance(packet, dict), "pilot evidence packet must be an object")
  _require(set(packet) == PACKET_FIELDS, "packet fields are not exactly bounded")
  _require(packet.get("schema_version") == "phase13.2-pilot-evidence-intake-v1", "unexpected packet schema")
  _require(packet.get("status") == "complete-technical-intake-pending-human-evidence", "packet status must remain pending")
  _require(packet.get("roadmap_item") == "Run structured first-time-user evaluation", "roadmap item drifted")
  _require(packet.get("purpose") == EXPECTED_PURPOSE, "packet purpose is not canonical")
  _require(packet.get("evidence_limits") == EXPECTED_EVIDENCE_LIMITS, "evidence limits are not canonical")
  _require(packet.get("test_source") == EXPECTED_TEST_SOURCE, "test source is not canonical")
  _source_contract_is_present(packet)

  boundary = packet.get("intake_boundary")
  _require(isinstance(boundary, dict), "intake boundary must be an object")
  _require(set(boundary) == BOUNDARY_FIELDS, "intake boundary fields are not exactly bounded")
  for field in (
    "participant_results_present",
    "participant_identity_collected",
    "raw_media_collected",
    "raw_transcripts_collected",
    "private_game_state_collected",
    "browser_location_collected",
  ):
    _require(boundary.get(field) is False, f"intake boundary must keep {field} false")
  _require(
    isinstance(boundary.get("record_count"), int)
    and not isinstance(boundary["record_count"], bool)
    and boundary["record_count"] == 0,
    "preparation packet must contain zero records",
  )
  _require(boundary.get("decision_status") == "pending-human-evidence", "decision must remain pending")
  _require(boundary.get("go_no_go") is None, "go/no-go must remain unset")

  contract = packet.get("allowed_record_contract")
  _require(isinstance(contract, dict), "record contract must be an object")
  _require(set(contract) == CONTRACT_FIELDS, "record contract fields are not exactly bounded")
  canonical_contract = _canonical_record_contract()
  for field, expected in canonical_contract.items():
    _require(contract[field] == expected, f"record contract is not source-bound: {field}")
  _require(set(contract["record_fields"]) == RECORD_FIELDS, "record field contract drifted")

  records = packet.get("records")
  _require(isinstance(records, list), "records must be a list")
  _require(len(records) == boundary["record_count"], "record count does not match records")
  for record in records:
    validate_record(record, contract)

  decision = packet.get("decision")
  _require(isinstance(decision, dict), "decision must be an object")
  _require(set(decision) == DECISION_FIELDS, "decision fields are not exactly bounded")
  _require(decision.get("status") == "pending-human-evidence", "decision status must remain pending")
  for field in ("go_no_go", "authorized_reviewer", "recorded_at", "rationale"):
    _require(decision.get(field) is None, f"decision field must remain unset: {field}")


def main() -> int:
  try:
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    validate_packet(packet)
  except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
    print(json.dumps({"status": "fail", "errors": [str(error)]}, indent=2, sort_keys=True))
    return 1
  print(json.dumps({"status": "pass", "records": len(packet["records"])}, indent=2, sort_keys=True))
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
