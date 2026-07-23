import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_audio_packaging.py"
SCOPE = ROOT / "assets" / "audio-packaging-scope.json"


class AudioPackagingTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("check_audio_packaging", SCRIPT)
    cls.checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.checker)
    cls.document = json.loads(SCOPE.read_text(encoding="utf-8"))

  def test_current_scope_report_is_green_and_runtime_generated(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "audio-packaging-report-v1")
    self.assertEqual(report["compression_decision"], "not-applicable-runtime-generated")
    self.assertEqual(report["release_audio_count"], 0)
    self.assertEqual(report["release_audio_total_bytes"], 0)
    self.assertEqual(report["registry_entry_count"], 37)

  def test_cli_emits_green_json_report(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    report = json.loads(result.stdout)
    self.assertEqual(report["status"], "pass")

  def test_release_audio_is_rejected(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      release = root / "assets" / "release"
      release.mkdir(parents=True)
      (release / "unexpected.opus").write_bytes(b"not-audio")
      files = self.checker._files(root, "assets/release", {".opus"})
      self.assertEqual([path.name for path in files], ["unexpected.opus"])
      self.assertEqual(
        self.checker.release_audio_errors(root, files),
        ["release audio file is not allowed in current scope: assets/release/unexpected.opus"],
      )

  def test_scope_rejects_escaped_paths_and_wrong_decision(self):
    document = copy.deepcopy(self.document)
    document["release_root"] = "../outside"
    document["compression_decision"] = "compressed"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("path escapes repository root" in error for error in errors))
    self.assertTrue(any("compression_decision" in error for error in errors))

  def test_scope_rejects_non_object_and_missing_root(self):
    self.assertEqual(
      self.checker.validate_definition(ROOT, []),
      ["audio packaging scope document must be an object"],
    )
    document = copy.deepcopy(self.document)
    document["release_root"] = "assets/release/missing"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("directory does not exist" in error for error in errors))

  def test_registry_release_paths_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "audio.json"
      registry.write_text(json.dumps({"entries": [{"release_path": "audio/test.opus"}]}), encoding="utf-8")
      errors, entry_count = self.checker.registry_release_errors(root, ["audio.json"])
      self.assertEqual(entry_count, 1)
      self.assertTrue(any("must have an explicit null release_path" in error for error in errors))

  def test_registry_release_paths_must_be_explicit(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "audio.json"
      registry.write_text(json.dumps({"entries": [{}]}), encoding="utf-8")
      errors, entry_count = self.checker.registry_release_errors(root, ["audio.json"])
      self.assertEqual(entry_count, 1)
      self.assertTrue(any("must have an explicit null release_path" in error for error in errors))


if __name__ == "__main__":
  unittest.main()
