#!/usr/bin/env python3
"""Validate the empty asset-provenance review intake packet."""

from __future__ import annotations

import json
from pathlib import Path

import validate_assets
import validate_generation_metadata
import verify_asset_release


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
PACKET_PATH = ROOT / "docs/evaluation/phase13.1-asset-provenance-evidence-intake-packet.json"
PACKET_FIELDS = {
  "schema_version",
  "status",
  "roadmap_item",
  "purpose",
  "source_contract",
  "inventory",
  "review_boundary",
  "intake_boundary",
  "review_contract",
  "release_boundary",
  "records",
  "decision",
  "evidence_limits",
  "test_source",
}
SOURCE_FIELDS = {
  "visual_registry",
  "audio_registry",
  "portrait_queue",
  "generation_workflow",
  "ai_boundary",
  "feedback_instrument",
  "release_manifest",
}
INVENTORY_FIELDS = {
  "visual_count",
  "audio_count",
  "portrait_preview_count",
  "visual_ids",
  "audio_ids",
  "portrait_preview_ids",
}
REVIEW_BOUNDARY_FIELDS = {
  "technical_intake_complete",
  "inventory_parity_complete",
  "human_provenance_review_complete",
  "human_identity_and_resemblance_review_complete",
  "license_and_training_data_review_complete",
  "accessibility_and_design_review_complete",
  "release_derivative_review_complete",
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
  "asset_families",
  "review_statuses",
  "gate_statuses",
  "gate_ids",
  "finding_categories",
  "forbidden_fields",
}
RELEASE_BOUNDARY_FIELDS = {
  "new_registry_entries",
  "new_release_files",
  "portrait_previews_release_eligible",
  "public_release_approval",
}
DECISION_FIELDS = {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"}
RECORD_FIELDS = {
  "asset_id",
  "asset_family",
  "review_status",
  "gate_statuses",
  "finding_categories",
}
CANONICAL_RECORD_FIELDS = [
  "asset_id",
  "asset_family",
  "review_status",
  "gate_statuses",
  "finding_categories",
]
EXPECTED_SOURCE_CONTRACT = {
  "visual_registry": "assets/registry/visual-assets.json: \"schema_version\": \"asset-registry-v1\"",
  "audio_registry": "assets/registry/audio-assets.json: \"schema_version\": \"asset-registry-v1\"",
  "portrait_queue": "assets/generation/portrait-review-queue.json: \"schema_version\": \"fictional-portrait-review-queue-v1\"",
  "generation_workflow": "assets/generation/generation-workflow.json: \"schema_version\": \"generation-workflow-v1\"",
  "ai_boundary": "docs/evaluation/phase13.1-ai-generation-metadata-boundary.json: \"schema_version\": \"phase13.1-ai-generation-metadata-boundary-v1\"",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json: \"status\": \"ready-for-authorized-human-pilot\"",
  "release_manifest": "assets/ASSET_RELEASE_MANIFEST.json: \"schema_version\": \"asset-release-manifest-v1\"",
}
EXPECTED_PURPOSE = "Provide a privacy-bounded, source-bound intake contract for authorized provenance and release review of the current asset inventory without approving or promoting any asset."
EXPECTED_EVIDENCE_LIMITS = [
  "This packet contains no human provenance findings and does not approve, register, release, or promote any asset.",
  "The current registries and generated credits are technical source evidence, not legal clearance, training-data provenance, human design review, or public-release approval.",
  "The seven portrait previews remain hash-bound, unreleased, and missing actual model/seed metadata; no plausible values may be substituted.",
  "Human review, revision decisions, license/training-data conclusions, release-derivative approval, and public release remain separate authorization gates.",
]
EXPECTED_TEST_SOURCE = "tests/test_phase13_1_asset_provenance_evidence_intake.py"
EXPECTED_ASSET_FAMILIES = ["visual-registry", "audio-registry", "portrait-preview"]
EXPECTED_REVIEW_STATUSES = ["reviewed", "skipped", "not-observed"]
EXPECTED_GATE_STATUSES = ["pass", "fail", "pending", "not-applicable"]


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


def _canonical_inventory() -> tuple[dict, dict]:
  visual = _load_json(ROOT / "assets/registry/visual-assets.json")
  audio = _load_json(ROOT / "assets/registry/audio-assets.json")
  portraits = _load_json(ROOT / "assets/generation/portrait-review-queue.json")
  visual_ids = [entry["id"] for entry in visual["entries"]]
  audio_ids = [entry["id"] for entry in audio["entries"]]
  portrait_ids = [entry["asset_id"] for entry in portraits["entries"]]
  inventory = {
    "visual_count": len(visual_ids),
    "audio_count": len(audio_ids),
    "portrait_preview_count": len(portrait_ids),
    "visual_ids": visual_ids,
    "audio_ids": audio_ids,
    "portrait_preview_ids": portrait_ids,
  }
  families = {asset_id: "visual-registry" for asset_id in visual_ids}
  families.update({asset_id: "audio-registry" for asset_id in audio_ids})
  families.update({asset_id: "portrait-preview" for asset_id in portrait_ids})
  return inventory, families


def _canonical_review_contract() -> dict:
  workflow = _load_json(ROOT / "assets/generation/generation-workflow.json")
  portraits = _load_json(ROOT / "assets/generation/portrait-review-queue.json")
  feedback = _load_json(ROOT / "docs/evaluation/phase13.2-pilot-feedback-instrument.json")
  gate_ids = [
    "provenance",
    "license",
    "accessibility",
    "technical",
    "human-review",
    "release",
    *workflow["required_human_review_fields"],
    *portraits["required_gates"],
  ]
  return {
    "record_fields": CANONICAL_RECORD_FIELDS,
    "asset_families": EXPECTED_ASSET_FAMILIES,
    "review_statuses": EXPECTED_REVIEW_STATUSES,
    "gate_statuses": EXPECTED_GATE_STATUSES,
    "gate_ids": gate_ids,
    "finding_categories": feedback["finding_categories"],
    "forbidden_fields": feedback["session_record"]["forbidden"],
  }


def _validate_source_boundaries(inventory: dict) -> None:
  portrait_set = _load_json(ROOT / "assets/generation/portrait-set.json")
  portrait_previews = _load_json(ROOT / "assets/generation/portrait-previews.json")
  generation_manifest = _load_json(ROOT / "assets/generation/generation-manifest.json")
  portrait_queue = _load_json(ROOT / "assets/generation/portrait-review-queue.json")
  generation_errors = validate_generation_metadata.validate_portrait_documents(
    portrait_set,
    portrait_previews,
    generation_manifest,
    set(inventory["visual_ids"]) | set(inventory["audio_ids"]),
    ROOT,
  )
  generation_errors.extend(
    validate_generation_metadata.validate_portrait_review_queue(
      portrait_set,
      portrait_previews,
      portrait_queue,
      set(inventory["visual_ids"]) | set(inventory["audio_ids"]),
      ROOT,
    )
  )
  if generation_errors:
    raise ValueError(f"portrait generation boundary failed: {generation_errors[0]}")
  asset_errors = validate_assets.validate(ROOT)
  if asset_errors:
    raise ValueError(f"asset registry boundary failed: {asset_errors[0]}")
  release_errors = verify_asset_release.check_manifest(ROOT)
  if release_errors:
    raise ValueError(f"release manifest boundary failed: {release_errors[0]}")


def validate_record(record: object, contract: dict, families: dict) -> None:
  _require(isinstance(record, dict), "asset provenance records must be objects")
  _require(set(record) == RECORD_FIELDS, "asset provenance record fields are not exactly bounded")
  asset_id = record["asset_id"]
  _require(asset_id in families, "asset ID is not in the canonical inventory")
  _require(record["asset_family"] == families[asset_id], "asset family does not match the inventory")
  _require(record["review_status"] in contract["review_statuses"], "review status is not allowed")

  gate_statuses = record["gate_statuses"]
  _require(isinstance(gate_statuses, dict), "gate statuses must be an object")
  _require(
    record["review_status"] != "reviewed" or bool(gate_statuses),
    "reviewed records must contain gate evidence",
  )
  _require(set(gate_statuses).issubset(contract["gate_ids"]), "gate ID is not allowed")
  for status in gate_statuses.values():
    _require(status in contract["gate_statuses"], "gate status is not allowed")

  findings = record["finding_categories"]
  _require(isinstance(findings, list), "finding categories must be a list")
  _require(all(isinstance(item, str) for item in findings), "finding categories must be strings")
  _require(len(findings) == len(set(findings)), "finding categories must be unique")
  for finding in findings:
    _require(finding in contract["finding_categories"], "finding category is not allowed")


def validate_packet(packet: object) -> None:
  _require(isinstance(packet, dict), "asset provenance packet must be an object")
  _require(set(packet) == PACKET_FIELDS, "packet fields are not exactly bounded")
  _require(packet.get("schema_version") == "phase13.1-asset-provenance-evidence-intake-v1", "unexpected packet schema")
  _require(packet.get("status") == "complete-technical-intake-pending-human-review", "packet status must remain pending")
  _require(packet.get("roadmap_item") == "Complete asset provenance review", "roadmap item drifted")
  _require(packet.get("purpose") == EXPECTED_PURPOSE, "packet purpose is not canonical")
  _require(packet.get("evidence_limits") == EXPECTED_EVIDENCE_LIMITS, "evidence limits are not canonical")
  _require(packet.get("test_source") == EXPECTED_TEST_SOURCE, "test source is not canonical")
  _source_contract_is_present(packet)

  inventory, families = _canonical_inventory()
  _require(set(packet["inventory"]) == INVENTORY_FIELDS, "inventory fields are not exactly bounded")
  _require(packet["inventory"] == inventory, "inventory does not match canonical registries")
  for field in ("visual_count", "audio_count", "portrait_preview_count"):
    _require(
      isinstance(packet["inventory"][field], int)
      and not isinstance(packet["inventory"][field], bool),
      f"inventory count must be an integer: {field}",
    )
  _validate_source_boundaries(inventory)

  review_boundary = packet["review_boundary"]
  _require(set(review_boundary) == REVIEW_BOUNDARY_FIELDS, "review boundary fields are not exactly bounded")
  for field in ("technical_intake_complete", "inventory_parity_complete"):
    _require(review_boundary[field] is True, f"technical boundary must be complete: {field}")
  for field in REVIEW_BOUNDARY_FIELDS - {"technical_intake_complete", "inventory_parity_complete"}:
    _require(review_boundary[field] is False, f"human/release boundary must remain open: {field}")

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
  _require(intake_boundary["decision_status"] == "pending-human-review", "decision must remain pending")
  _require(intake_boundary["go_no_go"] is None, "go/no-go must remain unset")

  contract = packet["review_contract"]
  _require(set(contract) == REVIEW_CONTRACT_FIELDS, "review contract fields are not exactly bounded")
  canonical_contract = _canonical_review_contract()
  for field, expected in canonical_contract.items():
    _require(contract[field] == expected, f"review contract is not source-bound: {field}")
  _require(set(contract["record_fields"]) == RECORD_FIELDS, "record field contract drifted")

  release = packet["release_boundary"]
  _require(set(release) == RELEASE_BOUNDARY_FIELDS, "release boundary fields are not exactly bounded")
  for field in ("new_registry_entries", "new_release_files"):
    _require(
      isinstance(release[field], int)
      and not isinstance(release[field], bool)
      and release[field] == 0,
      f"release counter must remain integer zero: {field}",
    )
  _require(release["portrait_previews_release_eligible"] is False, "portrait promotion is not allowed")
  _require(release["public_release_approval"] is False, "public release must remain pending")

  records = packet["records"]
  _require(isinstance(records, list), "records must be a list")
  _require(len(records) == intake_boundary["record_count"], "record count does not match records")
  for record in records:
    validate_record(record, contract, families)

  decision = packet["decision"]
  _require(set(decision) == DECISION_FIELDS, "decision fields are not exactly bounded")
  _require(decision["status"] == "pending-human-review", "decision status must remain pending")
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
