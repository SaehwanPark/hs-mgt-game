import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs" / "evaluation" / "phase12-campaign-asset-need-decision.json"
INVENTORY = ROOT / "docs" / "evaluation" / "phase12-campaign-presentation-coverage.json"
REUSE = ROOT / "docs" / "evaluation" / "phase12-campaign-reuse-matrix.json"


class Phase12CampaignAssetNeedDecisionTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.decision = json.loads(DECISION.read_text(encoding="utf-8"))
    cls.inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    cls.reuse = json.loads(REUSE.read_text(encoding="utf-8"))

  def test_decision_sources_campaigns_and_fallback_match(self):
    decision = self.decision
    self.assertEqual(decision["schema_version"], "campaign-asset-need-decision-v1")
    self.assertEqual(decision["status"], "complete-current-contract-decision")
    for source_ref in decision["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    expected_campaigns = set(self.inventory["campaign_boundaries"])
    self.assertEqual(set(decision["campaigns"]), expected_campaigns)
    self.assertEqual(set(decision["campaigns"]), set(self.reuse["campaign_reuse"]))
    for campaign_id, campaign in decision["campaigns"].items():
      self.assertIn("none-required", campaign["asset_need_decision"])
      self.assertEqual(campaign["fallback_descriptor"], "generic-facility")
      self.assertIn("facility-fallback-boundary", campaign["existing_reuse_boundary"])
      self.assertTrue(campaign["written_equivalent"])
      self.assertGreaterEqual(len(campaign["reopen_triggers"]), 2, campaign_id)

  def test_limits_keep_asset_and_authority_claims_bounded(self):
    limits = " ".join(self.decision["limits"])
    for marker in ("placement/use", "visual quality", "human review", "future campaign art", "No new map", "true-state", "public-release"):
      if marker == "future campaign art":
        self.assertIn("future campaign art", limits)
      elif marker == "No new map":
        self.assertIn("No new map", limits)
      else:
        self.assertIn(marker, limits)
    self.assertEqual(self.decision["test_source"], "tests/test_phase12_campaign_asset_need_decision.py")


if __name__ == "__main__":
  unittest.main()
