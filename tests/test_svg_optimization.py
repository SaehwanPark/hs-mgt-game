import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "optimize_release_svg.py"


class SvgOptimizationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("optimize_release_svg", SCRIPT)
    cls.optimizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.optimizer)

  def test_normalization_is_whitespace_only_and_preserves_text(self):
    source = "<svg>\n  <title> A visible title </title>\n  <text x=\"1\">A B</text>\n</svg>\n"
    optimized = self.optimizer.normalize_svg(source)
    self.assertEqual(
      optimized,
      "<svg><title> A visible title </title><text x=\"1\">A B</text></svg>\n",
    )
    self.assertEqual(
      self.optimizer._semantic_projection(source),
      self.optimizer._semantic_projection(optimized),
    )
    self.assertEqual(self.optimizer.normalize_svg(optimized), optimized)

  def test_release_report_is_green_and_idempotent(self):
    report = self.optimizer.build_report(ROOT)
    self.assertEqual(report["schema_version"], "svg-optimization-report-v1")
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["file_count"], 15)
    self.assertEqual(report["after_total_bytes"], 20198)
    self.assertEqual(report["bytes_saved"], 0)
    self.assertEqual(report["errors"], [])

  def test_cli_reports_json_after_write(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    report = json.loads(result.stdout)
    self.assertEqual(report["schema_version"], "svg-optimization-report-v1")
    self.assertEqual(report["status"], "pass")

  def test_report_rejects_missing_release_directory(self):
    original = self.optimizer.RELEASE_ROOT
    try:
      self.optimizer.RELEASE_ROOT = Path("assets/release/missing-svg")
      report = self.optimizer.build_report(ROOT)
    finally:
      self.optimizer.RELEASE_ROOT = original
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("no release SVGs" in error for error in report["errors"]))

  def test_hash_report_rejects_malformed_registry_document(self):
    original = self.optimizer.VISUAL_REGISTRY
    with tempfile.TemporaryDirectory() as directory:
      registry = Path(directory) / "visual-assets.json"
      registry.write_text("[]", encoding="utf-8")
      try:
        self.optimizer.VISUAL_REGISTRY = registry
        errors = self.optimizer._hash_alignment_errors(ROOT)
      finally:
        self.optimizer.VISUAL_REGISTRY = original
    self.assertEqual(errors, [f"{registry}: entries must be a list"])


if __name__ == "__main__":
  unittest.main()
