import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-pressure-state-registration.json"


class Phase12PressureStateRegistrationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_registered_states_bind_visible_catalogs_and_sources(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "pressure-state-registration-v1")
    self.assertEqual(ledger["status"], "complete-current-shared-taxonomy")
    source_cache = {}
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      source_cache[source_path] = path.read_text(encoding="utf-8")
      self.assertIn(marker, source_cache[source_path], source_ref)
    visual_catalog = json.loads((ROOT / "gui" / "visual-catalog.json").read_text(encoding="utf-8"))
    status_ids = {entry["id"] for entry in visual_catalog["statuses"]}
    state_ids = set()
    for state in ledger["pressure_states"]:
      self.assertNotIn(state["id"], state_ids)
      state_ids.add(state["id"])
      self.assertTrue(state["visible_trigger_fields"], state["id"])
      self.assertTrue(state["written_equivalent"], state["id"])
      self.assertIn("static reduced-motion", state["non_color_motion"])
      self.assertIn(state["music_state_id"], source_cache["gui/music-stem-contract.mjs"])
      for status_id in state["status_ids"]:
        self.assertIn(status_id, status_ids, status_id)
      for source_id in state["overlay_ids"] + state["event_cue_ids"]:
        source_path = "gui/operational-overlays.mjs" if source_id.startswith("operational-") else "gui/audio-cue-contract.mjs"
        self.assertIn(source_id, source_cache[source_path], source_id)
      self.assertEqual(state["audio_mapping_boundary"], "eligible-visible-only-not-direct-campaign-mapping")
    self.assertGreaterEqual(len(state_ids), 8)
    for campaign in self.ledger["campaigns"].values():
      self.assertEqual(set(campaign["shared_registered_state_ids"]), state_ids)
      self.assertEqual(campaign["campaign_specific_registered_ids"], [])

  def test_limits_preserve_visible_only_and_no_new_asset_boundary(self):
    limits = " ".join(self.ledger["limits"])
    for marker in ("hidden severity", "direct campaign-envelope audio mapping", "No new campaign-specific pressure ID", "human quality", "educational usability", "true-state", "public-release"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_pressure_state_registration.py")


if __name__ == "__main__":
  unittest.main()
