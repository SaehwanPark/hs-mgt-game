import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.4-operating-outcome-debrief-validation"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "operating_outcome_debrief_validation", RUNNER_PATH
)
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


def make_run(transitions=None, missing_outcome_turns=(), include_rival=False):
  transitions = transitions or [make_transition(turn) for turn in range(1, 4)]
  trace = []
  debrief = []
  for transition in transitions:
    turn = transition["turn"]
    trace.append({
      "turn": turn,
      "observation": [
        "Cash runway: WATCH",
        "Workforce trust: moderate",
        "Prior-month operations: treated 0/0 demand units (0 unmet); revenue 0, cost 0, margin +0",
        "In-flight projects: none",
        "Policy: Labor market note: recruitment resolves after delays",
      ],
      "legal_commands": ["hold"],
      "submitted_command": "hold",
      "validation_failures": [],
      "latest_transition": transition,
    })
    debrief.extend([
      f"--- Month {turn} ---",
      "Player: hold",
    ])
    if turn not in missing_outcome_turns:
      debrief.append(
        f"Operating result: treated {transition['events'][0].split('treated ')[1]}"
      )
  if include_rival:
    debrief.append(
      "Operating result: Northlake Health treated 99/99 demand units; "
      "operating revenue 999, operating cost 1, operating margin +998."
    )
  debrief.extend([
    "Attributed mechanisms to inspect: monthly operating cycle changed cash by 1",
    "Resolved events: environment: Routine month.",
  ])
  return {
    "profile": "Access First",
    "seed": 42,
    "difficulty": "normal",
    "campaign": RUNNER.CAMPAIGN,
    "completion_status": "complete",
    "transition_count": len(transitions),
    "history": transitions,
    "turn_trace": trace,
    "validation_failures": [],
    "debrief": debrief,
  }


def make_artifact(run=None):
  run = run or make_run()
  return {
    "artifact_type": RUNNER.ARTIFACT_TYPE,
    "batch_id": RUNNER.BATCH_ID,
    "code_version": RUNNER.CODE_VERSION,
    "campaign": RUNNER.CAMPAIGN,
    "ruleset": RUNNER.RULESET,
    "state_hash_schema": RUNNER.STATE_HASH_SCHEMA,
    "seeds": [42],
    "difficulties": ["normal"],
    "profiles": ["Access First"],
    "runs": [run],
  }


class OperatingOutcomeDebriefValidationTests(unittest.TestCase):
  def test_real_matrix_matches_post_v0113_contract(self):
    artifact_path = RUNNER_PATH.with_name("capture.json")
    audit = RUNNER.build_audit(RUNNER.load_artifact(artifact_path))

    RUNNER.validate_audit(audit)
    self.assertEqual(audit["run_count"], 60)
    self.assertEqual(audit["transition_count"], 1440)
    self.assertEqual(audit["month_debrief_outcome_link_count"], 469)

  def test_missing_month_outcome_is_reported(self):
    run = make_run(missing_outcome_turns={2})
    audit = RUNNER.build_audit(make_artifact(run))

    self.assertEqual(audit["month_count"], 3)
    self.assertEqual(audit["month_debrief_outcome_link_count"], 2)
    self.assertEqual(audit["missing_month_outcome_count"], 1)
    self.assertEqual(audit["runtime_promotion"], "deferred")

  def test_debrief_month_alignment_is_required(self):
    run = make_run()
    run["debrief"] = run["debrief"][:3]
    audit = RUNNER.build_audit(make_artifact(run))

    self.assertEqual(audit["debrief_alignment_mismatch_count"], 1)
    with self.assertRaises(AssertionError):
      RUNNER.validate_audit(audit)

  def test_rival_operating_result_is_not_player_linkage(self):
    run = make_run(include_rival=True)
    audit = RUNNER.build_audit(make_artifact(run))

    self.assertEqual(audit["month_debrief_outcome_link_count"], 3)
    self.assertEqual(audit["rival_operating_result_count"], 1)
    self.assertEqual(audit["player_operating_result_count"], 3)

  def test_matrix_validation_rejects_duplicate_coordinates(self):
    artifact = make_artifact()
    artifact["runs"] = [make_run(), make_run()]
    audit = RUNNER.build_audit(artifact)

    with self.assertRaises(AssertionError):
      RUNNER.validate_audit(audit)

  def test_rendering_is_deterministic(self):
    audit = RUNNER.build_audit(make_artifact())

    first = RUNNER.render_json(audit)
    second = RUNNER.render_json(json.loads(first))

    self.assertEqual(first, second)
    self.assertIn("Month-level operating-outcome linkage", RUNNER.render_markdown(audit))


if __name__ == "__main__":
  unittest.main()
