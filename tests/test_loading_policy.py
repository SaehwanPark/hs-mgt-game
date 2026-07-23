import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_loading_policy.py"
POLICY = ROOT / "assets" / "loading-policy.json"


class LoadingPolicyTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("check_loading_policy", SCRIPT)
    cls.checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.checker)
    cls.document = json.loads(POLICY.read_text(encoding="utf-8"))

  def test_current_policy_report_is_green(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "loading-policy-report-v1")
    self.assertEqual(report["live_file_count"], 20)
    self.assertEqual(report["marker_hits"], [])
    self.assertEqual(report["entrypoint_sources"], ["gui/app.mjs"])
    self.assertEqual(len(report["module_sources"]), 18)
    self.assertEqual(len(report["discovered_sources"]), 19)
    self.assertEqual(report["decisions"], {
      "lazy_loading": "no-lazy-loading-needed",
      "preloading": "no-preload-directives",
    })

  def test_cli_emits_green_json_report(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["status"], "pass")

  def test_forbidden_preload_and_media_markers_fail(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "index.html"
      source.write_text('<link rel=preload href="x.woff2"><source srcset="x.webp">', encoding="utf-8")
      errors = self.checker.scan_markers(root, "index.html", self.checker._markers(self.document))
      self.assertTrue(any("html-speculative-preload" in error for error in errors))
      self.assertTrue(any("html-file-backed-media" in error for error in errors))

  def test_entrypoint_source_must_be_declared(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      entrypoint = root / "index.html"
      entrypoint.write_text('<script type="module" src="./unlisted.mjs"></script>', encoding="utf-8")
      (root / "unlisted.mjs").write_text("export {};", encoding="utf-8")
      document = copy.deepcopy(self.document)
      document["live_entrypoint"] = "index.html"
      document["live_files"] = ["index.html"]
      report = self.checker.build_report(root, document)
      self.assertEqual(report["status"], "fail")
      self.assertTrue(any("source is not declared" in error for error in report["errors"]))

  def test_transitive_module_source_must_be_declared(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "index.html").write_text('<script type="module" src="./app.mjs"></script>', encoding="utf-8")
      (root / "app.mjs").write_text('import { value } from "./unlisted.mjs"; export { value };', encoding="utf-8")
      (root / "unlisted.mjs").write_text("export const value = 1;", encoding="utf-8")
      document = copy.deepcopy(self.document)
      document["live_entrypoint"] = "index.html"
      document["live_files"] = ["index.html", "app.mjs"]
      report = self.checker.build_report(root, document)
      self.assertEqual(report["status"], "fail")
      self.assertTrue(any("source is not declared" in error for error in report["errors"]))

  def test_dynamic_module_source_must_be_declared(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "index.html").write_text('<script type="module" src="./app.mjs"></script>', encoding="utf-8")
      (root / "app.mjs").write_text('const load = () => import("./unlisted.mjs");', encoding="utf-8")
      (root / "unlisted.mjs").write_text("export const value = 1;", encoding="utf-8")
      document = copy.deepcopy(self.document)
      document["live_entrypoint"] = "index.html"
      document["live_files"] = ["index.html", "app.mjs"]
      report = self.checker.build_report(root, document)
      self.assertEqual(report["status"], "fail")
      self.assertTrue(any("source is not declared" in error for error in report["errors"]))

  def test_multiline_module_source_must_be_declared(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "index.html").write_text('<script type="module" src="./app.mjs"></script>', encoding="utf-8")
      (root / "app.mjs").write_text(
        'import {\n  value,\n} from "./unlisted.mjs";\n',
        encoding="utf-8",
      )
      (root / "unlisted.mjs").write_text("export const value = 1;", encoding="utf-8")
      document = copy.deepcopy(self.document)
      document["live_entrypoint"] = "index.html"
      document["live_files"] = ["index.html", "app.mjs"]
      report = self.checker.build_report(root, document)
      self.assertEqual(report["status"], "fail")
      self.assertTrue(any("source is not declared" in error for error in report["errors"]))

  def test_non_literal_dynamic_module_source_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "app.mjs"
      source.write_text("const load = (path) => import(path);", encoding="utf-8")
      sources, errors = self.checker.module_sources(root, ["app.mjs"])
      self.assertEqual(sources, [])
      self.assertTrue(any("must be a string literal" in error for error in errors))

  def test_executable_runtime_loads_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "app.mjs"
      source.write_text(
        'fetch(asset.url);\nimage.src = asset.release_path;\nnew URL(asset.path);\n',
        encoding="utf-8",
      )
      errors = self.checker.scan_markers(root, "app.mjs", self.checker._markers(self.document))
      self.assertEqual(sum("runtime-file-backed-load" in error for error in errors), 3)

  def test_external_or_escaped_entrypoint_sources_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      entrypoint = root / "index.html"
      entrypoint.write_text(
        '<script type="module" src="https://example.test/app.mjs"></script>'
        '<script type="module" src="../outside.mjs"></script>',
        encoding="utf-8",
      )
      sources, errors = self.checker.entrypoint_sources(root, "index.html")
      self.assertEqual(sources, [])
      self.assertTrue(any("source is not local" in error for error in errors))
      self.assertTrue(any("escapes repository root" in error for error in errors))

  def test_external_or_escaped_module_sources_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "app.mjs"
      source.write_text(
        'import "https://example.test/remote.mjs";\n'
        'export * from "../outside.mjs";\n',
        encoding="utf-8",
      )
      sources, errors = self.checker.module_sources(root, ["app.mjs"])
      self.assertEqual(sources, [])
      self.assertEqual(len(errors), 2)
      self.assertTrue(all("module source is not local" in error for error in errors))

  def test_policy_rejects_escaped_path_and_incomplete_requirements(self):
    document = copy.deepcopy(self.document)
    document["live_files"][0] = "../outside.html"
    document["future_asset_requirements"] = ["registry_id"]
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("path escapes repository root" in error for error in errors))
    self.assertTrue(any("complete loading contract" in error for error in errors))

  def test_policy_rejects_duplicate_future_requirements(self):
    document = copy.deepcopy(self.document)
    document["future_asset_requirements"].append("provenance")
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("must not contain duplicates" in error for error in errors))

  def test_policy_rejects_non_object_and_wrong_decision(self):
    self.assertEqual(
      self.checker.validate_definition(ROOT, []),
      ["loading policy document must be an object"],
    )
    document = copy.deepcopy(self.document)
    document["preloading_decision"] = "preload-everything"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("preloading_decision" in error for error in errors))


if __name__ == "__main__":
  unittest.main()
