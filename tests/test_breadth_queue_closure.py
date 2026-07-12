import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "_workspace" / "experiments" / "v0.12.12-breadth-queue-closure"
SPEC = importlib.util.spec_from_file_location(
  "breadth_queue_closure",
  ARTIFACT_DIR / "build_closure.py",
)
CLOSURE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CLOSURE)


class BreadthQueueClosureTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.artifact = json.loads(
      (ARTIFACT_DIR / "closure.json").read_text(encoding="utf-8")
    )
    CLOSURE.validate_closure(cls.artifact)

  def test_closure_identity_and_inventory(self):
    self.assertEqual(
      self.artifact["artifact_type"],
      "simulation_breadth_queue_closure",
    )
    self.assertEqual(self.artifact["code_version"], "0.12.12")
    self.assertEqual(
      self.artifact["closure_status"],
      "complete_no_unexplained_breadth_gap",
    )
    self.assertEqual(len(self.artifact["breadth_inventory"]), 5)

  def test_repeated_play_evidence_is_bounded_and_varied(self):
    evidence = self.artifact["evidence"]["all_tier"]
    self.assertEqual(evidence["run_count"], 60)
    self.assertEqual(evidence["transition_count"], 1440)
    self.assertEqual(evidence["distinct_command_trajectories"], 10)
    self.assertTrue(evidence["no_dominant_first_command"])

  def test_traceability_sources_have_no_structural_gap(self):
    current = self.artifact["evidence"]["current_code"]
    review = self.artifact["evidence"]["teachability_review"]
    self.assertEqual(current["run_count"], 9)
    self.assertEqual(current["transition_count"], 216)
    self.assertEqual(review["complete_run_count"], 18)
    self.assertEqual(review["transition_count"], 270)
    self.assertEqual(review["gap_count"], 0)

  def test_actor_observation_boundary_is_explicit(self):
    boundary = self.artifact["actor_observation_boundary"]
    self.assertIn("private rival actions", boundary["true_state"])
    self.assertIn("lagged public rival actions", boundary["player_observation"])
    self.assertIn("unobserved rival private actions", boundary["private_during_play"])
    self.assertIn("committed events and effects", boundary["debrief"])

  def test_queue_closure_preserves_deferred_scope(self):
    self.assertEqual(
      self.artifact["queue_action"],
      "remove_item_from_future_queue",
    )
    self.assertFalse(self.artifact["runtime_change_authorized"])
    self.assertEqual(self.artifact["runtime_promotion"], "deferred")
    self.assertIn("individual patient simulation", self.artifact["deferred_scope"])
    self.assertIn("full Medicare payment reproduction", self.artifact["deferred_scope"])

  def test_source_markers_are_supported(self):
    self.assertTrue(
      all(
        value["status"] == "supported"
        for value in self.artifact["source_marker_contract"].values()
      )
    )

  def test_reopening_condition_requires_new_evidence(self):
    self.assertIn("new", self.artifact["next_action"])
    self.assertIn("concrete", self.artifact["next_action"])
    self.assertIn("gap", self.artifact["next_action"])


if __name__ == "__main__":
  unittest.main()
