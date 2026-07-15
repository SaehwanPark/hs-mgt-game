import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_gui_playtests.py"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "gui_playtest_matrix"
SPEC = importlib.util.spec_from_file_location("analyze_gui_playtests", SCRIPT)
ANALYZER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ANALYZER)


class GuiPlaytestAnalysisTests(unittest.TestCase):
  def test_matrix_preserves_declared_coverage_and_prioritizes_observable_gap(self):
    report = ANALYZER.analyze_paths([FIXTURE_DIR])
    self.assertEqual(report["input_count"], 5)
    self.assertEqual(report["valid_count"], 5)
    self.assertEqual(report["invalid_count"], 0)
    self.assertEqual(report["coverage"]["campaign"], [
      "competitive-regional-v1",
      "regional-affiliation-v1",
      "stabilization-v1",
    ])
    self.assertEqual(report["coverage"]["role"], [
      "access-check",
      "first-time",
      "recovery-check",
      "strategy-review",
    ])
    self.assertEqual(len(report["revision_findings"]), 1)
    self.assertEqual(report["revision_findings"][0]["priority"], 2)
    self.assertEqual(report["revision_findings"][0]["code"], "command_without_history")
    self.assertNotIn("affiliation_recovery_check_seed44.json", report["revision_findings"][0]["capture"])

  def test_same_inputs_have_byte_stable_cli_output(self):
    first = subprocess.run(
      ["python3", str(SCRIPT), str(FIXTURE_DIR)],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    second = subprocess.run(
      ["python3", str(SCRIPT), str(FIXTURE_DIR)],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(first.returncode, 0, first.stderr)
    self.assertEqual(first.stdout, second.stdout)
    self.assertEqual(json.loads(first.stdout)["schema_version"], "gui-playtest-analysis-v1")

  def test_invalid_capture_is_visible_and_not_valid_task_evidence(self):
    source = FIXTURE_DIR / "competitive_strategy_review_seed43.json"
    capture = json.loads(source.read_text(encoding="utf-8"))
    capture["schema_version"] = "gui-playtest-v0"
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "invalid.json"
      path.write_text(json.dumps(capture), encoding="utf-8")
      report = ANALYZER.analyze_paths([path])
    self.assertEqual(report["valid_count"], 0)
    self.assertEqual(report["invalid_count"], 1)
    self.assertEqual(report["revision_findings"][0]["priority"], 0)
    self.assertEqual(report["revision_findings"][0]["category"], "capture_contract")

  def test_missing_input_is_reported_instead_of_becoming_empty_success(self):
    missing = ROOT / "tests" / "fixtures" / "gui_playtest_matrix" / "does-not-exist.json"
    report = ANALYZER.analyze_paths([missing])
    self.assertEqual(report["input_count"], 1)
    self.assertEqual(report["valid_count"], 0)
    self.assertEqual(report["invalid_count"], 1)
    self.assertEqual(report["revision_findings"][0]["category"], "capture_contract")

  def test_incomplete_task_is_not_counted_as_valid_task_evidence(self):
    source = FIXTURE_DIR / "competitive_strategy_review_seed43.json"
    capture = json.loads(source.read_text(encoding="utf-8"))
    capture["events"] = [event for event in capture["events"] if event["type"] != "task_completed"]
    for sequence, event in enumerate(capture["events"]):
      event["sequence"] = sequence
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "incomplete.json"
      path.write_text(json.dumps(capture), encoding="utf-8")
      report = ANALYZER.analyze_paths([path])
    self.assertEqual(report["valid_count"], 0)
    self.assertEqual(report["invalid_count"], 1)
    self.assertEqual(report["revision_findings"][0]["category"], "task_recovery")

  def test_report_does_not_score_strategy_or_human_experience(self):
    rendered = json.dumps(ANALYZER.analyze_paths([FIXTURE_DIR]), sort_keys=True).lower()
    for forbidden in ("strategy_score", "optimal_action", "human_usability", "learning_score", "causal_inference"):
      self.assertNotIn(forbidden, rendered)
    self.assertIn("evidence_limits", rendered)


if __name__ == "__main__":
  unittest.main()
