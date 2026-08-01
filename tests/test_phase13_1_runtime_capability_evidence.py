import ast
import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-runtime-capability-evidence.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_runtime_capability_evidence.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase13RuntimeCapabilityEvidenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    spec = importlib.util.spec_from_file_location("validate_runtime_capability_evidence", VALIDATOR_PATH)
    cls.validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.validator)

  def test_packet_validates_and_preserves_pending_boundaries(self):
    self.validator.validate_packet(self.packet)
    self.assertEqual(self.packet["status"], "complete-supported-chromium-host-smoke-pending-cross-engine-certification")
    self.assertEqual(self.packet["observation"]["browser"]["version"], "150.0.0.0")
    self.assertEqual(self.packet["observation"]["shell"]["status"], "competitive regional session loaded: session-12")
    self.assertEqual(self.packet["review_boundary"]["firefox_runtime_certification_complete"], False)
    self.assertEqual(self.packet["review_boundary"]["webkit_runtime_certification_complete"], False)
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
    self.assertEqual(report["observed_browser"]["engine"], "Chromium")

  def test_validator_rejects_non_loopback_url(self):
    packet = copy.deepcopy(self.packet)
    packet["observation"]["url"] = "https://example.com/"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_browser_identity_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["observation"]["browser"]["name"] = "Firefox"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_host_or_console_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["observation"]["shell"]["session_id"] = "not-opaque"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["observation"]["console"]["error_count"] = 1
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_support_or_release_promotion(self):
    packet = copy.deepcopy(self.packet)
    packet["review_boundary"]["webkit_runtime_certification_complete"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)
    packet = copy.deepcopy(self.packet)
    packet["release_boundary"]["public_release_approval"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_source_marker_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["source_contract"]["required_markers"][0] = "assets/browser-compatibility-policy.json: missing marker"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_source_is_valid_python(self):
    tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"), filename=str(VALIDATOR_PATH))
    self.assertIsNotNone(tree)

  def test_existing_browser_device_contracts_remain_authoritative(self):
    result = subprocess.run(
      [
        sys.executable,
        "-m",
        "unittest",
        "tests.test_browser_compatibility",
        "tests.test_device_performance",
        "tests.test_phase13_technical_coverage",
        "tests.test_phase13_1_cross_browser_device_review_packet",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
  unittest.main()
