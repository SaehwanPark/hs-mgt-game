import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.50-teachability-observation-capture"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "teachability_observation_capture", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class TeachabilityObservationCaptureTests(unittest.TestCase):
  def test_matrix_is_three_profiles_across_three_seeds(self):
    self.assertEqual(RUNNER.SEEDS, [42, 43, 44])
    self.assertEqual(
      [profile["id"] for profile in RUNNER.PROFILES],
      ["fiscal_steward", "access_expansion_advocate", "first_time_executive"],
    )

  def test_policies_are_stable_for_visible_observation_fixture(self):
    observation = [
      "Cash runway: stable",
      "Workforce trust: 60",
      "Reported access index: 74",
      "Northlake Health rival report",
    ]
    legal = [
      "Available resources: AP 3, cash 500, political capital 2",
      "hold",
      "monitor target=northlake|summit depth=<1-3>",
      "commit pledge_type=access|quality|workforce level=<1-5>",
    ]

    outputs = [
      RUNNER.observation_policy(profile["id"], observation, legal, 1)
      for profile in RUNNER.PROFILES
    ]

    self.assertEqual(outputs[0], "monitor target=northlake depth=1; hold")
    self.assertEqual(
      outputs[1],
      "monitor target=northlake depth=1; commit pledge_type=access level=1",
    )
    self.assertEqual(outputs[2], "monitor target=northlake depth=1; hold")

  def test_policy_falls_back_when_a_visible_command_is_unavailable(self):
    legal = ["hold"]
    command = RUNNER.observation_policy(
      "fiscal_steward",
      ["Northlake Health rival report"],
      legal,
      1,
    )

    self.assertEqual(command, "hold")

  def test_run_record_preserves_trace_failures_and_retries(self):
    transition = {"state_hash": "abc123"}
    trace = [{
      "turn": 1,
      "submitted_command": "bad command",
      "retry_commands": ["hold"],
      "validation_failures": [{"turn": 1, "error": "invalid command"}],
      "latest_transition": transition,
    }]
    record = RUNNER.build_run_record(
      RUNNER.PROFILES[0],
      42,
      trace,
      [transition],
      trace[0]["validation_failures"],
      ["final"],
      ["debrief"],
    )

    self.assertEqual(record["completion_status"], "incomplete")
    self.assertEqual(record["retry_count"], 1)
    self.assertEqual(record["validation_failures"][0]["error"], "invalid command")
    self.assertEqual(record["turn_trace"][0]["retry_commands"], ["hold"])

  def test_artifact_shape_and_json_rendering_are_stable(self):
    artifact = RUNNER.build_artifact([])
    first = json.dumps(artifact, indent=2) + "\n"
    second = json.dumps(json.loads(first), indent=2) + "\n"

    self.assertEqual(first, second)
    self.assertEqual(artifact["batch_id"], "v0.10.50-teachability-observation-capture")
    self.assertEqual(artifact["difficulty"], "hard")
    self.assertEqual(artifact["seed"], "42, 43, 44")
    self.assertEqual(artifact["runs"], [])


if __name__ == "__main__":
  unittest.main()
