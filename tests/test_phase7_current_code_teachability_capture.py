import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.12-phase7-current-code-teachability-capture"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "current_code_teachability_capture",
  RUNNER_PATH,
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_transition(turn):
  return {
    "turn": turn,
    "state_hash": f"hash-{turn}",
    "events": [
      "operations: Riverside Community Health: treated 20/24 demand units; "
      "operating revenue 35, cost 34, margin +1",
      "operations: Northlake Health: treated 30/30 demand units; "
      "operating revenue 50, cost 20, margin +30",
    ],
    "effects": [
      "monthly demand allocation changed monthly_demand by 24",
      "staffed volume resolution changed monthly_treated_volume by 20",
      "capacity shortfall changed monthly_unmet_demand by 4",
      "revenue realization changed monthly_operating_revenue by 35",
      "operating expense changed monthly_operating_cost by 34",
      "monthly operating cycle changed cash by 1",
    ],
  }


def make_run(profile_id, seed, retry=False):
  history = [make_transition(turn) for turn in range(1, 25)]
  trace = []
  for transition in history:
    entry = {
      "turn": transition["turn"],
      "observation": ["Cash runway: stable", "Reported access index: 74"],
      "legal_commands": ["hold", "monitor target=northlake depth=<1-3>"],
      "submitted_command": "hold",
      "validation_failures": [],
      "retry_commands": [],
      "latest_transition": transition,
      "done_after_submit": transition["turn"] == 24,
    }
    if retry and transition["turn"] == 1:
      entry["validation_failures"] = [{
        "turn": 1,
        "command": "monitor target=northlake depth=3",
        "error": "insufficient action points",
      }]
      entry["retry_commands"] = ["hold"]
    trace.append(entry)

  return {
    "profile_id": profile_id,
    "profile_name": f"{profile_id} / hard / seed {seed}",
    "persona_prompt": "Use only actor-visible observations and legal hints.",
    "decision_source": "deterministic observation-driven policy",
    "seed": seed,
    "difficulty": RUNNER.DIFFICULTY,
    "campaign": RUNNER.CAMPAIGN,
    "completion_status": "complete",
    "transition_count": len(history),
    "history": history,
    "state_hashes": [transition["state_hash"] for transition in history],
    "final_hash": history[-1]["state_hash"],
    "turn_trace": trace,
    "commands": ["hold"] * len(trace),
    "validation_failures": [
      failure
      for entry in trace
      for failure in entry["validation_failures"]
    ],
    "retry_count": sum(len(entry["retry_commands"]) for entry in trace),
    "final_observation": ["Session complete."],
    "debrief": [
      *(f"--- Month {turn} ---" for turn in range(1, 25)),
      *("Player: hold" for _ in range(24)),
      "Decision quality and outcome quality remain separate.",
    ],
  }


def make_artifact(retry=False):
  runs = [
    make_run(profile_id, seed, retry=retry)
    for profile_id in RUNNER.PROFILES
    for seed in RUNNER.SEEDS
  ]
  return {
    "artifact_type": RUNNER.ARTIFACT_TYPE,
    "batch_id": RUNNER.BATCH_ID,
    "code_version": RUNNER.EXPECTED_CODE_VERSION,
    "campaign": RUNNER.CAMPAIGN,
    "ruleset": RUNNER.RULESET,
    "state_hash_schema": RUNNER.STATE_HASH_SCHEMA,
    "difficulty": RUNNER.DIFFICULTY,
    "seeds": RUNNER.SEEDS,
    "profiles": RUNNER.PROFILES,
    "runtime_promotion": "deferred",
    "control": {
      "campaign": RUNNER.CAMPAIGN,
      "seed": 42,
      "difficulty": "normal",
      "policy": "hold",
      "first_transition_hash": RUNNER.GOLDEN_CONTROL_HASH,
    },
    "runs": runs,
  }


class CurrentCodeTeachabilityCaptureTests(unittest.TestCase):
  def test_matrix_and_trace_contract_are_supported(self):
    artifact = make_artifact()
    RUNNER.validate_artifact(artifact)
    audit = RUNNER.build_audit(artifact)
    RUNNER.validate_audit(audit)

    self.assertEqual(audit["run_count"], 9)
    self.assertEqual(audit["complete_run_count"], 9)
    self.assertEqual(audit["transition_count"], 216)
    self.assertEqual(audit["runtime_promotion"], "deferred")

  def test_missing_matrix_member_is_rejected(self):
    artifact = make_artifact()
    artifact["runs"].pop()

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_retry_signal_is_preserved_as_supported_evidence(self):
    audit = RUNNER.build_audit(make_artifact(retry=True))

    self.assertEqual(audit["retry_count"], 9)
    self.assertEqual(audit["complete_run_count"], 9)
    self.assertEqual(audit["unexplained_gap_count"], 0)

  def test_rival_operating_events_are_not_player_evidence(self):
    audit = RUNNER.build_audit(make_artifact())

    self.assertEqual(audit["rival_operating_event_count"], 216)
    self.assertEqual(audit["player_operating_month_count"], 216)

  def test_malformed_trace_is_limited(self):
    artifact = make_artifact()
    artifact["runs"][0]["turn_trace"][0] = "malformed"
    audit = RUNNER.build_audit(artifact)

    self.assertEqual(audit["status"], "limited")
    self.assertIn("run validation", {gap["type"] for gap in audit["unexplained_gaps"]})

  def test_short_history_is_limited_without_crashing(self):
    artifact = make_artifact()
    artifact["runs"][0]["history"] = []
    artifact["runs"][0]["state_hashes"] = []
    artifact["runs"][0]["final_hash"] = None

    audit = RUNNER.build_audit(artifact)

    self.assertEqual(audit["status"], "limited")
    self.assertIn("run validation", {gap["type"] for gap in audit["unexplained_gaps"]})

  def test_malformed_retry_field_is_limited_without_crashing(self):
    artifact = make_artifact()
    artifact["runs"][0]["turn_trace"][0]["retry_commands"] = None

    audit = RUNNER.build_audit(artifact)

    self.assertEqual(audit["status"], "limited")
    self.assertIn("run validation", {gap["type"] for gap in audit["unexplained_gaps"]})

  def test_active_streak_uses_month_order(self):
    artifact = make_artifact()
    trace = artifact["runs"][0]["turn_trace"]
    trace[0]["submitted_command"] = "monitor target=northlake depth=1"
    trace[2]["submitted_command"] = "monitor target=northlake depth=1"

    audit = RUNNER.build_audit(artifact)

    self.assertEqual(audit["reports"][0]["longest_active_streak"], 1)

  def test_history_hash_contract_is_rejected(self):
    artifact = make_artifact()
    artifact["runs"][0]["state_hashes"][0] = "wrong-hash"

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_rendering_is_deterministic_and_limited(self):
    audit = RUNNER.build_audit(make_artifact())
    RUNNER.validate_audit(audit)

    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(
      json.loads(json.dumps(audit, sort_keys=True))
    )

    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)
    self.assertIn("not human or classroom evidence", first.lower())


if __name__ == "__main__":
  unittest.main()
