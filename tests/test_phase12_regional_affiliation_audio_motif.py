import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-audio-motif.json"


class Phase12RegionalAffiliationAudioMotifTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_audio_motif_sources_and_metadata_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-audio-motif-v1")
    self.assertEqual(ledger["status"], "complete-current-affiliation-audio-integration-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    music = ledger["motif"]["music"]
    self.assertEqual(music["id"], "affiliation_negotiation")
    self.assertEqual(music["loop_duration_ms"], 4600)
    self.assertEqual(music["normalization_gain"], 0.07)
    self.assertEqual(music["crossfade_ms"], 260)
    event = ledger["motif"]["event"]
    self.assertEqual(event["id"], "event.affiliation-milestone")
    self.assertEqual(event["priority_class"], "major")
    self.assertEqual(event["duration_ms"], 150)
    self.assertEqual(event["cooldown_ms"], 1500)

  def test_audio_surface_and_information_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("optional", surface["shared_audio_contract"])
    self.assertIn("written meaning", surface["audio_off_boundary"])
    self.assertIn("shared campaign-coverage panel", surface["live_gui_boundary"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertIn("no release audio file", surface["release_audio"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "optional",
      "explicit visible context",
      "agreement",
      "private intent",
      "No new recorded audio",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_regional_affiliation_audio_motif.py")


if __name__ == "__main__":
  unittest.main()
