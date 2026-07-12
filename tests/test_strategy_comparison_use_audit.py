import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.6-strategy-comparison-use-audit"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "strategy_comparison_use_audit",
  RUNNER_PATH,
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_transition(turn=1, demand=24, treated=20, revenue=35, cost=40):
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


def make_run(
  profile="Access First",
  seed=42,
  difficulty="normal",
  commands=None,
  include_signal=True,
  include_debrief=True,
  status="complete",
  validation_failure=False,
):
  commands = commands or [
    "recruit role=nurse headcount=1",
    "invest domain=beds amount=5; hold",
    "hold",
  ]
  history = [
    make_transition(
      turn,
      treated=24 if turn == 1 else 24,
      revenue=35 if turn == 1 else 42,
      cost=40 if turn == 1 else 34,
    )
    for turn in range(1, len(commands) + 1)
  ]
  trace = []
  debrief = []
  for index, transition in enumerate(history):
    turn = transition["turn"]
    observation = [
      "Available resources: AP 3, cash 60, political capital 15",
    ]
    if turn == 1:
      observation.append(
        "Prior-month operations: treated 0/0 demand units "
        "(0 unmet); revenue 0, cost 0, margin +0"
      )
    if include_signal and turn > 1:
      previous = history[index - 1]
      prior_values = previous["events"][0].split("treated ", 1)[1]
      prior_treated_demand, prior_rest = prior_values.split(
        " demand units; operating revenue ", 1
      )
      prior_treated, prior_demand = prior_treated_demand.split("/", 1)
      prior_revenue, prior_rest = prior_rest.split(", cost ", 1)
      prior_cost, prior_margin = prior_rest.split(", margin ", 1)
      observation.append(
        f"Prior-month operations: treated {prior_treated}/{prior_demand} "
        f"demand units ({int(prior_demand) - int(prior_treated)} unmet); "
        f"revenue {prior_revenue}, cost {prior_cost}, margin {prior_margin}"
      )
    trace.append({
      "turn": turn,
      "observation": observation,
      "submitted_command": commands[index],
      "latest_transition": transition,
      "validation_failures": [],
    })
    if include_debrief:
      values = transition["events"][0].split("treated ", 1)[1]
      treated_demand, rest = values.split(" demand units; operating revenue ", 1)
      treated, demand = treated_demand.split("/", 1)
      revenue, rest = rest.split(", cost ", 1)
      cost, margin = rest.split(", margin ", 1)
      debrief.extend([
        f"--- Month {turn} ---",
        f"Player: {commands[index]}",
        (
          f"Operating result: treated {treated}/{demand} demand units "
          f"({int(demand) - int(treated)} unmet); operating revenue {revenue}, "
          f"operating cost {cost}, operating margin {margin}."
        ),
      ])
  return {
    "profile": profile,
    "seed": seed,
    "difficulty": difficulty,
    "campaign": RUNNER.CAMPAIGN,
    "completion_status": status,
    "transition_count": len(history),
    "history": history,
    "state_hashes": [transition["state_hash"] for transition in history],
    "turn_trace": trace,
    "debrief": debrief,
    "validation_failures": [{"message": "expected probe"}]
    if validation_failure else [],
  }


class StrategyComparisonUseAuditTests(unittest.TestCase):
  def test_command_family_preserves_ordered_multi_action_commands(self):
    self.assertEqual(
      RUNNER.command_families(
        "monitor target=northlake depth=1; invest domain=beds amount=5; hold"
      ),
      ["monitor:northlake", "invest:beds", "hold"],
    )

  def test_audit_reports_signal_response_and_debrief_contract(self):
    report = RUNNER.audit_run(make_run())

    self.assertEqual(report["status"], "supported")
    self.assertEqual(report["transition_count"], 3)
    self.assertEqual(report["operating_outcome_match_count"], 3)
    self.assertEqual(report["response_opportunity_count"], 1)
    self.assertEqual(
      report["signal_to_command_counts"]["operating_loss"]["multi_action"],
      1,
    )
    self.assertEqual(report["multi_action_command_count"], 1)

  def test_terminal_signal_is_not_a_missing_response(self):
    report = RUNNER.audit_run(
      make_run(commands=["hold"], include_signal=True)
    )

    self.assertEqual(report["response_opportunity_count"], 0)
    self.assertEqual(report["response_gap_count"], 0)
    self.assertEqual(report["terminal_signal_count"], 1)

  def test_unknown_command_is_limited_and_preserved(self):
    report = RUNNER.audit_run(
      make_run(commands=["unknown_command"], include_signal=False)
    )

    self.assertEqual(report["status"], "limited")
    self.assertEqual(report["unknown_command_count"], 1)

  def test_missing_debrief_is_limited(self):
    report = RUNNER.audit_run(make_run(include_debrief=False))

    self.assertEqual(report["status"], "limited")
    self.assertEqual(report["debrief_gap_count"], 3)

  def test_validation_failure_is_limited_and_reported(self):
    report = RUNNER.audit_run(make_run(validation_failure=True))

    self.assertEqual(report["status"], "limited")
    self.assertEqual(report["validation_failure_count"], 1)

  def test_profile_summary_and_matrix_validation(self):
    artifact = RUNNER.make_minimal_artifact(make_run())
    audit = RUNNER.build_audit(artifact)

    RUNNER.validate_audit(audit)
    self.assertEqual(audit["run_count"], 60)
    self.assertEqual(audit["transition_count"], 180)
    self.assertIn("Access First", audit["profile_summary"])
    self.assertIn("normal", audit["difficulty_summary"])

    audit["run_reports"] = audit["run_reports"][:-1]
    audit["run_count"] -= 1
    with self.assertRaises(AssertionError):
      RUNNER.validate_audit(audit)

  def test_rendering_is_deterministic(self):
    audit = RUNNER.build_audit(
      RUNNER.make_minimal_artifact(make_run())
    )
    RUNNER.validate_audit(audit)

    first_json = RUNNER.render_json(audit)
    second_json = RUNNER.render_json(json.loads(first_json))
    self.assertEqual(first_json, second_json)
    self.assertIn("Promotion decision", RUNNER.render_markdown(audit))


if __name__ == "__main__":
  unittest.main()
