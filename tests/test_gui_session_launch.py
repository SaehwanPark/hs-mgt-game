import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "gui" / "index.html"
APP = ROOT / "gui" / "app.mjs"
README = ROOT / "gui" / "README.md"
DOC = ROOT / "docs" / "history" / "initiatives" / "visual-audio" / "visual-audio-phase11-session-launch-v0.12.27.md"


class GuiSessionLaunchTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_launch_controls_and_stable_contract_markers_exist(self):
    for marker in (
      'id="session-launch"',
      'id="session-launch-form"',
      'id="session-campaign"',
      'value="competitive-regional-v1"',
      'id="session-seed"',
      'id="session-difficulty"',
      'id="session-start"',
      'id="session-id"',
      'id="session-load"',
      'id="session-launch-status"',
      'aria-live="polite"',
    ):
      self.assertIn(marker, self.html)
    for marker in (
      "createSessionLauncher",
      "startSession",
      "session_id",
      "requestedSessionId",
      "sessionId = requestedSessionId",
    ):
      self.assertIn(marker, self.app)

  def test_documentation_keeps_host_boundary_and_non_goals_visible(self):
    combined = " ".join((self.doc + self.readme).lower().split())
    for marker in (
      "phase 11",
      "start_session",
      "host-authoritative",
      "does not create local session",
      "technical interface proxies",
    ):
      self.assertIn(marker, combined)
    for forbidden in (
      "CompetitiveWorldState",
      "resolved_inputs",
      "transition_competitive",
    ):
      self.assertNotIn(forbidden, self.app)

  def test_javascript_parses(self):
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_launcher_start_and_existing_load_use_host_boundary(self):
    script = r'''
      import { createSessionLauncher } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of [
        "#session-launch-form",
        "#session-start",
        "#session-id",
        "#session-load",
        "#session-launch-status",
        "#session-campaign",
        "#session-seed",
        "#session-difficulty",
      ]) {
        nodes.set(selector, {
          value: selector === "#session-campaign" ? "competitive-regional-v1"
            : selector === "#session-seed" ? "42"
              : selector === "#session-difficulty" ? "normal" : "",
          textContent: "",
          disabled: false,
          addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); },
        });
      }
      const adapter = {
        calls: [],
        async startSession(options) { this.calls.push(options); return { session_id: "session-new" }; },
      };
      const loaded = [];
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
      createSessionLauncher({ adapter, root, load: async (sessionId) => { loaded.push(sessionId); return { ok: true, envelope: { session_id: sessionId } }; } });
      await listeners.get("#session-launch-form:submit")({ preventDefault() {} });
      if (adapter.calls.length !== 1 || adapter.calls[0].campaign !== "competitive-regional-v1" || adapter.calls[0].seed !== 42 || adapter.calls[0].difficulty !== "normal") process.exit(1);
      if (loaded[0] !== "session-new" || nodes.get("#session-id").value !== "session-new") process.exit(2);
      nodes.get("#session-id").value = "session-existing";
      await listeners.get("#session-load:click")({ preventDefault() {} });
      if (loaded[1] !== "session-existing") process.exit(3);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_launcher_rejects_invalid_and_malformed_start_without_loading(self):
    script = r'''
      import { createSessionLauncher } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of [
        "#session-launch-form", "#session-start", "#session-id", "#session-load", "#session-launch-status",
        "#session-campaign", "#session-seed", "#session-difficulty",
      ]) nodes.set(selector, { value: selector === "#session-campaign" ? "competitive-regional-v1" : selector === "#session-seed" ? "not-a-seed" : selector === "#session-difficulty" ? "normal" : "", textContent: "", addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); } });
      let calls = 0;
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
      createSessionLauncher({ adapter: { async startSession() { calls += 1; return {}; } }, root, load: async () => { calls += 100; return { ok: true }; } });
      await listeners.get("#session-launch-form:submit")({ preventDefault() {} });
      if (calls !== 0 || !nodes.get("#session-launch-status").textContent.includes("non-negative integer")) process.exit(1);
      nodes.get("#session-seed").value = "42";
      await listeners.get("#session-launch-form:submit")({ preventDefault() {} });
      if (calls !== 1 || !nodes.get("#session-launch-status").textContent.includes("valid session ID")) process.exit(2);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_launcher_does_not_treat_demo_fixture_as_existing_session_load(self):
    script = r'''
      import { createSessionLauncher } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of ["#session-launch-form", "#session-start", "#session-id", "#session-load", "#session-launch-status", "#session-campaign", "#session-seed", "#session-difficulty"]) nodes.set(selector, { value: selector === "#session-campaign" ? "competitive-regional-v1" : selector === "#session-seed" ? "42" : selector === "#session-difficulty" ? "normal" : selector === "#session-id" ? "demo-id" : "", textContent: "", addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); } });
      let loaded = false;
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
      createSessionLauncher({ adapter: null, root, load: async () => { loaded = true; return { ok: true }; } });
      await listeners.get("#session-load:click")({ preventDefault() {} });
      if (loaded || !nodes.get("#session-launch-status").textContent.includes("requires a host adapter")) process.exit(1);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
