import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
AUDIO = ROOT / "gui" / "audio.mjs"
PLAYTEST = ROOT / "gui" / "playtest.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
DOC = ROOT / "docs" / "visual-audio-phase8-ai-agent-testplay-v0.12.24.md"
SCRIPT = ROOT / "scripts" / "diagnose_gui_playtests.py"
FIXTURE = ROOT / "tests" / "fixtures" / "gui_playtest_capture.json"

SPEC = importlib.util.spec_from_file_location("diagnose_gui_playtests", SCRIPT)
DIAGNOSTICS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(DIAGNOSTICS)


class GuiPlaytestTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.playtest = PLAYTEST.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_readiness_contract_and_controls_are_present(self):
    for marker in (
      "gui-playtest-v1",
      "PLAYTEST_CAPTURE_SCHEMA",
      "createPlaytestRecorder",
      "semanticSnapshot",
      "recordFailure",
      "recordHistory",
      "PLAYTEST_FAILURE_CLASSES",
      "createPresentationSettings",
      "recovery_retry",
      "onboarding_opened",
      "recordVisibleEnvelope",
      "recordAudio",
    ):
      self.assertIn(marker, self.playtest + self.app + self.audio)
    for selector in (
      'id="onboarding-panel"',
      'id="onboarding-next"',
      'id="settings-panel"',
      'id="settings-reduced-motion"',
      'id="settings-text-equivalents"',
      'id="recovery-panel"',
      'id="recovery-retry"',
    ):
      self.assertIn(selector, self.html)

  def test_recorder_is_allowlisted_and_deterministic(self):
    result = subprocess.run(
      [
        "node",
        "--input-type=module",
        "-e",
        "import { createPlaytestRecorder } from './gui/playtest.mjs'; const recorder = createPlaytestRecorder({ metadata: { campaign: 'stabilization-v1', role: 'first-time', task: 'demo' } }); recorder.record('command_submitted', { campaign: 'stabilization-v1', command: 'hold', turn: 1, raw_payload: { hidden: true } }); console.log(JSON.stringify(recorder.capture()));",
      ],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    capture = json.loads(result.stdout)
    self.assertEqual(capture["schema_version"], "gui-playtest-v1")
    self.assertNotIn("raw_payload", result.stdout)
    self.assertEqual(capture["events"][0]["sequence"], 0)
    self.assertNotIn("raw_payload", capture["events"][0])

  def test_diagnostics_accept_fixture_and_reject_forbidden_fields(self):
    capture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = DIAGNOSTICS.validate_capture(capture)
    self.assertEqual(result["issues"], [])
    self.assertEqual(result["event_count"], 7)
    self.assertEqual(result["evidence_lanes"]["human_question"], "unresolved")

    forbidden = json.loads(json.dumps(capture))
    forbidden["true_state"] = {"cash": 100}
    invalid = DIAGNOSTICS.validate_capture(forbidden)
    self.assertIn("capture_invalid", {entry["class"] for entry in invalid["issues"]})

    camel_case_forbidden = json.loads(json.dumps(capture))
    camel_case_forbidden["events"][0]["rawPayload"] = {"hidden": True}
    invalid = DIAGNOSTICS.validate_capture(camel_case_forbidden)
    self.assertIn("capture_invalid", {entry["class"] for entry in invalid["issues"]})

    unknown_evidence = json.loads(json.dumps(capture))
    unknown_evidence["evidence"]["unexpected"] = []
    invalid = DIAGNOSTICS.validate_capture(unknown_evidence)
    self.assertIn("capture_invalid", {entry["class"] for entry in invalid["issues"]})

    hidden_camel_case = json.loads(json.dumps(capture))
    hidden_camel_case["events"][2]["sections"][0]["worldState"] = {"cash": 100}
    invalid = DIAGNOSTICS.validate_capture(hidden_camel_case)
    self.assertIn("capture_invalid", {entry["class"] for entry in invalid["issues"]})

    malformed_snapshot = json.loads(json.dumps(capture))
    malformed_snapshot["events"][2]["controls"] = "not-a-list"
    invalid = DIAGNOSTICS.validate_capture(malformed_snapshot)
    self.assertIn("capture_invalid", {entry["class"] for entry in invalid["issues"]})

  def test_diagnostics_cli_and_docs_define_evidence_limits(self):
    result = subprocess.run(
      ["python3", str(SCRIPT), str(FIXTURE)],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    output = json.loads(result.stdout)
    self.assertEqual(output["schema_version"], "gui-playtest-v1")

    unsupported_path = FIXTURE.with_name("gui_playtest_capture_unsupported.json")
    unsupported = json.loads(FIXTURE.read_text(encoding="utf-8"))
    unsupported["schema_version"] = "gui-playtest-v0"
    unsupported_path.write_text(json.dumps(unsupported), encoding="utf-8")
    try:
      unsupported_result = subprocess.run(
        ["python3", str(SCRIPT), str(unsupported_path)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
      )
      self.assertEqual(unsupported_result.returncode, 2)
    finally:
      unsupported_path.unlink(missing_ok=True)
    for marker in (
      "## Readiness contract",
      "## Browser behavior",
      "## Roles and tasks",
      "## Diagnostics and failure classes",
      "technical correctness",
      "human usability",
      "screenshot references",
      "Phase 9",
    ):
      self.assertIn(marker, self.doc)
    for marker in (
      "gui-playtest-v1",
      "diagnose_gui_playtests.py",
      "reduced motion",
      "retry",
    ):
      self.assertIn(marker, self.readme.lower())

  def test_javascript_syntax_and_no_external_capture_boundary_break(self):
    for path in (APP, AUDIO, PLAYTEST):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)
    for forbidden in (
      "fetch(",
      "WebSocket",
      "http://",
      "https://",
      "WorldState",
      "ResolvedInputs",
      "effect_queue",
      "private_rival",
    ):
      self.assertNotIn(forbidden, self.playtest)


if __name__ == "__main__":
  unittest.main()
