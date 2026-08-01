import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.1-firefox-runtime-smoke-packet.json"
PROBE_PATH = ROOT / "scripts" / "check_firefox_runtime_smoke.py"
BROWSER_POLICY_PATH = ROOT / "assets" / "browser-compatibility-policy.json"

EXPECTED_SHELL = {
  "title": "Health Policy Strategy Game — Executive Desktop",
  "ready": "complete",
  "start_control": True,
  "demo_fixture": True,
  "url": "http://127.0.0.1:7878/",
}
EXPECTED_HOST_START = {
  "status": "competitive regional session loaded: session-1",
  "session": "session-1",
  "demo_fixture": False,
  "checkpoint_saved": True,
  "stored_session_id": "session-1",
}
EXPECTED_RESUME = {
  "status": "Host session refreshed after browser refresh: session-1",
  "session": "session-1",
  "stored_session_id": "session-1",
  "demo_fixture": False,
  "ready": "complete",
}
EXPECTED_REVIEW_BOUNDARY = {
  "firefox_shell_runtime_smoke_complete": True,
  "firefox_host_backed_start_smoke_complete": True,
  "firefox_browser_refresh_resume_smoke_complete": True,
  "firefox_full_campaign_certification_complete": False,
  "firefox_audio_decoder_review_complete": False,
  "webkit_runtime_certification_complete": False,
  "real_device_certification_complete": False,
  "hardware_performance_certification_complete": False,
  "human_accessibility_review_complete": False,
  "human_usability_review_complete": False,
  "public_release_approval": False,
}


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase13FirefoxRuntimeSmokePacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    cls.browser_policy = load_json(BROWSER_POLICY_PATH)
    spec = importlib.util.spec_from_file_location("check_firefox_runtime_smoke", PROBE_PATH)
    cls.probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.probe)

  def test_packet_is_observed_smoke_only(self):
    self.assertEqual(self.packet["schema_version"], "phase13.1-firefox-runtime-smoke-packet-v1")
    self.assertEqual(self.packet["status"], "complete-firefox-host-backed-smoke-pending-matrix")
    self.assertEqual(self.packet["roadmap_item"], "cross-browser/device certification")
    self.assertEqual(self.packet["policy_boundary"]["canonical_browser_policy_unchanged"], True)
    self.assertEqual(self.packet["policy_boundary"]["firefox_policy_status"], "not-certified")
    self.assertEqual(self.packet["policy_boundary"]["webkit_policy_status"], "not-certified")
    self.assertTrue(self.packet["policy_boundary"]["smoke_result_does_not_promote_browser_support"])
    self.assertEqual(self.packet["review_boundary"], EXPECTED_REVIEW_BOUNDARY)

  def test_runtime_observation_is_exact_and_host_backed(self):
    observation = self.packet["runtime_observation"]
    self.assertEqual(observation["status"], "pass")
    self.assertEqual(observation["url"], "http://127.0.0.1:7878/")
    self.assertEqual(observation["marionette_protocol"], 3)
    self.assertEqual(observation["browser"], {
      "name": "firefox",
      "version": "147.0.2",
      "platform": "mac",
      "headless": True,
    })
    self.assertEqual(observation["shell"], EXPECTED_SHELL)
    self.assertEqual(observation["host_start"], EXPECTED_HOST_START)
    self.assertEqual(observation["browser_refresh_resume"], EXPECTED_RESUME)
    self.assertTrue(self.packet["probe"]["writes_project_state"] is False)

  def test_probe_source_and_browser_policy_boundaries_are_exact(self):
    probe_text = PROBE_PATH.read_text(encoding="utf-8")
    for marker in self.packet["required_source_markers"]["probe"]:
      self.assertIn(marker, probe_text, marker)
    policy_text = BROWSER_POLICY_PATH.read_text(encoding="utf-8")
    for marker in self.packet["required_source_markers"]["browser_policy"]:
      self.assertIn(marker, policy_text, marker)
    guides_text = (
      (ROOT / "docs/guides/reproducible-distribution.md").read_text(encoding="utf-8")
      + (ROOT / "docs/guides/gui-how-to-play.md").read_text(encoding="utf-8")
    )
    for marker in self.packet["required_source_markers"]["guides"]:
      self.assertIn(marker, guides_text, marker)
    target_ids = {target["id"] for target in self.browser_policy["not_certified_targets"]}
    self.assertIn("firefox-desktop", target_ids)
    self.assertIn("webkit-desktop", target_ids)

  def test_safari_blocker_and_release_boundary_are_explicit(self):
    safari = self.packet["safari_webkit_boundary"]
    self.assertEqual(safari["status"], "blocked-permission")
    self.assertEqual(safari["support_status"], "not-certified")
    self.assertFalse(safari["runtime_result_recorded"])
    self.assertIn("Allow remote automation", safari["message"])
    limits = " ".join(self.packet["evidence_limits"])
    for marker in ("full-campaign", "audio decoding", "real hardware", "lived accessibility", "human", "public-release"):
      self.assertIn(marker, limits)
    release = self.packet["release_boundary"]
    self.assertTrue(all(release[key] == 0 for key in (
      "runtime_changes", "simulation_changes", "asset_changes", "audio_changes",
      "screenshot_changes", "release_manifest_changes",
    )))
    self.assertFalse(release["public_release_approval"])
    self.assertTrue(release["technical_packet_does_not_authorize_support_promotion"])

  def test_probe_is_valid_python_without_writing_bytecode(self):
    parsed = ast.parse(PROBE_PATH.read_text(encoding="utf-8"), filename=str(PROBE_PATH))
    self.assertIsNotNone(parsed)

  def test_probe_rejects_invalid_observations_and_non_loopback_urls(self):
    observation = self.packet["runtime_observation"]
    self.probe.validate_observations(
      observation["shell"],
      observation["host_start"],
      observation["url"],
      observation["browser"],
      observation["marionette_protocol"],
      observation["browser_refresh_resume"],
    )
    bad_host = dict(observation["host_start"])
    bad_host["status"] = "stabilization session loaded: session-1"
    with self.assertRaises(RuntimeError):
      self.probe.validate_observations(
        observation["shell"],
        bad_host,
        observation["url"],
        observation["browser"],
        observation["marionette_protocol"],
        observation["browser_refresh_resume"],
      )
    bad_browser = dict(observation["browser"])
    bad_browser["headless"] = False
    with self.assertRaises(RuntimeError):
      self.probe.validate_observations(
        observation["shell"],
        observation["host_start"],
        observation["url"],
        bad_browser,
        observation["marionette_protocol"],
        observation["browser_refresh_resume"],
      )
    with self.assertRaises(RuntimeError):
      self.probe.validate_observations(
        observation["shell"],
        observation["host_start"],
        "https://example.com/",
        observation["browser"],
        observation["marionette_protocol"],
        observation["browser_refresh_resume"],
      )
    with self.assertRaises(RuntimeError):
      self.probe._validate_loopback_url("http://example.com/")
    with self.assertRaises(RuntimeError):
      self.probe._validate_loopback_url("http://localhost:7878/")

  def test_existing_browser_device_and_technical_checks_remain_authoritative(self):
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
