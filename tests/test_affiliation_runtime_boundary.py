import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = (
  ROOT / "_workspace" / "experiments" / "v0.12.7-affiliation-runtime-boundary-proposal"
)
SPEC = importlib.util.spec_from_file_location(
  "affiliation_runtime_boundary_proposal",
  ARTIFACT_DIR / "build_proposal.py",
)
PROPOSAL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(PROPOSAL)


class AffiliationRuntimeBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.artifact = json.loads(
      (ARTIFACT_DIR / "proposal.json").read_text(encoding="utf-8")
    )
    PROPOSAL.validate_proposal(cls.artifact)

  def test_artifact_identity_and_existing_runtime_status(self):
    self.assertEqual(
      self.artifact["artifact_type"],
      "affiliation_runtime_boundary_proposal",
    )
    self.assertEqual(self.artifact["code_version"], "0.12.7")
    self.assertEqual(
      self.artifact["implementation_status"],
      "existing_opt_in_runtime_confirmed",
    )

  def test_minimum_contracts_are_source_supported(self):
    self.assertEqual(
      set(self.artifact["minimum_contracts"]),
      {
        "true_state",
        "actor_observation",
        "resolved_inputs",
        "deterministic_core",
        "history_and_replay",
        "debrief",
      },
    )
    self.assertTrue(
      all(
        value["status"] == "supported"
        for value in self.artifact["source_contract"].values()
      )
    )

  def test_committed_affiliation_evidence_is_complete(self):
    evidence = self.artifact["evidence_contract"]
    self.assertEqual(evidence["run_count"], 9)
    self.assertEqual(evidence["transition_count"], 54)
    self.assertEqual(evidence["observation_count"], 54)
    self.assertEqual(evidence["status"], "supported")

  def test_no_new_runtime_change_is_authorized(self):
    self.assertFalse(self.artifact["new_runtime_changes_authorized"])
    self.assertEqual(self.artifact["runtime_promotion"], "deferred")
    self.assertIn("direct acquisition branch", self.artifact["deferred_scope"])
    self.assertIn("changes to competitive-regional-v1", self.artifact["deferred_scope"])

  def test_decision_names_the_next_evidence_gate(self):
    decision = self.artifact["decision"]
    self.assertIn("existing regional-affiliation-v1 runtime", decision)
    self.assertIn("new concrete evidence gap", decision)


if __name__ == "__main__":
  unittest.main()
