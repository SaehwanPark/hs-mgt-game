import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.54-project-limit-recovery"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "project_limit_recovery", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def sample_run(seed=42):
  trace = []
  probe_results = []
  expected_failures = []
  for turn in range(1, RUNNER.EXPECTED_TRANSITIONS + 1):
    probe = RUNNER.PROBE_SCHEDULE.get(turn)
    command = probe["command"] if probe else "hold"
    failures = []
    retries = []
    turn_after_failure = None
    if probe and probe["expected_code"]:
      failure = {
        "turn": turn,
        "command": command,
        "error": "concurrent projects 3 exceed limit 2",
        "code": "too_many_concurrent_projects",
      }
      failures.append(failure)
      expected_failures.append(failure)
      retries = ["hold"]
      turn_after_failure = turn
    trace.append({
      "turn": turn,
      "observation": ["In-flight projects: two active projects"],
      "legal_commands": ["project kind=<kind> budget=<int>"],
      "planned_command": command,
      "submitted_command": command,
      "validation_failures": failures,
      "retry_commands": retries,
      "turn_after_failure": turn_after_failure,
      "observation_after_failure": (
        ["In-flight projects: two active projects"] if failures else None
      ),
      "latest_transition": {"state_hash": f"hash-{seed}-{turn}"},
      "done_after_submit": turn == RUNNER.EXPECTED_TRANSITIONS,
    })
    if probe:
      probe_results.append({
        "turn": turn,
        "probe_id": probe["probe_id"],
        "expected_code": probe["expected_code"],
        "observed_code": failures[0]["code"] if failures else None,
        "accepted": not failures,
        "retry_commands": retries,
        "turn_after_failure": turn_after_failure,
        "hint_present": bool(failures and failures[0].get("hint")),
        "resource_limit_present": bool(
          failures and failures[0].get("resource_limit")
        ),
      })
  return {
    "profile_id": "project_limit_recovery",
    "profile_name": f"Project-Limit Recovery / hard / seed {seed}",
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
    "debrief": [
      "Capital projects are limited to a maximum of 2 concurrent projects."
    ],
  }


class ProjectLimitRecoveryTests(unittest.TestCase):
  def test_probe_schedule_uses_two_accepted_projects_then_one_rejection(self):
    self.assertEqual(
      [
        (turn, probe["probe_id"], probe["expected_code"])
        for turn, probe in RUNNER.PROBE_SCHEDULE.items()
      ],
      [
        (4, "accepted_clinic_project", None),
        (6, "accepted_asc_project", None),
        (7, "concurrent_project_limit", "too_many_concurrent_projects"),
      ],
    )

  def test_artifact_requires_same_turn_recovery_and_complete_runs(self):
    artifact = RUNNER.build_artifact(
      [sample_run(seed) for seed in RUNNER.SEEDS]
    )
    RUNNER.validate_artifact(artifact)
    for run in artifact["runs"]:
      self.assertEqual(run["retry_count"], 1)
      failed = next(
        entry for entry in run["turn_trace"] if entry["validation_failures"]
      )
      self.assertEqual(failed["turn_after_failure"], failed["turn"])
      self.assertEqual(failed["retry_commands"], ["hold"])
      self.assertEqual(
        failed["observation_after_failure"], failed["observation"]
      )

  def test_project_limit_failure_preserves_code_without_resource_hint(self):
    failure = sample_run()["expected_probe_failures"][0]
    self.assertEqual(failure["code"], "too_many_concurrent_projects")
    self.assertNotIn("resource_limit", failure)
    self.assertNotIn("hint", failure)

  def test_incomplete_run_is_rejected(self):
    runs = [sample_run(seed) for seed in RUNNER.SEEDS]
    runs[0]["completion_status"] = "incomplete"
    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(RUNNER.build_artifact(runs))

  def test_unexpected_validation_failure_is_rejected(self):
    runs = [sample_run(seed) for seed in RUNNER.SEEDS]
    runs[0]["unexpected_failures"] = [{"code": "unexpected"}]
    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(RUNNER.build_artifact(runs))

  def test_generated_artifact_matches_expected_capture(self):
    artifact = RUNNER.json.loads(
      RUNNER_PATH.with_name("results.json").read_text(encoding="utf-8")
    )
    RUNNER.validate_artifact(artifact)
    self.assertEqual(
      [run["seed"] for run in artifact["runs"]],
      RUNNER.SEEDS,
    )

  def test_diagnostics_render_deterministically(self):
    artifact = RUNNER.build_artifact(
      [sample_run(seed) for seed in RUNNER.SEEDS]
    )
    first = RUNNER.render_diagnostics(artifact)
    second = RUNNER.render_diagnostics(artifact)
    self.assertEqual(first, second)
    self.assertIn("too_many_concurrent_projects", first)
    self.assertIn("Structured hint", first)


if __name__ == "__main__":
  unittest.main()
