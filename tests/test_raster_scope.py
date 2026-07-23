import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_raster_scope.py"
SCOPE = ROOT / "assets" / "raster-scope.json"


class RasterScopeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("check_raster_scope", SCRIPT)
    cls.checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.checker)
    cls.document = json.loads(SCOPE.read_text(encoding="utf-8"))

  def test_current_scope_report_is_green(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "raster-scope-report-v1")
    self.assertEqual(report["release_raster_count"], 0)
    self.assertEqual(report["preview_count"], 7)
    self.assertEqual(report["preview_total_bytes"], 15097805)
    self.assertEqual(max(item["dimensions"]["width"] for item in report["previews"]), 1254)

  def test_cli_emits_green_json_report(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["status"], "pass")

  def test_release_raster_is_rejected(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      release = root / "assets" / "release"
      release.mkdir(parents=True)
      (release / "unexpected.png").write_bytes(b"not-png")
      self.assertEqual(
        [path.name for path in self.checker._files(root, "assets/release", {".png"})],
        ["unexpected.png"],
      )
      self.assertEqual(
        self.checker.release_raster_errors(root, [release / "unexpected.png"]),
        ["release raster file is not allowed: assets/release/unexpected.png"],
      )

  def test_preview_limits_and_promotion_fields_fail_closed(self):
    document = copy.deepcopy(self.document)
    document["preview_max_file_bytes"] = 1
    document["preview_max_width"] = 1
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("preview bounds" in error or "preview bound" in error for error in report["errors"]))

  def test_invalid_png_dimensions_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      path = Path(directory) / "invalid.png"
      path.write_bytes(b"not-png")
      self.assertIsNone(self.checker.png_dimensions(path))

  def test_definition_rejects_absolute_paths_and_non_object(self):
    document = copy.deepcopy(self.document)
    document["release_root"] = str(ROOT / "assets" / "release")
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("path must be relative" in error for error in errors))
    self.assertEqual(
      self.checker.validate_definition(ROOT, []),
      ["raster scope document must be an object"],
    )

  def test_definition_rejects_missing_scope_root(self):
    document = copy.deepcopy(self.document)
    document["preview_root"] = "assets/generation/missing-previews"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("directory does not exist" in error for error in errors))

  def test_report_rejects_wrong_preview_count(self):
    document = copy.deepcopy(self.document)
    document["preview_expected_count"] = 6
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("entry count does not match" in error for error in report["errors"]))


if __name__ == "__main__":
  unittest.main()
