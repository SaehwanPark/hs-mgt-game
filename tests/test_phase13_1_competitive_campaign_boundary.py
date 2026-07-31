import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-competitive-campaign-boundary.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"

EXPECTED_SOURCE_CONTRACT = {
  "host_month_limit": (
    "src/mcp/session.rs",
    "pub(crate) const COMPETITIVE_MONTH_LIMIT: u32 = 24;",
  ),
  "host_completion_test": (
    "src/mcp/session.rs",
    "fn competitive_advances_twenty_four_months_then_done()",
  ),
  "cli_month_loop_test": (
    "src/cli/campaign.rs",
    "fn competitive_month_loop_runs_twenty_four_months_in_non_tty_context()",
  ),
  "competitive_campaign_id": (
    "src/mcp/session.rs",
    '"competitive-regional-v1" => Ok(CampaignId::CompetitiveRegionalV1),',
  ),
  "competitive_catalog_ledger": (
    "docs/evaluation/phase11.1-campaign-coverage-ledger.json",
    '"campaign": "competitive-regional-v1"',
  ),
  "competitive_catalog_test": (
    "tests/test_phase11_campaign_coverage.py",
    'self.assertEqual(self.ledger["campaign"], "competitive-regional-v1")',
  ),
  "campaign_coverage_scope": (
    "src/mcp/session.rs",
    "from_competitive",
  ),
  "competitive_companion_scope": (
    "gui/app.mjs",
    "refreshCompetitiveCoverageCompanion",
  ),
  "campaign_gui_boundary_test": (
    "tests/test_gui_campaign_coverage.py",
    "def test_browser_preserves_host_authority_and_no_external_boundary_break(self):",
  ),
  "history_test": (
    "tests/test_phase11_live_history.py",
    "def test_live_history_read_does_not_expose_simulation_authority(self):",
  ),
  "replay_test": (
    "tests/test_phase11_live_replay.py",
    "def test_live_replay_read_does_not_expose_simulation_authority(self):",
  ),
  "checkpoint_test": (
    "tests/test_phase11_live_checkpoint.py",
    "def test_checkpoint_boundary_does_not_add_browser_or_route_simulation_authority(self):",
  ),
  "debrief_test": (
    "tests/test_phase11_live_debrief.py",
    "def test_host_terminal_contract_is_explicit_and_presentation_only(self):",
  ),
}


class Phase131CompetitiveCampaignBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_source_contract_is_independently_anchored(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase13.1-competitive-campaign-boundary-v1",
    )
    self.assertEqual(
      self.ledger["status"],
      "complete-current-technical-competitive-campaign-boundary-only",
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key], f"{source_path}: {marker}"
      )
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      source_text = " ".join(path.read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, key)

  def test_technical_path_and_surface_contract_are_exactly_bounded(self):
    self.assertEqual(
      self.ledger["technical_path"],
      [
        "start competitive-regional-v1 through the host session boundary",
        "advance the host campaign for 24 monthly transitions",
        "render the current competitive actor-visible board, facility, overlay, event-cue, music, history, replay, checkpoint, and terminal-debrief surfaces",
        "retain host-owned history, replay metadata, checkpoint state, resolution, and terminal debrief",
        "use written fallbacks and recoverable read errors when optional GUI capability is unavailable",
        "serve competitive-regional-v1 through the host-owned campaign-coverage-v1 typed read while keeping competitive mutations on the existing action-catalog and validation path",
      ],
    )
    self.assertEqual(
      self.ledger["surface_contract"],
      {
        "campaign_id": "competitive-regional-v1",
        "max_turns": 24,
        "terminal_transition_count": 24,
        "competitive_presentation_surfaces": [
          "regional board",
          "facility components",
          "operational overlays",
          "event cues",
          "music states",
          "history",
          "replay",
          "checkpoint",
          "terminal debrief",
        ],
        "shared_campaign_coverage_envelope_support": [
          "competitive-regional-v1",
          "stabilization-v1",
          "regional-affiliation-v1",
        ],
        "host_owned_state": [
          "history",
          "replay metadata",
          "checkpoint state",
          "resolution",
          "terminal debrief",
        ],
        "browser_forbidden_authority_markers": [
          "transition_competitive",
          "resolved_inputs",
          "effect_queue",
          "CompetitiveWorldState",
          "WorldState",
          "WebSocket",
        ],
      },
    )

  def test_findings_authority_and_limits_keep_product_gates_open(self):
    self.assertEqual(
      self.ledger["findings"],
      {
        "host_campaign_runs_24_months_and_terminates": True,
        "current_competitive_presentation_surfaces_are_source_bound": True,
        "history_replay_checkpoint_and_debrief_are_host_bound": True,
        "browser_authority_boundary_is_preserved": True,
        "optional_audio_and_written_fallback_are_present": True,
        "competitive_campaign_coverage_envelope_is_host_bound": True,
        "competitive_coverage_companion_preserves_action_rail": True,
        "full_campaign_visual_content_review": False,
        "human_campaign_comprehension_and_educational_review": False,
      },
    )
    self.assertEqual(
      self.ledger["authority_boundary"],
      "The Rust host/core owns campaign transitions, actor-visible projections, history, replay metadata, checkpoint state, resolution, and debrief; the browser renders supplied competitive projections and local presentation preferences without simulation authority.",
    )
    self.assertEqual(
      self.ledger["limits"],
      [
        "This closes the current repository-owned technical competitive-regional campaign boundary only.",
        "It does not establish full-campaign facility placement/use coverage, campaign-specific visual or audio quality, screenshot completeness, cross-browser/device certification, human comprehension, or educational effectiveness.",
        "The broader Competitive campaign coverage complete roadmap item remains open for product/content review and structured human evaluation.",
      ],
    )

  def test_host_duration_path_executes_and_browser_fallbacks_are_concrete(self):
    result = subprocess.run(
      [
        "cargo",
        "test",
        "--lib",
        "mcp::session::tests::competitive_advances_twenty_four_months_then_done",
        "--",
        "--exact",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertIn("competitive_advances_twenty_four_months_then_done ... ok", result.stdout)

    session = (ROOT / "src" / "mcp" / "session.rs").read_text(encoding="utf-8")
    app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    html = (ROOT / "gui" / "index.html").read_text(encoding="utf-8")
    for marker in (
      "pub(crate) const COMPETITIVE_MONTH_LIMIT: u32 = 24;",
      "assert!(current.done);",
      "assert_eq!(current.turn, 24);",
      "assert_eq!(history.transition_count, 24);",
      "from_competitive(",
    ):
      self.assertIn(marker, session)
    for marker in (
      "campaign_coverage_adapter_missing",
      "Campaign coverage could not be read. Retry the current host read when the adapter is available.",
      "Campaign coverage could not be read: ${message}",
    ):
      self.assertIn(marker, app)
    self.assertIn(
      "Muting, reduced notifications, focus loss, or unavailable browser audio never removes the written result.",
      html,
    )
    for forbidden in self.ledger["surface_contract"]["browser_forbidden_authority_markers"]:
      self.assertNotIn(forbidden, app)

  def test_roadmap_keeps_bounded_technical_and_broad_campaign_gates_distinct(self):
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[ ] Competitive campaign coverage complete.", normalized)
    self.assertIn(
      "[x] Current technical competitive campaign boundary documented.",
      normalized,
    )
    for marker in (
      "full-campaign facility placement/use coverage",
      "campaign-specific visual or audio quality",
      "human comprehension",
      "structured human evaluation",
    ):
      self.assertIn(marker, " ".join(self.ledger["limits"]).lower())


if __name__ == "__main__":
  unittest.main()
