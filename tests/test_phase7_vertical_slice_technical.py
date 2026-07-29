import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase7-vertical-slice-technical-evidence.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"


class Phase7VerticalSliceTechnicalTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_source_contract_markers_exist(self):
    self.assertEqual(self.ledger["schema_version"], "phase7-vertical-slice-technical-evidence-v1")
    self.assertEqual(self.ledger["status"], "complete-current-supported-technical-slice")
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_five_technical_items_are_marked_with_bounded_limits(self):
    vertical_slice = self.roadmap.split("## Vertical-slice sprint", 1)[1].split("## 8. Final Program Rule", 1)[0]
    for label in self.ledger["roadmap_items"]:
      self.assertIn(f"[x] {label}.", vertical_slice, label)
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "full-campaign coverage",
      "asset provenance",
      "audio usefulness",
      "first-time-user comprehension",
      "human approval",
    ):
      self.assertIn(marker, limits)

  def test_authority_boundary_is_explicit(self):
    boundary = self.ledger["authority_boundary"]
    for marker in ("Host/core owns", "browser validates and renders", "without hidden-state access", "client simulation authority"):
      self.assertIn(marker, boundary)
    self.assertIn("Complete asset provenance review", self.roadmap)
    self.assertIn("Run structured first-time-user evaluation", self.roadmap)
    self.assertIn("Approve or reject expansion to full campaign coverage", self.roadmap)


if __name__ == "__main__":
  unittest.main()
