import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
PACKET = ROOT / "docs" / "evaluation" / "phase13.2-revision-decision-evidence-intake-packet.json"
FEEDBACK = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"
PILOT = ROOT / "docs" / "evaluation" / "phase13.2-pilot-evidence-intake-packet.json"
DEBRIEF = ROOT / "docs" / "evaluation" / "phase13.2-debrief-visual-evidence-intake-packet.json"
ASSET = ROOT / "docs" / "evaluation" / "phase13.1-asset-provenance-evidence-intake-packet.json"


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


VALIDATOR = load_module(
  "validate_revision_decision_evidence_intake",
  "scripts/validate_revision_decision_evidence_intake.py",
)


class Phase132RevisionDecisionEvidenceIntakeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.feedback = json.loads(FEEDBACK.read_text(encoding="utf-8"))
    cls.pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    cls.debrief = json.loads(DEBRIEF.read_text(encoding="utf-8"))
    cls.asset = json.loads(ASSET.read_text(encoding="utf-8"))

  def test_empty_pending_packet_and_validator_pass(self):
    VALIDATOR.validate_packet(self.packet)
    self.assertEqual(self.packet["status"], "complete-technical-intake-pending-human-evidence")
    self.assertEqual(self.packet["records"], [])
    self.assertEqual(self.packet["intake_boundary"]["record_count"], 0)
    self.assertEqual(self.packet["decision"]["status"], "pending-human-evidence")
    self.assertIsNone(self.packet["decision"]["go_no_go"])

  def test_source_packets_and_target_catalog_are_exactly_bounded(self):
    self.assertEqual(self.pilot["records"], [])
    self.assertEqual(self.debrief["records"], [])
    self.assertEqual(self.asset["records"], [])
    self.assertEqual(
      self.packet["target_catalog"]["pilot-task_ids"],
      [task["id"] for task in self.feedback["tasks"]],
    )
    self.assertEqual(
      self.packet["target_catalog"]["debrief-case_ids"],
      self.debrief["review_contract"]["case_ids"],
    )
    asset_ids = [
      *self.asset["inventory"]["visual_ids"],
      *self.asset["inventory"]["audio_ids"],
      *self.asset["inventory"]["portrait_preview_ids"],
    ]
    self.assertEqual(self.packet["target_catalog"]["asset_ids"], asset_ids)

  def test_decision_contract_reuses_finding_and_forbidden_vocabularies(self):
    contract = self.packet["decision_contract"]
    self.assertEqual(contract["finding_categories"], self.feedback["finding_categories"])
    self.assertEqual(contract["forbidden_fields"], self.feedback["session_record"]["forbidden"])
    self.assertEqual(
      contract["record_fields"],
      [
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
      ],
    )

  def test_representative_records_are_source_and_family_bound(self):
    _, target_families, contract = VALIDATOR._canonical_sources()
    records = [
      {
        "decision_id": "revision-pilot-evidence-pilot-audio-choice",
        "evidence_source": "pilot-evidence",
        "target_id": "pilot-audio-choice",
        "target_family": "pilot-task",
        "decision_status": "proposed",
        "finding_categories": ["preference"],
        "revision_disposition": "defer",
        "priority": "normal",
        "action_codes": ["additional-evidence"],
        "rationale_codes": ["insufficient-evidence"],
      },
      {
        "decision_id": "revision-debrief-visual-evidence-competitive-terminal-debrief",
        "evidence_source": "debrief-visual-evidence",
        "target_id": "competitive-terminal-debrief",
        "target_family": "debrief-case",
        "decision_status": "recorded",
        "finding_categories": ["defect"],
        "revision_disposition": "revise",
        "priority": "high",
        "action_codes": ["layout", "accessibility"],
        "rationale_codes": ["technical-defect", "accessibility-equivalent"],
      },
      {
        "decision_id": "revision-asset-provenance-audio.runtime-music",
        "evidence_source": "asset-provenance",
        "target_id": "audio.runtime-music",
        "target_family": "asset",
        "decision_status": "proposed",
        "finding_categories": ["scope-expansion"],
        "revision_disposition": "retain",
        "priority": "low",
        "action_codes": ["no-change"],
        "rationale_codes": ["scope-control"],
      },
    ]
    for record in records:
      with self.subTest(target=record["target_id"]):
        VALIDATOR.validate_record(record, contract, target_families)

  def test_unknown_envelope_and_private_fields_are_rejected(self):
    for location, field in (
      (self.packet, "unexpected"),
      (self.packet["intake_boundary"], "raw_transcript"),
      (self.packet["decision"], "notes"),
    ):
      mutated = copy.deepcopy(self.packet)
      target = mutated
      if location is self.packet["intake_boundary"]:
        target = mutated["intake_boundary"]
      elif location is self.packet["decision"]:
        target = mutated["decision"]
      target[field] = "not-allowed"
      with self.subTest(field=field):
        with self.assertRaisesRegex(ValueError, "fields are not exactly bounded"):
          VALIDATOR.validate_packet(mutated)

  def test_packet_rejects_source_target_and_pending_decision_drift(self):
    redirected = copy.deepcopy(self.packet)
    redirected["source_contract"]["revision_log"] = "README.md: revision decision"
    with self.assertRaisesRegex(ValueError, "source contract is not canonical"):
      VALIDATOR.validate_packet(redirected)

    target_drift = copy.deepcopy(self.packet)
    target_drift["target_catalog"]["asset_ids"].append("asset.private-state")
    with self.assertRaisesRegex(ValueError, "target catalog is not source-bound"):
      VALIDATOR.validate_packet(target_drift)

    premature = copy.deepcopy(self.packet)
    premature["decision"]["status"] = "recorded"
    with self.assertRaisesRegex(ValueError, "decision status must remain pending"):
      VALIDATOR.validate_packet(premature)

  def test_packet_rejects_source_privacy_and_revision_log_boundary_drift(self):
    target = PILOT.resolve()
    original_load = VALIDATOR._load_json

    def load_with_mutation(path):
      source = original_load(path)
      if path.resolve() == target:
        source["intake_boundary"]["raw_notes_collected"] = True
        source["decision"]["go_no_go"] = "approved"
      return source

    with patch.object(VALIDATOR, "_load_json", side_effect=load_with_mutation):
      with self.assertRaisesRegex(ValueError, "pilot-evidence source validation failed"):
        VALIDATOR.validate_packet(copy.deepcopy(self.packet))

    revision_log = (ROOT / "docs/evaluation/phase10.2-revision-log.md").read_text(encoding="utf-8")
    mutated_log = revision_log + "\n| revision-alice | — | — | defect | diagnosis | — | — | — | proposed |\n"
    with self.assertRaisesRegex(ValueError, "revision log empty boundary"):
      VALIDATOR._validate_revision_log_text(mutated_log)

    mutated_free_text = revision_log + "\nReviewer note: alice-health-diagnosis\n"
    with self.assertRaisesRegex(ValueError, "revision log empty boundary"):
      VALIDATOR._validate_revision_log_text(mutated_free_text)

  def test_packet_rejects_boolean_and_float_record_counts(self):
    for value in (True, 0.0):
      mutated = copy.deepcopy(self.packet)
      mutated["intake_boundary"]["record_count"] = value
      with self.subTest(value=value):
        with self.assertRaisesRegex(ValueError, "integer zero records"):
          VALIDATOR.validate_packet(mutated)

  def test_record_rejects_free_text_unknown_values_duplicates_and_mismatch(self):
    _, target_families, contract = VALIDATOR._canonical_sources()
    record = {
      "decision_id": "revision-pilot-evidence-pilot-start-to-resolution",
      "evidence_source": "pilot-evidence",
      "target_id": "pilot-start-to-resolution",
      "target_family": "pilot-task",
      "decision_status": "proposed",
      "finding_categories": ["defect"],
      "revision_disposition": "revise",
      "priority": "normal",
      "action_codes": ["copy"],
      "rationale_codes": ["technical-defect"],
    }

    with self.assertRaisesRegex(ValueError, "record fields are not exactly bounded"):
      VALIDATOR.validate_record({**record, "rationale": "free text"}, contract, target_families)

    with self.assertRaisesRegex(ValueError, "decision ID must be derived"):
      VALIDATOR.validate_record({**record, "decision_id": "revision-alice-health-diagnosis"}, contract, target_families)

    with self.assertRaisesRegex(ValueError, "target family does not match"):
      VALIDATOR.validate_record({**record, "target_family": "asset"}, contract, target_families)

    with self.assertRaisesRegex(ValueError, "contains an unknown value"):
      VALIDATOR.validate_record({**record, "action_codes": ["unknown"]}, contract, target_families)

    with self.assertRaisesRegex(ValueError, "must contain unique values"):
      VALIDATOR.validate_record({**record, "finding_categories": ["defect", "defect"]}, contract, target_families)


if __name__ == "__main__":
  unittest.main()
