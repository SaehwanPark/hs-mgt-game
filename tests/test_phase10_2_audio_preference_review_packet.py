import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "evaluation" / "phase10.2-audio-preference-review-packet.json"
PROTOCOL = ROOT / "docs" / "evaluation" / "phase10.2-evaluation-protocol.json"
PILOT = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
RELEASE_MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"


EXPECTED_SHARED_SOURCES = {
  "evaluation_protocol": "docs/evaluation/phase10.2-evaluation-protocol.json",
  "pilot_feedback_instrument": "docs/evaluation/phase13.2-pilot-feedback-instrument.json",
  "facilitator_guide": "docs/guides/phase10.2-structured-evaluation.md",
  "player_guide": "docs/guides/gui-how-to-play.md",
  "audio_cue_contract": "gui/audio-cue-contract.mjs",
  "audio_priority_contract": "gui/audio-priority-contract.mjs",
  "music_stem_contract": "gui/music-stem-contract.mjs",
  "ambience_contract": "gui/ambience-contract.mjs",
  "audio_runtime": "gui/audio.mjs",
  "presentation_settings": "gui/app.mjs",
  "audio_markup": "gui/index.html",
  "audio_registry": "gui/audio-catalog.json",
  "audio_contract_tests": "tests/test_gui_audio.py",
  "audio_fallback_tests": "tests/test_audio_fallback.py",
  "audio_priority_tests": "tests/test_audio_priority.py",
  "revision_log": "docs/evaluation/phase10.2-revision-log.md",
}


EXPECTED_SOURCE_CONTRACT = {
  "protocol_audio_task": (
    "docs/evaluation/phase10.2-evaluation-protocol.json",
    '"audio-preference-and-equivalent"',
  ),
  "protocol_rating_dimensions": (
    "docs/evaluation/phase10.2-evaluation-protocol.json",
    '"audio-usefulness"',
  ),
  "protocol_privacy": (
    "docs/evaluation/phase10.2-evaluation-protocol.json",
    '"repository_must_not_contain"',
  ),
  "protocol_pending_decision": (
    "docs/evaluation/phase10.2-evaluation-protocol.json",
    '"pending-human-evidence"',
  ),
  "pilot_audio_task": (
    "docs/evaluation/phase13.2-pilot-feedback-instrument.json",
    '"pilot-audio-choice"',
  ),
  "pilot_rating_dimensions": (
    "docs/evaluation/phase13.2-pilot-feedback-instrument.json",
    '"audio-fatigue"',
  ),
  "pilot_forbidden_fields": (
    "docs/evaluation/phase13.2-pilot-feedback-instrument.json",
    '"browser URLs or session IDs"',
  ),
  "facilitator_audio_sequence": (
    "docs/guides/phase10.2-structured-evaluation.md",
    "Try full audio, cues-only, mute, reduced notifications, unavailable audio",
  ),
  "facilitator_audio_off": (
    "docs/guides/phase10.2-structured-evaluation.md",
    "Begin with audio off and explain that every cue has a written equivalent",
  ),
  "player_audio_guidance": (
    "docs/guides/gui-how-to-play.md",
    "written equivalent",
  ),
  "cue_schema": (
    "gui/audio-cue-contract.mjs",
    "export const AUDIO_CUE_CONTRACT_SCHEMA",
  ),
  "cue_written_equivalent_policy": (
    "gui/audio-cue-contract.mjs",
    "written_equivalent_rule",
  ),
  "cue_only_channels": (
    "gui/audio-cue-contract.mjs",
    "cues_only_channels",
  ),
  "cue_trigger_contract": (
    "gui/audio-cue-contract.mjs",
    "trigger_is_visible_only",
  ),
  "priority_schema": (
    "gui/audio-priority-contract.mjs",
    "export const AUDIO_PRIORITY_MANAGER_SCHEMA",
  ),
  "priority_limits": (
    "gui/audio-priority-contract.mjs",
    "maximum_critical_per_batch",
  ),
  "music_schema": (
    "gui/music-stem-contract.mjs",
    "export const MUSIC_STEM_CONTRACT_SCHEMA",
  ),
  "music_fallback": (
    "gui/music-stem-contract.mjs",
    "Music unavailable or suppressed; the visible heading, status, source, and result remain complete.",
  ),
  "ambience_schema": (
    "gui/ambience-contract.mjs",
    "export const AMBIENCE_CONTRACT_SCHEMA",
  ),
  "ambience_fallback": (
    "gui/ambience-contract.mjs",
    "Ambience unavailable; written setting and decision-relevant text remain complete.",
  ),
  "visible_audio_projection": ("gui/audio.mjs", "export function audioPresentationFor"),
  "visible_music_projection": ("gui/audio.mjs", "export function classifyMusicState"),
  "visible_event_cues": ("gui/audio.mjs", "export function visibleEventCues"),
  "audio_mode_state": ("gui/audio.mjs", 'let mode = ["full", "cues-only"]'),
  "audio_unavailable_fallback": ("gui/audio.mjs", "Audio unavailable;"),
  "audio_muted_fallback": (
    "gui/audio.mjs",
    "Audio muted; visual and text equivalents remain active.",
  ),
  "cues_only_behavior": (
    "gui/audio.mjs",
    "Cues-only mode enabled; music and ambience are off",
  ),
  "written_audio_status": ("gui/index.html", 'id="audio-state"'),
  "audio_mode_control": ("gui/index.html", 'id="audio-mode"'),
  "audio_reduced_notifications_control": (
    "gui/index.html",
    'id="audio-reduced-notifications"',
  ),
  "audio_equivalent_copy": ("gui/index.html", 'id="audio-equivalent"'),
  "low_distraction_audio_boundary": ("gui/app.mjs", "applyLowDistractionAudio"),
  "focus_pause_boundary": ("gui/audio.mjs", "setFocused"),
  "registry_generated_source": (
    "gui/audio-catalog.json",
    '"generated_source": "gui/audio.mjs"',
  ),
  "registry_no_third_party_assets": (
    "gui/audio-catalog.json",
    '"third_party_assets": []',
  ),
  "fallback_test": (
    "tests/test_audio_fallback.py",
    "test_audio_projection_and_runtime_failures_preserve_visible_equivalents",
  ),
  "priority_test": (
    "tests/test_audio_priority.py",
    "test_policy_plans_priority_critical_limit_and_aggregation",
  ),
  "contract_test": (
    "tests/test_gui_audio.py",
    "test_catalog_covers_phase0_music_and_cues_with_registry_entries",
  ),
}


EXPECTED_MUSIC_IDS = [
  "menu",
  "stable_operations",
  "pressure",
  "regulatory_scrutiny",
  "competitive_escalation",
  "affiliation_negotiation",
  "debrief",
]

EXPECTED_INTERFACE_CUES = [
  "ui.action-confirm",
  "ui.action-reject",
  "ui.action-add",
  "ui.action-remove",
  "ui.submit",
  "ui.advance-month",
  "ui.report-received",
  "ui.save-complete",
]

EXPECTED_EVENT_CUES = [
  "event.project-complete",
  "event.staffing-constraint",
  "event.operating-loss",
  "event.operating-recovery",
  "event.payer-decision",
  "event.regulatory-decision",
  "event.rival-expansion",
  "event.affiliation-milestone",
]

EXPECTED_AMBIENCE_IDS = [
  "ambience.executive-office",
  "ambience.hospital-lobby",
  "ambience.hospital-campus-exterior",
  "ambience.construction-site",
  "ambience.boardroom",
  "ambience.press-policy-event",
  "ambience.regional-city-bed",
]

EXPECTED_ACCESSIBILITY_SOURCES = {
  "audio-off-written-equivalent": ("gui/index.html", 'id="audio-equivalent"'),
  "audio-status-live-region": (
    "gui/index.html",
    'id="audio-state" aria-live="polite"',
  ),
  "cues-only-channel-boundary": (
    "gui/audio-cue-contract.mjs",
    "cues_only_channels",
  ),
  "unavailable-audio-fallback": (
    "tests/test_audio_fallback.py",
    "test_audio_projection_and_runtime_failures_preserve_visible_equivalents",
  ),
  "reduced-notifications": (
    "gui/index.html",
    'id="audio-reduced-notifications"',
  ),
  "low-distraction-audio": ("gui/app.mjs", "applyLowDistractionAudio"),
  "focus-loss-recovery": ("gui/audio.mjs", "setFocused"),
  "keyboard-audio-controls": (
    "gui/app.mjs",
    "#audio-panel button, #audio-panel input, #audio-panel select",
  ),
}


class AudioPreferenceReviewPacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    cls.pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_packet_is_technical_only_and_not_a_release_asset(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase10.2-audio-preference-review-packet-v1",
    )
    self.assertEqual(
      self.packet["status"],
      "complete-technical-packet-pending-human-review",
    )
    self.assertTrue(self.packet["review_boundary"]["technical_packet_complete"])
    for key, value in self.packet["review_boundary"].items():
      if key != "technical_packet_complete":
        self.assertFalse(value, key)
    self.assertEqual(
      self.packet["response_shape"]["decision_fields"],
      {
        "status": "pending-human-evidence",
        "go_no_go": None,
        "authorized_reviewer": None,
        "recorded_at": None,
        "rationale": None,
      },
    )
    self.assertFalse(self.packet["release_boundary"]["release_ready"])
    self.assertTrue(self.packet["release_boundary"]["technical_packet_does_not_authorize_release"])
    self.assertNotIn(
      "phase10.2-audio-preference-review-packet.json",
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

  def test_protocol_and_pilot_audio_fields_are_mirrored_without_results(self):
    protocol_task = next(
      task for task in self.protocol["tasks"] if task["id"] == "audio-preference-and-equivalent"
    )
    self.assertEqual(
      protocol_task,
      {
        "id": "audio-preference-and-equivalent",
        "category": "audio",
        "prompt": "Try full audio, cues-only, mute, reduced notifications, unavailable audio, and written equivalents.",
        "success_observation": "Participant reports usefulness, fatigue, and any lost meaning without sound.",
      },
    )
    pilot_task = next(task for task in self.pilot["tasks"] if task["id"] == "pilot-audio-choice")
    self.assertEqual(
      pilot_task,
      {
        "id": "pilot-audio-choice",
        "source_task": "audio-preference-and-equivalent",
        "prompt": "Try audio off, mute, cues-only, reduced notifications, and written equivalents; rate usefulness and fatigue only if observed.",
        "response": "completed | skipped | not-observed",
      },
    )
    self.assertIn("audio-usefulness", self.protocol["rating_dimensions"])
    self.assertIn("audio-fatigue", self.protocol["rating_dimensions"])
    self.assertIn("audio-usefulness", self.pilot["rating_dimensions"])
    self.assertIn("audio-fatigue", self.pilot["rating_dimensions"])
    self.assertEqual(
      self.packet["response_shape"]["task_status"],
      ["completed", "skipped", "not-observed"],
    )
    self.assertEqual(
      self.packet["response_shape"]["finding_categories"],
      ["defect", "preference", "scope-expansion"],
    )
    self.assertFalse(self.packet["review_boundary"]["participant_results_present"])

  def test_audio_catalog_contract_ids_and_limits_are_exact(self):
    technical = self.packet["technical_contract"]
    self.assertEqual(technical["music_state_ids"], EXPECTED_MUSIC_IDS)
    self.assertEqual(technical["interface_cue_ids"], EXPECTED_INTERFACE_CUES)
    self.assertEqual(technical["event_cue_ids"], EXPECTED_EVENT_CUES)
    self.assertEqual(technical["ambience_ids"], EXPECTED_AMBIENCE_IDS)
    self.assertEqual(
      technical["preference_modes"],
      [
        "full",
        "cues-only",
        "muted/audio-off",
        "reduced-notifications",
        "music-only-mute",
        "focus-loss",
        "audio-unavailable",
      ],
    )
    self.assertEqual(
      technical["priority_limits"],
      {
        "maximum_critical_per_batch": 1,
        "maximum_batch_cues": 4,
        "maximum_queued_cues": 4,
        "maximum_simultaneous_cue_voices": 1,
        "routine_aggregation_minimum": 2,
      },
    )
    registry = json.loads((ROOT / "gui" / "audio-catalog.json").read_text(encoding="utf-8"))
    self.assertEqual(registry["schema_version"], "audio-registry-v1")
    self.assertEqual(registry["third_party_assets"], [])
    self.assertEqual(len(registry["entries"]), 30)
    registry_ids = {entry["id"] for entry in registry["entries"]}
    self.assertEqual(
      registry_ids,
      set(EXPECTED_MUSIC_IDS + EXPECTED_INTERFACE_CUES + EXPECTED_EVENT_CUES + EXPECTED_AMBIENCE_IDS),
    )

  def test_sequence_and_fallback_checks_are_complete_and_pending(self):
    self.assertEqual(
      [step["id"] for step in self.packet["evaluation_sequence"]],
      [
        "audio-off-baseline",
        "full-audio-comparison",
        "cues-only-comparison",
        "mute-and-reduced-notifications",
        "unavailable-and-focus-recovery",
        "written-equivalent-reconstruction",
      ],
    )
    self.assertEqual(len(self.packet["review_questions"]), 7)
    self.assertTrue(all(question.endswith("?") for question in self.packet["review_questions"]))
    self.assertEqual(
      {check["id"] for check in self.packet["accessibility_and_fallback_checks"]},
      {
        "audio-off-written-equivalent",
        "audio-status-live-region",
        "cues-only-channel-boundary",
        "unavailable-audio-fallback",
        "reduced-notifications",
        "low-distraction-audio",
        "focus-loss-recovery",
        "keyboard-audio-controls",
      },
    )
    for check in self.packet["accessibility_and_fallback_checks"]:
      source_path, marker = EXPECTED_ACCESSIBILITY_SOURCES[check["id"]]
      self.assertEqual(check["source"], f"{source_path}: {marker}")
      source = ROOT / source_path
      self.assertTrue(source.is_file(), check["id"])
      source_text = " ".join(source.read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, check["id"])
      self.assertTrue("pending" in check["status"] or "executable" in check["status"])
    self.assertTrue(self.packet["technical_observations"]["human_listening_quality_is_unverified"])

  def test_authority_privacy_provenance_and_roadmap_limits_are_explicit(self):
    boundary = self.packet["authority_privacy_provenance_boundary"]
    self.assertIn("Rust host owns", boundary["host_authority"])
    self.assertIn("browser", boundary["browser_authority"].lower())
    self.assertIn("no third-party audio files", boundary["audio_provenance"].lower())
    for forbidden_claim in (
      "participant preference or usefulness result",
      "audio fatigue or listening quality result",
      "universal accessibility",
      "educational effectiveness",
      "cross-browser or device certification",
      "legal clearance or public-release approval",
      "go/no-go decision",
    ):
      self.assertIn(forbidden_claim, boundary["forbidden_claims"])
    for marker in (
      "Audio preference feedback collected",
      "Quantitative ratings collected",
      "Qualitative interviews completed",
      "Findings classified as defect, preference, or scope expansion",
      "Go/no-go decision recorded",
    ):
      self.assertIn(f"- [ ] {marker}", self.roadmap)
    self.assertIn("phase10.2-audio-preference-review-packet.json", self.roadmap)
    self.assertIn("Current technical audio preference/listening review packet prepared", self.roadmap)

  def test_audio_contract_tests_and_node_syntax_pass(self):
    commands = [
      [
        sys.executable,
        "-m",
        "unittest",
        "tests/test_gui_audio.py",
        "tests/test_audio_fallback.py",
        "tests/test_audio_priority.py",
        "tests/test_audio_cue_contract.py",
        "tests/test_music_stem_contract.py",
        "tests/test_ambience_contract.py",
      ],
      ["node", "--check", "gui/audio.mjs"],
      ["node", "--check", "gui/audio-cue-contract.mjs"],
      ["node", "--check", "gui/audio-priority-contract.mjs"],
      ["node", "--check", "gui/music-stem-contract.mjs"],
      ["node", "--check", "gui/ambience-contract.mjs"],
    ]
    for command in commands:
      result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, f"{command}\n{result.stdout}\n{result.stderr}")


if __name__ == "__main__":
  unittest.main()
