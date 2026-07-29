import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-player-help-boundary.json"


class Phase13PlayerHelpBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_source_contract_markers_exist(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase13.1-player-help-boundary-v1",
    )
    self.assertEqual(
      self.ledger["status"],
      "complete-current-gui-settings-help-documentation-only",
    )
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_user_contract_and_limits_are_explicit(self):
    audience = self.ledger["audience_and_use_case"]
    self.assertIn("first-time", audience["primary_users"])
    self.assertIn("facilitators", audience["supporting_users"])

    contract = " ".join(self.ledger["documented_contract"].values())
    for marker in (
      "Reduced motion",
      "Standard/Large text",
      "session-local fallback",
      "cues-only",
      "independent channel volume",
      "Asset credits and provenance",
      "next actions",
      "do not change host commands",
    ):
      self.assertIn(marker, contract)

    limits = " ".join(self.ledger["limits"])
    for marker in (
      "human accessibility",
      "educational usability",
      "classroom readiness",
      "public-release approval",
      "authority paths",
    ):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
