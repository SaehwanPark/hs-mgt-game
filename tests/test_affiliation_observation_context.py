import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.12.2-affiliation-observation-context"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "affiliation_observation_context",
  RUNNER_PATH,
)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)

ARTIFACT_PATH = RUNNER_PATH.with_name("results.json")


def load_artifact():
  return json.loads(ARTIFACT_PATH.read_text())


class AffiliationObservationContextTests(unittest.TestCase):
  def test_post_fix_matrix_has_complete_context_and_history(self):
    artifact = load_artifact()
    RUNNER.validate_artifact(artifact)
    audit = RUNNER.build_audit(artifact)
    RUNNER.validate_audit(audit)

    self.assertEqual(audit["run_count"], 9)
    self.assertEqual(audit["transition_count"], 54)
    self.assertEqual(audit["missing_typed_context_fields"], [])
    self.assertTrue(audit["history_unchanged"])

  def test_every_observation_contains_safe_context_labels(self):
    artifact = load_artifact()

    for run in artifact["runs"]:
      for trace in run["turn_trace"]:
        observation = trace["observation"]
        self.assertTrue(any(line.startswith("Commitments:") for line in observation))
        self.assertGreaterEqual(
          sum(line.startswith("Alternative:") for line in observation),
          2,
        )
        self.assertEqual(
          sum(line.startswith("Assumption:") for line in observation),
          2,
        )

  def test_missing_context_is_rejected(self):
    artifact = load_artifact()
    artifact["runs"][0]["turn_trace"][0]["observation"] = [
      line
      for line in artifact["runs"][0]["turn_trace"][0]["observation"]
      if not line.startswith("Commitments:")
    ]

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_markdown_rendering_is_deterministic(self):
    audit = RUNNER.build_audit(load_artifact())

    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Status: `supported`", first)
    self.assertIn("Missing typed context fields | 0", first)
    self.assertIn("not human-learning", first.lower())


if __name__ == "__main__":
  unittest.main()
