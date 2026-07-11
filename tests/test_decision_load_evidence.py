import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.52-decision-load-evidence"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("decision_load_audit", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class DecisionLoadEvidenceTests(unittest.TestCase):
  def test_source_matrix_and_profile_metrics_are_supported(self):
    audit = RUNNER.build_audit()

    self.assertEqual(audit["status"], "supported")
    self.assertEqual(audit["source_run_count"], 9)
    self.assertEqual(audit["complete_run_count"], 9)
    self.assertEqual(audit["unexplained_gap_count"], 0)
    self.assertEqual(audit["runtime_promotion"], "deferred")

    summaries = audit["profile_summaries"]
    self.assertEqual(
      summaries["fiscal_steward"]["metrics"],
      {
        "action_commands": 5,
        "active_months": 5,
        "hold_commands": 24,
        "max_actions_in_month": 1,
        "multi_action_months": 0,
      },
    )
    self.assertEqual(
      summaries["access_expansion_advocate"]["metrics"],
      {
        "action_commands": 10,
        "active_months": 8,
        "hold_commands": 22,
        "max_actions_in_month": 2,
        "multi_action_months": 2,
      },
    )
    self.assertEqual(
      summaries["first_time_executive"]["metrics"],
      {
        "action_commands": 7,
        "active_months": 7,
        "hold_commands": 24,
        "max_actions_in_month": 1,
        "multi_action_months": 0,
      },
    )

  def test_command_segments_count_actions_and_holds_by_turn(self):
    summary = RUNNER.summarize_run({
      "profile_id": "fixture",
      "profile_name": "Fixture",
      "seed": 42,
      "difficulty": "hard",
      "completion_status": "complete",
      "transition_count": 2,
      "turn_trace": [
        {"turn": 1, "submitted_command": "monitor target=northlake depth=1; hold"},
        {"turn": 2, "submitted_command": "hold"},
      ],
      "validation_failures": [],
      "retry_count": 0,
      "state_hashes": ["one", "two"],
      "debrief": ["fixture"],
    })

    self.assertEqual(summary["action_commands"], 1)
    self.assertEqual(summary["hold_commands"], 2)
    self.assertEqual(summary["active_months"], 1)
    self.assertEqual(summary["multi_action_months"], 0)
    self.assertEqual(summary["max_actions_in_month"], 1)
    self.assertEqual(summary["action_counts_by_month"], [{"turn": 1, "actions": 1}])

  def test_incomplete_and_malformed_runs_are_limited(self):
    incomplete = RUNNER.audit_run(
      {"completion_status": "incomplete", "turn_trace": None},
      "fixture/incomplete.json",
    )
    malformed = RUNNER.audit_run("malformed run", "fixture/malformed.json")

    self.assertEqual(incomplete["status"], "limited")
    self.assertEqual(malformed["status"], "limited")
    self.assertTrue(incomplete["issues"])
    self.assertTrue(malformed["issues"])

  def test_unhashable_identity_fields_remain_limited(self):
    audit = RUNNER.build_audit(source={
      "batch_id": RUNNER.SOURCE_BATCH_ID,
      "code_version": RUNNER.SOURCE_CODE_VERSION,
      "campaign": RUNNER.CAMPAIGN,
      "difficulty": RUNNER.SOURCE_DIFFICULTY,
      "seeds": RUNNER.EXPECTED_SEEDS,
      "runs": [{"profile_id": [], "seed": {}}],
    })

    self.assertEqual(audit["status"], "limited")
    self.assertIn("matrix continuity", {gap["type"] for gap in audit["unexplained_gaps"]})

  def test_source_identity_mismatch_is_limited(self):
    audit = RUNNER.build_audit(source={
      "batch_id": RUNNER.SOURCE_BATCH_ID,
      "code_version": RUNNER.SOURCE_CODE_VERSION,
      "campaign": "wrong-campaign",
      "difficulty": RUNNER.SOURCE_DIFFICULTY,
      "seeds": RUNNER.EXPECTED_SEEDS,
      "runs": [],
    })

    self.assertEqual(audit["status"], "limited")
    self.assertIn("source identity", {gap["type"] for gap in audit["unexplained_gaps"]})
    self.assertEqual(audit["runtime_promotion"], "deferred")

  def test_audit_and_markdown_render_deterministically(self):
    audit = RUNNER.build_audit()
    RUNNER.validate_audit(audit)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)
    self.assertIn("not human or classroom evidence", first.lower())
    self.assertIn("decision-load", first.lower())


if __name__ == "__main__":
  unittest.main()
