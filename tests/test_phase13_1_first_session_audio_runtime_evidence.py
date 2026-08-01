import ast
import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-first-session-audio-runtime-evidence.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_first_session_audio_runtime_evidence.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase13FirstSessionAudioRuntimeEvidenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    spec = importlib.util.spec_from_file_location("validate_first_session_audio_runtime_evidence", VALIDATOR_PATH)
    cls.validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.validator)

  def test_packet_validates_and_keeps_human_boundaries_pending(self):
    self.validator.validate_packet(self.packet)
    self.assertEqual(self.packet["observation"]["first_session_rail"]["stage_count"], 7)
    self.assertEqual(self.packet["audio_observation"]["cues_only_state"]["playback_verified"], False)
    self.assertEqual(self.packet["review_boundary"]["first_time_user_evaluation_complete"], False)
    self.assertEqual(self.packet["review_boundary"]["audio_preference_feedback_collected"], False)
    self.assertEqual(self.packet["review_boundary"]["public_release_approval"], False)

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
    self.assertEqual(report["flow_schema"], "competitive-first-month-v1")

  def test_validator_rejects_url_browser_and_rail_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["observation"]["url"] = "https://example.com/"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["observation"]["browser"]["version"] = "149.0.0.0"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["observation"]["first_session_rail"]["stage_labels"].pop()
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_hidden_equivalent_and_playback_claims(self):
    packet = copy.deepcopy(self.packet)
    packet["audio_observation"]["muted_state"]["written_equivalent_present"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["audio_observation"]["cues_only_state"]["playback_verified"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["audio_observation"]["optional_equivalent_contract"]["written_results_remain_complete_when_hidden"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_human_or_release_promotion_and_type_coercion(self):
    packet = copy.deepcopy(self.packet)
    packet["review_boundary"]["audio_preference_feedback_collected"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["release_boundary"]["audio_changes"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_source_marker_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["source_contract"]["required_markers"][0] = "gui/index.html: missing marker"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_source_is_valid_python(self):
    tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"), filename=str(VALIDATOR_PATH))
    self.assertIsNotNone(tree)

  def test_existing_first_session_and_audio_contracts_remain_authoritative(self):
    result = subprocess.run(
      [
        sys.executable,
        "-m",
        "unittest",
        "tests.test_phase13_1_first_session_boundary",
        "tests.test_phase13_1_first_session_review_packet",
        "tests.test_phase10_2_audio_preference_review_packet",
        "tests.test_audio_fallback",
        "tests.test_audio_priority",
        "tests.test_gui_audio",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
  unittest.main()
