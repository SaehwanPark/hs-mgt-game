import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
HTML = ROOT / "gui" / "index.html"
SERVER = ROOT / "src" / "gui_server.rs"
MCP_SERVER = ROOT / "src" / "mcp" / "server.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"


class LiveCheckpointContinuityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.adapter = ADAPTER.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.mcp_server = MCP_SERVER.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")

  def test_host_checkpoint_routes_controls_and_browser_boundary_are_present(self):
    for marker in (
      "competitive-save-v1",
      "SaveEnvelope",
      "SAVE_SCHEMA_VERSION",
      "SaveSessionRequest",
      "LoadSessionRequest",
      "save_session",
      "load_session",
      '"/api/v1/sessions/{session_id}/save"',
      '"/api/v1/sessions/{session_id}/load"',
      "checkpoints",
    ):
      self.assertIn(marker, self.server + self.mcp_server + self.session)
    for marker in (
      "saveSession",
      "loadSession",
      "createCheckpointClient",
      "validateSaveEnvelope",
      "checkpoint_refresh_error",
      "checkpoint_save_error",
      "checkpoint_autosave_error",
      "checkpoint_load_error",
      "checkpoint_missing",
      "autosave",
      "automatic",
      "ui.save-complete",
    ):
      self.assertIn(marker, self.app + self.adapter)
    for selector in (
      'id="session-save"',
      'id="session-restore"',
      "Save host checkpoint",
      "Restore host checkpoint",
      "autosave through the same host-only checkpoint path",
    ):
      self.assertIn(selector, self.html)

  def test_autosave_reuses_checkpoint_client_and_preserves_committed_session_on_failure(self):
    script = f"""
import {{ createCheckpointClient }} from {APP.as_uri()!r};
const saved = {{
  schema_version: "competitive-save-v1",
  operation: "saved",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  seed: 42,
  transition_count: 1,
  latest_state_hash: "hash-1",
}};
function node() {{ return {{ disabled: false, textContent: "", addEventListener() {{}} }}; }}
const root = {{ querySelector() {{ return node(); }} }};
const cues = [];
let calls = 0;
const adapter = {{ async saveSession() {{ calls += 1; return saved; }} }};
const client = createCheckpointClient({{ adapter, root, audio: {{ playCue(id) {{ cues.push(id); }} }} }});
client.setEnabled(true);
const autosaved = await client.autosave("session-1");
const failing = createCheckpointClient({{ adapter: {{ async saveSession() {{ throw new Error("disk full"); }} }}, root }});
failing.setEnabled(true);
const failure = await failing.autosave("session-1");
console.log(JSON.stringify({{ autosaved: autosaved.ok, automatic: autosaved.automatic, calls, cues, failure: failure.code }}));
"""
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(
      json.loads(result.stdout),
      {
        "autosaved": True,
        "automatic": True,
        "calls": 1,
        "cues": ["ui.save-complete"],
        "failure": "checkpoint_autosave_error",
      },
    )

  def test_autosave_is_after_host_acceptance_for_competitive_and_campaign_paths(self):
    for marker in (
      "response = await adapter.submitTurn(validation.canonical_command_text);",
      "await checkpointClient.autosave(sessionId);",
      "const response = await adapter.submitTurn(command);",
      "if (typeof autosave === \"function\") await autosave(adapter.sessionId);",
      "autosave: (sessionId) => checkpointClient.autosave(sessionId)",
      "current session remains active",
    ):
      self.assertIn(marker, self.app + self.html + self.adapter)
    competitive_submit = self.app.index("response = await adapter.submitTurn(validation.canonical_command_text);")
    competitive_autosave = self.app.index("await checkpointClient.autosave(sessionId);")
    campaign_submit = self.app.index("const response = await adapter.submitTurn(command);")
    campaign_autosave = self.app.index("if (typeof autosave === \"function\") await autosave(adapter.sessionId);")
    self.assertLess(competitive_submit, competitive_autosave)
    self.assertLess(campaign_submit, campaign_autosave)

  def test_autosave_waits_for_an_existing_checkpoint_operation(self):
    script = f"""
import {{ createCheckpointClient }} from {APP.as_uri()!r};
const saved = {{
  schema_version: "competitive-save-v1",
  operation: "saved",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  seed: 42,
  transition_count: 1,
  latest_state_hash: "hash-1",
}};
function node() {{ return {{ disabled: false, textContent: "", addEventListener() {{}} }}; }}
const root = {{ querySelector() {{ return node(); }} }};
const resolvers = [];
let calls = 0;
const adapter = {{
  saveSession() {{ calls += 1; return new Promise((resolve) => resolvers.push(resolve)); }},
}};
const client = createCheckpointClient({{ adapter, root }});
client.setEnabled(true);
const manual = client.save("session-1");
await new Promise((resolve) => setTimeout(resolve, 0));
const automatic = client.autosave("session-1");
await new Promise((resolve) => setTimeout(resolve, 0));
resolvers.shift()(saved);
await new Promise((resolve) => setTimeout(resolve, 0));
resolvers.shift()({{ ...saved, transition_count: 2, latest_state_hash: "hash-2" }});
const results = await Promise.all([manual, automatic]);
const concurrentOne = client.autosave("session-1");
const concurrentTwo = client.autosave("session-1");
await new Promise((resolve) => setTimeout(resolve, 0));
resolvers.shift()({{ ...saved, transition_count: 3, latest_state_hash: "hash-3" }});
await new Promise((resolve) => setTimeout(resolve, 0));
resolvers.shift()({{ ...saved, transition_count: 4, latest_state_hash: "hash-4" }});
const concurrent = await Promise.all([concurrentOne, concurrentTwo]);
console.log(JSON.stringify({{ calls, manual: results[0].ok, automatic: results[1].ok, automaticFlag: results[1].automatic, transitionCount: results[1].envelope.transition_count, concurrent: concurrent.map((result) => result.ok) }}));
"""
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(
      json.loads(result.stdout),
      {"calls": 4, "manual": True, "automatic": True, "automaticFlag": True, "transitionCount": 2, "concurrent": [True, True]},
    )

  def test_checkpoint_validation_capability_and_refresh_are_explicit(self):
    script = f"""
import {{ createCheckpointClient, validateSaveEnvelope }} from {APP.as_uri()!r};
const empty = {{
  schema_version: "competitive-save-v1",
  operation: "saved",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  seed: 42,
  transition_count: 0,
  latest_state_hash: null,
}};
const loaded = {{ ...empty, operation: "loaded", transition_count: 1, latest_state_hash: "hash-1" }};
const invalidOperation = {{ ...empty, operation: "rewound" }};
const invalidHash = {{ ...loaded, latest_state_hash: "" }};
function node() {{ return {{ disabled: false, textContent: "", addEventListener() {{}} }}; }}
const root = {{ querySelector() {{ return node(); }} }};
let refreshed = 0;
const adapter = {{
  async saveSession() {{ return empty; }},
  async loadSession() {{ return loaded; }},
}};
const client = createCheckpointClient({{
  adapter,
  root,
  refresh: async () => {{ refreshed += 1; return {{ ok: true, envelope: {{ session_id: "session-1" }} }}; }},
}});
client.setEnabled(true);
const saved = await client.save("session-1");
const restored = await client.load("session-1");
const missing = await createCheckpointClient({{ adapter: {{}}, root }}).save("session-1");
console.log(JSON.stringify({{
  empty: validateSaveEnvelope(empty).ok,
  loaded: validateSaveEnvelope(loaded).ok,
  invalidOperation: validateSaveEnvelope(invalidOperation).code,
  invalidHash: validateSaveEnvelope(invalidHash).code,
  saved: saved.ok,
  restored: restored.ok,
  refreshed,
  missing: missing.code,
}}));
"""
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(
      json.loads(result.stdout),
      {
        "empty": True,
        "loaded": True,
        "invalidOperation": "incomplete_save",
        "invalidHash": "incomplete_save",
        "saved": True,
        "restored": True,
        "refreshed": 1,
        "missing": "save_adapter_missing",
      },
    )

  def test_checkpoint_boundary_does_not_add_browser_or_route_simulation_authority(self):
    for forbidden in (
      "transition_competitive",
      "resolved_inputs",
      "effect_queue",
      "CompetitiveWorldState",
      "WebSocket",
    ):
      self.assertNotIn(forbidden, self.app)
      self.assertNotIn(forbidden, self.server)
    for function_name in ("async fn save_session", "async fn load_session"):
      handler = self.server.split(function_name, 1)[1].split("async fn ", 1)[0]
      self.assertNotIn("submit_turn", handler)
    self.assertIn("*session = snapshot", self.session)
    self.assertIn("checkpoint", self.session)

  def test_checkpoint_scripts_are_syntactically_valid(self):
    for path in (APP, ADAPTER):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, f"{path}: {result.stderr}")


if __name__ == "__main__":
  unittest.main()
