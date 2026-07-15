import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
COVERAGE = ROOT / "src" / "mcp" / "campaign_coverage.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
SERVER = ROOT / "src" / "mcp" / "server.rs"
DOC = ROOT / "docs" / "visual-audio-phase7-campaign-coverage-v0.12.23.md"


class GuiCampaignCoverageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.coverage = COVERAGE.read_text(encoding="utf-8")
    cls.session = SESSION.read_text(encoding="utf-8")
    cls.server = SERVER.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_typed_campaign_contract_and_endpoint_are_present(self):
    for marker in (
      "campaign-coverage-v1",
      "CampaignCoverageEnvelope",
      "CampaignCoverageStage",
      "CampaignCoverageBriefing",
      "CampaignCoverageMetric",
      "CampaignCoverageActor",
      "CampaignCoverageProcess",
      "CampaignCoverageDecision",
      "CampaignCoverageReplayMetadata",
      "stabilization-v1",
      "regional-affiliation-v1",
      "AffiliationObservation",
      "educational_debrief",
      "affiliation_debrief",
    ):
      self.assertIn(marker, self.coverage)
    self.assertIn("GetCampaignCoverageRequest", self.session)
    self.assertIn("get_campaign_coverage", self.session)
    self.assertIn('name = "get_campaign_coverage"', self.server)
    for forbidden in (
      "pub resolved_inputs",
      "pub effect_queue",
      "pub integration_drag",
      "pub condition_index",
    ):
      self.assertNotIn(forbidden, self.coverage)

  def test_campaign_views_forms_audio_and_adapter_are_present(self):
    for marker in (
      "CAMPAIGN_COVERAGE_SCHEMA",
      "renderCampaignCoverage",
      "createCampaignCoverageClient",
      "coverageCommand",
      "getCampaignCoverage",
      "campaign_coverage_adapter_error",
      "campaign_submit_rejected",
      "event.affiliation-milestone",
      "campaignAudioInput",
    ):
      self.assertIn(marker, self.app)
    for selector in (
      'id="campaign-coverage-panel"',
      'id="campaign-role"',
      'id="campaign-stage"',
      'id="campaign-briefing-list"',
      'id="campaign-metric-list"',
      'id="campaign-actor-list"',
      'id="campaign-process-list"',
      'id="campaign-decision-list"',
      'id="campaign-history-list"',
      'id="campaign-debrief-list"',
    ):
      self.assertIn(selector, self.html)
    for marker in (
      "getCampaignCoverage",
      "campaign-coverage-v1",
      "stabilization",
      "regional-affiliation",
      "canonical command path",
    ):
      self.assertIn(marker, self.readme)

  def test_browser_preserves_host_authority_and_no_external_boundary_break(self):
    for marker in (
      "{{staffed_beds}} {{capital_spend}} {{requested_rate}}",
      "{{posture}}",
      "{{community}}",
      "{{decision}}",
    ):
      self.assertIn(marker, self.coverage)
    for forbidden in (
      "ResolvedInputs",
      "resolved_inputs",
      "effect_queue",
      "integration_drag",
      "condition_index",
      "WorldState",
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

  def test_phase7_docs_preserve_campaign_distinctions_and_scope_boundary(self):
    for marker in (
      "## Typed campaign-coverage contract",
      "## Campaign distinctions",
      "## Browser behavior",
      "## Source and visibility boundary",
      "get_campaign_coverage(session_id)",
      "true-state/instructor views",
      "human comprehension",
      "Phase 8",
    ):
      self.assertIn(marker, self.doc)


if __name__ == "__main__":
  unittest.main()
