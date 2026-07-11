import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.51-adversarial-resource-probe"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "adversarial_resource_probe", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def sample_run(seed):
  trace = []
  probe_results = []
  expected_failures = []
  for turn in range(1, RUNNER.EXPECTED_TRANSITIONS + 1):
    probe = RUNNER.PROBE_SCHEDULE.get(turn)
    command = probe["command"] if probe else "hold"
    failures = []
    retry_commands = []
    turn_after_failure = None
    if probe and probe["expected_code"]:
      failure = {
        "turn": turn,
        "command": command,
        "error": f"expected {probe['expected_code']}",
        "code": probe["expected_code"],
      }
      failures.append(failure)
      expected_failures.append(failure)
      retry_commands = ["hold"]
      turn_after_failure = turn
    trace.append({
      "turn": turn,
      "observation": [],
      "legal_commands": [],
      "planned_command": command,
      "submitted_command": command,
      "validation_failures": failures,
      "retry_commands": retry_commands,
      "turn_after_failure": turn_after_failure,
      "latest_transition": {"state_hash": f"hash-{seed}-{turn}"},
      "done_after_submit": turn == RUNNER.EXPECTED_TRANSITIONS,
    })
    if probe:
      probe_results.append({
        "turn": turn,
        "probe_id": probe["probe_id"],
        "expected_code": probe["expected_code"],
        "observed_code": probe["expected_code"],
        "accepted": probe["expected_code"] is None,
        "retry_commands": retry_commands,
        "turn_after_failure": turn_after_failure,
      })
  return {
    "profile_id": "adversarial_resource_probe",
    "profile_name": f"Adversarial Resource Probe / hard / seed {seed}",
    "seed": seed,
    "difficulty": "hard",
    "completion_status": "complete",
    "turn_trace": trace,
    "probe_results": probe_results,
    "validation_failures": expected_failures,
    "expected_probe_failures": expected_failures,
    "unexpected_failures": [],
    "retry_count": len(expected_failures),
    "transition_count": RUNNER.EXPECTED_TRANSITIONS,
    "state_hashes": [f"hash-{seed}-{turn}" for turn in range(1, 25)],
    "final_hash": f"hash-{seed}-24",
    "final_observation": [],
    "debrief": ["debrief"],
  }


class AdversarialResourceProbeTests(unittest.TestCase):
  def test_probe_schedule_covers_expected_validation_boundaries(self):
    self.assertEqual(
      [
        (turn, probe["expected_code"])
        for turn, probe in RUNNER.PROBE_SCHEDULE.items()
      ],
      [
        (1, "insufficient_cash"),
        (2, "ap_budget_exceeded"),
        (3, None),
        (4, None),
        (5, "insufficient_cash"),
        (6, None),
        (7, "too_many_concurrent_projects"),
        (12, "insufficient_cash"),
      ],
    )

  def test_advertised_verbs_are_detected_from_mcp_hints(self):
    legal = [
      "Available resources: AP 3, cash 60, political capital 8",
      "hold",
      "invest domain=beds amount=<int>",
      "project kind=clinic_network budget=<int>",
    ]
    self.assertEqual(
      RUNNER.advertised_verbs(legal),
      {"hold", "invest", "project"},
    )

  def test_sample_artifact_preserves_rejected_turns_and_retries(self):
    runs = [sample_run(seed) for seed in RUNNER.SEEDS]
    controls = [
      {
        "profile_name": f"First-Time Executive / hard / seed {seed}",
        "seed": seed,
        "completion_status": "complete",
        "transition_count": 24,
        "final_hash": f"control-{seed}",
      }
      for seed in RUNNER.SEEDS
    ]
    artifact = RUNNER.build_artifact(runs, controls)
    RUNNER.validate_artifact(artifact)
    for run in artifact["runs"]:
      self.assertEqual(run["retry_count"], 5)
      self.assertTrue(
        all(
          entry["turn_after_failure"] == entry["turn"]
          for entry in run["turn_trace"]
          if entry["validation_failures"]
        )
      )

  def test_diagnostics_render_deterministically(self):
    runs = [sample_run(seed) for seed in RUNNER.SEEDS]
    controls = [
      {
        "profile_name": f"First-Time Executive / hard / seed {seed}",
        "seed": seed,
        "completion_status": "complete",
        "transition_count": 24,
        "final_hash": f"control-{seed}",
      }
      for seed in RUNNER.SEEDS
    ]
    artifact = RUNNER.build_artifact(runs, controls)
    first = RUNNER.render_diagnostics(artifact)
    second = RUNNER.render_diagnostics(artifact)
    self.assertEqual(first, second)
    self.assertIn("initial_cash_overrun", first)
    self.assertIn("too_many_concurrent_projects", first)

  def test_control_summary_uses_existing_first_time_matrix(self):
    controls = RUNNER.control_summary()
    self.assertEqual([control["seed"] for control in controls], [42, 43, 44])
    self.assertTrue(
      all(control["profile_name"].startswith("First-Time Executive") for control in controls)
    )

  def test_generated_artifact_matches_expected_capture(self):
    artifact_path = RUNNER_PATH.with_name("results.json")
    artifact = RUNNER.json.loads(artifact_path.read_text(encoding="utf-8"))
    RUNNER.validate_artifact(artifact)
    self.assertEqual(
      [run["seed"] for run in artifact["runs"]],
      [42, 43, 44],
    )

  def test_generated_probe_errors_preserve_structured_resource_metadata(self):
    artifact = RUNNER.json.loads(
      RUNNER_PATH.with_name("results.json").read_text(encoding="utf-8")
    )
    failures = artifact["runs"][0]["expected_probe_failures"]
    by_code = {failure["code"]: failure for failure in failures}
    for code in ("insufficient_cash", "ap_budget_exceeded"):
      self.assertIn("resource_limit", by_code[code])
      self.assertIn("hint", by_code[code])
    self.assertEqual(
      by_code["too_many_concurrent_projects"]["code"],
      "too_many_concurrent_projects",
    )


if __name__ == "__main__":
  unittest.main()
