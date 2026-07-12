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
  / "v0.12.3-phase7-teachability-review"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("phase7_teachability_review", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


def load_source(source_id):
  contract = RUNNER.SOURCE_CONTRACTS[source_id]
  return RUNNER.load_artifact(ROOT / contract["path"])


class Phase7TeachabilityReviewTests(unittest.TestCase):
  def test_review_covers_both_sources(self):
    report = RUNNER.build_report()
    RUNNER.validate_report(report)

    self.assertEqual(report["aggregate"]["source_count"], 2)
    self.assertEqual(report["aggregate"]["run_count"], 18)
    self.assertEqual(report["aggregate"]["complete_run_count"], 18)
    self.assertEqual(report["aggregate"]["transition_count"], 270)
    self.assertEqual(report["aggregate"]["gaps"], [])
    self.assertEqual(report["finding"], "no_structural_gap")

  def test_source_contracts_preserve_campaign_specific_context(self):
    report = RUNNER.build_report()
    by_source = {source["source_id"]: source for source in report["sources"]}

    self.assertEqual(
      by_source["affiliation"]["context_contract"],
      "commitments, alternatives, assumptions",
    )
    self.assertEqual(
      by_source["competitive"]["context_contract"],
      "consultant options and advisory comparison",
    )
    for source in by_source.values():
      self.assertEqual(source["coverage"]["strategy_comparison"]["status"], "supported")

  def test_malformed_source_identity_is_rejected(self):
    artifact = load_source("affiliation")
    artifact["batch_id"] = "wrong-batch"

    with self.assertRaises(AssertionError):
      RUNNER.audit_source(
        "affiliation",
        artifact,
        RUNNER.SOURCE_CONTRACTS["affiliation"],
      )

  def test_missing_context_marker_is_reported_as_gap(self):
    artifacts = {
      "affiliation": load_source("affiliation"),
      "competitive": load_source("competitive"),
    }
    artifacts["affiliation"] = copy.deepcopy(artifacts["affiliation"])
    observation = artifacts["affiliation"]["runs"][0]["turn_trace"][0]["observation"]
    artifacts["affiliation"]["runs"][0]["turn_trace"][0]["observation"] = [
      line for line in observation if not str(line).startswith("Assumption:")
    ]

    report = RUNNER.build_report(artifacts)

    self.assertEqual(report["finding"], "structural_gap")
    self.assertGreater(report["aggregate"]["gap_count"], 0)
    self.assertTrue(any("assumptions" in gap["issue"] for gap in report["aggregate"]["gaps"]))

  def test_markdown_rendering_is_deterministic(self):
    report = RUNNER.build_report()
    first = RUNNER.render_markdown(report)
    second = RUNNER.render_markdown(json.loads(json.dumps(report, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Runs reviewed:** 18 of 18", first)
    self.assertIn("No structural decision-to-debrief", first)
    self.assertIn("not human or classroom evidence", first)


if __name__ == "__main__":
  unittest.main()
