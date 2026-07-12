import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "_workspace" / "experiments" / "v0.12.10-affiliation-queue-closure"
SPEC = importlib.util.spec_from_file_location(
  "affiliation_queue_closure",
  ARTIFACT_DIR / "build_closure.py",
)
CLOSURE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CLOSURE)


class AffiliationQueueClosureTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.artifact = json.loads(
      (ARTIFACT_DIR / "closure.json").read_text(encoding="utf-8")
    )
    CLOSURE.validate_closure(cls.artifact)

  def test_closure_identity_and_existing_runtime(self):
    self.assertEqual(self.artifact["artifact_type"], "affiliation_queue_closure")
    self.assertEqual(self.artifact["code_version"], "0.12.10")
    self.assertEqual(
      self.artifact["closure_status"],
      "complete_existing_runtime",
    )
    self.assertEqual(self.artifact["proposal"]["minimum_contract_count"], 6)

  def test_existing_affiliation_evidence_is_complete(self):
    proposal = self.artifact["proposal"]
    self.assertEqual(proposal["run_count"], 9)
    self.assertEqual(proposal["transition_count"], 54)
    self.assertEqual(proposal["observation_count"], 54)
    self.assertEqual(proposal["implementation_status"], "existing_opt_in_runtime_confirmed")

  def test_queue_closure_preserves_deferred_scope(self):
    self.assertEqual(self.artifact["queue_action"], "remove_item_from_future_queue")
    self.assertFalse(self.artifact["runtime_change_authorized"])
    self.assertEqual(self.artifact["runtime_promotion"], "deferred")
    self.assertIn("direct acquisition branch", self.artifact["deferred_scope"])
    self.assertIn("changes to competitive-regional-v1", self.artifact["deferred_scope"])

  def test_source_markers_are_supported(self):
    self.assertTrue(
      all(
        value["status"] == "supported"
        for value in self.artifact["source_marker_contract"].values()
      )
    )

  def test_reopening_condition_requires_new_evidence(self):
    self.assertIn("new evidence", self.artifact["next_action"])
    self.assertIn("concrete", self.artifact["next_action"])


if __name__ == "__main__":
  unittest.main()
