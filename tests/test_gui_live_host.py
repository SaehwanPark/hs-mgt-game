import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
SERVER = ROOT / "src" / "gui_server.rs"


class GuiLiveHostTests(unittest.TestCase):
  def test_live_host_and_static_demo_boundaries_are_present(self):
    adapter = ADAPTER.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    server = SERVER.read_text(encoding="utf-8")
    self.assertIn("HS_MGT_GAME_HOST_ADAPTER", html)
    self.assertNotIn('src="./host-adapter.mjs"', html)
    self.assertIn("host-adapter.mjs", server)
    self.assertIn("deny_unknown_fields", server)
    self.assertIn("scenario_path: None", server)
    self.assertIn("HsMgtGameActionAdapter", adapter)
    self.assertIn("Demo fixture loaded; start a host session to play", app)
    self.assertNotIn("campaignCoverageClient.load(sessionId)", app)
    self.assertEqual(app.count("campaignCoverageClient.load(requestedSessionId)"), 2)

  def test_local_adapter_maps_requests_and_preserves_session_on_failure(self):
    script = r'''
      import { createLocalActionAdapter } from "./gui/host-adapter.mjs";
      const calls = [];
      let fail = false;
      const fetchImpl = async (path, options = {}) => {
        calls.push({ path, options });
        if (fail) return { ok: false, status: 404, async json() { return { error: "unknown session" }; } };
        if (path === "/api/v1/sessions") return { ok: true, status: 200, async json() { return { session_id: "session-1" }; } };
        return { ok: true, status: 200, async json() { return { schema_version: "ok" }; } };
      };
      const adapter = createLocalActionAdapter({ fetchImpl });
      await adapter.startSession({ campaign: "competitive-regional-v1", seed: 42, difficulty: "normal" });
      if (adapter.sessionId !== null) process.exit(1);
      await adapter.getPresentation("session-1");
      if (adapter.sessionId !== null) process.exit(9);
      adapter.activateSession("session-1");
      if (adapter.sessionId !== "session-1") process.exit(10);
      await adapter.validateTurn("session-1", "hold");
      await adapter.submitTurn("hold");
      await adapter.getResolution("session-1", 1);
      await adapter.endSession("session-1");
      if (calls[0].path !== "/api/v1/sessions" || calls[0].options.method !== "POST") process.exit(2);
      if (calls[2].path !== "/api/v1/sessions/session-1/validation") process.exit(3);
      if (JSON.parse(calls[3].options.body).command_text !== "hold") process.exit(4);
      if (!calls[4].path.endsWith("/resolution?turn=1")) process.exit(5);
      if (calls[5].path !== "/api/v1/sessions/session-1/end" || calls[5].options.method !== "POST") process.exit(11);
      fail = true;
      try { await adapter.getPresentation("session-2"); process.exit(6); } catch (error) {
        if (!error.message.includes("unknown session")) process.exit(7);
      }
      if (adapter.sessionId !== "session-1") process.exit(8);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_changed_javascript_parses(self):
    for path in (ADAPTER, APP):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
