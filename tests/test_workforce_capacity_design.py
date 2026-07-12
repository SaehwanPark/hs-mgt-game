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
  / "v0.12.5-workforce-capacity-design"
  / "build_design.py"
)
SPEC = importlib.util.spec_from_file_location("workforce_capacity_design", RUNNER_PATH)
RUNNER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUNNER)


class WorkforceCapacityDesignTests(unittest.TestCase):
  def test_design_requires_observation_follow_up_without_runtime_tuning(self):
    design = RUNNER.build_design()
    RUNNER.validate_design(design)

    self.assertTrue(design["observation_context_follow_up_required"])
    self.assertFalse(design["runtime_difficulty_change_authorized"])
    self.assertEqual(design["runtime_promotion"], "deferred")
    self.assertEqual(
      design["candidate_signal"]["all_tier_counts"],
      {"easy": 0, "normal": 15, "hard": 30, "expert": 160},
    )

  def test_projection_uses_only_safe_typed_fields(self):
    design = RUNNER.build_design()
    safe_fields = set(design["typed_fields_omitted_by_mcp"])
    hidden_fields = set(design["hidden_fields_excluded"])
    lines = design["proposed_next_projection"]["lines"]

    self.assertTrue(safe_fields)
    self.assertTrue(safe_fields.isdisjoint(hidden_fields))
    self.assertEqual(len(lines), 2)
    self.assertIn("nurses <n>", lines[0])
    self.assertIn("staffed beds <n>", lines[1])
    self.assertTrue(design["proposed_next_projection"]["not_a_new_mechanism"])

  def test_missing_source_marker_is_rejected(self):
    original = RUNNER.SOURCE_MARKERS["src/mcp/session.rs"]
    RUNNER.SOURCE_MARKERS["src/mcp/session.rs"] = original + ["missing marker"]

    try:
      with self.assertRaises(AssertionError):
        RUNNER.build_design()
    finally:
      RUNNER.SOURCE_MARKERS["src/mcp/session.rs"] = original

  def test_hidden_field_in_projection_is_rejected(self):
    design = copy.deepcopy(RUNNER.build_design())
    design["typed_fields_omitted_by_mcp"].append("role_targets")

    with self.assertRaises(AssertionError):
      RUNNER.validate_design(design)

  def test_markdown_rendering_is_deterministic(self):
    design = RUNNER.build_design()
    first = RUNNER.render_markdown(design)
    second = RUNNER.render_markdown(json.loads(json.dumps(design, sort_keys=True)))

    self.assertEqual(first, second)
    self.assertIn("observation-context follow-up required", first)
    self.assertIn("Runtime difficulty change authorized:** no", first)
    self.assertIn("role targets", first)


if __name__ == "__main__":
  unittest.main()
