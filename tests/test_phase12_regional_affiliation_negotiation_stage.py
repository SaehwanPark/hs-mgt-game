import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-negotiation-stage.json"


class Phase12RegionalAffiliationNegotiationStageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_stage_sources_and_decision_fields_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-negotiation-stage-v1")
    self.assertEqual(ledger["status"], "complete-current-negotiation-stage-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    stage = ledger["negotiation_stage"]
    self.assertEqual(stage["stage_enum"], "NegotiateCommitments")
    self.assertEqual(stage["stage_label"], "Negotiate commitments")
    self.assertEqual(stage["process_id"], "affiliation-stage")
    self.assertEqual(stage["process_status"], "active")
    decision = stage["decision"]
    self.assertEqual(decision["id"], "set-commitments")
    self.assertEqual(
      [parameter["id"] for parameter in decision["parameters"]],
      ["community", "workforce", "continuity"],
    )
    self.assertTrue(all(parameter["minimum"] == 1 and parameter["maximum"] == 8 for parameter in decision["parameters"]))

  def test_stage_surface_and_information_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("host-supplied", surface["shared_process_renderer"])
    self.assertIn("canonical host command", surface["shared_decision_renderer"])
    self.assertIn("competitive-regional-v1 only", surface["live_gui_boundary"])
    self.assertIn("optional", surface["audio_state"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "hidden partner intent",
      "commitment threshold",
      "Optional audio",
      "No new map",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_regional_affiliation_negotiation_stage.py")


if __name__ == "__main__":
  unittest.main()
