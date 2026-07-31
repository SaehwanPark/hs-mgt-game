import json
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "evaluation" / "phase13.1-competitive-campaign-review-packet.json"
BOUNDARY = ROOT / "docs" / "evaluation" / "phase13.1-competitive-campaign-boundary.json"
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"
RASTER_MANIFEST = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-raster-evidence.json"
TRANSCRIPT = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-terminal-capture-transcript.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
RELEASE_MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"


EXPECTED_SHARED_SOURCES = {
  "competitive_boundary": "docs/evaluation/phase13.1-competitive-campaign-boundary.json",
  "campaign_coverage_ledger": "docs/evaluation/phase11.1-campaign-coverage-ledger.json",
  "raster_manifest": "docs/evaluation/phase11.1-full-campaign-raster-evidence.json",
  "terminal_transcript": "docs/evaluation/phase11.1-full-campaign-terminal-capture-transcript.json",
  "first_session_packet": "docs/evaluation/phase13.1-first-session-review-packet.json",
  "player_help_boundary": "docs/evaluation/phase13.1-player-help-boundary.json",
  "pilot_preparation": "docs/evaluation/phase13.2-pilot-preparation-boundary.json",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json",
  "facilitator_guide": "docs/guides/phase10.2-structured-evaluation.md",
  "player_guide": "docs/guides/gui-how-to-play.md",
}


EXPECTED_SOURCE_CONTRACT = {
  "month_limit": ("src/mcp/session.rs", "pub(crate) const COMPETITIVE_MONTH_LIMIT: u32 = 24;"),
  "completion_test": ("src/mcp/session.rs", "fn competitive_advances_twenty_four_months_then_done()"),
  "facility_continuity_test": (
    "src/mcp/session.rs",
    "fn regional_world_facility_projection_covers_all_competitive_months()",
  ),
  "coverage_projection": ("src/mcp/campaign_coverage.rs", "from_competitive"),
  "coverage_renderer": ("gui/app.mjs", "renderCampaignCoverage"),
  "coverage_route": (
    "src/gui_server.rs",
    "/api/v1/sessions/{session_id}/campaign-coverage",
  ),
  "regional_world_projection": ("src/mcp/regional_world.rs", "from_competitive_world"),
  "regional_board_renderer": ("gui/regional-board.mjs", "presentationFixtureToSceneData"),
  "event_cue_projection": ("src/mcp/resolution.rs", "visible_event_cue_ids"),
  "music_state_projection": ("src/mcp/resolution.rs", "visible_music_state_id"),
  "audio_cue_contract": ("gui/audio-cue-contract.mjs", "AUDIO_CUE_CONTRACT"),
  "music_contract": ("gui/music-stem-contract.mjs", "MUSIC_STEM_CONTRACT"),
  "resolution_projection": ("src/mcp/resolution.rs", "from_competitive_transition"),
  "history_projection": ("src/mcp/session.rs", "get_history"),
  "replay_projection": ("src/mcp/session.rs", "get_replay"),
  "replay_client": ("gui/app.mjs", "createReplayClient"),
  "checkpoint_continuity_test": (
    "src/mcp/session.rs",
    "fn competitive_durable_checkpoint_covers_full_campaign_continuation",
  ),
  "checkpoint_client": ("gui/app.mjs", "createCheckpointClient"),
  "checkpoint_recovery_behavior": ("gui/app.mjs", "checkpoint_refresh_error"),
  "terminal_raster_manifest": (
    "docs/evaluation/phase11.1-full-campaign-raster-evidence.json",
    '"competitive-regional-v1"',
  ),
  "terminal_capture_transcript": (
    "docs/evaluation/phase11.1-full-campaign-terminal-capture-transcript.json",
    '"competitive-regional-v1"',
  ),
  "facility_catalog": ("gui/facility-components.mjs", "FACILITY_COMPONENTS"),
  "overlay_catalog": ("gui/operational-overlays.mjs", "OPERATIONAL_OVERLAY_SET"),
  "history_renderer": ("gui/index.html", 'id="history-list"'),
  "debrief_renderer": ("gui/index.html", 'id="debrief-list"'),
  "recovery_control": ("gui/index.html", 'id="recovery-retry"'),
}


EXPECTED_ACCESSIBILITY_SOURCES = {
  "facility-labels-and-fallbacks": ("gui/facility-components.mjs", "FACILITY_COMPONENTS"),
  "overlay-meaning-and-fallback": ("gui/operational-overlays.mjs", "OPERATIONAL_OVERLAY_SET"),
  "written-equivalent": ("gui/index.html", 'id="result-list"'),
  "audio-off-and-cues-only": (
    "gui/audio.mjs",
    'mode === "cues-only"',
  ),
  "audio-written-fallback": ("gui/index.html", 'id="audio-state"'),
  "reduced-motion": ("gui/app.mjs", "const effectiveReducedMotion ="),
  "large-text": ("gui/app.mjs", "const effectiveTextScale ="),
  "keyboard-navigation": ("gui/index.html", 'id="skip-to-content"'),
  "retry-recovery": ("gui/index.html", 'id="recovery-retry"'),
}


class CompetitiveCampaignReviewPacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.raster_manifest = json.loads(RASTER_MANIFEST.read_text(encoding="utf-8"))
    cls.transcript = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_packet_is_technical_only_and_not_a_release_asset(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase13.1-competitive-campaign-review-packet-v1",
    )
    self.assertEqual(
      self.packet["status"],
      "complete-technical-packet-pending-human-review",
    )
    self.assertEqual(
      self.packet["review_boundary"],
      {
        "technical_packet_complete": True,
        "participant_results_present": False,
        "full_campaign_human_review_complete": False,
        "human_visual_review_complete": False,
        "human_accessibility_review_complete": False,
        "educational_and_classroom_review_complete": False,
        "audio_listening_review_complete": False,
        "expansion_approval": False,
        "public_release_approval": False,
      },
    )
    self.assertEqual(
      self.packet["human_review_record"],
      {
        "status": "pending-authorized-human-review",
        "participant_results_present": False,
        "authorized_reviewer": None,
        "recorded_at": None,
        "decision": None,
        "expansion_go_no_go": None,
        "public_release_approval": None,
      },
    )
    self.assertNotIn(
      "phase13.1-competitive-campaign-review-packet.json",
      RELEASE_MANIFEST.read_text(encoding="utf-8"),
    )

  def test_shared_sources_and_source_contract_are_exactly_anchored(self):
    self.assertEqual(self.packet["shared_sources"], EXPECTED_SHARED_SOURCES)
    for source_path in self.packet["shared_sources"].values():
      self.assertTrue((ROOT / source_path).is_file(), source_path)
    self.assertEqual(set(self.packet["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(self.packet["source_contract"][key], f"{source_path}: {marker}")
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      source_text = " ".join(path.read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, key)

  def test_packet_mirrors_authoritative_campaign_and_terminal_evidence(self):
    technical = self.packet["technical_contract"]
    surface = self.boundary["surface_contract"]
    facility_coverage = self.ledger["facility_placement_use_coverage"]
    self.assertEqual(technical["campaign"], self.boundary["campaign"])
    self.assertEqual(technical["campaign"], "competitive-regional-v1")
    self.assertEqual(technical["max_turns"], surface["max_turns"])
    self.assertEqual(technical["presentation_surfaces"], surface["competitive_presentation_surfaces"])
    self.assertEqual(technical["host_owned_state"], surface["host_owned_state"])
    self.assertEqual(
      technical["browser_forbidden_authority_markers"],
      surface["browser_forbidden_authority_markers"],
    )
    self.assertEqual(technical["facility_component_ids"], facility_coverage["facility_component_ids"])
    self.assertEqual(technical["capacity_metric_labels"], facility_coverage["capacity_metric_labels"])
    self.assertEqual(
      facility_coverage["status"],
      "complete-competitive-24-month-host-read",
    )
    terminal_manifest = [
      record for record in self.raster_manifest["state_records"]
      if record["campaign"] == "competitive-regional-v1" and record["state"] == "terminal"
    ]
    self.assertEqual(len(terminal_manifest), 1)
    manifest_record = terminal_manifest[0]
    self.assertEqual(manifest_record["artifact"], "docs/evaluation/phase11.1-campaign-raster/competitive-regional-v1-terminal-1024x768.jpg")
    artifact = ROOT / manifest_record["artifact"]
    self.assertTrue(artifact.is_file())
    artifact_bytes = artifact.read_bytes()
    self.assertEqual(manifest_record["mime_type"], "image/jpeg")
    self.assertEqual(manifest_record["byte_size"], len(artifact_bytes))
    self.assertEqual(manifest_record["sha256"], hashlib.sha256(artifact_bytes).hexdigest())
    self.assertEqual((manifest_record["width"], manifest_record["height"]), (1024, 768))
    self.assertEqual(manifest_record["host_state"]["campaign"], "competitive-regional-v1")
    self.assertEqual(manifest_record["host_state"]["turn"], "24/24")
    self.assertIn("competitive campaign complete", manifest_record["host_state"]["stage"].lower())
    self.assertTrue(manifest_record["session_done"])
    self.assertEqual(manifest_record["history_count"], 24)
    self.assertGreater(manifest_record["debrief_line_count"], 0)
    self.assertTrue(manifest_record["terminal_debrief"])
    self.assertTrue(manifest_record["written_equivalent"])
    self.assertTrue(manifest_record["optional_audio"])
    self.assertEqual(
      manifest_record["terminal_controls"],
      {
        "campaign_decision_count": 0,
        "submit_host_shaped_decision_count": 0,
        "commit_decision_count": 0,
      },
    )
    self.assertIn("Twenty-four committed history and replay rows", manifest_record["observed_content"])
    self.assertIn("No campaign decision is available after completion", manifest_record["observed_content"])
    transcript_records = [
      record for record in self.transcript["captures"]
      if record["campaign"] == "competitive-regional-v1"
    ]
    self.assertEqual(len(transcript_records), 1)
    transcript_record = transcript_records[0]
    self.assertEqual(transcript_record["artifact"], manifest_record["artifact"])
    self.assertEqual(transcript_record["capture_source"], "same in-app browser run as the persisted JPEG")
    host_envelope = transcript_record["host_envelope"]
    self.assertEqual(host_envelope["session"], {"campaign": "competitive-regional-v1", "turn": "24/24", "max_turns": 24, "done": True})
    self.assertIn("competitive campaign complete", host_envelope["stage"]["label"].lower())
    self.assertEqual(host_envelope["replay"]["transition_count"], 24)
    self.assertEqual(host_envelope["history_count"], 24)
    self.assertEqual(host_envelope["debrief_line_count"], manifest_record["debrief_line_count"])
    self.assertEqual(
      host_envelope["terminal_controls"],
      manifest_record["terminal_controls"],
    )
    observed_excerpt = transcript_record["observed_dom"]["campaign_coverage_excerpt"]
    for marker in ("Committed campaign history", "Campaign debrief", "No campaign decision is available", "Competitive campaign complete"):
      self.assertIn(marker, observed_excerpt, marker)

  def test_tasks_questions_and_fallbacks_are_complete_and_pending(self):
    self.assertEqual(
      [task["id"] for task in self.packet["participant_tasks"]],
      [
        "orient-and-enter-campaign",
        "trace-facility-continuity",
        "trace-visible-consequences",
        "use-history-replay-checkpoint",
        "review-terminal-campaign",
      ],
    )
    self.assertEqual(len(self.packet["review_questions"]), 6)
    self.assertTrue(all(question.endswith("?") for question in self.packet["review_questions"]))
    self.assertEqual(
      {check["id"] for check in self.packet["accessibility_and_fallback_checks"]},
      set(EXPECTED_ACCESSIBILITY_SOURCES),
    )
    for check in self.packet["accessibility_and_fallback_checks"]:
      source_path, marker = EXPECTED_ACCESSIBILITY_SOURCES[check["id"]]
      self.assertEqual(check["source"], f"{source_path}: {marker}")
      source_text = " ".join((ROOT / source_path).read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, check["id"])
      self.assertTrue("pending" in check["status"] or "protocol-ready" in check["status"])

  def test_authority_provenance_and_roadmap_limits_remain_explicit(self):
    self.assertEqual(
      self.packet["causality_privacy_and_provenance_boundary"],
      {
        "host_owned_transitions_only": True,
        "actor_visible_observations_only": True,
        "no_hidden_state_inference": True,
        "no_causal_certainty": True,
        "no_private_rival_intent": True,
        "evaluation_artifacts_not_release_assets": True,
        "source": "docs/evaluation/phase13.1-competitive-campaign-boundary.json",
      },
    )
    self.assertEqual(
      self.packet["evidence_assertions"]["human_campaign_comprehension_is_unverified"],
      True,
    )
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[ ] Competitive campaign coverage complete.", normalized)
    self.assertIn("[x] Current technical competitive campaign boundary documented.", normalized)
    self.assertIn("[x] Current competitive full-campaign technical review packet prepared.", normalized)
    self.assertIn("pending human", normalized.lower())

  def test_authoritative_facility_and_checkpoint_tests_execute(self):
    for test_name in (
      "mcp::session::tests::competitive_advances_twenty_four_months_then_done",
      "mcp::session::tests::regional_world_facility_projection_covers_all_competitive_months",
      "mcp::session::tests::competitive_durable_checkpoint_covers_full_campaign_continuation",
    ):
      result = __import__("subprocess").run(
        ["cargo", "test", "--lib", test_name, "--", "--exact"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
      self.assertIn(f"{test_name.rsplit('::', 1)[-1]} ... ok", result.stdout)


if __name__ == "__main__":
  unittest.main()
