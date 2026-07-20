import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
REGIONAL = ROOT / "src" / "mcp" / "regional_world.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
SERVER = ROOT / "src" / "mcp" / "server.rs"
DOC = ROOT / "docs" / "history" / "initiatives" / "visual-audio" / "visual-audio-phase6-regional-world-v0.12.22.md"


class GuiRegionalWorldTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.regional = REGIONAL.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_typed_host_contract_and_visibility_boundary_are_present(self):
    for marker in (
      "competitive-regional-world-v1",
      "RegionalWorldEnvelope",
      "RegionalWorldEntity",
      "RegionalWorldFacility",
      "RegionalWorldSignal",
      "RegionalWorldProcess",
      "RegionalWorldOverlay",
      "RegionalWorldNavigation",
      "RegionalWorldMissing",
      "PUBLIC_RIVAL_LAG_MONTHS",
      "PlayerObservation",
      "PublicActionEntry via one-month observation lag",
      "Private rival operations",
      "PlayerObservation.monthly_demand",
      "PlayerObservation.reported_access_index",
    ):
      self.assertIn(marker, self.regional)
    self.assertIn("GetRegionalWorldRequest", self.session)
    self.assertIn("get_regional_world", self.session)
    self.assertIn('name = "get_regional_world"', self.server)
    for forbidden in ("pub effect_queue", "pub event_metadata", "resolved_inputs"):
      self.assertNotIn(forbidden, self.regional)

  def test_browser_map_overlay_navigation_and_adapter_are_present(self):
    for marker in (
      "REGIONAL_WORLD_SCHEMA",
      "renderRegionalWorld",
      "createRegionalWorldClient",
      "getRegionalWorld",
      "regionalEntitiesToFixture",
      "renderRegionalOverlays",
      "renderRegionalNavigation",
      "Visible processes",
      "Unavailable detail",
      "regional_world_adapter_error",
      "regional_world_adapter_missing",
      "observed month",
      "private rival detail remains unavailable",
    ):
      self.assertIn(marker, self.app)
    for selector in (
      'id="regional-navigation"',
      'id="regional-overlay-list"',
      'id="map-list"',
      'id="entity-detail"',
      'id="pending-list"',
    ):
      self.assertIn(selector, self.html)
    self.assertIn("getRegionalWorld", self.readme)

  def test_browser_has_no_map_simulation_or_external_asset_boundary_break(self):
    for forbidden in (
      "CompetitiveWorldState",
      "HealthSystemState",
      "effect_queue",
      "resolved_inputs",
      "fetch(",
      "WebSocket",
      "http://",
      "https://",
      "distance",
      "patient movement",
    ):
      self.assertNotIn(forbidden, self.app)
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_phase6_docs_preserve_source_lag_and_scope_boundary(self):
    for marker in (
      "## Typed regional-world contract",
      "## Source and authority map",
      "## Browser behavior",
      "## Static review checklist",
      "get_regional_world(session_id)",
      "one-month observation lag",
      "true geography",
      "Phase 7",
      "human",
    ):
      self.assertIn(marker, self.doc)


if __name__ == "__main__":
  unittest.main()
