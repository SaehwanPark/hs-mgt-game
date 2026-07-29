import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-stabilization-audio-state-mapping.json"
PRESSURE_LEDGER = ROOT / "docs" / "evaluation" / "phase12-pressure-state-registration.json"


class Phase12StabilizationAudioStateMappingTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.pressure = json.loads(PRESSURE_LEDGER.read_text(encoding="utf-8"))

  def test_mapping_contract_and_sources_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "stabilization-audio-state-mapping-v1")
    self.assertEqual(ledger["status"], "complete-current-stabilization-audio-integration-boundary")
    self.assertEqual(ledger["campaign"], "stabilization-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

    expected_ids = [state["id"] for state in self.pressure["pressure_states"]]
    self.assertEqual([mapping["id"] for mapping in ledger["mappings"]], expected_ids)
    pressure_by_id = {state["id"]: state for state in self.pressure["pressure_states"]}
    source_cache = {
      path: (ROOT / path).read_text(encoding="utf-8")
      for path in ("gui/music-stem-contract.mjs", "gui/audio-cue-contract.mjs", "gui/audio-direction.mjs")
    }
    for mapping in ledger["mappings"]:
      self.assertEqual(mapping["music_state_id"], pressure_by_id[mapping["id"]]["music_state_id"])
      self.assertEqual(mapping["event_cue_ids"], pressure_by_id[mapping["id"]]["event_cue_ids"])
      self.assertTrue(mapping["visible_trigger_source"])
      self.assertTrue(mapping["text_equivalent"])
      self.assertIn("eligible-visible-only", mapping["audio_boundary"])
      self.assertIn(mapping["music_state_id"], source_cache["gui/music-stem-contract.mjs"])
      for cue_id in mapping["event_cue_ids"]:
        self.assertIn(cue_id, source_cache["gui/audio-cue-contract.mjs"])
      for prototype_id in mapping["direction_prototype_ids"]:
        self.assertIn(prototype_id, source_cache["gui/audio-direction.mjs"])

  def test_campaign_audio_boundary_and_limits_remain_bounded(self):
    surface = self.ledger["campaign_surface"]
    self.assertIn("text-first", surface["current_cli"])
    self.assertIn("shared campaign-coverage", surface["live_gui"])
    self.assertEqual(surface["shared_mapping_status"], "complete-current-shared-contract-mapping")
    self.assertEqual(surface["direct_campaign_audio_status"], "complete-current-host-projected-metadata")
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in ("hidden severity", "Host-sourced music states", "explicit empty", "No new cue", "human comprehension", "true-state", "public-release"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_stabilization_audio_state_mapping.py")


if __name__ == "__main__":
  unittest.main()
