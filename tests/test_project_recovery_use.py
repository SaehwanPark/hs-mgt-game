import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.56-project-recovery-use"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "project_recovery_use", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
ARTIFACT_PATH = RUNNER_PATH.with_name("results.json")


def sample_run(seed=42):
  source_hashes = RUNNER.source_hashes_by_seed()[seed]
  trace = []
  expected_failures = []
  probe_results = []
  for turn in range(1, RUNNER.EXPECTED_TRANSITIONS + 1):
    failure = []
    retry_commands = []
    turn_after_failure = None
    observation = ["In-flight projects: ClinicNetwork, AscUnit"]
    if turn == 7:
      failure = [{
        "turn": turn,
        "command": "project kind=neurology_unit budget=6",
        "error": "concurrent projects 3 exceed limit 2",
        "code": "too_many_concurrent_projects",
      }]
      expected_failures.extend(failure)
      retry_commands = ["hold"]
      turn_after_failure = turn
    trace.append({
      "turn": turn,
      "observation": observation,
      "legal_commands": ["project kind=<kind> budget=<int>"],
      "planned_command": (
        "project kind=neurology_unit budget=6" if turn == 7 else "hold"
      ),
      "submitted_command": (
        "project kind=neurology_unit budget=6" if turn == 7 else "hold"
      ),
      "validation_failures": failure,
      "retry_commands": retry_commands,
      "turn_after_failure": turn_after_failure,
      "observation_after_failure": observation if failure else None,
      "recovery_decision": (
        {
          "basis": "plain_error_and_unchanged_observation",
          "command": "hold",
          "recognized_limit": True,
          "used_structured_fields": False,
        }
        if failure
        else None
      ),
      "latest_transition": {
        "turn": turn,
        "state_hash": source_hashes[turn - 1],
      },
      "done_after_submit": turn == RUNNER.EXPECTED_TRANSITIONS,
    })
    if turn in RUNNER.PROBE_SCHEDULE:
      probe = RUNNER.PROBE_SCHEDULE[turn]
      failure = failure[0] if failure else {}
      probe_results.append({
        "turn": turn,
        "probe_id": probe["probe_id"],
        "expected_code": probe["expected_code"],
        "observed_code": failure.get("code"),
        "accepted": not bool(failure),
        "retry_commands": retry_commands,
        "turn_after_failure": turn_after_failure,
        "response_conditioned": bool(failure),
      })
  return {
    "profile_id": "project_recovery_use",
    "profile_name": f"Project-Recovery Use / hard / seed {seed}",
    "persona_prompt": (
      "Use only actor-visible observations and the plain validation error to "
      "recover from the concurrent-project rejection."
    ),
    "decision_source": (
      "response-conditioned policy using actor-visible observation and error text"
    ),
    "seed": seed,
    "difficulty": RUNNER.DIFFICULTY,
    "completion_status": "complete",
    "turn_trace": trace,
    "probe_results": probe_results,
    "validation_failures": expected_failures,
    "expected_probe_failures": expected_failures,
    "unexpected_failures": [],
    "retry_count": 1,
    "transition_count": RUNNER.EXPECTED_TRANSITIONS,
    "state_hashes": source_hashes,
    "final_hash": source_hashes[-1],
    "final_observation": [],
    "debrief": [
      "Capital projects are limited to a maximum of 2 concurrent projects."
    ],
  }


class ProjectRecoveryUseTests(unittest.TestCase):
  def test_probe_schedule_and_recovery_surface(self):
    self.assertEqual(
      RUNNER.PROBE_SCHEDULE[7]["expected_code"],
      "too_many_concurrent_projects",
    )
    artifact = RUNNER.build_artifact(
      [sample_run(seed) for seed in RUNNER.SEEDS]
    )
    RUNNER.validate_artifact(artifact)
    surface = artifact["recovery_surface"]
    self.assertEqual(surface["response_conditioned_recovery_count"], 3)
    self.assertEqual(surface["structured_field_use_count"], 0)

  def test_recovery_uses_plain_error_and_preserves_rejected_turn(self):
    run = sample_run()
    failed = next(
      entry for entry in run["turn_trace"] if entry["validation_failures"]
    )
    self.assertEqual(
      failed["recovery_decision"]["basis"],
      "plain_error_and_unchanged_observation",
    )
    self.assertEqual(failed["retry_commands"], ["hold"])
    self.assertEqual(failed["turn_after_failure"], failed["turn"])
    self.assertEqual(
      failed["observation_after_failure"], failed["observation"]
    )

  def test_probe_month_is_bound_to_expected_schedule(self):
    artifact = RUNNER.build_artifact(
      [sample_run(seed) for seed in RUNNER.SEEDS]
    )
    tampered = json.loads(json.dumps(artifact))
    tampered["runs"][0]["probe_results"][2]["turn"] = 8
    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(tampered)

  def test_project_failure_does_not_use_structured_fields(self):
    failure = sample_run()["expected_probe_failures"][0]
    self.assertEqual(failure["code"], "too_many_concurrent_projects")
    self.assertNotIn("hint", failure)
    self.assertNotIn("resource_limit", failure)

  def test_hash_sequences_match_v01055_source(self):
    artifact = RUNNER.build_artifact(
      [sample_run(seed) for seed in RUNNER.SEEDS]
    )
    for run in artifact["runs"]:
      self.assertEqual(
        run["state_hashes"],
        RUNNER.source_hashes_by_seed()[run["seed"]],
      )

  def test_incomplete_run_is_rejected(self):
    runs = [sample_run(seed) for seed in RUNNER.SEEDS]
    runs[0]["completion_status"] = "incomplete"
    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(RUNNER.build_artifact(runs))

  def test_unexpected_failure_is_rejected(self):
    runs = [sample_run(seed) for seed in RUNNER.SEEDS]
    runs[0]["unexpected_failures"] = [{"code": "unexpected"}]
    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(RUNNER.build_artifact(runs))

  def test_diagnostics_render_deterministically(self):
    artifact = RUNNER.build_artifact(
      [sample_run(seed) for seed in RUNNER.SEEDS]
    )
    first = RUNNER.render_diagnostics(artifact)
    second = RUNNER.render_diagnostics(json.loads(json.dumps(artifact)))
    self.assertEqual(first, second)
    self.assertIn("Response-conditioned recoveries", first)

  def test_generated_artifact_matches_contract(self):
    if not ARTIFACT_PATH.exists():
      self.skipTest("generated capture is created after the runner implementation")
    artifact = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    RUNNER.validate_artifact(artifact)


if __name__ == "__main__":
  unittest.main()
