import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-limitations-statement.json"
GUIDE = ROOT / "docs" / "guides" / "gui-how-to-play.md"


class Phase131LimitationsStatementTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.guide = GUIDE.read_text(encoding="utf-8")

  def test_source_contract_markers_exist(self):
    self.assertEqual(self.ledger["schema_version"], "phase13.1-limitations-statement-v1")
    self.assertEqual(self.ledger["status"], "complete-documentation-boundary-only")
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_statement_distinguishes_simulation_from_real_world_advice(self):
    normalized_guide = " ".join(self.guide.split())
    for marker in (
      "fictional educational simulation",
      "not a calibrated policy forecast",
      "operational, clinical, financial, regulatory,",
      "The host remains authoritative",
      "human accessibility, educational, audio-quality, provenance, resemblance,",
      "use the game to make real-world decisions",
    ):
      self.assertIn(marker, normalized_guide)
    self.assertFalse(self.ledger["claims"].get("policy_validity", False))
    self.assertIn("public-release approval", " ".join(self.ledger["remaining_gates"]))


if __name__ == "__main__":
  unittest.main()
