import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = (
  ROOT / "_workspace" / "experiments" / "v0.12.6-workforce-capacity-observation"
)
AUDIT_PATH = ARTIFACT_DIR / "run_audit.py"
ARTIFACT_PATH = ARTIFACT_DIR / "results.json"
SPEC = importlib.util.spec_from_file_location(
  "workforce_capacity_observation_audit",
  AUDIT_PATH,
)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


class WorkforceCapacityObservationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.artifact = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    cls.audit = AUDIT.build_audit(cls.artifact)

  def test_artifact_identity_and_matrix(self):
    self.assertEqual(
      self.artifact["artifact_type"],
      "workforce_capacity_observation_validation",
    )
    self.assertEqual(self.artifact["code_version"], "0.12.6")
    self.assertEqual(len(self.artifact["runs"]), 75)
    self.assertEqual(self.audit["transition_count"], 1800)
    self.assertEqual(self.audit["completed_run_count"], 75)

  def test_safe_projection_is_present_in_every_trace_entry(self):
    for run in self.artifact["runs"]:
      for entry in run["turn_trace"]:
        observation = entry["observation"]
        self.assertTrue(any(line.startswith("Staffing:") for line in observation))
        self.assertTrue(
          any(line.startswith("Physical capacity:") for line in observation)
        )

  def test_projection_counts_and_exclusions(self):
    projection = self.artifact["observation_projection"]
    self.assertEqual(projection["trace_entry_count"], 1800)
    self.assertEqual(projection["staffing_line_count"], 1800)
    self.assertEqual(projection["physical_capacity_line_count"], 1800)
    self.assertEqual(projection["hidden_marker_count"], 0)

  def test_all_tier_and_expert_histories_match_controls(self):
    comparisons = self.audit["source_comparisons"]
    self.assertEqual(comparisons["all_tiers"]["run_count"], 60)
    self.assertEqual(comparisons["all_tiers"]["history_match_count"], 60)
    self.assertEqual(comparisons["all_tiers"]["state_hash_match_count"], 60)
    self.assertEqual(comparisons["expert"]["run_count"], 15)
    self.assertEqual(comparisons["expert"]["history_match_count"], 15)
    self.assertEqual(comparisons["expert"]["state_hash_match_count"], 15)

  def test_runtime_promotion_remains_deferred(self):
    self.assertFalse(self.artifact["difficulty_change_authorized"])
    self.assertEqual(self.artifact["runtime_promotion"], "deferred")
    self.assertTrue(self.audit["exact_history_match"])
    self.assertTrue(self.audit["exact_state_hash_match"])


if __name__ == "__main__":
  unittest.main()
