import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "evaluation" / "phase13.1-first-session-review-packet.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
RELEASE_MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"


EXPECTED_SOURCE_CONTRACT = {
  "launch_markup": ("gui/index.html", 'id="session-launch-form"'),
  "launch_client": ("gui/app.mjs", "createSessionLauncher"),
  "first_month_flow": ("gui/first-month.mjs", "FIRST_MONTH_FLOW_SCHEMA"),
  "campaign_coverage_flow": ("gui/first-month.mjs", "CAMPAIGN_COVERAGE_FLOW_SCHEMA"),
  "first_month_stage_ids": (
    "gui/first-month.mjs",
    "export const FIRST_MONTH_STAGES = Object.freeze([",
  ),
  "campaign_coverage_stage_ids": (
    "gui/first-month.mjs",
    "export const CAMPAIGN_COVERAGE_STAGES = Object.freeze([",
  ),
  "first_month_test": (
    "tests/test_gui_first_month.py",
    "test_host_adapter_sequence_reaches_continue_and_rejection_stays_recoverable",
  ),
  "campaign_first_session_test": (
    "tests/test_phase12_live_campaign_coverage.py",
    "test_campaign_coverage_rail_advances_only_after_host_refresh",
  ),
  "settings_help": (
    "docs/evaluation/phase13.1-player-help-boundary.json",
    '"documented_contract"',
  ),
  "recovery_guidance": (
    "docs/guides/gui-how-to-play.md",
    "Use **Retry current read** when offered.",
  ),
}

EXPECTED_SHARED_SOURCES = {
  "technical_first_session_boundary": "docs/evaluation/phase13.1-first-session-boundary.json",
  "competitive_campaign_boundary": "docs/evaluation/phase13.1-competitive-campaign-boundary.json",
  "player_help_boundary": "docs/evaluation/phase13.1-player-help-boundary.json",
  "pilot_preparation": "docs/evaluation/phase13.2-pilot-preparation-boundary.json",
  "feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json",
  "facilitator_guide": "docs/guides/phase10.2-structured-evaluation.md",
  "player_guide": "docs/guides/gui-how-to-play.md",
}

EXPECTED_ACCESSIBILITY_SOURCES = {
  "written-equivalent": ("gui/index.html", 'id="result-list"'),
  "audio-off-and-cues-only": (
    "docs/evaluation/phase13.1-player-help-boundary.json",
    '"audio"',
  ),
  "reduced-motion-and-pacing": (
    "docs/evaluation/phase13.2-low-distraction-mode.json",
    '"enabled"',
  ),
  "large-text-and-keyboard": (
    "docs/guides/phase10.2-structured-evaluation.md",
    "keyboard navigation",
  ),
  "rejection-and-retry": ("gui/index.html", 'id="recovery-retry"'),
  "storage-limit": (
    "docs/guides/gui-how-to-play.md",
    "a storage failure does not block",
  ),
}


class FirstSessionReviewPacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_packet_is_technical_only_and_human_review_is_pending(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase13.1-first-session-review-packet-v1",
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
        "structured_first_time_user_evaluation_complete": False,
        "human_accessibility_review_complete": False,
        "educational_usability_review_complete": False,
        "competitive_campaign_human_review_complete": False,
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
        "go_no_go": None,
      },
    )
    self.assertNotIn("phase13.1-first-session-review-packet.json", RELEASE_MANIFEST.read_text(encoding="utf-8"))

  def test_source_contract_is_exact_and_independently_anchored(self):
    self.assertEqual(set(self.packet["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(self.packet["source_contract"][key], f"{source_path}: {marker}")
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      source_text = " ".join(path.read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, key)

  def test_stage_ids_match_the_exported_source_arrays(self):
    source = (ROOT / "gui" / "first-month.mjs").read_text(encoding="utf-8")

    def stage_ids(export_name):
      match = re.search(
        rf"export const {export_name} = Object\.freeze\(\[(.*?)\]\);",
        source,
        re.DOTALL,
      )
      self.assertIsNotNone(match, export_name)
      return re.findall(r'id: "([^"]+)"', match.group(1))

    technical = self.packet["technical_contract"]
    self.assertEqual(stage_ids("FIRST_MONTH_STAGES"), technical["competitive_stages"])
    self.assertEqual(
      stage_ids("CAMPAIGN_COVERAGE_STAGES"),
      technical["campaign_coverage_stages"],
    )

  def test_exact_flow_stages_and_participant_tasks_are_present(self):
    technical = self.packet["technical_contract"]
    self.assertEqual(technical["competitive_flow_schema"], "competitive-first-month-v1")
    self.assertEqual(
      technical["competitive_stages"],
      ["start", "inspect", "draft", "validate", "submit", "resolution", "continue"],
    )
    self.assertEqual(
      technical["campaign_coverage_flow_schema"],
      "campaign-coverage-first-session-v1",
    )
    self.assertEqual(
      technical["campaign_coverage_stages"],
      ["start", "inspect", "choose", "review", "continue"],
    )
    self.assertEqual(len(self.packet["participant_tasks"]), 5)
    self.assertEqual(
      [task["id"] for task in self.packet["participant_tasks"]],
      [
        "orient-and-launch",
        "complete-first-month",
        "recover-from-friction",
        "recognize-campaign-coverage",
        "adjust-presentation",
      ],
    )
    self.assertTrue(all(task["prompt"].endswith(".") for task in self.packet["participant_tasks"]))
    self.assertEqual(len(self.packet["review_questions"]), 5)
    self.assertTrue(all(question.endswith("?") for question in self.packet["review_questions"]))

  def test_authority_accessibility_and_recovery_limits_are_explicit(self):
    technical = self.packet["technical_contract"]
    self.assertEqual(
      technical["forbidden_browser_state_markers"],
      [
        "transition_competitive",
        "resolved_inputs",
        "effect_queue",
        "CompetitiveWorldState",
        "WorldState",
        "WebSocket",
      ],
    )
    first_session = json.loads(
      (ROOT / "docs" / "evaluation" / "phase13.1-first-session-boundary.json")
      .read_text(encoding="utf-8")
    )
    competitive = json.loads(
      (ROOT / "docs" / "evaluation" / "phase13.1-competitive-campaign-boundary.json")
      .read_text(encoding="utf-8")
    )
    self.assertEqual(technical["authority"], first_session["authority_boundary"])
    self.assertEqual(
      technical["forbidden_browser_state_markers"],
      competitive["surface_contract"]["browser_forbidden_authority_markers"],
    )
    authoritative_text = " ".join(
      [
        json.dumps(first_session),
        (ROOT / "docs" / "guides" / "gui-how-to-play.md").read_text(encoding="utf-8"),
        (ROOT / "docs" / "evaluation" / "phase13.1-player-help-boundary.json")
        .read_text(encoding="utf-8"),
        (ROOT / "docs" / "evaluation" / "phase13.2-pilot-preparation-boundary.json")
        .read_text(encoding="utf-8"),
      ]
    ).lower()
    for marker in (
      "rejected submission",
      "refresh failure",
      "storage limit",
      "audio",
      "reduced-motion",
      "large text",
      "keyboard",
      "skip/review",
    ):
      self.assertIn(marker, authoritative_text, marker)
    self.assertEqual(self.packet["shared_sources"], EXPECTED_SHARED_SOURCES)
    for source_path in self.packet["shared_sources"].values():
      self.assertTrue((ROOT / source_path).is_file(), source_path)
    self.assertEqual(
      technical["required_recovery_paths"],
      [
        "rejected submission",
        "refresh/read failure",
        "storage limit",
        "audio unavailable or muted",
        "reduced-motion or pacing friction",
      ],
    )
    self.assertEqual(
      technical["required_presentation_accommodations"],
      [
        "written equivalents",
        "audio-off and cues-only",
        "reduced motion",
        "Large text",
        "keyboard navigation",
        "skip/review controls",
      ],
    )
    for marker in (
      "rejected submission",
      "refresh",
      "storage",
      "mute",
      "reduced motion",
      "written equivalent",
      "cues-only",
      "large text",
      "keyboard",
      "skip/review",
    ):
      self.assertIn(marker, authoritative_text, marker)
    self.assertEqual(
      {check["id"] for check in self.packet["accessibility_and_recovery_checks"]},
      set(EXPECTED_ACCESSIBILITY_SOURCES),
    )
    for check in self.packet["accessibility_and_recovery_checks"]:
      source_path, marker = EXPECTED_ACCESSIBILITY_SOURCES[check["id"]]
      self.assertEqual(check["source"], f"{source_path}: {marker}")
      source_text = " ".join((ROOT / source_path).read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, check["id"])
    self.assertTrue(
      all(
        "pending" in check["status"] or "protocol-ready" in check["status"]
        for check in self.packet["accessibility_and_recovery_checks"]
      )
    )
    self.assertEqual(
      self.packet["causality_and_privacy_boundary"],
      {
        "host_owned_transitions_only": True,
        "actor_visible_observations_only": True,
        "no_hidden_state_inference": True,
        "no_causal_certainty": True,
        "no_participant_identity_in_packet": True,
        "no_external_data_collection": True,
        "source": "docs/evaluation/phase13.1-first-session-boundary.json",
      },
    )

  def test_roadmap_keeps_human_gates_open_and_records_packet(self):
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[ ] First-session workflow complete.", normalized)
    self.assertIn("[ ] Competitive campaign coverage complete.", normalized)
    self.assertIn("[x] Current technical first-session path documented and recoverable.", normalized)
    self.assertIn("[x] Current first-session technical review packet prepared.", normalized)
    self.assertIn("participant-ready", normalized)
    self.assertIn("pending human", normalized.lower())


if __name__ == "__main__":
  unittest.main()
