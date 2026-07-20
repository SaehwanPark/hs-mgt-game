import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "gui" / "audio.mjs"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
REGISTRY = ROOT / "gui" / "audio-catalog.json"
CREDITS = ROOT / "gui" / "ASSET_CREDITS.md"
DOC = ROOT / "docs" / "history" / "initiatives" / "visual-audio" / "visual-audio-phase5-foundational-audio-v0.12.21.md"


class GuiAudioTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cls.credits = CREDITS.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_catalog_covers_phase0_music_and_cues_with_registry_entries(self):
    for marker in (
      'schema_version: "audio-catalog-v1"',
      'id: "menu"',
      'id: "stable_operations"',
      'id: "pressure"',
      'id: "debrief"',
      'ui.action-confirm',
      'ui.action-reject',
      'ui.action-add',
      'ui.action-remove',
      'ui.submit',
      'ui.advance-month',
      'ui.report-received',
      'ui.save-complete',
      'event.project-complete',
      'event.staffing-constraint',
      'event.operating-loss',
      'event.operating-recovery',
      'event.payer-decision',
      'event.regulatory-decision',
      'event.rival-expansion',
      'event.affiliation-milestone',
      'regional_ambience',
      'visible_source',
      'equivalent',
      'cooldown_ms',
    ):
      self.assertIn(marker, self.audio)
    self.assertEqual(self.registry["schema_version"], "audio-registry-v1")
    self.assertEqual(self.registry["third_party_assets"], [])
    self.assertEqual(len(self.registry["entries"]), 21)
    for entry in self.registry["entries"]:
      for field in (
        "id",
        "source",
        "creator",
        "license",
        "attribution_text",
        "approval_status",
      ):
        self.assertIn(field, entry)

  def test_classifier_and_recording_sink_are_visible_only(self):
    for marker in (
      "classifyMusicState",
      "visibleEventCues",
      "createRecordingSink",
      "recordCue",
      "operations.margin",
      "operations.unmet_demand",
      "cash_runway_signal",
      "explicit page stage",
      "visual and text equivalents",
    ):
      self.assertIn(marker, self.audio)
    for forbidden in (
      "CompetitiveWorldState",
      "resolved_inputs",
      "effect_queue",
      "private_rival",
      "fetch(",
      "WebSocket",
      "http://",
      "https://",
    ):
      self.assertNotIn(forbidden, self.audio)

  def test_controls_and_integration_are_present(self):
    for marker in (
      "createAudioClient",
      "AUDIO_CATALOG",
      "ui.action-confirm",
      "ui.action-reject",
      "ui.action-add",
      "ui.action-remove",
      "ui.submit",
      "ui.advance-month",
      "ui.report-received",
      "visibleEventCues",
      "audio-enable",
      "audio_unsupported",
      "reducedNotifications",
      "visibilitychange",
      "setVolume",
      "setMuted",
      "setFocused",
    ):
      self.assertIn(marker, self.audio + self.app)
    for selector in (
      'id="audio-panel"',
      'id="audio-enable"',
      'id="audio-mute"',
      'id="audio-reduced-notifications"',
      'id="audio-master-volume"',
      'id="audio-music-volume"',
      'id="audio-interface-volume"',
      'id="audio-event-volume"',
      'id="audio-ambience-volume"',
    ):
      self.assertIn(selector, self.html)

  def test_registry_credits_and_phase_boundary_are_explicit(self):
    for marker in (
      "no third-party audio files",
      "Web Audio API",
      "retrieval date",
      "license URL",
      "approval",
    ):
      self.assertIn(marker, self.credits + self.doc)
    for marker in (
      "## Typed/pure presentation contract",
      "## Source and authority map",
      "## Browser behavior",
      "## Registry and credits",
      "## Static review checklist",
      "Phase 6",
      "human",
    ):
      self.assertIn(marker, self.doc)
    self.assertIn("audio-catalog-v1", self.readme + self.doc)

  def test_javascript_syntax_is_valid(self):
    for path in (AUDIO, APP):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
