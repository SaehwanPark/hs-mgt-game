import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "_workspace" / "experiments" / "v0.12.8-teachability-queue-closure"
SPEC = importlib.util.spec_from_file_location(
  "teachability_queue_closure",
  ARTIFACT_DIR / "build_closure.py",
)
CLOSURE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CLOSURE)


class TeachabilityQueueClosureTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.artifact = json.loads(
      (ARTIFACT_DIR / "closure.json").read_text(encoding="utf-8")
    )
    CLOSURE.validate_closure(cls.artifact)

  def test_closure_identity_and_source_matrix(self):
    self.assertEqual(
      self.artifact["artifact_type"],
      "competitive_teachability_queue_closure",
    )
    self.assertEqual(self.artifact["code_version"], "0.12.8")
    report = self.artifact["source_report"]
    self.assertEqual(report["source_count"], 2)
    self.assertEqual(report["run_count"], 18)
    self.assertEqual(report["complete_run_count"], 18)
    self.assertEqual(report["transition_count"], 270)

  def test_no_structural_gap_is_authoritative(self):
    report = self.artifact["source_report"]
    self.assertEqual(report["gap_count"], 0)
    self.assertEqual(report["finding"], "no_structural_gap")
    self.assertTrue(
      all(
        source["status"] == "supported"
        for source in report["sources"]
      )
    )

  def test_all_review_coverage_steps_are_supported(self):
    for source in self.artifact["source_report"]["sources"]:
      for coverage in source["coverage"].values():
        self.assertEqual(coverage["status"], "supported")
        self.assertEqual(coverage["eligible_runs"], coverage["supported_runs"])

  def test_queue_closure_does_not_promote_runtime_changes(self):
    self.assertEqual(
      self.artifact["closure_status"],
      "complete_no_actionable_gap",
    )
    self.assertEqual(self.artifact["queue_action"], "remove_item_from_future_queue")
    self.assertFalse(self.artifact["runtime_change_authorized"])
    self.assertEqual(self.artifact["runtime_promotion"], "deferred")

  def test_source_markers_are_supported(self):
    self.assertTrue(
      all(
        contract["status"] == "supported"
        for contract in self.artifact["source_marker_contract"].values()
      )
    )


if __name__ == "__main__":
  unittest.main()
