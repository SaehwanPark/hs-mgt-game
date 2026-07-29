import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-export-behavior-boundary.json"


class Phase12ExportBehaviorBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_export_sources_are_present_and_linked(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase12-export-behavior-boundary-v1",
    )
    self.assertEqual(
      self.ledger["status"],
      "complete-current-post-run-export-boundary-only",
    )
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_campaign_formats_and_authority_limits_are_explicit(self):
    contract = self.ledger["campaign_contract"]
    for marker in (
      "versioned replay-artifact-0.1.15",
      "serialized CompetitiveHistory JSON",
      "versioned regional-affiliation replay artifact",
      "empty export input skips writing",
      "never browser state",
      "mid-run saves",
    ):
      self.assertIn(marker, " ".join(contract.values()))

    surface = self.ledger["presentation_surface"]
    self.assertIn("no browser export route", surface["browser_boundary"])
    self.assertEqual(surface["asset_audio"], "none involved")
    limits = " ".join(self.ledger["limits"])
    for marker in ("durable persistence", "competitive export versioning", "public-release packaging"):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
