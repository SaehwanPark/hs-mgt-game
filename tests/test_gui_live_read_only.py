import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
PRESENTATION = ROOT / "src" / "mcp" / "presentation.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
SERVER = ROOT / "src" / "mcp" / "server.rs"
DOC = ROOT / "docs" / "visual-audio-phase2-live-read-only-v0.12.18.md"


class GuiLiveReadOnlyTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.presentation = PRESENTATION.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_typed_read_only_contract_is_connected(self):
    for marker in (
      "competitive-read-only-v1",
      "createReadOnlyClient",
      "getPresentation",
      "renderReadOnlyEnvelope",
      "validateReadOnlyEnvelope",
      "entityIds",
      "adapter_error",
      "empty_presentation",
      "Loading read-only presentation",
      "Unsupported read-only presentation schema",
      "Action submission is deferred to Phase 3",
    ):
      self.assertIn(marker, self.app)
    self.assertIn('id="presentation-state"', self.html)
    self.assertIn('id="command-form" hidden', self.html)

  def test_read_only_client_does_not_submit_commands(self):
    start = self.app.index("export function createReadOnlyClient")
    end = self.app.index("export function renderPresentation")
    client_source = self.app[start:end]
    self.assertIn("getPresentation", client_source)
    self.assertNotIn("submitTurn", client_source)
    self.assertIn("createThinClient", self.app)
    self.assertIn("not wired into the Phase 2 page", self.readme)

  def test_rust_projection_and_tool_are_explicitly_read_only(self):
    for marker in (
      "ReadOnlyPresentationEnvelope",
      "ReadOnlyObservation",
      "ReadOnlyInstitution",
      "ReadOnlyPendingEffect",
      "ReadOnlyReplayMetadata",
      "PRESENTATION_SCHEMA_VERSION",
      "from_competitive_observation",
      "month_name",
    ):
      self.assertIn(marker, self.presentation)
    self.assertIn("GetPresentationRequest", self.session)
    self.assertIn("get_presentation", self.session)
    self.assertIn('name = "get_presentation"', self.server)
    for forbidden in (
      "CompetitiveWorldState",
      "resolved_inputs",
      "effect_queue",
      "event_metadata",
      "rna_strike_active",
    ):
      self.assertNotIn(forbidden, self.presentation)

  def test_contract_document_records_scope_and_exit_gate(self):
    for marker in (
      "## Typed read-only contract",
      "## Source and authority map",
      "## Browser adapter behavior",
      "## Static review checklist",
      "## Explicit non-goals and next gate",
      "Phase 3",
      "human usability",
      "missing",
    ):
      self.assertIn(marker, self.doc)

  def test_no_external_assets_or_network_calls(self):
    self.assertNotIn("http://", self.html.lower())
    self.assertNotIn("https://", self.html.lower())
    self.assertNotIn("fetch(", self.app)
    self.assertNotIn("WebSocket", self.app)
    self.assertIn("zero downloaded assets", self.readme.lower())

  def test_javascript_parses(self):
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
