import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-decision-time-recovery-boundary.json"


class Phase12DecisionTimeRecoveryBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_recovery_sources_and_contract_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "phase12-decision-time-recovery-boundary-v1")
    self.assertEqual(ledger["status"], "complete-current-recovery-boundary-only")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    recovery = ledger["recovery_contract"]
    self.assertIn("observation paired with its command", recovery["core_history"])
    self.assertIn("before each command", recovery["debrief"])
    self.assertIn("hash continuity", recovery["host_history_replay"])
    self.assertIn("does not replay full historical observations", recovery["browser_current"])
    self.assertIn("written text", recovery["written_fallback"])

  def test_surface_and_no_expansion_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("read-only", surface["core_authority"])
    self.assertIn("narrower than the core", surface["host_summary_boundary"])
    self.assertIn("competitive-regional-v1 only", surface["browser_boundary"])
    self.assertIn("none-required", surface["new_surface_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "technical recovery boundaries only",
      "not expose resolved inputs",
      "No observation field",
      "causal graph",
      "counterfactual",
      "distributional view",
      "export format",
      "No human visual quality",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_decision_time_recovery_boundary.py")


if __name__ == "__main__":
  unittest.main()
