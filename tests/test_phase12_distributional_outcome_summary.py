import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-distributional-outcome-summary.json"


class Phase12DistributionalOutcomeSummaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_summary_is_source_linked_and_scoped(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase12-distributional-outcome-summary-v1",
    )
    self.assertEqual(
      self.ledger["status"],
      "complete-current-descriptive-instructor-summary-only",
    )
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_responsible_distributional_language_is_explicit(self):
    summary = " ".join(self.ledger["summary_contract"].values())
    for marker in (
      "shown separately",
      "without ranking",
      "may have been unobserved",
      "explicit written fallback",
      "no aggregate welfare score",
      "no causal claim",
    ):
      self.assertIn(marker, summary)

    surface = self.ledger["presentation_surface"]
    self.assertIn("read-only", surface["host_authority"])
    self.assertEqual(surface["player_observation"], "unchanged")
    self.assertEqual(surface["audio_visual_assets"], "none required")
    limits = " ".join(self.ledger["limits"])
    for marker in ("distributional fairness", "Export behavior", "human educational review"):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
