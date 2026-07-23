import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "gui" / "audio.mjs"
AUDIO_CONTRACT = ROOT / "gui" / "audio-cue-contract.mjs"
APP = ROOT / "gui" / "app.mjs"
APP_URI = APP.as_uri()
RESOLUTION = ROOT / "src" / "mcp" / "resolution.rs"


class Phase11LiveEventCueTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.resolution = RESOLUTION.read_text(encoding="utf-8")

  def test_legacy_visible_classifier_covers_every_supported_event_cue(self):
    script = f"""
      import {{ visibleEventCues }} from {json.dumps(AUDIO.as_uri())};
      import {{ AUDIO_CUE_CONTRACT }} from {json.dumps(AUDIO_CONTRACT.as_uri())};

      const fixtures = [
        {{ steps: ["Project complete was reported"] }},
        {{ observation: {{ workforce_trust: "Staffing constraint reported" }} }},
        {{ before: {{ observation: {{ operations: {{ margin: 0 }} }} }}, after: {{ observation: {{ operations: {{ margin: -1 }} }} }} }},
        {{ before: {{ observation: {{ operations: {{ margin: -1 }} }} }}, after: {{ observation: {{ operations: {{ margin: 0 }} }} }} }},
        {{ steps: ["Payer decision was reported"] }},
        {{ steps: ["Regulatory policy decision was reported"] }},
        {{ steps: ["Public rival expansion was observed"] }},
        {{ steps: ["Affiliation milestone was committed"] }},
      ];
      const expected = [
        "event.project-complete",
        "event.staffing-constraint",
        "event.operating-loss",
        "event.operating-recovery",
        "event.payer-decision",
        "event.regulatory-decision",
        "event.rival-expansion",
        "event.affiliation-milestone",
      ];
      const actual = fixtures.map((fixture) => visibleEventCues(fixture)).flat();
      const catalog = new Set(AUDIO_CUE_CONTRACT.entries.map((entry) => entry.id));
      if (JSON.stringify([...new Set(actual)]) !== JSON.stringify(expected)) process.exit(1);
      if (expected.some((cueId) => !catalog.has(cueId))) process.exit(2);
      console.log(JSON.stringify({{ actual, expected }}));
    """
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["expected"], json.loads(result.stdout)["actual"])

  def test_live_resolution_prefers_explicit_host_projection_and_preserves_legacy_fallback(self):
    self.assertIn("export function resolutionAudioCueIds", self.app)
    self.assertIn("const cueIds = resolutionAudioCueIds(resolution.envelope)", self.app)
    script = f"""
      import {{ resolutionAudioCueIds }} from {json.dumps(APP_URI)};
      const explicitEmpty = resolutionAudioCueIds({{ audio_cue_ids: [], steps: ["Project complete"] }});
      const explicitList = resolutionAudioCueIds({{ audio_cue_ids: ["event.payer-decision"] }});
      const legacy = resolutionAudioCueIds({{ steps: ["Payer decision was reported"] }});
      const malformed = resolutionAudioCueIds({{ audio_cue_ids: "event.payer-decision", steps: ["Payer decision was reported"] }});
      const unknown = resolutionAudioCueIds({{ audio_cue_ids: ["event.unknown"] }});
      if (explicitEmpty.length !== 0) process.exit(1);
      if (JSON.stringify(explicitList) !== JSON.stringify(["event.payer-decision"])) process.exit(2);
      if (JSON.stringify(legacy) !== JSON.stringify(["event.payer-decision"])) process.exit(3);
      if (JSON.stringify(malformed) !== JSON.stringify(["event.payer-decision"])) process.exit(4);
      if (JSON.stringify(unknown) !== JSON.stringify(["event.unknown"])) process.exit(5);
      console.log(JSON.stringify({{ explicitEmpty, explicitList, legacy, malformed, unknown }}));
    """
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["explicitEmpty"], [])
    self.assertIn("for (const cueId of cueIds) audioClient.playCue(cueId)", self.app)
    self.assertIn("audio_cue_ids", self.resolution)
    self.assertIn("visible_event_cue_ids", self.resolution)
    self.assertIn("TransitionSummary", self.resolution)
    self.assertIn("ReadOnlyObservation", self.resolution)
    for cue_id in (
      "event.project-complete",
      "event.staffing-constraint",
      "event.operating-loss",
      "event.operating-recovery",
      "event.payer-decision",
      "event.regulatory-decision",
      "event.rival-expansion",
      "event.affiliation-milestone",
    ):
      self.assertIn(cue_id, self.resolution)
    for forbidden in (
      "resolved_inputs",
      "effect_queue",
      "private_rival",
      "fetch(",
      "WebSocket",
      "http://",
      "https://",
    ):
      self.assertNotIn(forbidden, self.app)
      self.assertNotIn(forbidden, self.resolution)
    self.assertNotIn("CompetitiveWorldState", self.app)

  def test_javascript_syntax_is_valid(self):
    for path in (AUDIO, AUDIO_CONTRACT, APP):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
