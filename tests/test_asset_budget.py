import copy
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_asset_budget.py"
BUDGET_PATH = ROOT / "assets" / "asset-budget.json"


class AssetBudgetTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = {
      "name": "asset_budget_checker",
      "path": SCRIPT,
    }
    import importlib.util
    module_spec = importlib.util.spec_from_file_location(spec["name"], spec["path"])
    cls.checker = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(cls.checker)
    cls.document = json.loads(BUDGET_PATH.read_text(encoding="utf-8"))

  def test_current_budget_report_is_green_and_deterministic(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "asset-budget-report-v1")
    self.assertEqual(
      [(item["id"], item["file_count"], item["total_bytes"]) for item in report["budgets"]],
      [
        ("release-visual-svg", 15, 20681),
        ("release-package", 15, 20681),
      ],
    )
    self.assertEqual(
      report["budgets"][0]["largest_file"],
      {"path": "assets/release/visual/svg/utility-plant.svg", "bytes": 1654},
    )

  def test_cli_emits_json_report(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    report = json.loads(result.stdout)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["scope"], "tracked release assets")

  def test_definition_rejects_escaped_root(self):
    document = copy.deepcopy(self.document)
    document["budgets"][0]["root"] = "../outside"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("escapes repository root" in error for error in errors))

  def test_definition_rejects_absolute_root(self):
    document = copy.deepcopy(self.document)
    document["budgets"][0]["root"] = str(ROOT / "assets" / "release")
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("path must be relative" in error for error in errors))

  def test_definition_rejects_non_object_document(self):
    self.assertEqual(
      self.checker.validate_definition(ROOT, []),
      ["budget document must be an object"],
    )

  def test_report_fails_when_a_limit_is_exceeded(self):
    document = copy.deepcopy(self.document)
    document["budgets"][0]["max_total_bytes"] = 1
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("exceeds 1" in error for error in report["errors"]))

  def test_report_fails_for_an_empty_class(self):
    document = copy.deepcopy(self.document)
    document["budgets"][0]["include"] = ["*.does-not-exist"]
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("matched no files" in error for error in report["errors"]))


if __name__ == "__main__":
  unittest.main()
