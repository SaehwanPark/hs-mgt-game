import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-campaign-presentation-coverage.json"


class Phase12CampaignPresentationCoverageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_campaign_contract_and_shared_surfaces_match_sources(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "campaign-presentation-coverage-v1")
    self.assertEqual(ledger["status"], "complete-current-inventory")
    self.assertEqual(ledger["campaigns"], ["competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"])
    source_cache = {}
    for key, source_ref in ledger["contract"].items():
      if key == "schema":
        continue
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      source_cache[source_path] = path.read_text(encoding="utf-8")
      self.assertIn(marker, source_cache[source_path], source_ref)
    self.assertEqual(ledger["contract"]["schema"], "campaign-coverage-v1")
    self.assertGreaterEqual(len(ledger["shared_surfaces"]), 8)
    for surface in ledger["shared_surfaces"]:
      source_refs = [surface["browser_source"]]
      if "host_source" in surface:
        source_refs.insert(0, surface["host_source"])
      for source_ref in source_refs:
        source_path, marker = source_ref.split(": ", 1)
        path = ROOT / source_path
        self.assertTrue(path.is_file(), source_ref)
        content = source_cache.setdefault(source_path, path.read_text(encoding="utf-8"))
        self.assertIn(marker, content, source_ref)
      self.assertTrue(surface["visible_equivalent"], surface["id"])
    self.assertEqual(
      set(ledger["campaign_boundaries"]),
      {"competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"},
    )
    self.assertIn("canonical action metadata", ledger["campaign_boundaries"]["competitive-regional-v1"]["current_surface"])
    self.assertIn("none-required", ledger["campaign_boundaries"]["stabilization-v1"]["map_or_facility_asset_need"])
    self.assertIn("none-required", ledger["campaign_boundaries"]["regional-affiliation-v1"]["map_or_facility_asset_need"])

  def test_supporting_evidence_and_limits_keep_authority_boundary_explicit(self):
    evidence = self.ledger["supporting_evidence"]
    for source in [evidence["campaign_contract_test"], *evidence["accessibility_contract_tests"], *evidence["audio_contract_tests"], *evidence["provenance_checks"]]:
      self.assertTrue((ROOT / source).is_file(), source)
    self.assertIn("host adapter", evidence["read_only_boundary"])
    limits = " ".join(self.ledger["limits"])
    for marker in ("tutorial", "pressure-state", "human comprehension", "educational usability", "true-state"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_campaign_presentation_coverage.py")


if __name__ == "__main__":
  unittest.main()
