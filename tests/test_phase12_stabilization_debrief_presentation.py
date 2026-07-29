import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-stabilization-debrief-presentation.json"


class Phase12StabilizationDebriefPresentationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_debrief_contract_and_sources_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "stabilization-debrief-presentation-v1")
    self.assertEqual(ledger["status"], "complete-current-cli-host-debrief-contract")
    self.assertEqual(ledger["campaign"], "stabilization-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    self.assertEqual(
      ledger["debrief_contract"]["sections"],
      [
        "run-level-tradeoff",
        "actor-rationales-at-decision-time",
        "attributed-mechanisms-to-inspect",
        "reflection-prompt",
        "decision-quality-versus-outcome-quality",
        "observation-revision-note-when-present",
      ],
    )
    self.assertEqual(
      ledger["debrief_contract"]["instructor_appendix"]["status"],
      "existing-cli-appendix-not-new-surface",
    )
    self.assertIn("committed history", ledger["debrief_contract"]["ownership"])
    self.assertIn("latest state hash", ledger["debrief_contract"]["history_replay_alignment"])
    self.assertIn("without audio", ledger["debrief_contract"]["written_equivalent"])

  def test_surface_and_instructor_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("five-turn", surface["current_cli"])
    self.assertIn("shared campaign-coverage panel", surface["live_gui_boundary"])
    self.assertIn("Optional debrief music", surface["audio"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in ("complete visual stabilization debrief", "existing CLI instructor appendix", "No new debrief copy", "human comprehension", "counterfactual", "public-release"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_stabilization_debrief_presentation.py")


if __name__ == "__main__":
  unittest.main()
