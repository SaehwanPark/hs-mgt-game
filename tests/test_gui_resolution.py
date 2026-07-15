import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
RESOLUTION = ROOT / "src" / "mcp" / "resolution.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
SERVER = ROOT / "src" / "mcp" / "server.rs"
DOC = ROOT / "docs" / "visual-audio-phase4-resolution-causal-v0.12.20.md"


class GuiResolutionTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.resolution = RESOLUTION.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_typed_resolution_contract_and_eight_steps_are_present(self):
    for marker in (
      "competitive-resolution-v1",
      "ResolutionEnvelope",
      "ResolutionSnapshot",
      "ResolutionStep",
      "ResolutionEffect",
      "RESOLUTION_SCHEMA_VERSION",
      '"submitted"',
      '"responses"',
      '"processes"',
      '"operations"',
      '"resources"',
      '"effects"',
      '"information"',
      '"pending"',
    ):
      self.assertIn(marker, self.resolution)
    self.assertIn("GetResolutionRequest", self.session)
    self.assertIn("get_resolution", self.session)
    self.assertIn('name = "get_resolution"', self.server)

  def test_browser_resolution_controls_and_host_boundary_are_present(self):
    for marker in (
      "createResolutionClient",
      "renderResolution",
      "getResolution",
      "resolution_adapter_error",
      "prefers-reduced-motion",
      "resolution-play",
      "resolution-pause",
      "resolution-skip",
      "resolution-review",
      "Review mode: all committed resolution text remains available.",
      "Committed response received; read-only refresh failed",
    ):
      self.assertIn(marker, self.app)
    for selector in (
      'id="resolution-panel"',
      'id="resolution-step-list"',
      'id="resolution-before-list"',
      'id="resolution-after-list"',
      'id="resolution-effect-list"',
      'id="resolution-turn"',
      'id="load-resolution"',
    ):
      self.assertIn(selector, self.html)
    self.assertIn("competitive-resolution-v1", self.readme)

  def test_resolution_docs_preserve_source_and_phase_boundary(self):
    for marker in (
      "## Typed resolution contract",
      "## Source and authority map",
      "## Browser behavior",
      "## Static review checklist",
      "## Explicit non-goals and next gate",
      "get_resolution(session_id, turn?)",
      "Phase 5",
      "inferred causal graph",
      "human comprehension",
    ):
      self.assertIn(marker, self.doc)

  def test_browser_has_no_simulation_or_external_asset_boundary_break(self):
    for forbidden in (
      "action_cost",
      "sum_action_costs",
      "transition_competitive",
      "resolved_inputs",
      "effect_queue",
      "fetch(",
      "WebSocket",
      "http://",
      "https://",
    ):
      self.assertNotIn(forbidden, self.app)
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
