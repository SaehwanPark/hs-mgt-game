import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "_workspace" / "experiments" / "v0.12.9-difficulty-queue-closure"
SPEC = importlib.util.spec_from_file_location(
  "difficulty_queue_closure",
  ARTIFACT_DIR / "build_closure.py",
)
CLOSURE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CLOSURE)


class DifficultyQueueClosureTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.artifact = json.loads(
      (ARTIFACT_DIR / "closure.json").read_text(encoding="utf-8")
    )
    CLOSURE.validate_closure(cls.artifact)

  def test_closure_identity_and_pressure_signal(self):
    self.assertEqual(
      self.artifact["artifact_type"],
      "difficulty_depth_queue_closure",
    )
    self.assertEqual(self.artifact["code_version"], "0.12.9")
    evidence = self.artifact["difficulty_evidence"]
    self.assertEqual(evidence["run_count"], 75)
    self.assertEqual(evidence["transition_count"], 1800)
    self.assertEqual(evidence["pressure_dimension"], "workforce_capacity")
    self.assertEqual(evidence["expert_clearability_runs"], 15)

  def test_current_observation_context_preserves_controls(self):
    evidence = self.artifact["observation_evidence"]
    self.assertEqual(evidence["run_count"], 75)
    self.assertEqual(evidence["transition_count"], 1800)
    self.assertTrue(evidence["exact_history_match"])
    self.assertTrue(evidence["exact_state_hash_match"])
    self.assertEqual(evidence["hidden_marker_count"], 0)

  def test_no_runtime_tuning_is_authorized(self):
    self.assertEqual(
      self.artifact["closure_status"],
      "complete_no_unexplained_gap",
    )
    self.assertFalse(self.artifact["runtime_difficulty_change_authorized"])
    self.assertEqual(self.artifact["runtime_promotion"], "deferred")
    self.assertEqual(self.artifact["queue_action"], "remove_item_from_future_queue")

  def test_source_markers_and_limits_are_present(self):
    self.assertTrue(
      all(
        value["status"] == "supported"
        for value in self.artifact["source_marker_contract"].values()
      )
    )
    self.assertGreaterEqual(len(self.artifact["evidence_limits"]), 4)

  def test_reopening_condition_requires_new_gap(self):
    self.assertIn("new unexplained", self.artifact["next_action"])
    self.assertIn("design gate", self.artifact["next_action"])


if __name__ == "__main__":
  unittest.main()
