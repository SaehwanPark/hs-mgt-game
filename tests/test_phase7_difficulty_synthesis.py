import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.10-phase7-difficulty-synthesis"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "phase7_difficulty_synthesis",
  RUNNER_PATH,
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_strategy_source():
  reports = []
  for profile in RUNNER.PROFILES:
    for seed in RUNNER.SEEDS:
      for difficulty in RUNNER.DIFFICULTIES:
        reports.append({
          "profile": profile,
          "seed": seed,
          "difficulty": difficulty,
          "status": "supported",
        })
  return {
    "artifact_type": "strategy_comparison_use_audit",
    "batch_id": "v0.11.6-strategy-comparison-use-audit",
    "code_version": "0.11.6",
    "campaign": RUNNER.CAMPAIGN,
    "ruleset": RUNNER.RULESET,
    "state_hash_schema": RUNNER.STATE_HASH_SCHEMA,
    "seeds": RUNNER.SEEDS,
    "difficulties": RUNNER.DIFFICULTIES,
    "profiles": RUNNER.PROFILES,
    "run_count": 60,
    "expected_run_count": 60,
    "completed_run_count": 60,
    "transition_count": 1440,
    "expected_month_count": 1440,
    "trace_count": 1440,
    "prior_observation_match_count": 1380,
    "debrief_outcome_match_count": 1440,
    "debrief_outcome_gap_count": 0,
    "trace_hash_match_count": 1440,
    "observation_gap_count": 0,
    "response_gap_count": 0,
    "validation_failure_count": 0,
    "unexplained_gaps": [],
    "run_reports": reports,
  }


def make_expert_run(profile, seed, complete=True):
  transition_count = 24 if complete else 3
  trace = [
    {
      "turn": turn,
      "observation": ["visible observation"],
      "legal_commands": ["hold"],
      "submitted_command": "hold",
      "validation_failures": [],
      "latest_transition": {"state_hash": f"{seed}-{turn}"},
      "done_after_submit": turn == transition_count,
    }
    for turn in range(1, transition_count + 1)
  ]
  run = {
    "profile_name": profile,
    "seed": seed,
    "difficulty": "expert",
    "completion_status": "complete" if complete else "failed",
    "turn_trace": trace,
    "validation_failures": [] if complete else [{"message": "failed"}],
    "transition_count": transition_count,
    "history": [{"state_hash": f"{seed}-{turn}"} for turn in range(1, transition_count + 1)],
    "state_hashes": [f"{seed}-{turn}" for turn in range(1, transition_count + 1)],
    "final_observation": ["final observation"],
    "debrief": ["debrief"],
  }
  if not complete:
    run["run_error"] = "failed"
  return run


def make_expert_source():
  runs = [
    make_expert_run(profile, seed)
    for profile in RUNNER.PROFILES
    for seed in RUNNER.SEEDS
  ]
  return {
    "batch_id": "v0.11.9-expert-difficulty-validation",
    "code_version": "0.11.9",
    "campaign": RUNNER.CAMPAIGN,
    "seeds": RUNNER.SEEDS,
    "difficulty": "expert",
    "profiles": RUNNER.PROFILES,
    "runs": runs,
  }


class Phase7DifficultySynthesisTests(unittest.TestCase):
  def test_accepts_complete_source_contracts(self):
    synthesis = RUNNER.build_synthesis(
      make_strategy_source(),
      make_expert_source(),
    )

    RUNNER.validate_synthesis(synthesis)
    self.assertEqual(synthesis["gap_status"], "no_structural_gap")
    self.assertEqual(synthesis["runtime_promotion"], "deferred")
    self.assertEqual(synthesis["golden_control_hash"], "61357596d8800592")
    self.assertEqual(synthesis["source_artifacts"][1]["run_count"], 15)

  def test_rejects_missing_expert_coordinate(self):
    source = make_expert_source()
    source["runs"] = source["runs"][:-1]

    with self.assertRaises(AssertionError):
      RUNNER.build_synthesis(make_strategy_source(), source)

  def test_rejects_incomplete_expert_trace(self):
    source = make_expert_source()
    source["runs"][0]["turn_trace"][0].pop("latest_transition")

    with self.assertRaises(AssertionError):
      RUNNER.build_synthesis(make_strategy_source(), source)

  def test_rejects_mismatched_campaign(self):
    source = make_expert_source()
    source["campaign"] = "other-campaign"

    with self.assertRaises(AssertionError):
      RUNNER.build_synthesis(make_strategy_source(), source)

  def test_rendering_is_deterministic_and_preserves_source_boundaries(self):
    synthesis = RUNNER.build_synthesis(
      make_strategy_source(),
      make_expert_source(),
    )

    first_json = RUNNER.render_json(synthesis)
    second_json = RUNNER.render_json(json.loads(first_json))
    self.assertEqual(first_json, second_json)
    markdown = RUNNER.render_markdown(synthesis)
    self.assertIn("v0.11.6-strategy-comparison-use-audit", markdown)
    self.assertIn("v0.11.9-expert-difficulty-validation", markdown)
    self.assertIn("No structural gap identified.", markdown)


if __name__ == "__main__":
  unittest.main()
