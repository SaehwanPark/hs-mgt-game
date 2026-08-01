import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "docs" / "evaluation" / "phase13-remaining-gate-technical-audit.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_remaining_gate_technical_audit.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase13RemainingGateTechnicalAuditTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.audit = load_json(AUDIT_PATH)
    spec = importlib.util.spec_from_file_location(
      "validate_remaining_gate_technical_audit",
      VALIDATOR_PATH,
    )
    cls.validator = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(cls.validator)

  def test_audit_maps_all_open_markers_and_keeps_promotion_blocked(self):
    self.validator.validate_audit(self.audit)
    self.assertEqual(self.audit["schema_version"], "phase13-remaining-gate-technical-audit-v1")
    self.assertEqual(self.audit["package_version"], "0.13.103")
    self.assertEqual(len(self.audit["gates"]), 8)
    runtime_check = next(check for check in self.audit["technical_checks"] if check["id"] == "runtime-boundary-evidence")
    self.assertIn("docs/evaluation/phase13.2-terminal-debrief-runtime-evidence.json", runtime_check["sources"])
    archive_check = next(check for check in self.audit["technical_checks"] if check["id"] == "durable-checkpoint-archive")
    self.assertIn("src/mcp/persistence.rs", archive_check["sources"])
    discovery_check = next(check for check in self.audit["technical_checks"] if check["id"] == "checkpoint-discovery")
    self.assertIn("gui/app.mjs", discovery_check["sources"])
    self.assertTrue(self.audit["decision_boundary"]["human_or_runtime_gates_remaining"])
    self.assertTrue(self.audit["decision_boundary"]["promotion_blocked"])
    self.assertIsNone(self.audit["decision_boundary"]["go_no_go"])

  def test_audit_cli_accepts_source_bound_packet(self):
    result = subprocess.run(
      [sys.executable, str(VALIDATOR_PATH)],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
    self.assertIn('"status": "pass"', result.stdout)
    self.assertIn('"gate_count": 8', result.stdout)

  def test_validator_rejects_source_marker_and_roadmap_marker_drift(self):
    audit = copy.deepcopy(self.audit)
    audit["gates"][0]["sources"][0] = "README.md: no such marker"
    with self.assertRaisesRegex(ValueError, "source marker is missing"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["roadmap_contract"]["open_item_markers"][0]["text"] = "Current technical competitive campaign boundary documented."
    with self.assertRaisesRegex(ValueError, "roadmap marker contract drifted"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["roadmap_contract"]["path"] = "/etc/passwd"
    with self.assertRaisesRegex(ValueError, "roadmap path must be relative"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    browser_marker = next(
      marker
      for marker in audit["roadmap_contract"]["open_item_markers"]
      if marker["id"] == "browser-device-certification"
    )
    browser_marker["text"] = "cross-browser/device certification"
    with self.assertRaisesRegex(ValueError, "roadmap marker contract drifted"):
      self.validator.validate_audit(audit)

  def test_validator_rejects_status_promotion_and_type_coercion(self):
    audit = copy.deepcopy(self.audit)
    audit["gates"][0]["human_status"] = "approved"
    with self.assertRaisesRegex(ValueError, "human status is not pending"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["gates"][0]["blocking_promotion"] = 1
    with self.assertRaisesRegex(ValueError, "open gate must block promotion"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["decision_boundary"]["promotion_blocked"] = 1
    with self.assertRaisesRegex(ValueError, "promotion must remain blocked"):
      self.validator.validate_audit(audit)

  def test_validator_rejects_unmapped_or_released_gate(self):
    audit = copy.deepcopy(self.audit)
    audit["gates"][0]["roadmap_marker_ids"].append("portrait-prompt-seed")
    with self.assertRaisesRegex(ValueError, "gate markers must be unique"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["decision_boundary"]["go_no_go"] = "approved"
    with self.assertRaisesRegex(ValueError, "decision field must remain unset"):
      self.validator.validate_audit(audit)

  def test_validator_rejects_absolute_and_non_string_check_paths(self):
    audit = copy.deepcopy(self.audit)
    audit["technical_checks"][0]["sources"][0] = "/etc/passwd"
    with self.assertRaisesRegex(ValueError, "check source must be relative"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["technical_checks"][0]["sources"][0] = 7
    with self.assertRaisesRegex(ValueError, "check source must be a string"):
      self.validator.validate_audit(audit)

    audit = copy.deepcopy(self.audit)
    audit["test_source"] = 7
    with self.assertRaisesRegex(ValueError, "test source must be a string"):
      self.validator.validate_audit(audit)


if __name__ == "__main__":
  unittest.main()
