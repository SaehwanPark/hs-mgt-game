import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.49-teachability-gate-synthesis"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("teachability_gate_audit", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class TeachabilityGateSynthesisTests(unittest.TestCase):
  def test_current_artifacts_close_the_evidence_gate_without_runtime_promotion(self):
    audit = RUNNER.build_audit()

    self.assertEqual(audit["source_count"], 4)
    self.assertEqual(audit["completed_source_count"], 4)
    self.assertEqual(audit["matrix_continuity"]["status"], "supported")
    self.assertEqual(audit["unexplained_gap_count"], 0)
    self.assertEqual(audit["runtime_promotion"], "deferred")

  def test_missing_dimension_is_reported_as_limited(self):
    report = RUNNER.audit_source(
      {
        "batch_id": "fixture",
        "code_version": "0.10.49",
        "campaign": RUNNER.CAMPAIGN,
        "runs": [
          {
            "completion_status": "complete",
            "turn_trace": [{"submitted_command": "hold"}],
          }
        ],
      },
      "fixture/results.json",
    )

    self.assertEqual(report["status"], "limited")
    self.assertIn("explanation", report["limited_dimensions"])
    self.assertIn("outcome", report["limited_dimensions"])

  def test_incomplete_and_malformed_records_remain_limited(self):
    report = RUNNER.audit_source(
      {
        "batch_id": "fixture",
        "code_version": "0.10.49",
        "campaign": RUNNER.CAMPAIGN,
        "runs": [
          {
            "completion_status": "incomplete",
            "turn_trace": None,
          },
          "malformed run",
        ],
      },
      "fixture/results.json",
    )

    self.assertEqual(report["status"], "limited")
    self.assertIn("visibility", report["limited_dimensions"])

  def test_endpoint_differences_do_not_create_a_runtime_promotion(self):
    audit = RUNNER.build_audit()

    self.assertEqual(audit["runtime_promotion"], "deferred")
    self.assertIn("not causal", audit["promotion_basis"].lower())
    self.assertEqual(audit["unexplained_gap_count"], 0)

  def test_missing_source_and_matrix_member_are_explicit_gaps(self):
    audit = RUNNER.build_audit(RUNNER.SOURCE_PATHS[:-1])

    self.assertEqual(audit["runtime_promotion"], "deferred")
    self.assertEqual(
      {gap["type"] for gap in audit["unexplained_gaps"]},
      {"source coverage", "matrix continuity"},
    )

  def test_audit_and_markdown_are_deterministic_and_bounded(self):
    audit = RUNNER.build_audit()
    RUNNER.validate_audit(audit)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)
    self.assertIn("command-to-effect traceability", first)
    self.assertIn("not human or classroom evidence", first.lower())


if __name__ == "__main__":
  unittest.main()
