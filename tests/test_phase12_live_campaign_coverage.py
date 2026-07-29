import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-live-campaign-coverage.json"

EXPECTED_SOURCE_CONTRACT = {
  "gui_route": (
    "src/gui_server.rs",
    "/api/v1/sessions/{session_id}/campaign-coverage",
  ),
  "session_identity_route": ("src/gui_server.rs", "/api/v1/sessions/{session_id}"),
  "gui_store_call": ("src/gui_server.rs", "GetCampaignCoverageRequest"),
  "gui_launch_boundary": (
    "src/gui_server.rs",
    "GUI_CAMPAIGN_COVERAGE_CAMPAIGNS",
  ),
  "host_adapter": ("gui/host-adapter.mjs", "getCampaignCoverage"),
  "launcher_campaign_set": ("gui/app.mjs", "SESSION_LAUNCH_CAMPAIGNS"),
  "campaign_fallback": ("gui/app.mjs", "loadCampaignCoverage"),
  "campaign_renderer": ("gui/app.mjs", "renderCampaignCoverage"),
  "campaign_audio_projection": ("src/mcp/campaign_coverage.rs", "CampaignCoverageAudio"),
  "campaign_audio_client": ("gui/app.mjs", "campaignMusicStateId"),
  "canonical_mutation": ("gui/app.mjs", "adapter.submitTurn(command)"),
}


class Phase12LiveCampaignCoverageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_ledger_and_source_contract_are_exact(self):
    self.assertEqual(
      self.ledger["status"],
      "complete-current-technical-browser-and-audio-handoff-only",
    )
    self.assertEqual(
      self.ledger["campaigns"],
      ["stabilization-v1", "regional-affiliation-v1"],
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key],
        f"{source_path}: {marker}",
      )
      source = (ROOT / source_path).read_text(encoding="utf-8")
      self.assertIn(marker, " ".join(source.split()), key)
    self.assertEqual(
      self.ledger["findings"],
      {
        "loopback_route_uses_existing_typed_projection": True,
        "both_campaign_coverage_campaigns_are_launchable": True,
        "competitive_difficulty_and_action_path_remain_separate": True,
        "campaign_decisions_use_host_submit_turn": True,
        "existing_session_campaign_is_resolved_from_host": True,
        "rejected_campaign_decisions_do_not_advance_history": True,
        "campaign_audio_metadata_uses_existing_catalog_only": True,
        "explicit_empty_campaign_cues_disable_legacy_fallback": True,
        "browser_true_state_or_new_authority_added": False,
        "campaign_specific_visual_audio_quality_review": False,
        "human_accessibility_educational_or_public_release_review": False,
      },
    )

  def test_gui_surfaces_keep_campaign_and_authority_boundaries_visible(self):
    html = (ROOT / "gui" / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    adapter = (ROOT / "gui" / "host-adapter.mjs").read_text(encoding="utf-8")
    for marker in (
      'value="stabilization-v1"',
      'value="regional-affiliation-v1"',
      'id="campaign-coverage-panel"',
    ):
      self.assertIn(marker, html)
    for marker in (
      "campaign-coverage-v1",
      "SESSION_LAUNCH_CAMPAIGNS",
      "getCampaignCoverage",
      "loadCampaignCoverage",
      "adapter.submitTurn(command)",
      "campaignMusicStateId",
      "campaignAudioCueIds",
      "setMusicState(musicStateId, audioInput)",
      "competitive-regional-v1",
    ):
      self.assertIn(marker, app + adapter)
    for forbidden in (
      "WorldState",
      "ResolvedInputs",
      "resolved_inputs",
      "effect_queue",
      "fetch(\"https://",
    ):
      self.assertNotIn(forbidden, app)

  def test_launcher_accepts_campaign_coverage_campaign_without_difficulty(self):
    script = r'''
      import { createSessionLauncher } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of [
        "#session-launch-form", "#session-start", "#session-id", "#session-load",
        "#session-launch-status", "#session-campaign", "#session-seed", "#session-difficulty",
      ]) {
        nodes.set(selector, {
          value: selector === "#session-campaign" ? "stabilization-v1"
            : selector === "#session-seed" ? "42"
              : selector === "#session-difficulty" ? "not-used" : "",
          textContent: "",
          disabled: false,
          addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); },
        });
      }
      const calls = [];
      const adapter = {
        async startSession(options) { calls.push(options); return { session_id: "session-new", campaign: options.campaign }; },
      };
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
      createSessionLauncher({ adapter, root, load: async () => ({ ok: true, envelope: {} }) });
      await listeners.get("#session-launch-form:submit")({ preventDefault() {} });
      if (JSON.stringify(calls) !== JSON.stringify([{ campaign: "stabilization-v1", seed: 42 }])) process.exit(1);
      if (!nodes.get("#session-start").textContent.includes("stabilization")) process.exit(2);
      if (!nodes.get("#session-difficulty").disabled) process.exit(3);
      console.log(JSON.stringify({ calls }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_campaign_audio_projection_honors_allowlist_empty_and_legacy_fallback(self):
    script = r'''
      import { campaignAudioCueIds, campaignMusicStateId } from "./gui/app.mjs";
      const direct = {
        audio: {
          music_state_id: "affiliation_negotiation",
          audio_cue_ids: ["event.affiliation-milestone", "not-a-cue"],
        },
      };
      if (campaignMusicStateId(direct) !== "affiliation_negotiation") process.exit(1);
      if (JSON.stringify(campaignAudioCueIds(direct)) !== JSON.stringify(["event.affiliation-milestone"])) process.exit(2);
      if (campaignAudioCueIds({ audio: { audio_cue_ids: [] } }).length !== 0) process.exit(3);
      if (campaignAudioCueIds({}) !== null) process.exit(4);
      if (campaignMusicStateId({ audio: { music_state_id: "" } }) !== null) process.exit(5);
      console.log(JSON.stringify({ direct: campaignMusicStateId(direct), empty: campaignAudioCueIds({ audio: { audio_cue_ids: [] } }) }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_campaign_client_applies_host_audio_after_load_and_refresh(self):
    script = r'''
      function makeNode(tagName = "div") {
        return {
          tagName: tagName.toUpperCase(),
          children: [],
          dataset: {},
          classList: { add() {}, toggle() {} },
          hidden: false,
          value: "",
          textContent: "",
          append(...children) { this.children.push(...children); },
          replaceChildren(...children) { this.children = children; },
          addEventListener() {},
          setAttribute(name, value) { this[name] = value; },
          removeAttribute(name) { delete this[name]; },
          querySelector() { return null; },
          querySelectorAll() { return []; },
          focus() {},
          scrollIntoView() {},
        };
      }
      const documentStub = { createElement: (tagName) => makeNode(tagName), documentElement: makeNode("html") };
      globalThis.document = undefined;
      globalThis.matchMedia = () => ({ matches: false });
      const { createCampaignCoverageClient } = await import("./gui/app.mjs");
      globalThis.document = documentStub;
      const root = {
        __hsMgtPresentationSettings: null,
        documentElement: makeNode("html"),
        querySelector() { return makeNode(); },
        querySelectorAll() { return []; },
        addEventListener() {},
      };
      const calls = [];
      const audio = {
        state() { return { muted: false, reducedNotifications: false }; },
        setMuted() {},
        setReducedNotifications() {},
        setMusicState(id) { calls.push(["music", id]); },
        setMusicFromVisible() { calls.push(["legacy-music"]); },
        setAmbienceFromVisible() {},
        playCue(id) { calls.push(["cue", id]); },
      };
      const envelope = {
        schema_version: "campaign-coverage-v1",
        campaign_role: "Affiliation",
        session: { session_id: "coverage-audio", campaign: "regional-affiliation-v1", turn: 1, max_turns: 6, done: false },
        stage: { label: "Assess partner", detail: "Visible stage" },
        briefing: [], metrics: [], actors: [], processes: [], decisions: [], history: [], debrief: [],
        audio: { music_state_id: "affiliation_negotiation", audio_cue_ids: ["event.affiliation-milestone"] },
      };
      const adapter = {
        sessionId: "coverage-audio",
        async getCampaignCoverage() { return envelope; },
        async submitTurn() { envelope.audio = { music_state_id: "affiliation_negotiation", audio_cue_ids: [] }; return { accepted: true }; },
      };
      const client = createCampaignCoverageClient({ adapter, root, audio });
      await client.load();
      if (!calls.some(([kind, id]) => kind === "music" && id === "affiliation_negotiation")) process.exit(1);
      calls.length = 0;
      const result = await client.submit("host-shaped");
      if (!result.ok) process.exit(2);
      if (calls.some(([kind, id]) => kind === "cue" && id === "event.affiliation-milestone")) process.exit(3);
      console.log(JSON.stringify({ calls }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_campaign_history_renders_decision_time_observation_disclosure(self):
    script = r'''
      function makeNode(tagName = "div") {
        return {
          tagName: tagName.toUpperCase(),
          children: [],
          dataset: {},
          classList: { add() {}, toggle() {} },
          hidden: false,
          textContent: "",
          append(...children) { this.children.push(...children); },
          replaceChildren(...children) { this.children = children; },
          addEventListener() {},
          setAttribute(name, value) { this[name] = value; },
          removeAttribute(name) { delete this[name]; },
          querySelector() { return null; },
          querySelectorAll() { return []; },
          focus() {},
        };
      }
      globalThis.document = undefined;
      const { renderCampaignCoverage } = await import("./gui/app.mjs");
      globalThis.document = { createElement: (tagName) => makeNode(tagName), documentElement: makeNode("html") };
      const nodes = new Map();
      const root = {
        querySelector(selector) {
          if (!nodes.has(selector)) nodes.set(selector, makeNode());
          return nodes.get(selector);
        },
        querySelectorAll() { return []; },
      };
      const result = renderCampaignCoverage({
        schema_version: "campaign-coverage-v1",
        campaign_role: "Stabilization",
        session: { campaign: "stabilization-v1", turn: 2, max_turns: 5 },
        stage: { label: "Turn 2", detail: "Visible stage" },
        briefing: [], metrics: [], actors: [], processes: [], decisions: [], debrief: [],
        history: [{ turn: 1, command: "stabilize", state_hash: "hash-1", observation: ["Turn 1", "Cash: 100"] }],
      }, root);
      if (!result.ok) process.exit(1);
      const history = nodes.get("#campaign-history-list");
      const item = history.children[0];
      const details = item.children.find((child) => child.tagName === "DETAILS");
      if (!details || details.children[0].textContent !== "Decision-time observation") process.exit(2);
      if (!details.children[1].children.some((line) => line.textContent === "Cash: 100")) process.exit(3);
      console.log(JSON.stringify({ detail: details.children[0].textContent, lines: details.children[1].children.length }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_campaign_coverage_rail_advances_only_after_host_refresh(self):
    script = r'''
      function makeNode(tagName = "div") {
        return {
          tagName: tagName.toUpperCase(),
          children: [],
          dataset: {},
          classList: { add() {}, toggle() {} },
          hidden: false,
          value: "",
          textContent: "",
          append(...children) { this.children.push(...children); },
          replaceChildren(...children) { this.children = children; },
          addEventListener() {},
          setAttribute(name, value) { this[name] = value; },
          removeAttribute(name) { delete this[name]; },
          querySelector() { return null; },
          querySelectorAll() { return []; },
          focus() {},
        };
      }
      function makeRoot() {
        const nodes = new Map();
        return {
          documentElement: makeNode("html"),
          querySelector(selector) {
            if (!nodes.has(selector)) nodes.set(selector, makeNode());
            return nodes.get(selector);
          },
          querySelectorAll() { return []; },
          addEventListener() {},
        };
      }
      const documentStub = { createElement: (tagName) => makeNode(tagName), documentElement: makeNode("html") };
      globalThis.document = undefined;
      const { createActionClient } = await import("./gui/app.mjs");
      globalThis.document = documentStub;
      globalThis.matchMedia = () => ({ matches: false });

      const envelope = {
        schema_version: "campaign-coverage-v1",
        campaign_role: "Stabilization",
        session: { session_id: "coverage-1", campaign: "stabilization-v1", turn: 1, max_turns: 5 },
        stage: { label: "Assess", detail: "Visible stage" },
        briefing: [], metrics: [], actors: [], processes: [],
        decisions: [{ label: "Assess", command_template: "assess", parameters: [], uncertainty: "Visible uncertainty" }],
        history: [], debrief: [],
      };
      function adapterFor({ reject = false, failRefreshAfterCommit = false } = {}) {
        return {
          sessionId: "coverage-1",
          campaign: "stabilization-v1",
          malformed: false,
          failRefresh: false,
          activateSession(sessionId, campaign) { this.sessionId = sessionId; this.campaign = campaign; },
          async getCampaignCoverage() {
            if (this.failRefresh) throw new Error("coverage refresh failed");
            if (this.malformed) return { ...envelope, schema_version: "unsupported" };
            return envelope;
          },
          async submitTurn(command) {
            if (reject) throw new Error("host rejected decision");
            if (command !== "assess") throw new Error("unexpected command");
            this.failRefresh = failRefreshAfterCommit;
            return { accepted: true };
          },
        };
      }

      const client = createActionClient({ adapter: adapterFor(), root: makeRoot() });
      await client.load("coverage-1");
      if (client.firstMonthFlow.stage.id !== "choose") process.exit(1);
      const accepted = await client.campaignCoverage.submit("assess");
      if (!accepted.ok || client.firstMonthFlow.stage.id !== "continue") process.exit(2);

      const rejectedClient = createActionClient({ adapter: adapterFor({ reject: true }), root: makeRoot() });
      await rejectedClient.load("coverage-1");
      const rejected = await rejectedClient.campaignCoverage.submit("assess");
      if (rejected.ok || rejectedClient.firstMonthFlow.stage.id !== "choose") process.exit(3);

      const malformedAdapter = adapterFor();
      const malformedClient = createActionClient({ adapter: malformedAdapter, root: makeRoot() });
      await malformedClient.load("coverage-1");
      malformedAdapter.malformed = true;
      const malformed = await malformedClient.campaignCoverage.load("coverage-1");
      if (malformed.ok || malformedClient.firstMonthFlow.stage.id !== "choose") process.exit(4);

      const refreshFailureClient = createActionClient({
        adapter: adapterFor({ failRefreshAfterCommit: true }),
        root: makeRoot(),
      });
      await refreshFailureClient.load("coverage-1");
      const refreshFailure = await refreshFailureClient.campaignCoverage.submit("assess");
      if (refreshFailure.ok || refreshFailureClient.firstMonthFlow.stage.id !== "choose") process.exit(5);
      console.log(JSON.stringify({ accepted: client.firstMonthFlow.stage.id, rejected: rejectedClient.firstMonthFlow.stage.id, malformed: malformedClient.firstMonthFlow.stage.id, refreshFailure: refreshFailureClient.firstMonthFlow.stage.id }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
  unittest.main()
