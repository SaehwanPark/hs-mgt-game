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
  / "v0.10.57-debrief-use-audit"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location("debrief_use_audit", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class DebriefUseAuditTests(unittest.TestCase):
  def test_current_sources_cover_each_review_step(self):
    audit = RUNNER.build_audit()

    self.assertEqual(audit["source_count"], 6)
    self.assertEqual(audit["completed_source_count"], 6)
    self.assertEqual(audit["hash_continuity"]["status"], "supported")
    self.assertEqual(audit["runtime_promotion"], "deferred")
    for source in audit["source_reports"]:
      self.assertEqual(
        [step["status"] for step in source["review_steps"]],
        ["supported"] * 5,
      )

  def test_project_recovery_chain_is_explicitly_supported(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.56-project-recovery-use"]
    artifact = RUNNER.load_artifact(ROOT / contract["path"])
    report = RUNNER.audit_artifact(artifact, contract)

    self.assertEqual(report["lane"], "project-recovery")
    self.assertEqual(report["status"], "supported")
    self.assertEqual(report["evidence_gaps"], [])
    self.assertEqual(report["run_reports"][0]["missing_steps"], [])

  def test_missing_debrief_is_reported_as_a_limited_explanation(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.56-project-recovery-use"]
    artifact = RUNNER.load_artifact(ROOT / contract["path"])
    tampered = copy.deepcopy(artifact)
    tampered["runs"][0]["debrief"] = []

    report = RUNNER.audit_artifact(tampered, contract)
    statuses = {step["name"]: step["status"] for step in report["review_steps"]}

    self.assertEqual(statuses["explanation"], "limited")
    self.assertEqual(report["status"], "limited")
    self.assertEqual(report["run_reports"][0]["missing_steps"], ["explanation"])

  def test_malformed_runs_are_limited_without_crashing(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.43-rival-info-follow-through"]
    report = RUNNER.audit_artifact(
      {
        "batch_id": "v0.10.43-rival-info-follow-through",
        "code_version": "0.10.43",
        "campaign": RUNNER.CAMPAIGN,
        "runs": [{"completion_status": "complete"}, "malformed"],
      },
      contract,
    )

    self.assertEqual(report["status"], "limited")
    self.assertIn("visibility", report["run_reports"][0]["missing_steps"])
    self.assertEqual(report["completed_run_count"], 1)

  def test_source_identity_mismatch_is_reported(self):
    contract = RUNNER.SOURCE_CONTRACTS["v0.10.43-rival-info-follow-through"]
    report = RUNNER.audit_artifact(
      {
        "batch_id": contract["batch_id"],
        "code_version": "0.10.42",
        "campaign": RUNNER.CAMPAIGN,
        "runs": [],
      },
      contract,
    )

    self.assertEqual(report["identity_status"], "limited")
    self.assertEqual(report["evidence_gaps"][0]["missing_steps"], ["source_identity"])

  def test_hash_continuity_detects_tampered_source(self):
    artifacts = [
      RUNNER.load_artifact(ROOT / contract["path"])
      for contract in RUNNER.SOURCE_CONTRACTS.values()
    ]
    tampered = copy.deepcopy(artifacts)
    tampered[5]["runs"][0]["state_hashes"][0] = "tampered"

    continuity = RUNNER.hash_continuity(tampered)

    self.assertEqual(continuity["status"], "limited")
    self.assertEqual(continuity["comparisons"][1]["status"], "limited")

  def test_audit_and_markdown_are_deterministic(self):
    audit = RUNNER.build_audit()
    RUNNER.validate_audit(audit)
    first = RUNNER.render_markdown(audit)
    second = RUNNER.render_markdown(json.loads(json.dumps(audit, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("Runtime promotion: deferred", first)
    self.assertIn("Evidence limits", first)


if __name__ == "__main__":
  unittest.main()
