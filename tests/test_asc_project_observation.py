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
  / "v0.10.55-asc-project-observation"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "asc_project_observation", RUNNER_PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
ARTIFACT_PATH = RUNNER_PATH.with_name("results.json")


class AscProjectObservationTests(unittest.TestCase):
  def artifact(self):
    return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

  def test_matrix_and_source_are_versioned(self):
    artifact = self.artifact()

    self.assertEqual(RUNNER.SOURCE_RUNNER.SEEDS, [42, 43, 44])
    self.assertEqual(artifact["batch_id"], "v0.10.55-asc-project-observation")
    self.assertEqual(artifact["code_version"], "0.10.55")
    self.assertEqual(artifact["profile"], "ASC Project Observation")
    self.assertIn("concrete actor-visible omission", artifact["promotion_basis"])
    self.assertEqual(
      artifact["source"]["batch_id"],
      "v0.10.54-project-limit-recovery",
    )

  def test_asc_and_clinic_projects_are_visible_before_limit_probe(self):
    artifact = self.artifact()
    RUNNER.validate_artifact(artifact)

    self.assertEqual(artifact["project_observation"]["asc_visible_count"], 3)
    self.assertEqual(
      artifact["project_observation"]["clinic_visible_count"],
      3,
    )
    for run in artifact["project_observation"]["runs"]:
      self.assertIn(
        "AscUnit (5 mos left, $1k/mo draw)",
        "\n".join(run["observation"]),
      )

  def test_visibility_gap_is_rejected(self):
    artifact = copy.deepcopy(self.artifact())
    artifact["project_observation"]["asc_visible_count"] = 2
    artifact["project_observation"]["runs"][0]["asc_unit_visible"] = False

    with self.assertRaises(AssertionError):
      RUNNER.validate_artifact(artifact)

  def test_project_limit_recovery_and_hash_continuity_are_preserved(self):
    artifact = self.artifact()
    RUNNER.validate_artifact(artifact)

    for run in artifact["runs"]:
      self.assertEqual(run["transition_count"], 24)
      self.assertEqual(run["retry_count"], 1)
      self.assertEqual(run["unexpected_failures"], [])
      self.assertEqual(
        run["expected_probe_failures"][0]["code"],
        "too_many_concurrent_projects",
      )

  def test_diagnostics_render_deterministically(self):
    artifact = self.artifact()
    first = RUNNER.render_diagnostics(artifact)
    second = RUNNER.render_diagnostics(json.loads(json.dumps(artifact)))

    self.assertEqual(first, second)
    self.assertIn("ASC Project Observation Diagnostics v0.10.55", first)
    self.assertIn("ASC project visible at month 7: 3/3 runs", first)
    self.assertIn("State-hash sequences match", first)


if __name__ == "__main__":
  unittest.main()
