import hashlib
import json
import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "evaluation" / "phase13.2-debrief-visual-review-packet.json"
MANIFEST = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-raster-evidence.json"
TRANSCRIPT = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-terminal-capture-transcript.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
RELEASE_MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"


CASES = {
  "competitive-regional-v1": {"turn": "24/24", "history": 24},
  "stabilization-v1": {"turn": "5/5", "history": 5},
  "regional-affiliation-v1": {"turn": "6/6", "history": 6},
}


def jpeg_dimensions(data):
  if not data.startswith(b"\xff\xd8"):
    raise AssertionError("artifact is not a JPEG")
  sof_markers = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
  }
  offset = 2
  while offset < len(data):
    if data[offset] != 0xFF:
      offset += 1
      continue
    while offset < len(data) and data[offset] == 0xFF:
      offset += 1
    marker = data[offset]
    offset += 1
    if marker in (0xD8, 0xD9):
      continue
    if marker == 0xDA:
      break
    segment_length = struct.unpack(">H", data[offset:offset + 2])[0]
    if marker in sof_markers:
      height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
      return width, height
    offset += segment_length
  raise AssertionError("JPEG dimensions were not found")


class DebriefVisualReviewPacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cls.transcript = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_packet_is_exact_three_case_technical_boundary(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase13.2-debrief-visual-review-packet-v1",
    )
    self.assertEqual(
      self.packet["status"],
      "complete-technical-packet-pending-human-review",
    )
    self.assertEqual(
      self.packet["review_boundary"],
      {
        "technical_packet_complete": True,
        "human_visual_review_complete": False,
        "human_accessibility_review_complete": False,
        "educational_and_classroom_review_complete": False,
        "audio_listening_review_complete": False,
        "public_release_approval": False,
      },
    )
    self.assertEqual(
      {case["campaign"] for case in self.packet["cases"]},
      set(CASES),
    )
    self.assertEqual(len(self.packet["cases"]), 3)
    self.assertEqual(len(self.packet["review_questions"]), 5)
    self.assertTrue(all(question.endswith("?") for question in self.packet["review_questions"]))

  def test_cases_bind_corrected_terminal_artifacts_and_transcript(self):
    manifest_records = {
      record["campaign"]: record
      for record in self.manifest["state_records"]
      if record["state"] == "terminal"
    }
    transcript_records = {
      record["campaign"]: record
      for record in self.transcript["captures"]
    }
    self.assertEqual(
      {(record["campaign"], record["state"]) for record in self.manifest["state_records"]},
      {(campaign, state) for campaign in CASES for state in ("active", "terminal")},
    )
    self.assertEqual(len(self.manifest["state_records"]), 6)
    self.assertEqual(len(self.transcript["captures"]), 3)
    self.assertEqual(len(manifest_records), 3)
    self.assertEqual(len(transcript_records), 3)
    self.assertEqual(set(manifest_records), set(CASES))
    self.assertEqual(set(transcript_records), set(CASES))
    release_manifest_text = RELEASE_MANIFEST.read_text(encoding="utf-8")
    for case in self.packet["cases"]:
      campaign = case["campaign"]
      expected = CASES[campaign]
      manifest = manifest_records[campaign]
      transcript = transcript_records[case["transcript_campaign"]]
      artifact = ROOT / case["raster_artifact"]
      data = artifact.read_bytes()
      observed = transcript["observed_dom"]
      host = transcript["host_envelope"]
      self.assertEqual(case["terminal_turn"], expected["turn"])
      self.assertEqual(
        case["host_visible_sections"],
        ["committed campaign history", "campaign debrief", "host-shaped decision"],
      )
      self.assertEqual(
        case["technical_assertions"],
        {
          "session_done": True,
          "history_count": expected["history"],
          "debrief_non_empty": True,
          "placeholder_debrief": False,
          "campaign_decision_controls": 0,
          "written_equivalent": True,
          "optional_audio": True,
          "replay_state_remains_host_owned": True,
          "actor_visible_only": True,
        },
      )
      self.assertEqual(manifest["artifact"], case["raster_artifact"])
      self.assertEqual(transcript["artifact"], case["raster_artifact"])
      self.assertTrue(artifact.is_file())
      self.assertEqual(jpeg_dimensions(data), (1024, 768))
      self.assertEqual(manifest["sha256"], hashlib.sha256(data).hexdigest())
      self.assertEqual(transcript["normalized_artifact"]["mime_type"], "image/jpeg")
      self.assertEqual(transcript["normalized_artifact"]["byte_size"], len(data))
      self.assertEqual(
        transcript["normalized_artifact"]["sha256"],
        hashlib.sha256(data).hexdigest(),
      )
      self.assertEqual(
        (transcript["normalized_artifact"]["width"], transcript["normalized_artifact"]["height"]),
        (1024, 768),
      )
      self.assertEqual(host["session"]["campaign"], campaign)
      self.assertEqual(host["session"]["turn"], expected["turn"])
      self.assertTrue(host["session"]["done"])
      self.assertEqual(host["history_count"], expected["history"])
      self.assertGreater(host["debrief_line_count"], 0)
      self.assertEqual(host["terminal_controls"]["campaign_decision_count"], 0)
      self.assertFalse(observed["placeholder_present"])
      self.assertIn("No campaign decision is available", observed["decision_excerpt"])
      self.assertNotIn("Submit host-shaped decision", observed["decision_excerpt"])
      self.assertNotIn("Commit decision", observed["decision_excerpt"])
      self.assertEqual(
        len(re.findall(r"- strong: Turn [0-9]+", observed["history_excerpt"])),
        expected["history"],
      )
      self.assertEqual(
        len(re.findall(r"- listitem:", observed["debrief_excerpt"])),
        host["debrief_line_count"],
      )
      self.assertNotIn(case["raster_artifact"], release_manifest_text)

  def test_source_accessibility_causality_and_human_review_limits_are_explicit(self):
    source_paths = self.packet["shared_sources"]
    for key, value in source_paths.items():
      source_path = value.split(":", 1)[0]
      self.assertTrue((ROOT / source_path).is_file(), key)
    source_markers = {
      "renderer": [("gui/app.mjs", "renderCampaignCoverage")],
      "audio": [("gui/audio.mjs", "createAudioClient")],
      "desktop_surface": [
        ("gui/index.html", 'id="campaign-debrief-list"'),
        ("gui/index.html", 'id="campaign-history-list"'),
      ],
      "host_projection": [
        ("src/mcp/campaign_coverage.rs", "from_stabilization"),
        ("src/mcp/campaign_coverage.rs", "from_affiliation"),
        ("src/mcp/campaign_coverage.rs", "from_competitive"),
      ],
      "terminal_tests": [("src/mcp/session.rs", "fn campaign_coverage_terminal_")],
    }
    for key, markers in source_markers.items():
      for source_path, marker in markers:
        source_text = (ROOT / source_path).read_text(encoding="utf-8")
        self.assertIn(marker, source_text, key)
    renderer = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    audio = (ROOT / "gui" / "audio.mjs").read_text(encoding="utf-8")
    surface = (ROOT / "gui" / "index.html").read_text(encoding="utf-8")
    host = (ROOT / "src" / "mcp" / "campaign_coverage.rs").read_text(encoding="utf-8")
    self.assertIn("renderCampaignCoverage", renderer)
    self.assertIn("No campaign decision is available", renderer)
    self.assertIn("createAudioClient", audio)
    self.assertIn('id="campaign-debrief-list"', surface)
    self.assertIn('id="campaign-history-list"', surface)
    self.assertIn("let decisions = if done", host)
    self.assertEqual(
      {check["id"] for check in self.packet["accessibility_and_fallback_checks"]},
      {"written-equivalent", "audio-off-and-mute", "reduced-motion", "large-text-and-keyboard", "recovery"},
    )
    self.assertTrue(all("human" in check["status"] or "pending" in check["status"] for check in self.packet["accessibility_and_fallback_checks"]))
    self.assertEqual(
      self.packet["causality_and_replay_boundary"],
      {
        "committed_effects_only": True,
        "no_hidden_state_inference": True,
        "no_causal_certainty": True,
        "history_is_immutable": True,
        "browser_has_no_transition_authority": True,
        "source": "docs/evaluation/phase13.2-debrief-visual-boundary.json",
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
    normalized_roadmap = " ".join(self.roadmap.split())
    self.assertIn("[ ] Debrief visuals reviewed.", normalized_roadmap)
    self.assertIn(
      "[x] Current technical debrief visual review packet prepared.",
      normalized_roadmap,
    )


if __name__ == "__main__":
  unittest.main()
