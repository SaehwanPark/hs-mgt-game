import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-provenance-audit.json"


class Phase12RegionalAffiliationProvenanceAuditTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_provenance_sources_and_audit_checks_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-provenance-audit-v1")
    self.assertEqual(ledger["status"], "complete-current-technical-provenance-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    self.assertEqual(len(ledger["audit_checks"]), 8)
    for check in ledger["audit_checks"]:
      source_path, marker = check["source"].split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), check["source"])
      self.assertIn(marker, path.read_text(encoding="utf-8"), check["source"])
      self.assertEqual(check["status"], "pass")
      self.assertTrue(check["coverage"])

  def test_campaign_provenance_and_release_boundaries_remain_bounded(self):
    boundary = self.ledger["campaign_boundary"]
    self.assertIn("repository-authored", boundary["reusable_visuals"])
    self.assertIn("runtime-generated", boundary["reusable_audio"])
    self.assertIn("none-required", boundary["new_asset_need"])
    self.assertEqual(boundary["third_party_release_count"], 0)
    self.assertEqual(boundary["release_audio_count"], 0)
    self.assertIn("unreleased", boundary["portrait_preview_status"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "technical provenance audit",
      "legal clearance",
      "training-data provenance",
      "No new map",
      "Unverified portrait previews",
      "public-release",
      "educational",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(
      self.ledger["test_source"],
      "tests/test_phase12_regional_affiliation_provenance_audit.py",
    )


if __name__ == "__main__":
  unittest.main()
