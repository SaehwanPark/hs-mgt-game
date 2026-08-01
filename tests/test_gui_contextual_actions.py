import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
ACTION = ROOT / "src" / "mcp" / "action.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
SERVER = ROOT / "src" / "mcp" / "server.rs"
DOC = ROOT / "docs" / "history" / "initiatives" / "visual-audio" / "visual-audio-phase3-contextual-actions-v0.12.19.md"


class GuiContextualActionTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.action = ACTION.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_action_builder_surface_and_host_contract_are_present(self):
    for marker in (
      "createActionClient",
      "getActionCatalog",
      "validateTurn",
      "commandForParameters",
      "normalizeActionViewModel",
      "normalizeCampaignDecision",
      "renderUnifiedActionSurface",
      "drafts",
      "renderDraftActions",
      "Save",
      "Remove",
      "submit_rejected",
    ):
      self.assertIn(marker, self.app)
    for marker in ("competitive-actions-v1", "competitive-validation-v1"):
      self.assertIn(marker, self.action)
    for selector in (
      'id="action-builder"',
      'id="action-preview-list"',
      'id="action-plan"',
      'id="draft-action-list"',
      'id="validate-actions"',
      'id="submit-month"',
      'id="validation-status"',
      'id="technical-controls"',
    ):
      self.assertIn(selector, self.html)
    for label in ("Check plan", "Commit month", "Technical controls"):
      self.assertIn(label, self.html)
    self.assertIn('"Details", "action-details visual-token"', self.app)
    for forbidden in ("Host-shaped decision", "Host catalog", "Submit host-shaped decision"):
      self.assertNotIn(forbidden, self.html)

  def test_read_only_path_has_no_submit_call(self):
    start = self.app.index("export function createReadOnlyClient")
    end = self.app.index("export function createActionClient")
    self.assertNotIn("submitTurn", self.app[start:end])
    action_start = end
    action_end = self.app.index("export function renderPresentation")
    action_source = self.app[action_start:action_end]
    self.assertIn("submitTurn", action_source)
    self.assertIn("validation?.valid", action_source)
    self.assertIn("validation_required", action_source)

  def test_host_action_catalog_covers_all_existing_families(self):
    sources = self.action + self.session
    for marker in (
      '"hold"',
      '"invest"',
      '"recruit"',
      '"monitor"',
      '"negotiate"',
      '"commit"',
      '"project"',
      "ActionCatalogEnvelope",
      "ValidateTurnEnvelope",
      "sum_action_costs",
      "parse_competitive_batch",
      "validate_competitive_batch",
    ):
      self.assertIn(marker, sources)
    self.assertIn("GetActionCatalogRequest", self.session)
    self.assertIn("ValidateTurnRequest", self.session)
    self.assertIn('name = "get_action_catalog"', self.server)
    self.assertIn('name = "validate_turn"', self.server)

  def test_docs_preserve_phase_boundary_and_evidence_limits(self):
    for marker in (
      "## Typed action catalog and validation contract",
      "## Draft and submit behavior",
      "## Static review checklist",
      "## Explicit non-goals and next gate",
      "Phase 4",
      "rejected",
      "human usability",
    ):
      self.assertIn(marker, self.doc)
    self.assertIn("client-side cost formula", self.readme)

  def test_no_external_assets_or_network_calls_and_javascript_parses(self):
    self.assertNotIn("http://", self.html.lower())
    self.assertNotIn("https://", self.html.lower())
    self.assertNotIn("fetch(", self.app)
    self.assertNotIn("WebSocket", self.app)
    self.assertIn("zero downloaded assets", self.readme.lower())
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_unified_surface_keeps_one_open_card_and_host_ordered_overflow(self):
    script = r'''
      function makeNode(tagName = "div") {
        const node = {
          tagName: tagName.toUpperCase(),
          children: [],
          dataset: {},
          listeners: {},
          hidden: false,
          open: false,
          disabled: false,
          value: "",
          textContent: "",
          ownerDocument: null,
          append(...children) {
            for (const child of children) {
              this.children.push(child);
              child.parentNode = this;
              if (child.name) this.elements._values[child.name] = child;
              for (const descendant of child.children ?? []) {
                if (descendant.name) this.elements._values[descendant.name] = descendant;
              }
            }
          },
          replaceChildren(...children) { this.children = []; this.append(...children); },
          addEventListener(type, listener) { (this.listeners[type] ??= []).push(listener); },
          dispatch(type, event = {}) {
            event.target ??= this;
            for (const listener of this.listeners[type] ?? []) listener(event);
          },
          setAttribute(name, value) { this[name] = String(value); },
          removeAttribute(name) { delete this[name]; },
          querySelector(selector) {
            if (selector === "summary") {
              return this.children.find((child) => child.tagName === "SUMMARY") ?? (this._summary ??= makeNode("summary"));
            }
            if (selector === "button[type=submit]") {
              return this.children.flatMap((child) => child.children ?? []).find((child) => child.tagName === "BUTTON") ?? null;
            }
            return null;
          },
          querySelectorAll() { return []; },
          focus() { this.focused = (this.focused ?? 0) + 1; },
          showModal() { this.open = true; },
        };
        node.elements = { _values: {}, namedItem(name) { return this._values[name] ?? null; } };
        return node;
      }
      const documentStub = {
        createElement(tagName) { const node = makeNode(tagName); node.ownerDocument = documentStub; return node; },
        documentElement: makeNode("html"),
      };
      const nodes = new Map();
      const root = {
        ownerDocument: documentStub,
        querySelector(selector) {
          if (!nodes.has(selector)) {
            const node = documentStub.createElement(selector === "#action-preview-more" ? "details" : "div");
            nodes.set(selector, node);
          }
          return nodes.get(selector);
        },
      };
      globalThis.document = undefined;
      const { normalizeActionViewModel, renderCampaignCoverage } = await import("./gui/app.mjs");
      globalThis.document = documentStub;
      const submitted = [];
      const decisions = Array.from({ length: 7 }, (_, index) => ({
        id: `decision-${index + 1}`,
        label: `Decision ${index + 1}`,
        command_template: `choose {{level}} ${index + 1}`,
        uncertainty: "Host-reported uncertainty",
        parameters: [{ name: "level", label: "Level", input_type: "number", min: 1, max: 5 }],
      }));
      const envelope = {
        schema_version: "campaign-coverage-v1",
        campaign_role: "Stabilization",
        session: { campaign: "stabilization-v1", turn: 1, max_turns: 5, done: false },
        stage: { label: "Turn 1", detail: "Visible stage" },
        briefing: [], metrics: [], actors: [], processes: [], decisions,
        history: [], debrief: [],
      };
      const normalized = normalizeActionViewModel(decisions[0], "commit");
      if (normalized.id !== "decision-1" || normalized.submissionMode !== "commit") process.exit(1);
      const result = renderCampaignCoverage(envelope, root, (command) => submitted.push(command));
      const list = nodes.get("#action-preview-list");
      const more = nodes.get("#action-preview-more");
      if (!result.ok || list.children.length !== 6 || more.hidden || more.querySelector("summary").textContent !== "Show 1 more") process.exit(2);
      const first = list.children[0];
      const second = list.children[1];
      const firstToggle = first.children[0].children[0];
      const secondToggle = second.children[0].children[0];
      firstToggle.dispatch("click");
      if (first.children[1].hidden || second.children[1].hidden !== true || firstToggle.focused !== 1) process.exit(3);
      secondToggle.dispatch("click");
      if (first.children[1].hidden !== true || second.children[1].hidden || secondToggle.focused !== 1) process.exit(4);
      const details = second.children[0].children[1];
      details.dispatch("click", { stopPropagation() {} });
      if (!nodes.get("#context-drawer").open) process.exit(5);
      const form = second.children[1].children[0];
      form.elements.namedItem("level").value = "3";
      form.dispatch("submit", { preventDefault() {} });
      if (submitted[0] !== "choose 3 2") process.exit(6);
      console.log(JSON.stringify({ cards: list.children.length, overflow: more.querySelector("summary").textContent, submitted: submitted[0] }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    payload = json.loads(result.stdout)
    self.assertEqual(payload["cards"], 6)
    self.assertEqual(payload["overflow"], "Show 1 more")
    self.assertEqual(payload["submitted"], "choose 3 2")


if __name__ == "__main__":
  unittest.main()
