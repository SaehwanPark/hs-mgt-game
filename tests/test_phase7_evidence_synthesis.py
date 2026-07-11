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
  / "v0.10.53-evidence-synthesis"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("phase7_evidence_synthesis", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class Phase7EvidenceSynthesisTests(unittest.TestCase):
  def test_current_sources_are_continuous_without_runtime_promotion(self):
    audit = RUNNER.build_audit()

    self.assertEqual(audit["source_count"], 3)
    self.assertEqual(audit["completed_source_count"], 3)
    self.assertEqual(audit["source_coverage"]["status"], "supported")
    self.assertEqual(audit["control_continuity"]["status"], "supported")
    self.assertEqual(audit["matrix_continuity"]["status"], "supported")
    self.assertEqual(audit["evidence_gap_count"], 0)
    self.assertEqual(audit["runtime_promotion"], "deferred")

  def test_current_audit_satisfies_its_validation_contract(self):
    audit = RUNNER.build_audit()

    RUNNER.validate_audit(audit)
    self.assertEqual(
      {report["batch_id"] for report in audit["source_reports"]},
      set(RUNNER.EXPECTED_BATCHES),
    )

  def test_missing_source_is_explicit_evidence_gap(self):
    audit = RUNNER.build_audit(RUNNER.SOURCE_PATHS[:-1])

    self.assertEqual(audit["runtime_promotion"], "deferred")
    self.assertGreater(audit["evidence_gap_count"], 0)
    self.assertIn(
      "source coverage",
      {gap["type"] for gap in audit["evidence_gaps"]},
    )

  def test_malformed_source_is_limited_without_becoming_supported(self):
    report = RUNNER.audit_source(
      {
        "batch_id": "v0.10.50-teachability-observation-capture",
        "code_version": "0.10.50",
        "campaign": RUNNER.CAMPAIGN,
        "runs": [{"completion_status": "incomplete"}, "malformed run"],
      },
      "fixture/results.json",
    )

    self.assertEqual(report["status"], "limited")
    self.assertIn("run completeness", report["limited_dimensions"])

  def test_source_identity_mismatch_is_limited(self):
    report = RUNNER.audit_source(
      {
        "batch_id": "v0.10.51-adversarial-resource-probe",
        "code_version": "0.10.51",
        "campaign": "wrong-campaign",
        "runs": [],
      },
      "fixture/results.json",
    )

    self.assertEqual(report["status"], "limited")

  def test_non_object_sources_do_not_crash_continuity_checks(self):
    self.assertEqual(
      RUNNER._control_continuity([[], {}])["status"],
      "limited",
    )
    self.assertEqual(
      RUNNER._matrix_continuity([[], {}])["status"],
      "limited",
    )

  def test_markdown_rendering_is_deterministic_and_bounded(self):
    audit = RUNNER.build_audit()

    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(copy.deepcopy(audit), sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)
    self.assertIn("control continuity", first.lower())
    self.assertIn("not human or classroom evidence", first.lower())


if __name__ == "__main__":
  unittest.main()
