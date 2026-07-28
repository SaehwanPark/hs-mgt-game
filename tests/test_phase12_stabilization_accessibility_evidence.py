import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-stabilization-accessibility-evidence.json"


class Phase12StabilizationAccessibilityEvidenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_accessibility_contract_sources_and_checks_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "stabilization-accessibility-evidence-v1")
    self.assertEqual(ledger["status"], "complete-current-technical-accessibility-contract")
    self.assertEqual(ledger["campaign"], "stabilization-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    self.assertEqual(len(ledger["checks"]), 6)
    for check in ledger["checks"]:
      source_path, marker = check["source"].split(": ", 1)
      self.assertTrue((ROOT / source_path).is_file(), check["source"])
      self.assertIn(marker, (ROOT / source_path).read_text(encoding="utf-8"), check["source"])
      self.assertEqual(check["status"], "pass")
      self.assertTrue(check["coverage"])

  def test_scope_and_human_accessibility_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("text-first", surface["stabilization_boundary"])
    self.assertIn("competitive-regional-v1 only", surface["stabilization_boundary"])
    self.assertIn("do not enter commands", surface["settings_ownership"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in ("Technical interface proxies", "human accessibility", "screen-reader", "No new accessibility behavior", "public-release", "human-review"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_stabilization_accessibility_evidence.py")


if __name__ == "__main__":
  unittest.main()
