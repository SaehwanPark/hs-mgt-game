import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
SERVER = ROOT / "src" / "gui_server.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"


class LiveHistoryHandoffTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.adapter = ADAPTER.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")

  def test_host_route_and_browser_history_boundary_are_present(self):
    for marker in (
      "competitive-history-v1",
      "HistoryEnvelope",
      "HISTORY_SCHEMA_VERSION",
      "GetHistoryRequest",
      "get_history",
      "get_competitive_history",
      "unsupported_gui_campaign_history",
      '"/api/v1/sessions/{session_id}/history"',
    ):
      self.assertIn(marker, self.server + self.session)
    for marker in (
      "getHistory",
      "createHistoryClient",
      "validateHistoryEnvelope",
      "renderHistoryEnvelope",
      "historyClient.load",
      "history_adapter_missing",
      "history_adapter_error",
    ):
      self.assertIn(marker, self.app + self.adapter)

  def test_history_client_validation_and_failure_are_explicit(self):
    script = f"""
import {{ createHistoryClient, validateHistoryEnvelope }} from {APP.as_uri()!r};
const valid = {{
  schema_version: "competitive-history-v1",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  transition_count: 1,
  transitions: [{{ turn: 1, state_hash: "hash-1" }}],
}};
const invalidCount = {{ ...valid, transition_count: 2 }};
const invalidSchema = {{ ...valid, schema_version: "future-history-v9" }};
const invalidMissingTurn = {{ ...valid, transitions: [{{ state_hash: "hash-1" }}] }};
const invalidStringTurn = {{ ...valid, transitions: [{{ turn: "1", state_hash: "hash-1" }}] }};
const invalidNegativeTurn = {{ ...valid, transitions: [{{ turn: -1, state_hash: "hash-1" }}] }};
const invalidCampaign = {{ ...valid, campaign: "stabilization-v1" }};
const missingAdapter = await createHistoryClient({{ adapter: {{}}, root: {{}} }}).load("session-1");
const throwingAdapter = await createHistoryClient({{
  adapter: {{ getHistory: async () => {{ throw new Error("read failed"); }} }},
  root: {{}},
}}).load("session-1");
console.log(JSON.stringify({{
  valid: validateHistoryEnvelope(valid).ok,
  invalidCount: validateHistoryEnvelope(invalidCount).code,
  invalidSchema: validateHistoryEnvelope(invalidSchema).code,
  invalidMissingTurn: validateHistoryEnvelope(invalidMissingTurn).code,
  invalidStringTurn: validateHistoryEnvelope(invalidStringTurn).code,
  invalidNegativeTurn: validateHistoryEnvelope(invalidNegativeTurn).code,
  invalidCampaign: validateHistoryEnvelope(invalidCampaign).code,
  missingAdapter: missingAdapter.code,
  throwingAdapter: throwingAdapter.code,
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
        "valid": True,
        "invalidCount": "incomplete_history",
        "invalidSchema": "unsupported_history_schema",
        "invalidMissingTurn": "incomplete_history",
        "invalidStringTurn": "incomplete_history",
        "invalidNegativeTurn": "incomplete_history",
        "invalidCampaign": "unsupported_history_campaign",
        "missingAdapter": "history_adapter_missing",
        "throwingAdapter": "history_adapter_error",
      },
    )

  def test_history_client_renders_and_preserves_view_on_failure(self):
    script = f"""
import {{ createHistoryClient }} from {APP.as_uri()!r};
function node() {{
  return {{
    children: [],
    hidden: false,
    append(...items) {{ this.children.push(...items); }},
    replaceChildren() {{ this.children = []; }},
    setAttribute() {{}},
    textContent: "",
    onclick: null,
  }};
}}
const list = node();
const meta = node();
const status = node();
const presentationState = node();
const recoveryPanel = node();
recoveryPanel.hidden = true;
const recoveryDetail = node();
const recoveryRetry = node();
globalThis.document = {{ createElement: node }};
const nodes = {{
  "#history-list": list,
  "#session-meta": meta,
  "#session-status": status,
  "#presentation-state": presentationState,
  "#recovery-panel": recoveryPanel,
  "#recovery-detail": recoveryDetail,
  "#recovery-retry": recoveryRetry,
}};
const root = {{ querySelector(selector) {{ return nodes[selector] ?? null; }} }};
let shouldFail = false;
const adapter = {{
  async getHistory() {{
    if (shouldFail) throw new Error("temporary read failure");
    return {{
      schema_version: "competitive-history-v1",
      session_id: "session-1",
      campaign: "competitive-regional-v1",
      transition_count: 1,
      transitions: [{{ turn: 1, state_hash: "hash-1" }}],
    }};
  }},
}};
const client = createHistoryClient({{ adapter, root }});
const first = await client.load("session-1");
shouldFail = true;
const failed = await client.load("session-1");
const failureVisible = !recoveryPanel.hidden;
const failureMessage = recoveryDetail.textContent;
shouldFail = false;
await recoveryRetry.onclick({{}});
console.log(JSON.stringify({{
  first: first.ok,
  failed: failed.code,
  renderedItems: list.children.length,
  renderedHash: list.children[0]?.children[2]?.textContent,
  cachedHash: client.envelope.transitions[0].state_hash,
  recoveryVisible: failureVisible,
  recoveryMessage: failureMessage,
  recoveryVisibleAfterRetry: !recoveryPanel.hidden,
  statusAfterRetry: status.textContent,
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
        "first": True,
        "failed": "history_adapter_error",
        "renderedItems": 1,
        "renderedHash": "state hash: hash-1",
        "cachedHash": "hash-1",
        "recoveryVisible": True,
        "recoveryMessage": "The current history view was preserved. Retry the live history read.",
        "recoveryVisibleAfterRetry": False,
        "statusAfterRetry": "Live history loaded from the host.",
      },
    )

  def test_live_history_read_does_not_expose_simulation_authority(self):
    for forbidden in (
      "transition_competitive",
      "resolved_inputs",
      "effect_queue",
      "CompetitiveWorldState",
      "WebSocket",
    ):
      self.assertNotIn(forbidden, self.app)
      self.assertNotIn(forbidden, self.server)
    history_handler = self.server.split("async fn get_history", 1)[1].split("async fn end_session", 1)[0]
    history_guard = self.server.split("fn get_competitive_history", 1)[1].split("async fn get_history", 1)[0]
    self.assertIn("get_competitive_history(store, session_id)", history_handler)
    self.assertIn("store.get_history(GetHistoryRequest { session_id })", history_guard)
    self.assertIn("unsupported_gui_campaign_history", history_guard)
    self.assertNotIn("submit_turn", history_handler)

  def test_live_history_scripts_are_syntactically_valid(self):
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
