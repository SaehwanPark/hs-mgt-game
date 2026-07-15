import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUI_DIR = ROOT / "gui"
HTML = GUI_DIR / "index.html"
APP = GUI_DIR / "app.mjs"
README = GUI_DIR / "README.md"
DOC = ROOT / "docs" / "visual-audio-phase1-static-desktop-v0.12.17.md"


class GuiStaticDesktopTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_required_executive_regions_are_present(self):
    for selector in (
      'id="header-metrics"',
      'id="briefing-list"',
      'id="map-list"',
      'id="entity-detail"',
      'id="action-preview-list"',
      'id="pending-list"',
      'id="result-list"',
      'id="observation-list"',
      'id="history-list"',
      'id="debrief-list"',
    ):
      self.assertIn(selector, self.html)

  def test_fixture_covers_visible_decision_information(self):
    for marker in (
      "presentation_fixture",
      "header_metrics",
      "briefing",
      "entities",
      "facilities",
      "actions",
      "pending",
      "monthly_result",
      "Cash",
      "Monthly margin",
      "Workforce trust",
      "Access",
      "Public rival",
      "Private actions",
    ):
      self.assertIn(marker, self.app)

  def test_selection_is_presentation_only(self):
    for marker in (
      "selectedEntityId",
      "renderSelectedEntity",
      "dataset.entityId",
      "renderPresentation",
      "preview only in Phase 1",
    ):
      self.assertIn(marker, self.html if marker == "preview only in Phase 1" else self.app)
    self.assertNotIn("transition_competitive", self.app)
    self.assertNotIn("CompetitiveWorldState", self.app)
    self.assertNotIn("resolved_inputs", self.app)

  def test_responsive_and_accessible_surface_markers_exist(self):
    for marker in (
      "--space-1",
      "--teal",
      "status--watch",
      "@media (max-width: 760px)",
      "@media (prefers-reduced-motion: reduce)",
      'aria-label="Executive metrics"',
    ):
      self.assertIn(marker, self.html)
    self.assertIn('card.type = "button"', self.app)

  def test_surface_has_no_external_assets_or_network_calls(self):
    self.assertNotIn("<img", self.html.lower())
    self.assertNotIn("http://", self.html.lower())
    self.assertNotIn("https://", self.html.lower())
    self.assertNotIn("fetch(", self.app)
    self.assertNotIn("WebSocket", self.app)
    self.assertIn("zero downloaded assets", self.readme.lower())

  def test_existing_adapter_path_and_phase_checklist_remain_documented(self):
    for marker in (
      "HsMgtGameAdapter",
      "submitTurn",
      "MCP adapter remains authoritative for validation",
    ):
      self.assertIn(marker, self.app)
    for marker in (
      "## User and use context",
      "## Implemented presentation surface",
      "## Static review checklist",
      "raw JSON or CLI output",
      "do not establish human usability",
      "Phase 2 is the next candidate",
    ):
      self.assertIn(marker, self.doc)

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
