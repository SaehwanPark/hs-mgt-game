import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-cross-browser-device-review-packet.json"
BROWSER_POLICY_PATH = ROOT / "assets" / "browser-compatibility-policy.json"
DEVICE_POLICY_PATH = ROOT / "assets" / "device-performance-policy.json"
LOADING_POLICY_PATH = ROOT / "assets" / "loading-policy.json"
OFFLINE_POLICY_PATH = ROOT / "assets" / "offline-policy.json"
TECHNICAL_COVERAGE_PATH = ROOT / "docs" / "evaluation" / "phase13.1-technical-coverage.json"

EXPECTED_SHARED_SOURCES = [
  "assets/browser-compatibility-policy.json",
  "assets/device-performance-policy.json",
  "assets/loading-policy.json",
  "assets/offline-policy.json",
  "scripts/check_browser_compatibility.py",
  "scripts/check_device_performance.py",
  "tests/test_browser_compatibility.py",
  "tests/test_device_performance.py",
  "docs/evaluation/phase13.1-technical-coverage.json",
  "tests/test_phase13_technical_coverage.py",
  "docs/guides/reproducible-distribution.md",
  "docs/guides/gui-how-to-play.md",
]

EXPECTED_REQUIRED_CAPABILITIES = ["es-modules", "fetch", "native-svg", "css-grid"]
EXPECTED_OPTIONAL_CAPABILITIES = ["web-audio", "local-storage"]
EXPECTED_QUEUE = [
  ("chromium-evergreen-desktop", "technical-contract-pass"),
  ("low-power-browser-proxy", "emulated-proxy-pass"),
  ("firefox-desktop", "pending-runtime-check"),
  ("webkit-desktop", "pending-runtime-check"),
  ("real-hardware", "pending-device-check"),
  ("human-accessibility-usability", "pending-human-review"),
]
EXPECTED_REVIEW_BOUNDARY = {
  "technical_packet_complete": True,
  "declared_browser_matrix_complete": True,
  "chromium_target_check_complete": True,
  "emulated_low_power_proxy_check_complete": True,
  "firefox_runtime_certification_complete": False,
  "webkit_runtime_certification_complete": False,
  "real_device_certification_complete": False,
  "hardware_performance_certification_complete": False,
  "human_accessibility_review_complete": False,
  "human_usability_review_complete": False,
  "public_release_approval": False,
}
EXPECTED_FORBIDDEN_CLAIMS = [
  "Firefox is supported",
  "WebKit is supported",
  "Firefox/WebKit certified",
  "real-device certification complete",
  "battery certification complete",
  "human accessibility review complete",
  "public release approved",
]


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


def run_json_command(*args):
  result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
  if result.returncode != 0:
    raise AssertionError(f"command failed: {' '.join(args)}\n{result.stderr}")
  return json.loads(result.stdout)


class Phase13CrossBrowserDeviceReviewPacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    cls.browser_policy = load_json(BROWSER_POLICY_PATH)
    cls.device_policy = load_json(DEVICE_POLICY_PATH)
    cls.loading_policy = load_json(LOADING_POLICY_PATH)
    cls.offline_policy = load_json(OFFLINE_POLICY_PATH)
    cls.technical_coverage = load_json(TECHNICAL_COVERAGE_PATH)

  def test_packet_is_technical_only_and_fail_closed(self):
    self.assertEqual(self.packet["schema_version"], "phase13.1-cross-browser-device-review-packet-v1")
    self.assertEqual(self.packet["status"], "complete-technical-packet-pending-runtime-certification")
    self.assertEqual(self.packet["roadmap_item"], "cross-browser/device certification")
    self.assertEqual(self.packet["review_boundary"], EXPECTED_REVIEW_BOUNDARY)
    self.assertEqual(self.packet["release_boundary"]["public_release_approval"], False)
    self.assertTrue(self.packet["release_boundary"]["technical_packet_does_not_authorize_support_promotion"])
    self.assertEqual(
      {key: self.packet["release_boundary"][key] for key in (
        "runtime_changes", "simulation_changes", "asset_changes", "audio_changes",
        "screenshot_changes", "release_manifest_changes",
      )},
      {key: 0 for key in (
        "runtime_changes", "simulation_changes", "asset_changes", "audio_changes",
        "screenshot_changes", "release_manifest_changes",
      )},
    )

  def test_shared_sources_and_source_markers_are_exact(self):
    self.assertEqual(self.packet["shared_sources"], EXPECTED_SHARED_SOURCES)
    for relative in EXPECTED_SHARED_SOURCES:
      self.assertTrue((ROOT / relative).is_file(), relative)
    markers = self.packet["source_contract"]["required_source_markers"]
    source_text = {
      "browser_policy": BROWSER_POLICY_PATH.read_text(encoding="utf-8"),
      "device_policy": DEVICE_POLICY_PATH.read_text(encoding="utf-8"),
      "guides": (
        (ROOT / "docs/guides/reproducible-distribution.md").read_text(encoding="utf-8")
        + (ROOT / "docs/guides/gui-how-to-play.md").read_text(encoding="utf-8")
      ),
      "technical_coverage": TECHNICAL_COVERAGE_PATH.read_text(encoding="utf-8"),
      "validators": (
        (ROOT / "scripts/check_browser_compatibility.py").read_text(encoding="utf-8")
        + (ROOT / "scripts/check_device_performance.py").read_text(encoding="utf-8")
        + (ROOT / "tests/test_browser_compatibility.py").read_text(encoding="utf-8")
        + (ROOT / "tests/test_device_performance.py").read_text(encoding="utf-8")
      ),
    }
    self.assertEqual(set(markers), {"browser_policy", "device_policy", "guides", "technical_coverage", "validators"})
    for source_id, required in markers.items():
      for marker in required:
        self.assertIn(marker, source_text[source_id], f"{source_id}: {marker}")

  def test_browser_contract_mirrors_policy_and_checker(self):
    contract = self.packet["browser_contract"]
    policy_fields = {
      "policy_schema_version": "schema_version",
      "policy_status": "status",
      "surface": "surface",
      "entrypoint": "entrypoint",
    }
    for field, policy_field in policy_fields.items():
      self.assertEqual(contract[field], self.browser_policy[policy_field], field)
    self.assertEqual(contract["supported_targets"], self.browser_policy["supported_targets"])
    self.assertEqual(contract["not_certified_targets"], self.browser_policy["not_certified_targets"])
    required = [item["id"] for item in self.browser_policy["capabilities"] if item["required"]]
    optional = [item["id"] for item in self.browser_policy["capabilities"] if not item["required"]]
    self.assertEqual(required, EXPECTED_REQUIRED_CAPABILITIES)
    self.assertEqual(optional, EXPECTED_OPTIONAL_CAPABILITIES)
    self.assertEqual(contract["required_capabilities"], required)
    self.assertEqual(contract["optional_capabilities"], optional)
    self.assertEqual(contract["capabilities"], self.browser_policy["capabilities"])
    self.assertEqual(contract["boundary_checks"], self.browser_policy["boundary_checks"])
    report = run_json_command(sys.executable, "scripts/check_browser_compatibility.py")
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["supported_targets"], contract["supported_targets"])
    self.assertEqual(report["not_certified_targets"], contract["not_certified_targets"])
    self.assertEqual(contract["check_status"], {
      "overall": report["status"],
      "loading_policy": report["loading_policy_status"],
      "offline_policy": report["offline_policy_status"],
      "syntax": report["syntax_status"],
      "authority_boundary": report["boundary_status"],
    })

  def test_device_contract_mirrors_policy_and_checker(self):
    contract = self.packet["device_contract"]
    policy_fields = {
      "policy_schema_version": "schema_version",
      "policy_status": "status",
      "surface": "surface",
      "live_entrypoint": "live_entrypoint",
    }
    for field, policy_field in policy_fields.items():
      self.assertEqual(contract[field], self.device_policy[policy_field], field)
    self.assertEqual(contract["profile"], self.device_policy["profile"])
    self.assertEqual(contract["limits"], self.device_policy["limits"])
    self.assertEqual(contract["measurements"], self.device_policy["measurements"])
    self.assertEqual(contract["evidence"], self.device_policy["evidence"])
    self.assertEqual(contract["certification"], self.device_policy["certification"])
    self.assertEqual(contract["check_status"], "pass")
    report = run_json_command(sys.executable, "scripts/check_device_performance.py")
    self.assertEqual(report["status"], "pass")
    self.assertEqual(report["profile"], contract["profile"])
    self.assertEqual(report["measurements"], contract["measurements"])

  def test_loading_offline_and_technical_coverage_boundaries_are_bound(self):
    self.assertEqual(self.packet["browser_contract"]["entrypoint"], self.loading_policy["live_entrypoint"])
    self.assertEqual(self.packet["device_contract"]["live_entrypoint"], self.loading_policy["live_entrypoint"])
    self.assertEqual(self.packet["device_contract"]["profile"]["network"], self.offline_policy["local_origin"]["binding"])
    self.assertEqual(self.offline_policy["local_origin"]["binding"], "loopback-only")
    check_ids = {check["id"]: check for check in self.technical_coverage["checks"]}
    self.assertEqual(check_ids["chromium-compatibility"]["status"], "pass-declared-target")
    self.assertEqual(check_ids["accessibility-presentation-contract"]["status"], "pass-technical-contract")
    self.assertIn("Firefox/WebKit", " ".join(self.technical_coverage["limits"]))
    self.assertIn("real hardware", " ".join(self.technical_coverage["limits"]))

  def test_queue_questions_limits_and_claims_remain_pending(self):
    self.assertEqual(
      [(item["id"], item["status"]) for item in self.packet["runtime_certification_queue"]],
      EXPECTED_QUEUE,
    )
    self.assertEqual(len(self.packet["review_tasks"]), 7)
    self.assertTrue(all(task.endswith(".") for task in self.packet["review_tasks"]))
    self.assertEqual(len(self.packet["evidence_limits"]), 5)
    limits = " ".join(self.packet["evidence_limits"])
    for marker in ("Firefox", "WebKit", "real-device", "battery", "thermal", "human usability", "public-release"):
      self.assertIn(marker, limits)
    forbidden = self.packet["source_contract"]["forbidden_claim_markers"]
    self.assertEqual(forbidden, EXPECTED_FORBIDDEN_CLAIMS)
    non_boundary_text = json.dumps({
      "browser_contract": self.packet["browser_contract"],
      "device_contract": self.packet["device_contract"],
      "runtime_certification_queue": self.packet["runtime_certification_queue"],
    })
    for marker in forbidden:
      self.assertNotIn(marker, non_boundary_text)

  def test_existing_contract_tests_remain_authoritative(self):
    result = subprocess.run(
      [
        sys.executable,
        "-m",
        "unittest",
        "tests.test_browser_compatibility",
        "tests.test_device_performance",
        "tests.test_phase13_technical_coverage",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
  unittest.main()
