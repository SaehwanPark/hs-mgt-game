import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
FLOW = ROOT / "gui" / "first-month.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
DOC = ROOT / "docs" / "visual-audio-phase13-first-month-continuity-v0.12.29.md"


class GuiFirstMonthTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.flow = FLOW.read_text(encoding="utf-8") if FLOW.exists() else ""
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_stage_function_covers_the_complete_first_month(self):
    script = r'''
      import { FIRST_MONTH_FLOW_SCHEMA, FIRST_MONTH_STAGES, firstMonthStageFor } from "./gui/first-month.mjs";
      const expected = ["start", "inspect", "draft", "validate", "submit", "resolution", "continue"];
      if (FIRST_MONTH_FLOW_SCHEMA !== "competitive-first-month-v1") process.exit(1);
      if (JSON.stringify(FIRST_MONTH_STAGES.map((stage) => stage.id)) !== JSON.stringify(expected)) process.exit(2);
      const states = [
        [{}, "start"],
        [{ sessionLoaded: true }, "inspect"],
        [{ sessionLoaded: true, actionCatalogLoaded: true }, "draft"],
        [{ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2 }, "validate"],
        [{ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2, validated: true }, "submit"],
        [{ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2, validated: true, submitted: true }, "resolution"],
        [{ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 0, submitted: true, resolutionVisible: true, refreshed: true }, "continue"],
        [{ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2, validated: true, submitted: true, resolutionVisible: true, refreshed: true }, "continue"],
      ];
      for (const [state, expectedStage] of states) {
        if (firstMonthStageFor(state) !== expectedStage) process.exit(10);
      }
      if (firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2, validated: true, submitted: true, resolutionVisible: true }) !== "resolution") process.exit(11);
      if (firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true, draftCount: -2 }) !== "draft") process.exit(12);
      console.log(JSON.stringify({ schema: FIRST_MONTH_FLOW_SCHEMA, stages: expected }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(json.loads(result.stdout)["stages"][-1], "continue")

  def test_renderer_exposes_text_first_current_completed_and_upcoming_states(self):
    script = r'''
      import { createFirstMonthFlow } from "./gui/first-month.mjs";
      function node() {
        return {
          children: [],
          dataset: {},
          hidden: false,
          textContent: "",
          replaceChildren(...children) { this.children = children; },
          append(...children) { this.children.push(...children); },
          setAttribute(name, value) { this[name] = value; },
          removeAttribute(name) { delete this[name]; },
        };
      }
      globalThis.document = { createElement: () => node() };
      const nodes = new Map([
        ["#first-month-flow-list", node()],
        ["#first-month-flow-state", node()],
        ["#first-month-flow-detail", node()],
      ]);
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; }, ownerDocument: globalThis.document };
      const flow = createFirstMonthFlow({ root });
      flow.update({ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2 });
      const list = nodes.get("#first-month-flow-list");
      if (list.children.length !== 7) process.exit(1);
      const states = list.children.map((item) => item.dataset.state);
      if (!states.includes("completed") || !states.includes("current") || !states.includes("upcoming")) process.exit(2);
      if (list.children[3]["aria-current"] !== "step") process.exit(3);
      if (!nodes.get("#first-month-flow-state").textContent.toLowerCase().includes("validate")) process.exit(4);
      if (!nodes.get("#first-month-flow-detail").textContent.includes("host")) process.exit(5);
      console.log(JSON.stringify({ stage: flow.stage.id, states }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(json.loads(result.stdout)["stage"], "validate")

  def test_host_adapter_sequence_reaches_continue_and_rejection_stays_recoverable(self):
    script = r'''
      function makeNode(tagName = "div") {
        const node = {
          tagName: tagName.toUpperCase(),
          children: [],
          dataset: {},
          classList: { add() {}, toggle() {} },
          listeners: {},
          hidden: false,
          value: "",
          textContent: "",
          append(...children) { this.children.push(...children); },
          replaceChildren(...children) { this.children = children; },
          addEventListener(type, listener) { (this.listeners[type] ??= []).push(listener); },
          dispatch(type, event = {}) { for (const listener of this.listeners[type] ?? []) listener(event); },
          setAttribute(name, value) { this[name] = value; },
          removeAttribute(name) { delete this[name]; },
          getAttribute(name) { return this[name] ?? null; },
          querySelector(selector) {
            if (selector === "button[type=submit]") return this.children.find((child) => child.tagName === "BUTTON") ?? null;
            return null;
          },
          querySelectorAll() { return []; },
          focus() {},
        };
        node.elements = { namedItem: () => null };
        return node;
      }
      function makeRoot() {
        const nodes = new Map();
        const root = {
          documentElement: makeNode("html"),
          querySelector(selector) {
            if (selector.startsWith("form[data-action-id=")) {
              const id = selector.match(/data-action-id=\\"([^\\"]+)\\"/)?.[1];
              return root.querySelector("#action-builder").children.find((child) => child.dataset.actionId === id) ?? null;
            }
            if (!nodes.has(selector)) nodes.set(selector, makeNode());
            return nodes.get(selector);
          },
          querySelectorAll(selector) {
            if (selector === "#resolution-step-list .resolution-step") return root.querySelector("#resolution-step-list").children;
            return [];
          },
          addEventListener() {},
          removeEventListener() {},
        };
        return root;
      }
      const documentStub = { createElement: (tagName) => makeNode(tagName), documentElement: makeNode("html") };
      globalThis.document = undefined;
      const { createActionClient } = await import("./gui/app.mjs");
      globalThis.document = documentStub;
      globalThis.matchMedia = () => ({ matches: false });

      const presentation = {
        schema_version: "competitive-read-only-v1",
        session: { session_id: "session-1", campaign: "competitive-regional-v1", turn: 1, max_turns: 24 },
        observation: { organization_name: "Riverside", operations: {} },
        institutions: [],
        resources: {},
        pending_effects: [],
        history: [],
        replay: {},
      };
      const resolution = {
        schema_version: "competitive-resolution-v1",
        turn: 1,
        steps: [],
        before: {},
        after: {},
        effects: [],
        replay: {},
      };
      function adapterFor(calls, rejectSubmit = false) {
        return {
          sessionId: "session-1",
          async startSession() { calls.push("start"); return { session_id: "session-1" }; },
          async getPresentation() { calls.push("presentation"); return presentation; },
          async getActionCatalog() {
            calls.push("catalog");
            return {
              schema_version: "competitive-actions-v1",
              turn: 1,
              actions: [
                { id: "hold", label: "Hold", command_template: "hold", parameters: [] },
                { id: "monitor", label: "Monitor", command_template: "monitor", parameters: [] },
              ],
            };
          },
          async validateTurn(sessionId, command) {
            calls.push("validate");
            return { valid: true, canonical_command_text: command, cost: {}, previews: [] };
          },
          async submitTurn() {
            calls.push("submit");
            if (rejectSubmit) throw new Error("host rejected batch");
            return { latest_transition: { turn: 1 } };
          },
          async getResolution() { calls.push("resolution"); return resolution; },
        };
      }
      async function prepare(client, root) {
        await client.load("session-1");
        const forms = root.querySelector("#action-builder").children.filter((child) => child.tagName === "FORM");
        for (const form of forms) form.dispatch("submit", { preventDefault() {} });
      }

      const calls = [];
      const root = makeRoot();
      root.querySelector("#session-campaign").value = "competitive-regional-v1";
      root.querySelector("#session-seed").value = "42";
      root.querySelector("#session-difficulty").value = "normal";
      const client = createActionClient({ adapter: adapterFor(calls), root });
      await client.sessionLauncher.start({ preventDefault() {} });
      if (client.firstMonthFlow.stage.id !== "draft") process.exit(1);
      await prepare(client, root);
      if (client.firstMonthFlow.stage.id !== "validate" || client.drafts.length !== 2) process.exit(2);
      await client.validate();
      if (client.firstMonthFlow.stage.id !== "submit") process.exit(3);
      await client.submit();
      if (client.firstMonthFlow.stage.id !== "continue") process.exit(4);
      if (JSON.stringify(calls) !== JSON.stringify(["start", "presentation", "catalog", "presentation", "catalog", "validate", "submit", "resolution", "presentation"])) process.exit(5);

      const failureCalls = [];
      const failureRoot = makeRoot();
      const failureClient = createActionClient({ adapter: adapterFor(failureCalls, true), root: failureRoot });
      await prepare(failureClient, failureRoot);
      await failureClient.validate();
      const rejected = await failureClient.submit();
      if (rejected.ok || failureClient.firstMonthFlow.stage.id !== "submit") process.exit(6);
      console.log(JSON.stringify({ calls, failureCalls, stage: failureClient.firstMonthFlow.stage.id }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(json.loads(result.stdout)["stage"], "submit")

  def test_adapter_handoff_order_and_failure_boundary_are_documented(self):
    for marker in (
      "createFirstMonthFlow",
      "actionCatalogLoaded",
      "draftCount: drafts.length",
      "validated: Boolean(validation.valid)",
      "submitted: true",
      "resolutionVisible: true",
      "refreshed: true",
      "competitive-first-month-v1",
    ):
      self.assertIn(marker, self.app + self.flow)
    for marker in (
      'id="first-month-flow"',
      'id="first-month-flow-list"',
      'id="first-month-flow-state"',
      'id="first-month-flow-detail"',
      "Start or load",
    ):
      self.assertIn(marker, self.html)
    self.assertIn("Continue", self.flow)
    for marker in (
      "start or load",
      "two draft",
      "host validation",
      "refreshed presentation",
      "technical",
      "human usability",
    ):
      self.assertIn(marker, (self.readme + self.doc).lower())
    for forbidden in (
      "transition_competitive",
      "resolved_inputs",
      "effect_queue",
      "fetch(",
      "WebSocket",
    ):
      self.assertNotIn(forbidden, self.flow)

  def test_javascript_syntax_and_boundary_metadata(self):
    for path in (APP, FLOW):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
