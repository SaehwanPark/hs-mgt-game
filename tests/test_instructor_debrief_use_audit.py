import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "_workspace" / "experiments" / "v0.10.45-instructor-debrief-use-audit"
RUNNER_SPEC = importlib.util.spec_from_file_location(
  "instructor_debrief_use_audit_runner",
  EXPERIMENT / "run_audit.py",
)
RUNNER = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(RUNNER)


SOURCE_PATHS = [
  ROOT / "_workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json",
  ROOT / "_workspace/experiments/v0.10.40-consultant-advice-evidence/results.json",
  ROOT / "_workspace/experiments/v0.10.41-consultant-advice-usage/results.json",
  ROOT / "_workspace/experiments/v0.10.43-rival-info-follow-through/results.json",
]


class InstructorDebriefUseAuditTests(unittest.TestCase):
  def test_current_artifacts_cover_all_review_steps(self):
    audit = RUNNER.build_audit(SOURCE_PATHS)

    self.assertEqual(audit["source_count"], 4)
    self.assertEqual(audit["run_count"], 70)
    for artifact in audit["artifacts"]:
      self.assertEqual(
        [step["status"] for step in artifact["review_steps"]],
        ["supported"] * 5,
      )

  def test_missing_trace_is_reported_as_limited(self):
    report = RUNNER.audit_artifact(
      {
        "batch_id": "fixture",
        "runs": [
          {
            "completion_status": "complete",
            "final_hash": "abc",
            "state_hashes": ["abc"],
            "transition_count": 1,
          },
          {
            "completion_status": "complete",
            "commands": ["hold"],
            "debrief": ["completed"],
            "final_hash": "def",
            "state_hashes": ["def"],
            "transition_count": 1,
            "turn_trace": [{"observation": ["visible cue"]}],
          },
        ],
      },
    )

    statuses = {step["name"]: step["status"] for step in report["review_steps"]}
    self.assertEqual(statuses["visibility"], "limited")
    self.assertEqual(statuses["response"], "limited")
    self.assertEqual(statuses["follow-through"], "limited")
    self.assertEqual(statuses["outcome"], "supported")
    self.assertEqual(statuses["explanation"], "limited")

  def test_rendered_audit_is_deterministic_and_bounded(self):
    audit = RUNNER.build_audit(SOURCE_PATHS)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("not causal", first.lower())
    self.assertIn("Visibility", first)
    self.assertIn("Explanation", first)


if __name__ == "__main__":
  unittest.main()
