import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUI_DIR = ROOT / "gui"
HTML = GUI_DIR / "index.html"
APP = GUI_DIR / "app.mjs"
README = GUI_DIR / "README.md"


class GuiThinClientTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")

  def test_surface_renders_all_existing_output_contracts(self):
    for selector in (
      'id="observation-list"',
      'id="legal-command-list"',
      'id="history-list"',
      'id="debrief-list"',
      'id="command-form"',
    ):
      self.assertIn(selector, self.html)
    for field in ("observation", "legal_commands", "history", "debrief"):
      self.assertIn(field, self.app)

  def test_adapter_boundary_owns_submission_and_validation(self):
    self.assertIn("HsMgtGameAdapter", self.app)
    self.assertIn("submitTurn", self.app)
    self.assertIn("MCP adapter remains authoritative for validation", self.app)
    self.assertNotIn("transition_competitive", self.app)
    self.assertNotIn("resolve_affiliation_turn", self.app)

  def test_surface_has_no_external_assets_or_network_calls(self):
    self.assertNotIn("<img", self.html.lower())
    self.assertNotIn("http://", self.html.lower())
    self.assertNotIn("https://", self.html.lower())
    self.assertNotIn("fetch(", self.app)
    self.assertIn("zero downloaded assets", self.readme.lower())

  def test_javascript_parses(self):
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_demo_is_explicitly_display_fixture_data(self):
    self.assertIn("const demoEnvelope", self.app)
    self.assertIn("display fixture data", self.readme)
    self.assertIn("duplicate simulation state", self.html)


if __name__ == "__main__":
  unittest.main()
