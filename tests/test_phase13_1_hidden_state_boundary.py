import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-hidden-state-boundary.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
BROWSER_MODULES = tuple(sorted((ROOT / "gui").glob("*.mjs")))


class Phase131HiddenStateBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_source_contract_markers_exist(self):
    self.assertEqual(self.ledger["schema_version"], "phase13.1-hidden-state-boundary-v1")
    self.assertEqual(self.ledger["status"], "complete-automated-source-boundary-only")
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_current_browser_modules_reject_forbidden_hidden_fields(self):
    source = "\n".join(path.read_text(encoding="utf-8") for path in BROWSER_MODULES)
    for field in self.ledger["forbidden_browser_fields"]:
      self.assertNotIn(field, source, field)
    for marker in ("getRegionalWorld", "renderHistoryEnvelope", "renderReplayEnvelope", "createCheckpointClient"):
      self.assertIn(marker, source)

  def test_roadmap_gate_and_limits_are_explicit(self):
    self.assertIn("[x] No hidden-state leak found.", self.roadmap)
    limits = " ".join(self.ledger["limits"]).lower()
    for marker in ("automated source-checkout boundary", "human content", "provenance", "educational", "public-release"):
      self.assertIn(marker, limits)
    self.assertIn("The host/core may retain true state internally", self.ledger["authority_boundary"])


if __name__ == "__main__":
  unittest.main()
