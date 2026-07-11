import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.46-expert-clearability-evidence"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "expert_clearability_evidence_runner", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_run(profile, seed, status="complete"):
  transition_count = 24 if status == "complete" else 3
  run = {
    "profile_id": profile.lower().replace(" ", "_"),
    "profile_name": profile,
    "persona_prompt": "Test policy.",
    "decision_source": "actor-visible MCP observation and legal resource hints",
    "seed": seed,
    "difficulty": "expert",
    "completion_status": status,
    "turn_trace": [
      {
        "turn": turn,
        "observation": ["visible observation"],
        "legal_commands": ["hold"],
        "submitted_command": "hold",
        "validation_failures": [],
        "latest_transition": {"state_hash": f"{seed:02d}-{turn:02d}"},
        "done_after_submit": turn == transition_count,
      }
      for turn in range(1, transition_count + 1)
    ],
    "validation_failures": [],
    "transition_count": transition_count,
    "state_hashes": [f"{seed:02d}-{turn:02d}" for turn in range(1, transition_count + 1)],
    "final_hash": f"{seed:02d}-{transition_count:02d}",
    "final_observation": ["final observation"],
    "debrief": ["debrief"],
  }
  if status == "failed":
    run["run_error"] = "policy failed after three transitions"
  return run


def make_artifact(failed=False):
  profiles = [
    "Fiscal Caution",
    "Capacity Growth",
    "Balanced Strategy",
    "Naive First-Time",
  ]
  runs = []
  for profile in profiles:
    for seed in [42, 43, 44]:
      status = "failed" if failed and profile == "Naive First-Time" and seed == 44 else "complete"
      runs.append(make_run(profile, seed, status))
  return {
    "filename": "results.json",
    "batch_id": "v0.10.46-expert-clearability-evidence",
    "code_version": "0.10.46",
    "campaign": "competitive-regional-v1",
    "seeds": [42, 43, 44],
    "difficulty": "expert",
    "profiles": profiles,
    "evidence_type": "deterministic Expert clearability matrix",
    "runs": runs,
  }


class ExpertClearabilityEvidenceTests(unittest.TestCase):
  def test_expected_matrix_contains_four_profiles_across_three_seeds(self):
    matrix = RUNNER.expected_matrix()

    self.assertEqual(len(matrix), 12)
    self.assertEqual({seed for _, seed in matrix}, {42, 43, 44})
    self.assertEqual(
      {profile for profile, _ in matrix},
      {
        "Fiscal Caution",
        "Capacity Growth",
        "Balanced Strategy",
        "Naive First-Time",
      },
    )

  def test_validation_accepts_a_recorded_failed_run(self):
    artifact = make_artifact(failed=True)

    RUNNER.validate_artifact(artifact)

    failed = [run for run in artifact["runs"] if run["completion_status"] == "failed"]
    self.assertEqual(len(failed), 1)
    self.assertIn("run_error", failed[0])

  def test_validation_rejects_missing_trace_fields(self):
    artifact = make_artifact()
    del artifact["runs"][0]["turn_trace"]

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_diagnostics_are_deterministic_and_label_failures(self):
    artifact = make_artifact(failed=True)

    first = RUNNER.render_diagnostics(artifact)
    second = RUNNER.render_diagnostics(artifact)

    self.assertEqual(first, second)
    self.assertIn("failed", first)
    self.assertIn("Naive First-Time", first)


if __name__ == "__main__":
  unittest.main()
