import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-integration-state.json"


class Phase12RegionalAffiliationIntegrationStateTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_integration_state_sources_and_decision_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-integration-state-v1")
    self.assertEqual(ledger["status"], "complete-current-integration-state-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    state = ledger["integration_state"]
    self.assertEqual(state["stage_enum"], "IntegrateOrDecline")
    self.assertEqual(state["stage_label"], "Integrate or decline")
    self.assertEqual(state["process_id"], "integration-obligation")
    self.assertEqual(state["process_status"], "visible")
    decision = state["decision"]
    self.assertEqual(decision["id"], "choose-integration")
    self.assertEqual(decision["options"], ["begin", "decline"])
    self.assertEqual(state["outcome_statuses"], ["Integrated", "IntegrationDeclined"])

  def test_integration_surface_and_information_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("host-supplied", surface["shared_process_renderer"])
    self.assertIn("canonical host command", surface["shared_decision_renderer"])
    self.assertIn("competitive-regional-v1 only", surface["live_gui_boundary"])
    self.assertIn("optional", surface["audio_state"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "Integration drag",
      "continuity shock",
      "private approval basis",
      "future integration trajectory",
      "Optional audio",
      "No new map",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_regional_affiliation_integration_state.py")


if __name__ == "__main__":
  unittest.main()
