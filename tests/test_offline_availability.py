import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_offline_availability.py"
POLICY = ROOT / "assets" / "offline-policy.json"


class OfflineAvailabilityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    spec = importlib.util.spec_from_file_location("check_offline_availability", SCRIPT)
    cls.checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.checker)
    cls.document = json.loads(POLICY.read_text(encoding="utf-8"))

  def test_current_policy_report_is_green(self):
    report = self.checker.build_report(ROOT, self.document)
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["schema_version"], "offline-policy-report-v1")
    self.assertEqual(report["resource_count"], 23)
    self.assertEqual(report["route_count"], 24)
    self.assertEqual(report["loading_policy_status"], "pass")

  def test_cli_emits_green_json_report(self):
    result = subprocess.run(
      ["python3", str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["status"], "pass")

  def test_missing_server_route_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["embedded_resources"][1]["urls"] = ["/missing.mjs"]
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("does not route declared URL" in error for error in report["errors"]))

  def test_swapped_route_source_fails_closed(self):
    document = copy.deepcopy(self.document)
    host_adapter = next(resource for resource in document["embedded_resources"] if resource["kind"] == "host-adapter")
    app = next(resource for resource in document["embedded_resources"] if resource["source"] == "gui/app.mjs")
    host_adapter["source"], app["source"] = app["source"], host_adapter["source"]
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("does not embed its declared source" in error for error in report["errors"]))

  def test_loading_graph_drift_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["embedded_resources"] = [
      resource
      for resource in document["embedded_resources"]
      if resource["source"] != "gui/scene.mjs"
    ]
    report = self.checker.build_report(ROOT, document)
    self.assertEqual(report["status"], "fail")
    self.assertTrue(any("not embedded in offline policy" in error for error in report["errors"]))

  def test_external_source_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["embedded_resources"][1]["source"] = "https://example.test/host-adapter.mjs"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("must be repository-local" in error for error in errors))

  def test_non_http_external_scheme_fails_closed(self):
    document = copy.deepcopy(self.document)
    document["embedded_resources"][1]["source"] = "data:text/javascript,alert(1)"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("must be repository-local" in error for error in errors))

  def test_protocol_relative_and_arbitrary_source_schemes_fail_closed(self):
    document = copy.deepcopy(self.document)
    document["embedded_resources"][1]["source"] = "gopher:host-adapter.mjs"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("must be repository-local" in error for error in errors))
    self.assertTrue(self.checker._external_uri("//cdn.example/app.js"))

  def test_html_external_attributes_fail_closed(self):
    tags = self.checker.HTML_TAG_PATTERN.findall(
      '<script src=//cdn.example/app.js></script>'
      '<img srcset="./local.png 1x, //cdn.example/remote.png 2x">'
    )
    external = []
    for tag in tags:
      for match in self.checker.HTML_ATTRIBUTE_PATTERN.finditer(tag):
        value = match.group("double") or match.group("single") or match.group("bare") or ""
        candidates = value.split(",") if match.group("name").lower() == "srcset" else [value]
        external.extend(
          candidate.strip().split()[0]
          for candidate in candidates
          if candidate.strip() and self.checker._external_uri(candidate.strip().split()[0])
        )
    self.assertEqual(external, ["//cdn.example/app.js", "//cdn.example/remote.png"])

  def test_path_escape_and_non_loopback_fail_closed(self):
    document = copy.deepcopy(self.document)
    document["server_source"] = "../gui_server.rs"
    document["local_origin"]["binding"] = "all-interfaces"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("path escapes repository root" in error for error in errors))
    self.assertTrue(any("loopback-only" in error for error in errors))

  def test_policy_rejects_wrong_kind_and_duplicate_route(self):
    document = copy.deepcopy(self.document)
    document["embedded_resources"][1]["kind"] = "service-worker"
    document["embedded_resources"][2]["urls"] = ["/host-adapter.mjs"]
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("unsupported kind" in error for error in errors))
    self.assertTrue(any("duplicate embedded route" in error for error in errors))

  def test_policy_rejects_non_object_and_wrong_schema(self):
    self.assertEqual(
      self.checker.validate_definition(ROOT, []),
      ["offline policy document must be an object"],
    )
    document = copy.deepcopy(self.document)
    document["schema_version"] = "offline-policy-v0"
    errors = self.checker.validate_definition(ROOT, document)
    self.assertTrue(any("unsupported offline policy schema_version" in error for error in errors))

  def test_malformed_loading_policy_returns_structured_failure(self):
    original = self.checker._loading_document
    self.checker._loading_document = lambda root: []
    try:
      report = self.checker.build_report(ROOT, self.document)
    finally:
      self.checker._loading_document = original
    self.assertEqual(report["status"], "fail")
    self.assertEqual(report["resource_count"], 23)

  def test_malformed_loading_file_shape_returns_structured_failure(self):
    original = self.checker._loading_document
    self.checker._loading_document = lambda root: {"live_files": [[]]}
    try:
      report = self.checker.build_report(ROOT, self.document)
    finally:
      self.checker._loading_document = original
    self.assertEqual(report["status"], "fail")
    self.assertEqual(report["resource_count"], 23)


if __name__ == "__main__":
  unittest.main()
