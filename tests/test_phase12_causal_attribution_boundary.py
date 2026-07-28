import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-causal-attribution-boundary.json"


class Phase12CausalAttributionBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_attribution_sources_and_contract_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "phase12-causal-attribution-boundary-v1")
    self.assertEqual(ledger["status"], "complete-current-direct-attribution-boundary-only")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    attribution = ledger["attribution_contract"]
    self.assertIn("source, metric, delta, and text", attribution["typed_effect"])
    self.assertIn("direct effects", attribution["resolution_sequence"])
    self.assertIn("attributed mechanisms", attribution["debrief"])
    self.assertIn("does not author effects", attribution["browser"])
    self.assertIn("without audio", attribution["written_fallback"])

  def test_surface_and_no_inference_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("read-only", surface["host_authority"])
    self.assertIn("without calculating", surface["shared_rendering"])
    self.assertIn("competitive-regional-v1 only", surface["browser_boundary"])
    self.assertIn("none-required", surface["new_surface_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "direct-effect attribution only",
      "causal certainty",
      "causal graph",
      "not hidden-input disclosure",
      "No causal inference engine",
      "counterfactual",
      "distributional view",
      "export format",
      "No human comprehension",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_causal_attribution_boundary.py")


if __name__ == "__main__":
  unittest.main()
