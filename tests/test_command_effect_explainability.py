import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.47-command-effect-explainability"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("command_effect_audit", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def make_run(commands, events=None, effects=None, status="complete"):
  command_text = "; ".join(commands)
  return {
    "profile_name": "Fixture Policy",
    "seed": 42,
    "completion_status": status,
    "turn_trace": [
      {
        "turn": 1,
        "observation": ["Organization: Riverside Community Health"],
        "submitted_command": command_text,
        "latest_transition": {
          "events": events or [],
          "effects": effects or [],
        },
      }
    ],
    "debrief": [f"Player: {command_text}"],
  }


def make_artifact(run):
  return {
    "campaign": RUNNER.CAMPAIGN,
    "runs": [run],
  }


class CommandEffectExplainabilityTests(unittest.TestCase):
  def test_parse_commands_supports_all_competitive_verbs(self):
    commands = RUNNER.parse_commands(
      "monitor target=northlake depth=1; recruit role=nurse headcount=2; "
      "invest domain=beds amount=5; negotiate payer=medicaid rate_posture=neutral; "
      "commit pledge_type=access level=1; project kind=icu_wing budget=60; hold"
    )

    self.assertEqual(
      [command["verb"] for command in commands],
      ["monitor", "recruit", "invest", "negotiate", "commit", "project", "hold"],
    )

  def test_supported_commands_require_trace_and_debrief_evidence(self):
    run = make_run(
      ["monitor target=northlake depth=1", "invest domain=beds amount=5"],
      events=[
        "health_system: Riverside Community Health: monitoring Northlake at depth 1",
        "health_system: Riverside Community Health: investing 5 in Beds",
      ],
      effects=["capacity investment changed access_index by 2"],
    )

    result = RUNNER.audit_run(run)

    self.assertEqual(result["coverage_status"], "supported")
    self.assertEqual(result["unsupported_commands"], [])
    self.assertEqual(result["missing_debrief_commands"], [])

  def test_unmatched_command_is_retained_with_reason(self):
    run = make_run(["project kind=icu_wing budget=60"], events=["routine month"])

    result = RUNNER.audit_run(run)

    self.assertEqual(result["coverage_status"], "limited")
    self.assertEqual(len(result["unsupported_commands"]), 1)
    self.assertIn("no action-specific", result["unsupported_commands"][0]["reason"])

  def test_hold_is_neutral_and_does_not_require_effect_evidence(self):
    result = RUNNER.audit_run(make_run(["hold"], events=["routine month"]))

    self.assertEqual(result["coverage_status"], "supported")
    self.assertEqual(result["commands"][0]["reason"], "neutral action; no effect required")

  def test_incomplete_runs_are_retained(self):
    result = RUNNER.audit_run(
      make_run(["hold"], status="incomplete")
    )

    self.assertEqual(result["completion_status"], "incomplete")
    self.assertEqual(result["command_count"], 1)

  def test_audit_and_markdown_are_deterministic(self):
    audit = RUNNER.build_audit()
    RUNNER.validate_audit(audit)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(audit["run_count"], 12)
    self.assertEqual(first, second)
    self.assertIn("Evidence limits", first)


if __name__ == "__main__":
  unittest.main()
