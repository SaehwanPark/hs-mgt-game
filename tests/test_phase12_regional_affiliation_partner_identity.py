import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-partner-identity.json"


class Phase12RegionalAffiliationPartnerIdentityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_partner_identity_sources_and_fields_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-partner-identity-v1")
    self.assertEqual(ledger["status"], "complete-current-partner-identity-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    self.assertEqual(
      ledger["identity_treatment"]["host_fields"],
      ["partner_name", "reported_condition", "status", "stage"],
    )
    self.assertEqual(ledger["identity_treatment"]["shared_identity_fallback"], "generic-actor")
    self.assertEqual(ledger["identity_treatment"]["portrait_preview"]["role_id"], "affiliation-partner-executive")
    self.assertIn("identity decoration only", ledger["identity_treatment"]["portrait_preview"]["equivalent"])

  def test_partner_scope_and_preview_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("partner", surface["current_host"])
    self.assertIn("written fallback", surface["shared_gui"])
    self.assertIn("actor-family catalog", surface["shared_gui"])
    self.assertIn("shared campaign-coverage panel", surface["live_gui_boundary"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in ("partner-specific visual treatment", "identity decoration only", "unverified/unreleased", "private partner intent", "No new portrait", "public-release"):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_regional_affiliation_partner_identity.py")


if __name__ == "__main__":
  unittest.main()
