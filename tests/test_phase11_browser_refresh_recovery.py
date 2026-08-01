import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
GUIDE = ROOT / "docs" / "guides" / "gui-how-to-play.md"
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"
SERVER = ROOT / "src" / "gui_server.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
PERSISTENCE = ROOT / "src" / "mcp" / "persistence.rs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"


class BrowserRefreshRecoveryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.guide = GUIDE.read_text(encoding="utf-8")
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")
    cls.persistence = PERSISTENCE.read_text(encoding="utf-8")
    cls.adapter = ADAPTER.read_text(encoding="utf-8")

  def run_node(self, script):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    return json.loads(result.stdout)

  def test_storage_is_opaque_optional_and_safe_when_blocked(self):
    result = self.run_node(r'''
      import { ACTIVE_SESSION_STORAGE_KEY, createSessionIdStorage } from "./gui/app.mjs";
      const values = new Map();
      const storage = {
        getItem(key) { return values.get(key) ?? null; },
        setItem(key, value) { values.set(key, value); },
        removeItem(key) { values.delete(key); },
      };
      const session = createSessionIdStorage({ storage });
      const empty = session.get();
      const stored = session.set(" session-7 ") && session.get();
      const key = values.get(ACTIVE_SESSION_STORAGE_KEY);
      const cleared = session.clear() && session.get();
      const blocked = createSessionIdStorage({
        storage: {
          getItem() { throw new Error("blocked"); },
          setItem() { throw new Error("blocked"); },
          removeItem() { throw new Error("blocked"); },
        },
      });
      console.log(JSON.stringify({ empty, stored, key, cleared, blockedGet: blocked.get(), blockedSet: blocked.set("session-8"), blockedClear: blocked.clear() }));
    ''')
    self.assertEqual(
      result,
      {
        "empty": None,
        "stored": "session-7",
        "key": "session-7",
        "cleared": None,
        "blockedGet": None,
        "blockedSet": False,
        "blockedClear": False,
      },
    )

  def test_launcher_persists_success_and_clears_only_unknown_session(self):
    result = self.run_node(r'''
      import { createSessionLauncher } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of ["#session-launch-form", "#session-start", "#session-id", "#session-load", "#session-launch-status", "#session-campaign", "#session-seed", "#session-difficulty"]) {
        nodes.set(selector, {
          value: selector === "#session-campaign" ? "competitive-regional-v1" : selector === "#session-seed" ? "42" : selector === "#session-difficulty" ? "normal" : "",
          textContent: "",
          disabled: false,
          addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); },
        });
      }
      const ids = [];
      let mode = "ok";
      const sessionStore = {
        get() { return ids.at(-1) ?? null; },
        set(value) { ids.push(`set:${value}`); return true; },
        clear() { ids.push("clear"); return true; },
      };
      const adapter = { async startSession() { return { session_id: "session-new" }; } };
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
      createSessionLauncher({ adapter, root, sessionStore, load: async (sessionId) => mode === "unknown"
        ? { ok: false, code: "action_adapter_error", message: `unknown session '${sessionId}'` }
        : mode === "transient" ? { ok: false, code: "action_adapter_error", message: "temporary host failure" }
        : { ok: true, envelope: { session_id: sessionId } } });
      await listeners.get("#session-launch-form:submit")({ preventDefault() {} });
      nodes.get("#session-id").value = "session-existing";
      await listeners.get("#session-load:click")({ preventDefault() {} });
      mode = "transient";
      await listeners.get("#session-load:click")({ preventDefault() {} });
      mode = "unknown";
      await listeners.get("#session-load:click")({ preventDefault() {} });
      console.log(JSON.stringify({ ids, status: nodes.get("#session-launch-status").textContent }));
    ''')
    self.assertEqual(
      result,
      {
        "ids": ["set:session-new", "set:session-existing", "clear"],
        "status": "unknown session 'session-existing'",
      },
    )

  def test_checkpoint_discovery_validates_metadata_and_only_fills_the_opaque_id(self):
    result = self.run_node(r'''
      import { renderCheckpointDiscovery, validateCheckpointDiscoveryEnvelope } from "./gui/app.mjs";
      const input = { value: "" };
      const list = { children: [], replaceChildren(...items) { this.children = items; }, append(...items) { this.children.push(...items); } };
      const status = { textContent: "" };
      const root = { querySelector(selector) { return { "#session-checkpoint-list": list, "#session-checkpoint-status": status, "#session-id": input }[selector] ?? null; } };
      globalThis.document = { createElement(tag) { return { tag, children: [], textContent: "", append(...items) { this.children.push(...items); }, addEventListener(_type, handler) { this.handler = handler; } }; } };
      const envelope = { schema_version: "gui-checkpoint-discovery-v1", invalid_entry_count: 0, checkpoints: [{ session_id: "session-7", campaign: "stabilization-v1", seed: 42, transition_count: 2, storage: "archive" }] };
      const rendered = renderCheckpointDiscovery(envelope, root);
      const initialStatus = status.textContent;
      list.children[0].children[0].handler();
      const invalid = validateCheckpointDiscoveryEnvelope({ ...envelope, checkpoints: [{ ...envelope.checkpoints[0], storage: "raw-save" }] });
      console.log(JSON.stringify({ rendered: rendered.ok, input: input.value, initialStatus, status: status.textContent, invalid: invalid.code }));
    ''')
    self.assertEqual(result["rendered"], True)
    self.assertEqual(result["input"], "session-7")
    self.assertIn("valid checkpoint", result["initialStatus"])
    self.assertIn("ready to load", result["status"])
    self.assertEqual(result["invalid"], "invalid_checkpoint_discovery_entry")
    self.assertIn("listCheckpoints", self.adapter)
    self.assertIn('request("/api/v1/checkpoints")', self.adapter)
    self.assertIn('"/api/v1/checkpoints"', self.server)
    self.assertIn("get_checkpoint_discovery", self.session)
    self.assertIn("discover_gui_session_checkpoints", self.persistence)
    self.assertIn("gui-checkpoint-discovery-v1", self.session)
    self.assertIn("session-checkpoints-refresh", self.html)
    self.assertIn("session-checkpoint-list", self.html)
    self.assertIn("Save contents remain host-only", self.html)

  def test_refresh_contract_and_authority_boundary_are_explicit(self):
    for marker in (
      "ACTIVE_SESSION_STORAGE_KEY",
      "createSessionIdStorage",
      "const storedSessionId = client.sessionStore.get()",
      "client.load(initialSessionId)",
      "isUnknownSessionResult",
      "sessionStore.clear()",
      "host process",
    ):
      self.assertIn(marker, self.app + self.html + self.guide)
    for forbidden in (
      "transition_competitive",
      "resolved_inputs",
      "CompetitiveWorldState",
      "effect_queue",
      "WebSocket",
      "serializeState",
    ):
      self.assertNotIn(forbidden, self.app)

  def test_action_client_retries_host_load_after_unknown_live_session(self):
    result = self.run_node(r'''
      function node() {
        return {
          children: [], dataset: {}, classList: { add() {}, toggle() {} },
          hidden: false, value: "", textContent: "", disabled: false,
          replaceChildren(...items) { this.children = items; },
          append(...items) { this.children.push(...items); },
          appendChild(item) { this.children.push(item); },
          addEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; },
          setAttribute() {}, removeAttribute() {}, focus() {},
        };
      }
      const nodes = new Map();
      const root = {
        documentElement: node(),
        querySelector(selector) { if (!nodes.has(selector)) nodes.set(selector, node()); return nodes.get(selector); },
        querySelectorAll() { return []; }, addEventListener() {}, removeEventListener() {},
      };
      globalThis.document = undefined;
      const { createActionClient } = await import("./gui/app.mjs");
      globalThis.document = { createElement: () => node(), documentElement: node() };
      globalThis.matchMedia = () => ({ matches: false });
      const calls = [];
      const presentation = {
        schema_version: "competitive-read-only-v1",
        session: { session_id: "session-7", campaign: "competitive-regional-v1", turn: 1, max_turns: 24 },
        observation: {}, institutions: [], resources: {}, pending_effects: [], history: [], replay: {},
      };
      const adapter = {
        sessionId: null,
        campaign: null,
        async getPresentation() { calls.push("presentation"); if (!this.sessionId) throw new Error("unknown session 'session-7'"); return presentation; },
        async loadSession(sessionId) { calls.push("load"); this.sessionId = sessionId; this.campaign = "competitive-regional-v1"; return { schema_version: "competitive-save-v1", operation: "loaded", session_id: sessionId, campaign: "competitive-regional-v1", seed: 42, transition_count: 0, latest_state_hash: null }; },
        async getActionCatalog() { calls.push("catalog"); return { schema_version: "competitive-actions-v1", turn: 1, actions: [] }; },
        async validateTurn() { return { valid: true, previews: [], errors: [] }; },
      };
      const values = new Map();
      const storage = { getItem(key) { return values.get(key) ?? null; }, setItem(key, value) { values.set(key, value); }, removeItem(key) { values.delete(key); } };
      const client = createActionClient({ adapter, root, storage });
      const result = await client.load("session-7");
      console.log(JSON.stringify({ ok: result.ok, calls, sessionId: client.sessionStore.get() }));
    ''')
    self.assertEqual(
      result,
      {"ok": True, "calls": ["presentation", "load", "presentation", "catalog"], "sessionId": "session-7"},
    )

  def test_durable_recovery_remains_host_only(self):
    for marker in (
      "GUI_COMPETITIVE_SAVE_SCHEMA_VERSION",
      "GUI_STABILIZATION_SAVE_SCHEMA_VERSION",
      "GUI_AFFILIATION_SAVE_SCHEMA_VERSION",
      "with_competitive_persistence",
      "hydrate_durable_session",
      "competitive_session_from_save",
      "stabilization_session_from_save",
      "affiliation_session_from_save",
      "gui-stabilization-save-v1",
      "gui-affiliation-save-v1",
      "Recovering durable host checkpoint",
      "allowDurableRecovery",
      "loadSession(requestedSessionId)",
      "competitive-save-v1",
    ):
      self.assertIn(marker, self.app + self.server + self.session + self.persistence)
    for forbidden in (
      "CompetitiveWorldState",
      "resolved_inputs",
      "serializeState",
      "history.transitions",
    ):
      self.assertNotIn(forbidden, self.app)

  def test_ledger_records_same_host_boundary_and_limits(self):
    coverage = self.ledger["browser_refresh_coverage"]
    self.assertEqual(coverage["status"], "complete-same-host-browser-recovery")
    self.assertEqual(coverage["storage_key"], "hs-mgt-active-session-id")
    self.assertIn("opaque", coverage["stored_value"])
    self.assertIn("cross-process", " ".join(coverage["limits"]))
    self.assertIn("tests/test_phase11_browser_refresh_recovery.py", coverage["test_source"])

  def test_full_campaign_checkpoint_continuity_is_host_bound(self):
    coverage = self.ledger["full_campaign_checkpoint_continuity"]
    self.assertEqual(
      coverage["status"],
      "complete-competitive-full-campaign-host-checkpoint-continuation",
    )
    self.assertEqual(coverage["checkpoint_turn"], 12)
    self.assertEqual(coverage["terminal_turn"], 24)
    self.assertEqual(
      coverage["test_source"],
      "src/mcp/session.rs: fn competitive_durable_checkpoint_covers_full_campaign_continuation",
    )
    self.assertEqual(
      coverage["comparison_surfaces"],
      [
        "competitive-replay-v1",
        "competitive-regional-world-v1",
        "campaign-coverage-v1",
      ],
    )
    for marker in (
      "fn competitive_durable_checkpoint_covers_full_campaign_continuation",
      "get_replay(GetReplayRequest",
      "get_regional_world(GetRegionalWorldRequest",
      "get_campaign_coverage(GetCampaignCoverageRequest",
      "end_session(EndSessionRequest",
    ):
      self.assertIn(marker, self.session)
    self.assertTrue(any("browser" in item.lower() for item in coverage["limits"]))

  def test_full_stabilization_checkpoint_continuity_is_host_bound(self):
    coverage = self.ledger["full_stabilization_checkpoint_continuity"]
    self.assertEqual(
      coverage["status"],
      "complete-stabilization-full-campaign-host-checkpoint-continuation",
    )
    self.assertEqual(coverage["checkpoint_stage"], 2)
    self.assertEqual(coverage["terminal_stage"], 5)
    self.assertEqual(
      coverage["test_source"],
      "src/mcp/session.rs: fn durable_stabilization_checkpoint_covers_full_campaign_continuation",
    )
    self.assertEqual(
      coverage["comparison_surfaces"],
      ["competitive-history-v1", "competitive-replay-v1", "campaign-coverage-v1"],
    )
    for marker in (
      "fn durable_stabilization_checkpoint_covers_full_campaign_continuation",
      "get_history(GetHistoryRequest",
      "get_replay(GetReplayRequest",
      "get_campaign_coverage(GetCampaignCoverageRequest",
      "end_session(EndSessionRequest",
    ):
      self.assertIn(marker, self.session)
    self.assertTrue(any("browser" in item.lower() for item in coverage["limits"]))

  def test_full_affiliation_checkpoint_continuity_is_host_bound(self):
    coverage = self.ledger["full_affiliation_checkpoint_continuity"]
    self.assertEqual(
      coverage["status"],
      "complete-affiliation-full-campaign-host-checkpoint-continuation",
    )
    self.assertEqual(coverage["checkpoint_stage"], 3)
    self.assertEqual(coverage["terminal_stage"], 6)
    self.assertEqual(
      coverage["test_source"],
      "src/mcp/session.rs: fn durable_affiliation_checkpoint_covers_full_campaign_continuation",
    )
    self.assertEqual(
      coverage["comparison_surfaces"],
      [
        "competitive-history-v1",
        "competitive-replay-v1",
        "campaign-coverage-v1",
      ],
    )
    for marker in (
      "fn durable_affiliation_checkpoint_covers_full_campaign_continuation",
      "get_history(GetHistoryRequest",
      "get_replay(GetReplayRequest",
      "get_campaign_coverage(GetCampaignCoverageRequest",
      "end_session(EndSessionRequest",
    ):
      self.assertIn(marker, self.session)
    self.assertTrue(any("browser" in item.lower() for item in coverage["limits"]))

  def test_cross_campaign_checkpoint_identity_is_host_bound(self):
    coverage = self.ledger["cross_campaign_checkpoint_identity"]
    self.assertEqual(
      coverage["status"],
      "complete-cross-campaign-per-session-archive-identity",
    )
    self.assertEqual(
      coverage["checkpoint_schemas"],
      [
        "gui-competitive-save-v1",
        "gui-stabilization-save-v1",
        "gui-affiliation-save-v1",
      ],
    )
    self.assertEqual(
      coverage["archive_directory_suffix"],
      ".checkpoints",
    )
    self.assertEqual(
      coverage["archived_campaigns"],
      [
        "competitive-regional-v1",
        "stabilization-v1",
        "regional-affiliation-v1",
      ],
    )
    self.assertEqual(
      coverage["test_source"],
      "src/mcp/session.rs: fn durable_checkpoint_archive_preserves_cross_campaign_identity",
    )
    for marker in (
      "fn durable_checkpoint_archive_preserves_cross_campaign_identity",
      "checkpoint_missing",
      "gui-competitive-save-v1",
      "gui-stabilization-save-v1",
      "gui-affiliation-save-v1",
      "gui_session_checkpoint_path",
      "load_gui_session_checkpoint",
      "remove_gui_session_checkpoint",
      ".checkpoints",
      "end_session(EndSessionRequest",
    ):
      self.assertIn(marker, self.session + self.persistence)
    self.assertTrue(any("browser serialization" in item.lower() for item in coverage["limits"]))

  def test_checkpoint_discovery_is_typed_metadata_only(self):
    coverage = self.ledger["checkpoint_discovery"]
    self.assertEqual(coverage["status"], "complete-host-browser-metadata-discovery")
    self.assertEqual(coverage["schema"], "gui-checkpoint-discovery-v1")
    self.assertEqual(coverage["route"], "GET /api/v1/checkpoints")
    self.assertEqual(coverage["storage_sources"], ["archive", "legacy"])
    self.assertEqual(
      coverage["metadata_fields"],
      ["session_id", "campaign", "seed", "transition_count", "storage"],
    )
    for marker in (
      "discover_gui_session_checkpoints",
      "get_checkpoint_discovery",
      "listCheckpoints",
      "renderCheckpointDiscovery",
      "session-checkpoints-refresh",
      "Use this session ID",
      "gui-checkpoint-discovery-v1",
    ):
      self.assertIn(
        marker,
        self.persistence + self.session + self.adapter + self.app + self.html + json.dumps(coverage),
      )
    for boundary in (
      "without exposing their contents",
      "without loading automatically",
      "Save contents remain host-only",
      "browser save serialization",
    ):
      self.assertIn(boundary, json.dumps(coverage) + self.html)


if __name__ == "__main__":
  unittest.main()
