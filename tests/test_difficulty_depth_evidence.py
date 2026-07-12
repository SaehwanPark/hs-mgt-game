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
  / "v0.12.4-difficulty-depth-evidence"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("difficulty_depth_evidence", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


def load_source(source_id):
  path = {
    "all_tiers": RUNNER.ALL_TIER_PATH,
    "expert": RUNNER.EXPERT_PATH,
  }[source_id]
  return RUNNER.load_artifact(ROOT / path)


class DifficultyDepthEvidenceTests(unittest.TestCase):
  def test_review_covers_all_tier_and_expert_sources(self):
    report = RUNNER.build_report()
    RUNNER.validate_report(report)

    self.assertEqual(report["aggregate"]["run_count"], 75)
    self.assertEqual(report["aggregate"]["supported_run_count"], 75)
    self.assertEqual(report["aggregate"]["transition_count"], 1800)
    self.assertEqual(report["pressure_signal"]["classification"], "candidate_visible_pressure_signal")
    self.assertEqual(report["clearability"]["standalone_expert_runs"], 15)

  def test_workforce_pressure_summary_is_source_derived(self):
    report = RUNNER.build_report()
    self.assertEqual(
      report["pressure_signal"]["all_tier_counts"],
      {"easy": 0, "normal": 15, "hard": 30, "expert": 160},
    )
    self.assertTrue(report["pressure_signal"]["monotonic_easy_to_expert"])
    self.assertTrue(report["aggregate"]["source_version_mismatch"])

  def test_non_monotonic_pressure_is_not_promoted(self):
    classification, monotonic = RUNNER.classify_pressure_signal(
      [0, 30, 15, 160],
      True,
    )

    self.assertFalse(monotonic)
    self.assertEqual(classification, "no_candidate_signal")

  def test_malformed_source_identity_is_rejected(self):
    artifact = load_source("all_tiers")
    artifact["batch_id"] = "wrong-batch"

    with self.assertRaises(AssertionError):
      RUNNER.audit_all_tier(artifact)

  def test_incomplete_expert_trace_is_reported(self):
    artifacts = {
      "all_tiers": load_source("all_tiers"),
      "expert": load_source("expert"),
    }
    artifacts["expert"] = copy.deepcopy(artifacts["expert"])
    artifacts["expert"]["runs"][0]["turn_trace"] = []

    report = RUNNER.build_report(artifacts)

    self.assertEqual(report["source_artifacts"][1]["status"], "limited")
    self.assertTrue(any("turn_trace" in issue for issue in report["issues"]))

  def test_markdown_rendering_is_deterministic(self):
    report = RUNNER.build_report()
    first = RUNNER.render_markdown(report)
    second = RUNNER.render_markdown(json.loads(json.dumps(report, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("0 → 15 → 30 → 160", first)
    self.assertIn("bounded clearability proxy", first)
    self.assertIn("not human or classroom evidence", first)


if __name__ == "__main__":
  unittest.main()
