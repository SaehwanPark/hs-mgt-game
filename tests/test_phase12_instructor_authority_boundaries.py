import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-instructor-authority-boundaries.json"


class Phase12InstructorAuthorityBoundariesTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_authority_sources_and_campaign_boundaries_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "phase12-instructor-authority-boundaries-v1")
    self.assertEqual(ledger["status"], "complete-current-boundary-only")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    boundaries = ledger["authority_contract"]
    self.assertEqual(set(boundaries), {"stabilization-v1", "competitive-regional-v1", "regional-affiliation-v1"})
    self.assertEqual(boundaries["stabilization-v1"]["status"], "existing-cli-boundary-documented")
    self.assertEqual(boundaries["competitive-regional-v1"]["status"], "existing-cli-boundary-documented")
    self.assertEqual(boundaries["regional-affiliation-v1"]["status"], "boundary-documented-no-new-instructor-surface")
    for boundary in boundaries.values():
      self.assertTrue(boundary["player_observation"])
      self.assertTrue(boundary["post_run_detail"])
      self.assertTrue(boundary["authority"])

  def test_presentation_and_no_expansion_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("read-only", surface["host_ownership"])
    self.assertIn("without authoring", surface["shared_rendering"])
    self.assertIn("competitive-regional-v1 only", surface["live_gui_boundary"])
    self.assertIn("readable", surface["written_fallback"])
    self.assertIn("none-required", surface["new_surface_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "documents current authority boundaries",
      "not a live actor observation",
      "No true-state field",
      "counterfactual",
      "No human comprehension",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_instructor_authority_boundaries.py")


if __name__ == "__main__":
  unittest.main()
