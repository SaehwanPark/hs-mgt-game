import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.48-strategy-diversity-evidence"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("strategy_diversity_audit", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_run(profile="Fiscal Caution", seed=42, status="complete"):
  trace = [
    {
      "turn": 1,
      "submitted_command": "monitor target=northlake depth=1; hold",
      "latest_transition": {},
    },
    {
      "turn": 2,
      "submitted_command": "invest domain=beds amount=5",
      "latest_transition": {},
    },
  ]
  run = {
    "profile_name": profile,
    "seed": seed,
    "difficulty": "expert",
    "completion_status": status,
    "transition_count": len(trace),
    "validation_failures": [],
    "turn_trace": trace,
    "debrief": [
      "Player: monitor target=northlake depth=1; hold",
      "Player: invest domain=beds amount=5",
      "Final player tradeoff: Riverside Community Health cash moved from 60 to 5, access from 68 to 75, quality from 72 to 77, workforce trust from 60 to 57, community trust from 64 to 66, and market share from 24 to 24.",
    ],
  }
  if status == "failed":
    run["run_error"] = "fixture failure"
  return run


def make_artifact():
  runs = [
    make_run(profile, seed)
    for profile in RUNNER.EXPECTED_PROFILES
    for seed in RUNNER.EXPECTED_SEEDS
  ]
  return {
    "campaign": RUNNER.CAMPAIGN,
    "profiles": RUNNER.EXPECTED_PROFILES,
    "seeds": RUNNER.EXPECTED_SEEDS,
    "difficulty": "expert",
    "runs": runs,
  }


class StrategyDiversityEvidenceTests(unittest.TestCase):
  def test_parse_commands_normalizes_action_families(self):
    commands = RUNNER.parse_commands(
      "monitor target=northlake depth=1; recruit role=nurse headcount=2; "
      "invest domain=beds amount=5; negotiate payer=medicaid rate_posture=neutral; "
      "commit pledge_type=access level=1; project kind=icu_wing budget=60; hold"
    )

    self.assertEqual(
      [command["family"] for command in commands],
      [
        "monitor:northlake",
        "recruit:nurse",
        "invest:beds",
        "negotiate:medicaid",
        "commit:access",
        "project:icu_wing",
        "hold",
      ],
    )

  def test_audit_preserves_incomplete_and_unknown_records(self):
    run = make_run(status="incomplete")
    run["turn_trace"][0]["submitted_command"] = "unknown_command"

    result = RUNNER.audit_run(run)

    self.assertEqual(result["completion_status"], "incomplete")
    self.assertEqual(result["status"], "limited")
    self.assertEqual(result["unknown_commands"][0]["verb"], "unknown")

  def test_audit_extracts_tradeoff_and_trajectory_data(self):
    result = RUNNER.audit_run(make_run())

    self.assertEqual(result["distinct_action_family_count"], 3)
    self.assertEqual(result["first_turn_families"], ["monitor:northlake", "hold"])
    self.assertEqual(result["final_tradeoff"]["access"], 75)
    self.assertEqual(result["hold_rate"], 0.3333)

  def test_validation_rejects_missing_matrix_member(self):
    audit = RUNNER.build_audit()
    audit["runs"] = audit["runs"][:-1]
    audit["run_count"] -= 1

    with self.assertRaises(AssertionError):
      RUNNER.validate_audit(audit)

  def test_audit_and_markdown_are_deterministic(self):
    audit = RUNNER.build_audit()
    RUNNER.validate_audit(audit)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertEqual(audit["run_count"], 12)
    self.assertGreater(audit["distinct_trajectory_count"], 1)
    self.assertIn("candidate common-action signal", first)


if __name__ == "__main__":
  unittest.main()
