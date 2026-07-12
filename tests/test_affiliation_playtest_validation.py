import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.12.1-affiliation-playtest-validation"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "affiliation_playtest_validation",
  RUNNER_PATH,
)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)

ARTIFACT_PATH = RUNNER_PATH.with_name("results.json")


def load_artifact():
  return json.loads(ARTIFACT_PATH.read_text())


class AffiliationPlaytestValidationTests(unittest.TestCase):
  def test_committed_matrix_is_complete_and_deterministic(self):
    artifact = load_artifact()
    RUNNER.validate_artifact(artifact)
    audit = RUNNER.build_audit(artifact)
    RUNNER.validate_audit(audit)

    self.assertEqual(audit["run_count"], 9)
    self.assertEqual(audit["transition_count"], 54)
    self.assertEqual(audit["validation_failure_count"], 0)

  def test_typed_context_gap_is_explicit_and_runtime_promotion_stays_deferred(self):
    audit = RUNNER.build_audit(load_artifact())

    self.assertEqual(audit["status"], "supported_with_gap")
    self.assertEqual(audit["unexplained_gap_count"], 1)
    self.assertEqual(
      audit["missing_typed_context_fields"],
      ["alternatives", "assumptions", "commitments"],
    )
    self.assertEqual(audit["runtime_promotion"], "deferred")

  def test_posture_and_actor_response_coverage_are_kept_separate(self):
    audit = RUNNER.build_audit(load_artifact())

    self.assertEqual(
      set(audit["final_status_counts"]),
      {"Independent", "Deferred", "Integrated"},
    )
    self.assertIn("Accepted", audit["response_coverage"]["partner"])
    self.assertIn("Approved", audit["response_coverage"]["review"])
    self.assertIn("Support", audit["response_coverage"]["community"])

  def test_malformed_history_is_rejected(self):
    artifact = load_artifact()
    artifact["runs"][0]["history"].pop()

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_misaligned_trace_is_rejected(self):
    artifact = load_artifact()
    artifact["runs"][0]["turn_trace"][0]["latest_transition"] = None

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_markdown_rendering_is_deterministic(self):
    audit = RUNNER.build_audit(load_artifact())

    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("supported_with_gap", first)
    self.assertIn("not human-learning", first.lower())
    self.assertIn("Next bounded candidate", first)


if __name__ == "__main__":
  unittest.main()
