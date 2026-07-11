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
  / "v0.10.58-debrief-coherence-audit"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("debrief_coherence_audit", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class DebriefCoherenceAuditTests(unittest.TestCase):
  def test_current_sources_have_complete_coherence_contracts(self):
    audit = RUNNER.build_audit()

    self.assertEqual(audit["source_count"], 6)
    self.assertEqual(audit["completed_source_count"], 6)
    self.assertEqual(audit["run_count"], 39)
    self.assertEqual(audit["runtime_promotion"], "deferred")
    expected_steps = {
      "decision_context",
      "action_response",
      "transition_follow_through",
      "delayed_or_partial_context",
      "outcome_context",
      "debrief_explanation",
    }
    for source in audit["source_reports"]:
      self.assertEqual(
        {step["name"] for step in source["review_steps"]},
        expected_steps,
      )
      self.assertNotIn(source["status"], {"unsupported", "error"})

  def test_missing_decision_observation_is_limited(self):
    contract = RUNNER.SOURCE_CONTRACTS[
      "v0.10.50-teachability-observation-capture"
    ]
    artifact = RUNNER.load_artifact(ROOT / contract["path"])
    tampered = copy.deepcopy(artifact)
    tampered["runs"][0]["turn_trace"][0]["observation"] = []

    report = RUNNER.audit_artifact(tampered, contract)
    steps = {step["name"]: step for step in report["review_steps"]}

    self.assertEqual(report["status"], "limited")
    self.assertEqual(steps["decision_context"]["status"], "limited")
    self.assertIn(1, steps["decision_context"]["limited_turns"])

  def test_retry_turn_must_preserve_observation_and_turn(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.56-project-recovery-use"]
    artifact = RUNNER.load_artifact(ROOT / contract["path"])
    tampered = copy.deepcopy(artifact)
    recovery_trace = next(
      trace for trace in tampered["runs"][0]["turn_trace"]
      if trace["validation_failures"]
    )
    recovery_trace["turn_after_failure"] = recovery_trace["turn"] + 1

    report = RUNNER.audit_artifact(tampered, contract)
    steps = {step["name"]: step for step in report["review_steps"]}

    self.assertEqual(report["status"], "limited")
    self.assertEqual(steps["action_response"]["status"], "limited")
    self.assertIn(recovery_trace["turn"], steps["action_response"]["limited_turns"])

  def test_project_trace_requires_visible_pending_project_context(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.56-project-recovery-use"]
    artifact = RUNNER.load_artifact(ROOT / contract["path"])
    tampered = copy.deepcopy(artifact)
    for trace in tampered["runs"][0]["turn_trace"]:
      trace["observation"] = [
        line
        for line in trace["observation"]
        if not line.startswith("In-flight projects:")
      ]

    report = RUNNER.audit_artifact(tampered, contract)
    steps = {step["name"]: step for step in report["review_steps"]}

    self.assertEqual(steps["delayed_or_partial_context"]["status"], "limited")
    self.assertTrue(steps["delayed_or_partial_context"]["evidence_gaps"])

  def test_source_identity_mismatch_is_reported(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.43-rival-info-follow-through"]
    artifact = {
      "batch_id": contract["batch_id"],
      "code_version": "0.10.42",
      "campaign": RUNNER.CAMPAIGN,
      "runs": [],
    }

    report = RUNNER.audit_artifact(artifact, contract)

    self.assertEqual(report["identity_status"], "limited")
    self.assertTrue(report["evidence_gaps"])

  def test_hash_continuity_detects_tampering(self):
    artifacts = [
      RUNNER.load_artifact(ROOT / contract["path"])
      for contract in RUNNER.SOURCE_CONTRACTS.values()
    ]
    tampered = copy.deepcopy(artifacts)
    tampered[-1]["runs"][0]["state_hashes"][0] = "tampered"

    continuity = RUNNER.hash_continuity(tampered)

    self.assertEqual(continuity["status"], "limited")
    self.assertTrue(any(item["status"] == "limited" for item in continuity["comparisons"]))

  def test_audit_and_markdown_are_deterministic(self):
    audit = RUNNER.build_audit()
    RUNNER.validate_audit(audit)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)
    self.assertIn("Decision-versus-outcome separation", first)


if __name__ == "__main__":
  unittest.main()
