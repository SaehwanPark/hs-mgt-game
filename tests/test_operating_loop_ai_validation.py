import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.1-operating-loop-ai-validation"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("operating_loop_ai_validation", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_transition(turn=1, demand=24, treated=20, revenue=35, cost=34):
  unmet = demand - treated
  margin = revenue - cost
  return {
    "turn": turn,
    "state_hash": f"hash-{turn}",
    "events": [
      (
        "operations: Riverside Community Health: treated "
        f"{treated}/{demand} demand units; operating revenue {revenue}, "
        f"cost {cost}, margin {margin:+}"
      )
    ],
    "effects": [
      f"monthly demand allocation changed monthly_demand by {demand}",
      f"staffed volume resolution changed monthly_treated_volume by {treated}",
      f"capacity shortfall changed monthly_unmet_demand by {unmet}",
      f"revenue realization changed monthly_operating_revenue by {revenue}",
      f"operating expense changed monthly_operating_cost by {cost}",
      f"monthly operating cycle changed cash by {margin}",
    ],
  }


def make_run(profile="Access First", seed=42, difficulty="normal"):
  transitions = [make_transition(turn) for turn in range(1, 4)]
  return {
    "profile": profile,
    "seed": seed,
    "difficulty": difficulty,
    "campaign": RUNNER.CAMPAIGN,
    "completion_status": "complete",
    "transition_count": len(transitions),
    "history": transitions,
    "turn_trace": [
      {
        "turn": transition["turn"],
        "observation": ["Available resources: AP 3, cash 60, political capital 10"],
        "legal_commands": ["hold"],
        "submitted_command": "hold",
        "validation_failures": [],
        "latest_transition": transition,
      }
      for transition in transitions
    ],
    "validation_failures": [],
    "final_observation": ["Session complete."],
    "debrief": [
      "Final player tradeoff: Riverside Community Health cash moved from 60 to 63.",
      "Decision quality and outcome quality remain separate.",
    ]
    + [line for turn in range(1, 4) for line in (f"--- Month {turn} ---", "Player: hold")],
  }


def make_artifact():
  runs = [
    make_run(profile, seed, difficulty)
    for profile in RUNNER.PROFILES
    for seed in RUNNER.SEEDS
    for difficulty in RUNNER.DIFFICULTIES
  ]
  return {
    "artifact_type": RUNNER.ARTIFACT_TYPE,
    "batch_id": RUNNER.BATCH_ID,
    "code_version": RUNNER.CODE_VERSION,
    "campaign": RUNNER.CAMPAIGN,
    "seeds": RUNNER.SEEDS,
    "difficulties": RUNNER.DIFFICULTIES,
    "profiles": RUNNER.PROFILES,
    "runs": runs,
  }


class OperatingLoopAiValidationTests(unittest.TestCase):
  def test_parse_operating_transition_reconstructs_accounting(self):
    parsed = RUNNER.parse_operating_transition(make_transition())

    self.assertEqual(parsed["demand"], 24)
    self.assertEqual(parsed["treated"], 20)
    self.assertEqual(parsed["unmet"], 4)
    self.assertEqual(parsed["revenue"], 35)
    self.assertEqual(parsed["cost"], 34)
    self.assertEqual(parsed["margin"], 1)
    self.assertEqual(parsed["cash_delta"], 1)
    self.assertEqual(parsed["accounting_status"], "supported")

  def test_tampered_operating_effect_is_limited(self):
    transition = make_transition()
    transition["effects"][-1] = "monthly operating cycle changed cash by 99"

    parsed = RUNNER.parse_operating_transition(transition)

    self.assertEqual(parsed["accounting_status"], "limited")
    self.assertTrue(parsed["evidence_gaps"])

  def test_matrix_and_markdown_are_deterministic(self):
    artifact = make_artifact()
    audit = RUNNER.build_audit(artifact)
    RUNNER.validate_audit(audit)

    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(audit["run_count"], 60)
    self.assertEqual(audit["completed_run_count"], 60)
    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)

  def test_missing_matrix_member_is_rejected(self):
    artifact = make_artifact()
    artifact["runs"].pop()
    audit = RUNNER.build_audit(artifact)

    with self.assertRaises(AssertionError):
      RUNNER.validate_audit(audit)

  def test_malformed_trace_is_limited(self):
    artifact = make_artifact()
    artifact["runs"][0]["turn_trace"][0] = "malformed"

    audit = RUNNER.build_audit(artifact)

    self.assertLess(audit["explanation_supported_run_count"], audit["run_count"])

  def test_rival_operating_event_is_not_accepted_as_player_evidence(self):
    artifact = make_artifact()
    artifact["runs"][0]["history"][0]["events"].append(
      "operations: Northlake Health: treated 30/30 demand units; operating revenue 50, cost 20, margin +30"
    )

    audit = RUNNER.build_audit(artifact)

    self.assertEqual(audit["rival_operating_event_count"], 1)
    self.assertEqual(audit["runtime_promotion"], "deferred")


if __name__ == "__main__":
  unittest.main()
