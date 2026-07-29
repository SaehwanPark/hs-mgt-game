import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-stabilization-tutorial-presentation.json"


class Phase12StabilizationTutorialPresentationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_tutorial_contract_and_sources_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "stabilization-tutorial-presentation-v1")
    self.assertEqual(ledger["status"], "complete-current-cli-tutorial-contract")
    self.assertEqual(ledger["campaign"], "stabilization-v1")
    self.assertEqual(ledger["tutorial_contract"]["turn_count"], 5)
    self.assertEqual(ledger["tutorial_contract"]["choice_count"], 3)
    self.assertEqual(
      ledger["tutorial_contract"]["choice_fields"],
      ["label", "pros", "cons", "tradeoff", "recommendability"],
    )
    for source_ref in ledger["sources"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    for marker in ("written", "host", "uncertain"):
      self.assertIn(marker, ledger["tutorial_contract"]["visible_equivalent"].lower() + ledger["tutorial_contract"]["command_owner"].lower())
    self.assertIn("shared campaign-coverage panel", ledger["presentation_surface"]["live_gui_boundary"])
    self.assertIn("none-required", ledger["presentation_surface"]["new_asset_need"])
    self.assertTrue(ledger["open_work"])

  def test_limits_keep_tutorial_and_authority_claims_bounded(self):
    limits = " ".join(self.ledger["limits"])
    for marker in ("visual browser tutorial", "human learning", "optimal policy", "No new tutorial copy", "true-state", "public-release"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_stabilization_tutorial_presentation.py")


if __name__ == "__main__":
  unittest.main()
