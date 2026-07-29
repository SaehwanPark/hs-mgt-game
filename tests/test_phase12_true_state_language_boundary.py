import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-true-state-language-boundary.json"


class Phase12TrueStateLanguageBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_language_sources_and_contract_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "phase12-true-state-language-boundary-v1")
    self.assertEqual(ledger["status"], "complete-current-textual-boundary-only")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    language = ledger["language_contract"]
    self.assertIn("Observed", language["player_visible"])
    self.assertIn("True Prior", language["true_state"])
    self.assertIn("True Outcome", language["true_state"])
    self.assertIn("not live player controls", language["true_state"])
    self.assertIn("REVEALED FOR INSTRUCTOR REVIEW", language["instructor_only"])
    self.assertIn("separately", language["decision_quality"])
    self.assertIn("typed/CLI", language["affiliation"])

  def test_surface_and_no_expansion_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("read-only", surface["host_ownership"])
    self.assertIn("without authoring", surface["shared_rendering"])
    self.assertIn("shared campaign-coverage", surface["browser_boundary"])
    self.assertIn("readable", surface["written_fallback"])
    self.assertIn("none-required", surface["new_surface_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "current textual boundary only",
      "not a live actor observation",
      "No true-state field",
      "counterfactual",
      "distributional",
      "export format",
      "No human comprehension",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_true_state_language_boundary.py")


if __name__ == "__main__":
  unittest.main()
