import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
SERVER = ROOT / "src" / "gui_server.rs"
MCP_SERVER = ROOT / "src" / "mcp" / "server.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"


class LiveReplayContinuityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.adapter = ADAPTER.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.mcp_server = MCP_SERVER.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")

  def test_host_replay_route_and_browser_boundary_are_present(self):
    for marker in (
      "competitive-replay-v1",
      "ReplayEnvelope",
      "REPLAY_SCHEMA_VERSION",
      "GetReplayRequest",
      "get_replay",
      "regenerate_competitive_history",
      "replay_verification_failed",
      '"/api/v1/sessions/{session_id}/replay"',
    ):
      self.assertIn(marker, self.server + self.mcp_server + self.session)
    for marker in (
      "getReplay",
      "createReplayClient",
      "validateReplayEnvelope",
      "renderReplayEnvelope",
      "replayClient.load",
      "replay_adapter_missing",
      "replay_adapter_error",
    ):
      self.assertIn(marker, self.app + self.adapter)

  def test_replay_validation_and_capability_fallback_are_explicit(self):
    script = f"""
import {{ createReplayClient, validateReplayEnvelope }} from {APP.as_uri()!r};
const empty = {{
  schema_version: "competitive-replay-v1",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  seed: 42,
  transition_count: 0,
  latest_state_hash: null,
  transitions: [],
}};
const committed = {{
  ...empty,
  transition_count: 1,
  latest_state_hash: "hash-1",
  transitions: [{{ turn: 1, state_hash: "hash-1" }}],
}};
const invalidLatest = {{ ...committed, latest_state_hash: "hash-2" }};
const invalidTransitions = {{ ...empty, transitions: {{ not: "a list" }} }};
const missingAdapter = await createReplayClient({{ adapter: {{}}, root: {{}} }}).load("session-1");
const throwingAdapter = await createReplayClient({{
  adapter: {{ getReplay: async () => {{ throw new Error("read failed"); }} }},
  root: {{}},
}}).load("session-1");
console.log(JSON.stringify({{
  empty: validateReplayEnvelope(empty).ok,
  committed: validateReplayEnvelope(committed).ok,
  invalidLatest: validateReplayEnvelope(invalidLatest).code,
  invalidTransitions: validateReplayEnvelope(invalidTransitions).code,
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
        "empty": True,
        "committed": True,
        "invalidLatest": "misaligned_replay",
        "invalidTransitions": "misaligned_replay",
        "missingAdapter": "replay_adapter_missing",
        "throwingAdapter": "replay_adapter_error",
      },
    )

  def test_replay_client_renders_and_preserves_history_on_failure(self):
    script = f"""
import {{ createReplayClient }} from {APP.as_uri()!r};
function node() {{
  return {{
    children: [],
    append(...items) {{ this.children.push(...items); }},
    replaceChildren() {{ this.children = []; }},
    setAttribute() {{}},
    textContent: "",
  }};
}}
const list = node();
const meta = node();
globalThis.document = {{ createElement: node }};
const root = {{ querySelector(selector) {{ return selector === "#history-list" ? list : meta; }} }};
let shouldFail = false;
const adapter = {{
  async getReplay() {{
    if (shouldFail) throw new Error("temporary read failure");
    return {{
      schema_version: "competitive-replay-v1",
      session_id: "session-1",
      campaign: "competitive-regional-v1",
      seed: 42,
      transition_count: 1,
      latest_state_hash: "hash-1",
      transitions: [{{ turn: 1, state_hash: "hash-1" }}],
    }};
  }},
}};
const client = createReplayClient({{ adapter, root }});
const first = await client.load("session-1");
shouldFail = true;
const failed = await client.load("session-1");
console.log(JSON.stringify({{
  first: first.ok,
  failed: failed.code,
  renderedItems: list.children.length,
  renderedHash: list.children[0]?.children[2]?.textContent,
  cachedHash: client.envelope.latest_state_hash,
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
        "failed": "replay_adapter_error",
        "renderedItems": 1,
        "renderedHash": "state hash: hash-1",
        "cachedHash": "hash-1",
      },
    )

  def test_replay_playback_cursor_moves_and_reports_written_row_detail(self):
    script = f"""
import {{ createReplayClient }} from {APP.as_uri()!r};
function node() {{
  return {{
    children: [],
    attributes: {{}},
    disabled: false,
    textContent: "",
    append(...items) {{ this.children.push(...items); }},
    replaceChildren() {{ this.children = []; }},
    setAttribute(name, value) {{ this.attributes[name] = value; }},
    addEventListener() {{}},
  }};
}}
const nodes = Object.fromEntries([
  "#history-list",
  "#replay-playback-status",
  "#replay-previous",
  "#replay-play",
  "#replay-pause",
  "#replay-next",
].map((selector) => [selector, node()]));
globalThis.document = {{ createElement: node }};
const root = {{ querySelector(selector) {{ return nodes[selector]; }} }};
const envelope = {{
  schema_version: "competitive-replay-v1",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  seed: 42,
  transition_count: 2,
  latest_state_hash: "hash-2",
  transitions: [
    {{ turn: 1, command: "hold", observation: ["Visible context"], events: ["event one"], effects: ["effect one"], state_hash: "hash-1" }},
    {{ turn: 2, command: "invest", observation: ["Updated context"], events: [], effects: ["effect two"], state_hash: "hash-2" }},
  ],
}};
const client = createReplayClient({{ adapter: {{ getReplay: async () => envelope }}, root }});
const loaded = await client.load("session-1");
const next = client.next();
const previous = client.previous();
const played = client.play();
const paused = client.pause();
console.log(JSON.stringify({{
  loaded: loaded.ok,
  loadedIndex: loaded.index,
  nextIndex: next.index,
  previousIndex: previous.index,
  played: played.ok,
  paused: paused.ok,
  selectedIndex: client.selectedIndex,
  selected: nodes["#history-list"].children[0].attributes["aria-current"] === "true",
  status: nodes["#replay-playback-status"].textContent,
  previousDisabled: nodes["#replay-previous"].disabled,
  nextDisabled: nodes["#replay-next"].disabled,
}}));
"""
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    report = json.loads(result.stdout)
    self.assertEqual(
      {key: report[key] for key in ("loaded", "loadedIndex", "nextIndex", "previousIndex", "played", "paused", "selectedIndex", "selected", "previousDisabled", "nextDisabled")},
      {"loaded": True, "loadedIndex": 0, "nextIndex": 1, "previousIndex": 0, "played": True, "paused": True, "selectedIndex": 0, "selected": True, "previousDisabled": True, "nextDisabled": False},
    )
    self.assertIn("observation: Visible context", report["status"])
    self.assertIn("effects: effect one", report["status"])
    self.assertIn("Paused.", report["status"])

  def test_replay_playback_empty_state_and_failed_read_preserve_cursor(self):
    script = f"""
import {{ createReplayClient }} from {APP.as_uri()!r};
function node() {{
  return {{
    children: [],
    attributes: {{}},
    disabled: false,
    textContent: "",
    append(...items) {{ this.children.push(...items); }},
    replaceChildren() {{ this.children = []; }},
    setAttribute(name, value) {{ this.attributes[name] = value; }},
    addEventListener() {{}},
  }};
}}
const nodes = Object.fromEntries([
  "#history-list",
  "#replay-playback-status",
  "#replay-previous",
  "#replay-play",
  "#replay-pause",
  "#replay-next",
].map((selector) => [selector, node()]));
globalThis.document = {{ createElement: node }};
const root = {{ querySelector(selector) {{ return nodes[selector]; }} }};
const empty = {{ schema_version: "competitive-replay-v1", session_id: "session-1", campaign: "competitive-regional-v1", seed: 42, transition_count: 0, latest_state_hash: null, transitions: [] }};
const committed = {{ ...empty, transition_count: 2, latest_state_hash: "hash-2", transitions: [{{ turn: 1, state_hash: "hash-1" }}, {{ turn: 2, state_hash: "hash-2" }}] }};
let fail = false;
const client = createReplayClient({{ adapter: {{ getReplay: async () => {{ if (fail) throw new Error("temporary read failure"); return fail ? empty : committed; }} }}, root }});
await client.load("session-1");
client.next();
client.previous();
client.play();
fail = true;
const failed = await client.load("session-1");
const failureStatus = nodes["#replay-playback-status"].textContent;
const failurePlayDisabled = nodes["#replay-play"].disabled;
const failurePauseDisabled = nodes["#replay-pause"].disabled;
const emptyClient = createReplayClient({{ adapter: {{ getReplay: async () => empty }}, root }});
const emptyResult = await emptyClient.load("session-1");
const emptyNext = emptyClient.next();
console.log(JSON.stringify({{
  failed: failed.code,
  preservedIndex: client.selectedIndex,
  preservedHash: client.envelope.latest_state_hash,
  failureStatus,
  failurePlayDisabled,
  failurePauseDisabled,
  empty: emptyResult.ok,
  emptyNext: emptyNext.code,
  emptyStatus: nodes["#replay-playback-status"].textContent,
  emptyPlayDisabled: nodes["#replay-play"].disabled,
  emptyNextDisabled: nodes["#replay-next"].disabled,
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
        "failed": "replay_adapter_error",
        "preservedIndex": 0,
        "preservedHash": "hash-2",
        "failureStatus": "Reviewing replay row 1 of 2 · Turn 1 · command — · no additional visible row detail · state hash hash-1. Paused.",
        "failurePlayDisabled": False,
        "failurePauseDisabled": True,
        "empty": True,
        "emptyNext": "replay_empty",
        "emptyStatus": "No committed replay rows yet.",
        "emptyPlayDisabled": True,
        "emptyNextDisabled": True,
      },
    )

  def test_replay_playback_controller_has_no_transition_or_regeneration_authority(self):
    controller = self.app.split("export function createReplayClient", 1)[1].split(
      "export function createCheckpointClient", 1
    )[0]
    for forbidden in ("submitTurn", "transition_competitive", "resolved_inputs", "fetch("):
      self.assertNotIn(forbidden, controller)
    for marker in (
      "replay-previous",
      "replay-play",
      "replay-pause",
      "replay-next",
      "replay-playback-status",
      "aria-current",
      "setInterval",
    ):
      self.assertIn(marker, self.app + (ROOT / "gui" / "index.html").read_text(encoding="utf-8"))

  def test_live_replay_read_does_not_expose_simulation_authority(self):
    for forbidden in (
      "transition_competitive",
      "resolved_inputs",
      "effect_queue",
      "CompetitiveWorldState",
      "WebSocket",
    ):
      self.assertNotIn(forbidden, self.app)
      self.assertNotIn(forbidden, self.server)
    replay_handler = self.server.split("async fn get_replay", 1)[1].split("async fn end_session", 1)[0]
    self.assertIn("store.get_replay(GetReplayRequest { session_id })", replay_handler)
    self.assertNotIn("submit_turn", replay_handler)
    self.assertIn("self.get_history(GetHistoryRequest", self.session)

  def test_live_replay_scripts_are_syntactically_valid(self):
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
