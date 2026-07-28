import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "evaluation" / "phase12-campaign-reuse-matrix.json"


class Phase12CampaignReuseMatrixTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))

  def test_catalog_sources_and_reuse_decisions_match_current_inventory(self):
    matrix = self.matrix
    self.assertEqual(matrix["schema_version"], "campaign-presentation-reuse-v1")
    self.assertEqual(matrix["status"], "complete-current-reuse-matrix")
    self.assertEqual(matrix["campaigns"], ["stabilization-v1", "regional-affiliation-v1"])
    decisions = {
      "current-contract-eligible",
      "current-contract-eligible-but-not-direct-mapping",
      "fallback-only",
    }
    for source_ref in matrix["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    shared_ids = set()
    for reuse_set in matrix["shared_reuse"]:
      shared_ids.add(reuse_set["id"])
      self.assertIn(reuse_set["reuse_decision"], decisions)
      self.assertTrue(reuse_set["visible_equivalent"], reuse_set["id"])
      for source in reuse_set["catalog_sources"]:
        content = (ROOT / source["path"]).read_text(encoding="utf-8")
        if "group" in source:
          catalog = json.loads(content)
          entries = catalog[source["group"]]
          known = {entry["id"] for entry in entries}
          for asset_id in source["ids"]:
            self.assertIn(asset_id, known, asset_id)
            entry = next(entry for entry in entries if entry["id"] == asset_id)
            self.assertEqual(entry["approval_status"], "approved", asset_id)
            if source["path"] == "gui/audio-catalog.json":
              self.assertIsNone(entry["release_path"], asset_id)
        else:
          self.assertIn(source["marker"], content)
          for asset_id in source["ids"]:
            self.assertIn(asset_id, content, asset_id)
    self.assertIn("facility-fallback-boundary", shared_ids)
    for campaign_id, campaign in matrix["campaign_reuse"].items():
      self.assertIn(campaign_id, matrix["campaigns"])
      self.assertTrue(set(campaign["reused_surface_sets"]).issubset(shared_ids), campaign_id)
      self.assertIn("none-required", campaign["new_asset_need"])
      self.assertIn("open_work", campaign)
      audio = campaign["audio_reuse"]
      self.assertIn(audio["reuse_decision"], decisions)
      self.assertTrue(audio["visible_equivalent"])

  def test_limits_keep_quality_and_authority_claims_bounded(self):
    limits = " ".join(self.matrix["limits"])
    for marker in ("directly mapped", "file-backed audio", "human comprehension", "audio usefulness", "true-state", "public-release"):
      self.assertIn(marker, limits)
    self.assertEqual(self.matrix["test_source"], "tests/test_phase12_campaign_reuse_matrix.py")


if __name__ == "__main__":
  unittest.main()
