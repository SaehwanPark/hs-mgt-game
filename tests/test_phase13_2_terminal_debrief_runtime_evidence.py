import ast
import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-terminal-debrief-runtime-evidence.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_terminal_debrief_runtime_evidence.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase13TerminalDebriefRuntimeEvidenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    spec = importlib.util.spec_from_file_location("validate_terminal_debrief_runtime_evidence", VALIDATOR_PATH)
    cls.validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.validator)

  def test_packet_validates_and_keeps_human_boundaries_pending(self):
    self.validator.validate_packet(self.packet)
    self.assertEqual(self.packet["terminal_surface"]["history"]["row_count"], 1)
    self.assertEqual(self.packet["terminal_surface"]["debrief"]["row_count"], 19)
    self.assertTrue(self.packet["renderer_contract"]["campaign_coverage_hidden_after_end_session"])
    self.assertFalse(self.packet["review_boundary"]["human_visual_debrief_review_complete"])
    self.assertFalse(self.packet["review_boundary"]["public_release_approval"])

  def test_validator_cli_reports_pass(self):
    result = subprocess.run(
      [sys.executable, str(VALIDATOR_PATH)],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    report = json.loads(result.stdout)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["history_count"], 1)
    self.assertEqual(report["debrief_count"], 19)

  def test_validator_rejects_host_history_and_debrief_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["observation"]["host_start"]["demo_fixture"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["terminal_surface"]["history"]["row_count"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["terminal_surface"]["debrief"]["instructor_only_markers_absent"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_read_only_and_renderer_boundary_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["terminal_surface"]["read_only"]["session_end_disabled"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["renderer_contract"]["campaign_coverage_hidden_after_end_session"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["terminal_surface"]["onboarding"]["directs_to_debrief"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_human_or_release_promotion(self):
    packet = copy.deepcopy(self.packet)
    packet["review_boundary"]["educational_usability_review_complete"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["release_boundary"]["public_release_approval"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_source_marker_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["source_contract"]["required_markers"][0] = "src/debrief/report.rs: missing marker"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_source_is_valid_python(self):
    tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"), filename=str(VALIDATOR_PATH))
    self.assertIsNotNone(tree)

  def test_existing_terminal_debrief_contracts_remain_authoritative(self):
    result = subprocess.run(
      [
        sys.executable,
        "-m",
        "unittest",
        "tests.test_phase11_live_debrief",
        "tests.test_phase13_2_debrief_visual_boundary",
        "tests.test_phase13_2_debrief_visual_review_packet",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
  unittest.main()
