import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_browser_compatibility.py"
POLICY = ROOT / "assets" / "browser-compatibility-policy.json"


class BrowserCompatibilityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("check_browser_compatibility", SCRIPT)
    cls.checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.checker)
    cls.document = json.loads(POLICY.read_text(encoding="utf-8"))

  def test_current_matrix_and_authority_audits_are_green(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "browser-compatibility-report-v1")
    self.assertEqual(report["loading_policy_status"], "pass")
    self.assertEqual(report["offline_policy_status"], "pass")
    self.assertEqual(report["syntax_status"], "pass")
    self.assertEqual(report["boundary_status"], "pass")
    self.assertIn("gui/host-adapter.mjs", report["syntax_files"])
    self.assertEqual([target["id"] for target in report["supported_targets"]], ["chromium-evergreen-desktop"])
    self.assertEqual(
      {target["support"] for target in report["not_certified_targets"]},
      {"not-certified", "unsupported"},
    )

  def test_cli_emits_green_json_report(self):
    result = subprocess.run(["python3", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["status"], "pass")

  def test_matrix_rejects_missing_required_capability(self):
    document = copy.deepcopy(self.document)
    document["supported_targets"][0]["required_capabilities"].pop()
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("every required capability" in error for error in errors))

  def test_matrix_rejects_duplicate_or_non_list_required_capabilities(self):
    duplicate = copy.deepcopy(self.document)
    duplicate["supported_targets"][0]["required_capabilities"].append("fetch")
    errors = self.checker.validate_definition(ROOT, duplicate)
    self.assertTrue(any("every required capability" in error for error in errors))
    non_list = copy.deepcopy(self.document)
    non_list["supported_targets"][0]["required_capabilities"] = "fetch"
    errors = self.checker.validate_definition(ROOT, non_list)
    self.assertTrue(any("as strings" in error for error in errors))

  def test_matrix_rejects_non_string_fallback(self):
    document = copy.deepcopy(self.document)
    document["capabilities"][4]["fallback"] = False
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("invalid fallback" in error for error in errors))

  def test_matrix_rejects_unsupported_target_without_reason(self):
    document = copy.deepcopy(self.document)
    document["not_certified_targets"][0]["reason"] = ""
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("needs a reason" in error for error in errors))

  def test_matrix_rejects_missing_boundary_policy(self):
    document = copy.deepcopy(self.document)
    document["boundary_checks"]["offline_policy"] = "assets/missing.json"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("does not exist" in error for error in errors))

  def test_report_fails_when_loading_policy_drifts(self):
    document = copy.deepcopy(self.document)
    document["entrypoint"] = "gui/visual-catalog.json"
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("entrypoint" in error or "loading policy" in error for error in report["errors"]))

  def test_report_uses_declared_boundary_policy_paths(self):
    document = copy.deepcopy(self.document)
    document["boundary_checks"]["loading_policy"] = "assets/offline-policy.json"
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("loading policy" in error for error in report["errors"]))


if __name__ == "__main__":
  unittest.main()
