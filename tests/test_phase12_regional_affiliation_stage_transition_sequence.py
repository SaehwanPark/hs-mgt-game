import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-stage-transition-sequence.json"


class Phase12RegionalAffiliationStageTransitionSequenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_sequence_sources_and_order_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-stage-transition-sequence-v1")
    self.assertEqual(ledger["status"], "complete-current-host-projected-stage-transition-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    stages = ledger["sequence"]["decision_stages"]
    self.assertEqual(
      [stage["id"] for stage in stages] + [ledger["sequence"]["terminal"]["id"]],
      [
        "assesspartner",
        "chooseposture",
        "negotiatecommitments",
        "submitreview",
        "resolvereview",
        "integrateordecline",
        "complete",
      ],
    )
    self.assertEqual(
      [stage["next"] for stage in stages],
      [stage["id"] for stage in stages[1:]] + ["complete"],
    )
    self.assertEqual(ledger["sequence"]["terminal"]["next"], "complete")
    self.assertTrue(all(stage["command"] and stage["uncertainty"] for stage in stages))

  def test_sequence_surfaces_and_information_boundaries_remain_bounded(self):
    ledger = self.ledger
    sequence = ledger["sequence"]
    surface = ledger["presentation_surface"]
    self.assertIn("immutable transition", sequence["advancement"])
    self.assertIn("committed history", sequence["written_equivalent"])
    self.assertIn("read-only", surface["host_boundary"])
    self.assertIn("shared campaign-coverage panel", surface["live_gui_boundary"])
    self.assertIn("competitive-first-month only", surface["shared_sequence_boundary"])
    self.assertIn("optional", surface["audio_boundary"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(ledger["open_work"])
    limits = " ".join(ledger["limits"])
    for marker in (
      "Resolved stochastic inputs",
      "private rationale",
      "hidden thresholds",
      "No browser animation",
      "No human",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(
      ledger["test_source"],
      "tests/test_phase12_regional_affiliation_stage_transition_sequence.py",
    )


if __name__ == "__main__":
  unittest.main()
