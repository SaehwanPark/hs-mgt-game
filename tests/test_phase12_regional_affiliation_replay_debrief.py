import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-replay-debrief.json"


class Phase12RegionalAffiliationReplayDebriefTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_replay_and_debrief_sources_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-replay-debrief-v1")
    self.assertEqual(ledger["status"], "complete-current-replay-debrief-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    replay = ledger["replay"]
    self.assertEqual(replay["artifact_version"], "regional-affiliation-replay-v1")
    self.assertEqual(
      replay["serialized_fields"],
      ["artifact_version", "seed", "ruleset_version", "history"],
    )
    for marker in ("ruleset version", "prior state", "actor observation", "state hashes"):
      self.assertIn(marker, replay["integrity"])
    debrief = ledger["debrief"]
    self.assertIn("not legal advice", debrief["title"])
    for content_marker in (
      "stages committed",
      "final status",
      "decision quality under reported observations",
      "independence or deferral alternative prompt",
    ):
      self.assertIn(content_marker, debrief["content"])
    self.assertIn("decision quality", debrief["quality_boundary"])

  def test_replay_debrief_surface_and_information_boundaries_remain_bounded(self):
    ledger = self.ledger
    replay = ledger["replay"]
    debrief = ledger["debrief"]
    surface = ledger["presentation_surface"]
    self.assertIn("written", surface["history_renderer"])
    self.assertIn("written", surface["debrief_renderer"])
    self.assertIn("completion fallback", surface["debrief_renderer"])
    self.assertIn("competitive-regional-v1 only", surface["live_gui_boundary"])
    self.assertIn("optional", surface["audio_boundary"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertIn("typed replay", debrief["resolved_detail_boundary"])
    self.assertIn("technical replay support", replay["cli_boundary"])
    self.assertTrue(ledger["open_work"])
    limits = " ".join(ledger["limits"])
    for marker in (
      "Resolved inputs",
      "post-resolution response detail",
      "not promoted",
      "No browser route",
      "No human",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(
      ledger["test_source"],
      "tests/test_phase12_regional_affiliation_replay_debrief.py",
    )


if __name__ == "__main__":
  unittest.main()
