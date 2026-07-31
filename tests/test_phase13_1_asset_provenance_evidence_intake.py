import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
PACKET = ROOT / "docs" / "evaluation" / "phase13.1-asset-provenance-evidence-intake-packet.json"
VISUAL_REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"
AUDIO_REGISTRY = ROOT / "assets" / "registry" / "audio-assets.json"
PORTRAIT_QUEUE = ROOT / "assets" / "generation" / "portrait-review-queue.json"
WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
FEEDBACK = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


VALIDATOR = load_module(
  "validate_asset_provenance_evidence_intake",
  "scripts/validate_asset_provenance_evidence_intake.py",
)


class Phase131AssetProvenanceEvidenceIntakeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.visual = json.loads(VISUAL_REGISTRY.read_text(encoding="utf-8"))
    cls.audio = json.loads(AUDIO_REGISTRY.read_text(encoding="utf-8"))
    cls.portraits = json.loads(PORTRAIT_QUEUE.read_text(encoding="utf-8"))
    cls.workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    cls.feedback = json.loads(FEEDBACK.read_text(encoding="utf-8"))

  def test_empty_pending_packet_and_validator_pass(self):
    VALIDATOR.validate_packet(self.packet)
    self.assertEqual(self.packet["status"], "complete-technical-intake-pending-human-review")
    self.assertEqual(self.packet["intake_boundary"]["record_count"], 0)
    self.assertEqual(self.packet["records"], [])
    self.assertEqual(self.packet["decision"]["status"], "pending-human-review")
    self.assertIsNone(self.packet["decision"]["go_no_go"])
    self.assertFalse(self.packet["release_boundary"]["public_release_approval"])

  def test_inventory_is_exactly_derived_from_canonical_sources(self):
    self.assertEqual(
      self.packet["inventory"]["visual_ids"],
      [entry["id"] for entry in self.visual["entries"]],
    )
    self.assertEqual(
      self.packet["inventory"]["audio_ids"],
      [entry["id"] for entry in self.audio["entries"]],
    )
    self.assertEqual(
      self.packet["inventory"]["portrait_preview_ids"],
      [entry["asset_id"] for entry in self.portraits["entries"]],
    )
    self.assertEqual(self.packet["inventory"]["visual_count"], len(self.visual["entries"]))
    self.assertEqual(self.packet["inventory"]["audio_count"], len(self.audio["entries"]))
    self.assertEqual(self.packet["inventory"]["portrait_preview_count"], len(self.portraits["entries"]))

  def test_review_contract_is_source_bound(self):
    contract = self.packet["review_contract"]
    expected_gates = [
      "provenance",
      "license",
      "accessibility",
      "technical",
      "human-review",
      "release",
      *self.workflow["required_human_review_fields"],
      *self.portraits["required_gates"],
    ]
    self.assertEqual(contract["gate_ids"], expected_gates)
    self.assertEqual(contract["finding_categories"], self.feedback["finding_categories"])
    self.assertEqual(contract["forbidden_fields"], self.feedback["session_record"]["forbidden"])
    self.assertEqual(
      contract["record_fields"],
      ["asset_id", "asset_family", "review_status", "gate_statuses", "finding_categories"],
    )

  def test_representative_record_is_bounded_and_source_bound(self):
    visual_id = self.packet["inventory"]["visual_ids"][0]
    record = {
      "asset_id": visual_id,
      "asset_family": "visual-registry",
      "review_status": "reviewed",
      "gate_statuses": {"provenance": "pending", "license": "pending"},
      "finding_categories": ["defect"],
    }
    _, families = VALIDATOR._canonical_inventory()
    VALIDATOR.validate_record(record, self.packet["review_contract"], families)

  def test_unknown_record_fields_and_private_fields_are_rejected(self):
    record = {
      "asset_id": self.packet["inventory"]["visual_ids"][0],
      "asset_family": "visual-registry",
      "review_status": "reviewed",
      "gate_statuses": {},
      "finding_categories": [],
      "name": "reviewer",
      "private_game_state": "hidden",
      "session_id": "session-1",
      "raw_notes": "free text",
    }
    _, families = VALIDATOR._canonical_inventory()
    with self.assertRaisesRegex(ValueError, "fields are not exactly bounded"):
      VALIDATOR.validate_record(record, self.packet["review_contract"], families)

  def test_packet_rejects_unknown_top_level_and_boundary_fields(self):
    for location, field in (
      (self.packet, "unexpected"),
      (self.packet["intake_boundary"], "raw_transcript"),
      (self.packet["release_boundary"], "release_url"),
      (self.packet["decision"], "notes"),
    ):
      mutated = copy.deepcopy(self.packet)
      target = mutated
      if location is self.packet["intake_boundary"]:
        target = mutated["intake_boundary"]
      elif location is self.packet["release_boundary"]:
        target = mutated["release_boundary"]
      elif location is self.packet["decision"]:
        target = mutated["decision"]
      target[field] = "not-allowed"
      with self.subTest(field=field):
        with self.assertRaisesRegex(ValueError, "fields are not exactly bounded"):
          VALIDATOR.validate_packet(mutated)

  def test_packet_rejects_source_redirect_inventory_drift_and_boolean_count(self):
    redirected = copy.deepcopy(self.packet)
    redirected["source_contract"]["visual_registry"] = "README.md: Health Policy Strategy Game"
    with self.assertRaisesRegex(ValueError, "source contract is not canonical"):
      VALIDATOR.validate_packet(redirected)

    drifted = copy.deepcopy(self.packet)
    drifted["inventory"]["visual_ids"].append("visual.unknown")
    with self.assertRaisesRegex(ValueError, "inventory does not match"):
      VALIDATOR.validate_packet(drifted)

    boolean_count = copy.deepcopy(self.packet)
    boolean_count["intake_boundary"]["record_count"] = False
    with self.assertRaisesRegex(ValueError, "zero records"):
      VALIDATOR.validate_packet(boolean_count)

  def test_packet_rejects_float_inventory_and_release_counters(self):
    float_inventory = copy.deepcopy(self.packet)
    float_inventory["inventory"]["visual_count"] = 38.0
    with self.assertRaisesRegex(ValueError, "inventory count must be an integer"):
      VALIDATOR.validate_packet(float_inventory)

    float_release = copy.deepcopy(self.packet)
    float_release["release_boundary"]["new_release_files"] = 0.0
    with self.assertRaisesRegex(ValueError, "release counter must remain integer zero"):
      VALIDATOR.validate_packet(float_release)

  def test_packet_rejects_portrait_promotion_and_release_boundary_mutations(self):
    def assert_source_mutation_rejected(relative_path, mutate):
      target = (ROOT / relative_path).resolve()
      original_load = VALIDATOR._load_json

      def load_with_mutation(path):
        document = original_load(path)
        if path.resolve() == target:
          mutate(document)
        return document

      with patch.object(VALIDATOR, "_load_json", side_effect=load_with_mutation):
        with self.assertRaisesRegex(ValueError, "portrait generation boundary failed"):
          VALIDATOR.validate_packet(copy.deepcopy(self.packet))

    assert_source_mutation_rejected(
      "assets/generation/portrait-review-queue.json",
      lambda queue: (
        queue.update({"release_eligible": True}),
        queue["entries"][0].update({"source_hash": "sha256:wrong"}),
      ),
    )
    assert_source_mutation_rejected(
      "assets/generation/portrait-previews.json",
      lambda previews: (
        previews.update({"release_eligible": True}),
        previews["entries"][0].update({"preview_status": "approved"}),
      ),
    )
    assert_source_mutation_rejected(
      "assets/generation/generation-manifest.json",
      lambda manifest: manifest.update({
        "entries": [{"asset_id": self.packet["inventory"]["portrait_preview_ids"][0]}],
      }),
    )

  def test_record_rejects_unknown_gate_status_and_portrait_family_mismatch(self):
    _, families = VALIDATOR._canonical_inventory()
    record = {
      "asset_id": self.packet["inventory"]["visual_ids"][0],
      "asset_family": "visual-registry",
      "review_status": "reviewed",
      "gate_statuses": {"unknown": "pending"},
      "finding_categories": [],
    }
    with self.assertRaisesRegex(ValueError, "gate ID is not allowed"):
      VALIDATOR.validate_record(record, self.packet["review_contract"], families)

    record["gate_statuses"] = {"provenance": "unknown"}
    with self.assertRaisesRegex(ValueError, "gate status is not allowed"):
      VALIDATOR.validate_record(record, self.packet["review_contract"], families)

    record["gate_statuses"] = {}
    record["asset_id"] = self.packet["inventory"]["portrait_preview_ids"][0]
    record["asset_family"] = "visual-registry"
    with self.assertRaisesRegex(ValueError, "asset family does not match"):
      VALIDATOR.validate_record(record, self.packet["review_contract"], families)

    record["asset_id"] = self.packet["inventory"]["visual_ids"][0]
    record["asset_family"] = "visual-registry"
    with self.assertRaisesRegex(ValueError, "reviewed records must contain gate evidence"):
      VALIDATOR.validate_record(record, self.packet["review_contract"], families)


if __name__ == "__main__":
  unittest.main()
