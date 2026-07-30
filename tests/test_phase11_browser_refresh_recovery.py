import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
GUIDE = ROOT / "docs" / "guides" / "gui-how-to-play.md"
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"


class BrowserRefreshRecoveryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.guide = GUIDE.read_text(encoding="utf-8")
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

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

  def test_ledger_records_same_host_boundary_and_limits(self):
    coverage = self.ledger["browser_refresh_coverage"]
    self.assertEqual(coverage["status"], "complete-same-host-browser-recovery")
    self.assertEqual(coverage["storage_key"], "hs-mgt-active-session-id")
    self.assertIn("opaque", coverage["stored_value"])
    self.assertIn("cross-process", " ".join(coverage["limits"]))
    self.assertIn("tests/test_phase11_browser_refresh_recovery.py", coverage["test_source"])


if __name__ == "__main__":
  unittest.main()
