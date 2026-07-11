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
  / "v0.11.2-operating-loss-explainability"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "operating_loss_explainability", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_transition(
  turn=1,
  demand=24,
  treated=24,
  revenue=30,
  cost=35,
  workforce=False,
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
  if workforce:
    events.append(
      "operations: Riverside Community Health: staffing capacity constraint "
      "reduces operational capacity"
    )
  return {
    "turn": turn,
    "state_hash": f"hash-{turn}",
    "events": events,
    "effects": effects,
  }


def make_run(transitions=None, include_month_outcome=False):
  transitions = transitions or [make_transition()]
  trace = []
  for transition in transitions:
    trace.append({
      "turn": transition["turn"],
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

  debrief = []
  for transition in transitions:
    debrief.extend([
      f"--- Month {transition['turn']} ---",
      "Player: hold",
      "Consultant options shown: A — Defensive capacity",
      "Advisory comparison: none is marked correct.",
    ])
    if include_month_outcome:
      debrief.append("Operating result: treated 24/24 demand units; margin +8")
  debrief.extend([
    "Attributed mechanisms to inspect: monthly operating cycle changed cash by 8",
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


def make_artifact(runs=None):
  return {
    "artifact_type": RUNNER.SOURCE_ARTIFACT_TYPE,
    "batch_id": RUNNER.SOURCE_BATCH_ID,
    "code_version": "0.11.1",
    "campaign": RUNNER.CAMPAIGN,
    "ruleset": "competitive-ruleset-0.2.0",
    "state_hash_schema": "competitive-state-hash-v9",
    "seeds": [42],
    "difficulties": ["normal"],
    "profiles": ["Access First"],
    "runs": runs or [make_run()],
  }


class OperatingLossExplainabilityTests(unittest.TestCase):
  def test_signal_categories_and_trace_markers_are_separate(self):
    transitions = [
      make_transition(turn=1, revenue=30, cost=35),
      make_transition(turn=2, demand=25, treated=20, revenue=42, cost=34),
      make_transition(turn=3, revenue=30, cost=35, workforce=True),
    ]
    audit = RUNNER.build_audit(make_artifact([make_run(transitions)]))

    self.assertEqual(
      audit["candidate_signal_counts"],
      {"capacity_or_demand": 1, "operating_loss": 2, "workforce_capacity": 1},
    )
    self.assertEqual(audit["candidate_signal_count"], 4)
    self.assertEqual(audit["decision_context_supported_count"], 4)
    self.assertEqual(audit["transition_attribution_supported_count"], 4)

  def test_global_debrief_summary_is_not_month_level_outcome_evidence(self):
    audit = RUNNER.build_audit(make_artifact([make_run()]))
    report = audit["run_reports"][0]

    self.assertEqual(report["month_debrief_outcome_link_count"], 0)
    self.assertTrue(report["global_debrief_attribution_present"])
    self.assertEqual(audit["global_debrief_attribution_run_count"], 1)

  def test_month_level_outcome_marker_is_counted_when_present(self):
    audit = RUNNER.build_audit(
      make_artifact([make_run(include_month_outcome=True)])
    )
    report = audit["run_reports"][0]

    self.assertEqual(report["month_debrief_outcome_link_count"], 1)

  def test_missing_actor_context_is_limited_without_raw_trace_output(self):
    run = make_run()
    run["turn_trace"][0]["observation"] = ["Workforce trust: moderate"]
    audit = RUNNER.build_audit(make_artifact([run]))

    report = audit["run_reports"][0]
    self.assertEqual(report["decision_context_limited_count"], 1)
    self.assertIn("missing_cash_runway", report["limited_reasons"])
    self.assertNotIn("Cash runway", json.dumps(audit["limited_records"]))

  def test_rival_operating_event_is_counted_but_not_copied(self):
    transition = make_transition()
    transition["events"].append(
      "operations: Northlake Health: treated 30/30 demand units; "
      "operating revenue 50, cost 20, margin +30"
    )
    audit = RUNNER.build_audit(make_artifact([make_run([transition])]))

    self.assertEqual(audit["rival_operating_event_count"], 1)
    self.assertNotIn("Northlake", json.dumps(audit["limited_records"]))

  def test_trace_transition_mismatch_limits_attribution(self):
    run = make_run()
    run["turn_trace"][0]["latest_transition"] = copy.deepcopy(
      run["turn_trace"][0]["latest_transition"]
    )
    run["turn_trace"][0]["latest_transition"]["state_hash"] = "wrong-hash"
    audit = RUNNER.build_audit(make_artifact([run]))

    report = audit["run_reports"][0]
    self.assertEqual(report["transition_attribution_limited_count"], 1)
    self.assertIn("trace_transition_mismatch", report["limited_reasons"])

  def test_real_v0111_source_matches_documented_matrix(self):
    source = RUNNER.load_source_artifact()
    audit = RUNNER.build_audit(source)
    RUNNER.validate_audit(audit)

    self.assertEqual(audit["run_count"], 60)
    self.assertEqual(audit["transition_count"], 1440)
    self.assertEqual(audit["candidate_signal_count"], 469)
    self.assertEqual(
      audit["candidate_signal_counts"],
      {"capacity_or_demand": 140, "operating_loss": 269, "workforce_capacity": 60},
    )
    self.assertEqual(audit["month_debrief_outcome_link_count"], 0)
    self.assertEqual(audit["global_debrief_attribution_run_count"], 60)

  def test_rendering_is_deterministic(self):
    audit = RUNNER.build_audit(make_artifact([make_run()]))

    first = RUNNER.render_json(audit)
    second = RUNNER.render_json(json.loads(first))

    self.assertEqual(first, second)
    self.assertIn(
      "month-level debrief outcome linkage",
      RUNNER.render_markdown(audit).casefold(),
    )


if __name__ == "__main__":
  unittest.main()
