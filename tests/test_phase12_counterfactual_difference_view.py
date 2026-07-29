import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-counterfactual-difference-view.json"


class Phase12CounterfactualDifferenceViewTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_renderer_and_tests_are_source_linked(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase12-counterfactual-difference-view-v1",
    )
    self.assertEqual(
      self.ledger["status"],
      "complete-current-descriptive-counterfactual-view-only",
    )
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_boundaries_and_fallbacks_are_explicit(self):
    comparison = self.ledger["comparison_contract"]
    for marker in (
      "same genesis",
      "committed next-state metric differences",
      "attributed-effect differences",
      "unequal resolved inputs",
      "no causal certainty",
    ):
      self.assertIn(marker, " ".join(comparison.values()))

    surface = self.ledger["presentation_surface"]
    self.assertIn("read-only", surface["host_authority"])
    self.assertIn("no browser route", surface["browser_boundary"])
    self.assertEqual(surface["audio_visual_assets"], "none required")

    limits = " ".join(self.ledger["limits"])
    for marker in (
      "does not recalculate",
      "causal validity",
      "Distributional outcomes",
      "human educational review",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(
      self.ledger["test_source"],
      "tests/test_phase12_counterfactual_difference_view.py",
    )


if __name__ == "__main__":
  unittest.main()
