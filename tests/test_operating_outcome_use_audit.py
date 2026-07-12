import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.5-operating-outcome-use-audit"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "operating_outcome_use_audit", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_transition(
  turn=1,
  demand=24,
  treated=20,
  revenue=35,
  cost=40,
  workforce_event=False,
):
  unmet = demand - treated
  margin = revenue - cost
  events = [
    (
      "operations: Riverside Community Health: treated "
      f"{treated}/{demand} demand units; operating revenue {revenue}, "
      f"cost {cost}, margin {margin:+}"
    )
  ]
  effects = [
    f"monthly demand allocation changed monthly_demand by {demand}",
    f"staffed volume resolution changed monthly_treated_volume by {treated}",
    f"capacity shortfall changed monthly_unmet_demand by {unmet}",
    f"revenue realization changed monthly_operating_revenue by {revenue}",
    f"operating expense changed monthly_operating_cost by {cost}",
    f"monthly operating cycle changed cash by {margin}",
  ]
  if workforce_event:
    events.append(
      "workforce: Riverside Community Health: understaffing creates a "
      "staffing capacity constraint"
    )
  return {
    "turn": turn,
    "state_hash": f"hash-{turn}",
    "events": events,
    "effects": effects,
  }


def operating_result_line(transition):
  event = transition["events"][0]
  values = event.split("treated ", 1)[1]
  treated_demand, rest = values.split(" demand units; operating revenue ", 1)
  treated, demand = treated_demand.split("/", 1)
  revenue, rest = rest.split(", cost ", 1)
  cost, margin = rest.split(", margin ", 1)
  unmet = int(demand) - int(treated)
  return (
    f"Operating result: treated {treated}/{demand} demand units ({unmet} unmet); "
    f"operating revenue {revenue}, operating cost {cost}, "
    f"operating margin {margin}."
  )


def prior_operations_line(transition):
  event = transition["events"][0]
  values = event.split("treated ", 1)[1]
  treated_demand, rest = values.split(" demand units; operating revenue ", 1)
  treated, demand = treated_demand.split("/", 1)
  revenue, rest = rest.split(", cost ", 1)
  cost, margin = rest.split(", margin ", 1)
  unmet = int(demand) - int(treated)
  return (
    f"Prior-month operations: treated {treated}/{demand} demand units "
    f"({unmet} unmet); revenue {revenue}, cost {cost}, margin {margin}"
  )


def make_run(
  transitions=None,
  commands=None,
  observation_overrides=None,
  debrief_overrides=None,
  include_rival=False,
):
  transitions = transitions or [
    make_transition(turn, workforce_event=(turn == 1))
    for turn in range(1, 4)
  ]
  commands = commands or ["hold", "recruit role=nurse headcount=1", "hold"]
  observation_overrides = observation_overrides or {}
  debrief_overrides = debrief_overrides or {}
  turn_trace = []
  debrief = []
  for index, transition in enumerate(transitions):
    turn = transition["turn"]
    if turn == 1:
      prior_line = (
        "Prior-month operations: treated 0/0 demand units "
        "(0 unmet); revenue 0, cost 0, margin +0"
      )
    else:
      prior_line = prior_operations_line(transitions[index - 1])
    prior_line = observation_overrides.get(turn, prior_line)
    turn_trace.append({
      "turn": turn,
      "observation": [
        "Cash runway: WATCH",
        prior_line,
      ],
      "legal_commands": ["hold"],
      "submitted_command": commands[index],
      "validation_failures": [],
      "latest_transition": transition,
    })
    debrief.extend([
      f"--- Month {turn} ---",
      f"Player: {commands[index]}",
      debrief_overrides.get(turn, operating_result_line(transition)),
    ])
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
    "turn_trace": turn_trace,
    "validation_failures": [],
    "debrief": debrief,
  }


class OperatingOutcomeUseAuditTests(unittest.TestCase):
  def test_real_matrix_matches_use_contract(self):
    artifact_path = RUNNER_PATH.parent.parent.parent.parent / "_workspace" / "experiments" / "v0.11.4-operating-outcome-debrief-validation" / "capture.json"
    artifact = RUNNER.load_artifact(artifact_path)
    audit = RUNNER.build_audit(artifact)

    RUNNER.validate_audit(audit)
    self.assertEqual(audit["run_count"], 60)
    self.assertEqual(audit["transition_count"], 1440)
    self.assertEqual(audit["initial_baseline_count"], 60)
    self.assertEqual(audit["prior_observation_match_count"], 1380)
    self.assertEqual(audit["response_opportunity_count"], 441)
    self.assertEqual(audit["terminal_signal_count"], 28)
    self.assertEqual(audit["debrief_outcome_match_count"], 1440)

  def test_prior_month_alignment_and_signal_response_are_reported(self):
    report = RUNNER.audit_run(make_run())

    self.assertEqual(report["initial_baseline_count"], 1)
    self.assertEqual(report["prior_observation_match_count"], 2)
    self.assertEqual(report["observation_gap_count"], 0)
    self.assertEqual(report["response_opportunity_count"], 5)
    self.assertEqual(report["response_gap_count"], 0)
    self.assertEqual(report["signal_to_command_counts"]["operating_loss"]["recruit"], 1)

  def test_terminal_signal_is_not_a_missing_response(self):
    transitions = [
      make_transition(1, demand=24, treated=24, revenue=42, cost=34),
      make_transition(2, demand=24, treated=24, revenue=42, cost=34),
      make_transition(3, demand=24, treated=10, revenue=20, cost=40),
    ]
    report = RUNNER.audit_run(make_run(transitions=transitions))

    self.assertGreater(report["terminal_signal_count"], 0)
    self.assertEqual(report["response_gap_count"], 0)

  def test_observation_mismatch_is_reported(self):
    run = make_run(observation_overrides={2: "Prior-month operations: malformed"})

    report = RUNNER.audit_run(run)

    self.assertEqual(report["observation_gap_count"], 1)
    self.assertEqual(report["prior_observation_match_count"], 1)

  def test_debrief_mismatch_is_reported(self):
    run = make_run(debrief_overrides={2: "Operating result: treated 1/1 demand units (0 unmet); operating revenue 1, operating cost 1, operating margin +0."})

    report = RUNNER.audit_run(run)

    self.assertEqual(report["debrief_outcome_gap_count"], 1)
    self.assertEqual(report["debrief_outcome_match_count"], 2)

  def test_rival_operating_result_is_not_player_linkage(self):
    report = RUNNER.audit_run(make_run(include_rival=True))

    self.assertEqual(report["debrief_outcome_match_count"], 3)
    self.assertEqual(report["rival_operating_result_count"], 1)

  def test_multi_action_command_is_labeled_without_losing_the_trace(self):
    commands = ["hold", "recruit role=nurse headcount=1; hold", "hold"]

    report = RUNNER.audit_run(make_run(commands=commands))

    self.assertEqual(report["multi_action_command_count"], 1)
    self.assertEqual(report["unknown_command_count"], 0)

  def test_rendering_is_deterministic(self):
    audit = RUNNER.build_audit(RUNNER.make_minimal_artifact(make_run()))

    first = RUNNER.render_json(audit)
    second = RUNNER.render_json(json.loads(first))

    self.assertEqual(first, second)
    self.assertIn("response opportunities", RUNNER.render_markdown(audit))


if __name__ == "__main__":
  unittest.main()
