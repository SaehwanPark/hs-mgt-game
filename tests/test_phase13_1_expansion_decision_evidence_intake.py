import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
PACKET = ROOT / "docs" / "evaluation" / "phase13.1-expansion-decision-evidence-intake-packet.json"
COMPETITIVE = ROOT / "docs" / "evaluation" / "phase13.1-competitive-campaign-review-packet.json"
FIRST_SESSION = ROOT / "docs" / "evaluation" / "phase13.1-first-session-review-packet.json"
PILOT = ROOT / "docs" / "evaluation" / "phase13.2-pilot-evidence-intake-packet.json"


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


VALIDATOR = load_module(
  "validate_expansion_decision_evidence_intake",
  "scripts/validate_expansion_decision_evidence_intake.py",
)


class Phase131ExpansionDecisionEvidenceIntakeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.competitive = json.loads(COMPETITIVE.read_text(encoding="utf-8"))
    cls.pilot = json.loads(PILOT.read_text(encoding="utf-8"))

  def test_empty_pending_packet_and_validator_pass(self):
    VALIDATOR.validate_packet(self.packet)
    self.assertEqual(self.packet["status"], "complete-technical-intake-pending-human-evidence")
    self.assertEqual(self.packet["records"], [])
    self.assertEqual(self.packet["intake_boundary"]["record_count"], 0)
    self.assertFalse(self.packet["decision_boundary"]["campaign_expansion_approved"])
    self.assertEqual(self.packet["decision"]["status"], "pending-human-evidence")
    self.assertIsNone(self.packet["decision"]["go_no_go"])

  def test_campaign_and_gate_catalogs_are_source_bound(self):
    self.assertEqual(
      self.packet["scope_catalog"]["campaign_ids"],
      self.pilot["allowed_record_contract"]["campaigns"],
    )
    gate_ids = {gate["gate_id"] for gate in self.packet["scope_catalog"]["gate_catalog"]}
    self.assertEqual(
      gate_ids,
      {
        "first-session-workflow",
        "competitive-campaign-coverage",
        "debrief-visuals",
        "educational-usability",
        "accessibility",
        "audio-usefulness",
        "revision-decisions",
        "asset-provenance",
        "legal-public-release",
      },
    )
    self.assertFalse(self.competitive["review_boundary"]["expansion_approval"])
    self.assertIsNone(self.competitive["human_review_record"]["expansion_go_no_go"])

  def test_decision_contract_preserves_bounded_values_and_privacy(self):
    contract = self.packet["decision_contract"]
    self.assertEqual(
      contract["record_fields"],
      [
        "decision_id",
        "campaign",
        "gate_id",
        "gate_status",
        "evidence_strength",
        "blocker_codes",
        "decision_outcome",
        "rationale_codes",
      ],
    )
    self.assertEqual(contract["forbidden_fields"], self.pilot["allowed_record_contract"]["forbidden_fields"])
    self.assertIn("expand", contract["decision_outcomes"])
    self.assertIn("retain-bounded", contract["decision_outcomes"])

  def test_representative_records_are_source_and_gate_bound(self):
    campaigns, gates, contract = VALIDATOR._canonical_sources()
    gate_ids = {gate["gate_id"] for gate in gates}
    records = [
      {
        "decision_id": "expansion-competitive-regional-v1-first-session-workflow",
        "campaign": "competitive-regional-v1",
        "gate_id": "first-session-workflow",
        "gate_status": "human-evidence-pending",
        "evidence_strength": "technical-only",
        "blocker_codes": ["first-session-review-pending"],
        "decision_outcome": "defer",
        "rationale_codes": ["insufficient-evidence"],
      },
      {
        "decision_id": "expansion-stabilization-v1-debrief-visuals",
        "campaign": "stabilization-v1",
        "gate_id": "debrief-visuals",
        "gate_status": "blocked",
        "evidence_strength": "not-observed",
        "blocker_codes": ["visual-review-pending", "accessibility-review-pending"],
        "decision_outcome": "retain-bounded",
        "rationale_codes": ["scope-control"],
      },
    ]
    for record in records:
      with self.subTest(gate=record["gate_id"]):
        VALIDATOR.validate_record(record, contract, campaigns, gate_ids)

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

  def test_packet_rejects_source_drift_gate_drift_and_premature_decision(self):
    redirected = copy.deepcopy(self.packet)
    redirected["source_contract"]["competitive_review_packet"] = "README.md: expansion"
    with self.assertRaisesRegex(ValueError, "source contract is not canonical"):
      VALIDATOR.validate_packet(redirected)

    gate_drift = copy.deepcopy(self.packet)
    gate_drift["scope_catalog"]["gate_catalog"][0]["human_status"] = "pass"
    with self.assertRaisesRegex(ValueError, "gate catalog is not source-bound"):
      VALIDATOR.validate_packet(gate_drift)

    premature = copy.deepcopy(self.packet)
    premature["decision"]["go_no_go"] = "expand"
    with self.assertRaisesRegex(ValueError, "decision field must remain unset"):
      VALIDATOR.validate_packet(premature)

  def test_packet_rejects_mutated_competitive_expansion_boundary(self):
    def assert_source_mutation_rejected(target_path, mutate, message):
      target = target_path.resolve()
      original_load = VALIDATOR._load_json

      def load_with_mutation(path):
        source = original_load(path)
        if path.resolve() == target:
          mutate(source)
        return source

      with patch.object(VALIDATOR, "_load_json", side_effect=load_with_mutation):
        with self.assertRaisesRegex(ValueError, message):
          VALIDATOR.validate_packet(copy.deepcopy(self.packet))

    assert_source_mutation_rejected(
      COMPETITIVE,
      lambda source: (
        source["review_boundary"].update({"expansion_approval": True}),
        source["human_review_record"].update({"expansion_go_no_go": "expand"}),
      ),
      "competitive boundary must remain open",
    )
    assert_source_mutation_rejected(
      COMPETITIVE,
      lambda source: source["human_review_record"].update({"participant_results_present": True}),
      "competitive participant results must remain absent",
    )
    assert_source_mutation_rejected(
      COMPETITIVE,
      lambda source: source["human_review_record"].update({"decision": "approve"}),
      "competitive human review field must remain unset",
    )
    assert_source_mutation_rejected(
      FIRST_SESSION,
      lambda source: source["human_review_record"].update({"go_no_go": "expand"}),
      "first-session human review field must remain unset",
    )

  def test_packet_rejects_boolean_and_float_record_counts(self):
    for value in (True, 0.0):
      mutated = copy.deepcopy(self.packet)
      mutated["intake_boundary"]["record_count"] = value
      with self.subTest(value=value):
        with self.assertRaisesRegex(ValueError, "integer zero records"):
          VALIDATOR.validate_packet(mutated)

  def test_record_rejects_free_text_ids_unknown_values_and_duplicates(self):
    campaigns, gates, contract = VALIDATOR._canonical_sources()
    gate_ids = {gate["gate_id"] for gate in gates}
    record = {
      "decision_id": "expansion-competitive-regional-v1-first-session-workflow",
      "campaign": "competitive-regional-v1",
      "gate_id": "first-session-workflow",
      "gate_status": "pass",
      "evidence_strength": "human-evidence",
      "blocker_codes": [],
      "decision_outcome": "expand",
      "rationale_codes": ["evidence-confirmed"],
    }
    with self.assertRaisesRegex(ValueError, "decision ID must be derived"):
      VALIDATOR.validate_record({**record, "decision_id": "expansion-alice-health-diagnosis"}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "record fields are not exactly bounded"):
      VALIDATOR.validate_record({**record, "rationale": "free text"}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "expand requires"):
      VALIDATOR.validate_record({**record, "gate_status": "blocked", "blocker_codes": ["technical-gap"]}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "expand requires"):
      VALIDATOR.validate_record({**record, "evidence_strength": "technical-only"}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "blocked or failed gates require"):
      VALIDATOR.validate_record({**record, "gate_status": "blocked", "decision_outcome": "defer", "blocker_codes": []}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "rationale codes are required"):
      VALIDATOR.validate_record({**record, "rationale_codes": []}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "contains an unknown value"):
      VALIDATOR.validate_record({**record, "decision_outcome": "defer", "blocker_codes": ["unknown"]}, contract, campaigns, gate_ids)
    with self.assertRaisesRegex(ValueError, "must contain unique values"):
      VALIDATOR.validate_record({**record, "rationale_codes": ["evidence-confirmed", "evidence-confirmed"]}, contract, campaigns, gate_ids)


if __name__ == "__main__":
  unittest.main()
