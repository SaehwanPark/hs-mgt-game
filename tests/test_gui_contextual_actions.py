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
      "actionCommand",
      "drafts",
      "renderDraftActions",
      "Replace draft",
      "Remove",
      "Validate the unchanged draft before submitting",
      "submit_rejected",
    ):
      self.assertIn(marker, self.app)
    for marker in ("competitive-actions-v1", "competitive-validation-v1"):
      self.assertIn(marker, self.action)
    for selector in (
      'id="action-builder"',
      'id="draft-action-list"',
      'id="validate-actions"',
      'id="submit-month"',
      'id="validation-status"',
    ):
      self.assertIn(selector, self.html)

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


if __name__ == "__main__":
  unittest.main()
