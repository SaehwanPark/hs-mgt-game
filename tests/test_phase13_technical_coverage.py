import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-technical-coverage.json"


class Phase13TechnicalCoverageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_current_technical_release_checks_have_sources_and_commands(self):
    self.assertEqual(self.ledger["schema_version"], "current-technical-release-coverage-v1")
    self.assertEqual(self.ledger["status"], "complete-current-technical-contract")
    self.assertEqual(self.ledger["package_version"], "0.13.20")
    check_ids = {check["id"] for check in self.ledger["checks"]}
    self.assertEqual(
      check_ids,
      {
        "rust-suite",
        "gui-and-governance-suite",
        "screenshot-and-structural-regression",
        "asset-license-and-provenance",
        "release-hash-and-security",
        "accessibility-presentation-contract",
        "offline-package",
        "chromium-compatibility",
        "immutable-replay",
        "in-memory-save-load",
      },
    )
    for check in self.ledger["checks"]:
      self.assertTrue(check["status"].startswith("pass-"), check["id"])
      self.assertTrue(check["command"], check["id"])
      for source in check["sources"]:
        self.assertTrue((ROOT / source).exists(), f"{check['id']}: {source}")
    self.assertEqual(self.ledger["test_source"], "tests/test_phase13_technical_coverage.py")
    self.assertTrue((ROOT / self.ledger["test_source"]).is_file())

  def test_release_limits_keep_product_and_human_gates_open(self):
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "full-campaign",
      "full raster suite",
      "durable persistence",
      "Firefox/WebKit",
      "human accessibility",
      "public-release readiness",
      "educational usability",
    ):
      self.assertIn(marker, limits)
    self.assertIn("No simulation, authority", " ".join(self.ledger["evidence"]))


if __name__ == "__main__":
  unittest.main()
