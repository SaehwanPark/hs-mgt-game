import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MUSIC = ROOT / "gui" / "music-stem-contract.mjs"
APP = ROOT / "gui" / "app.mjs"
RESOLUTION = ROOT / "src" / "mcp" / "resolution.rs"


class Phase11LiveMusicTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.music = MUSIC.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.resolution = RESOLUTION.read_text(encoding="utf-8")

  def test_visible_music_classifier_covers_each_live_selectable_state(self):
    script = f"""
      import {{ MUSIC_STEM_CONTRACT, classifyVisibleMusicState }} from {json.dumps(MUSIC.as_uri())};
      const fixtures = [
        {{ done: true }},
        {{ observation: {{ policy_bullets: ["Regulatory review letter reported"] }} }},
        {{ observation: {{ market_bullets: ["Affiliation partner negotiation reported"] }} }},
        {{ observation: {{ market_bullets: ["Public rival expansion reported"] }} }},
        {{ observation: {{ operations: {{ margin: -1, unmet_demand: 0 }} }} }},
        {{ observation: {{ operations: {{ margin: 10, unmet_demand: 0 }}, cash_runway_signal: "adequate", workforce_trust: "stable", in_flight_projects: "none" }} }},
      ];
      const expected = [
        "debrief",
        "regulatory_scrutiny",
        "affiliation_negotiation",
        "competitive_escalation",
        "pressure",
        "stable_operations",
      ];
      const actual = fixtures.map((fixture) => classifyVisibleMusicState(fixture));
      const catalog = new Set(MUSIC_STEM_CONTRACT.entries.map((entry) => entry.id));
      if (JSON.stringify(actual) !== JSON.stringify(expected)) process.exit(1);
      if (expected.some((state) => !catalog.has(state))) process.exit(2);
      console.log(JSON.stringify({{ actual, expected }}));
    """
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    payload = json.loads(result.stdout)
    self.assertEqual(payload["expected"], payload["actual"])

  def test_live_resolution_prefers_explicit_music_state_and_preserves_fallback(self):
    script = f"""
      import {{ resolutionMusicStateId }} from {json.dumps(APP.as_uri())};
      const valid = resolutionMusicStateId({{ music_state_id: "pressure" }});
      const empty = resolutionMusicStateId({{ music_state_id: "  " }});
      const malformed = resolutionMusicStateId({{ music_state_id: 42 }});
      const unknown = resolutionMusicStateId({{ music_state_id: "future-state" }});
      if (valid !== "pressure") process.exit(1);
      if (empty !== null || malformed !== null) process.exit(2);
      if (unknown !== "future-state") process.exit(3);
      console.log(JSON.stringify({{ valid, empty, malformed, unknown }}));
    """
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(json.loads(result.stdout)["valid"], "pressure")
    self.assertIn("music_state_id", self.resolution)
    self.assertIn("visible_music_state_id", self.resolution)
    self.assertIn("const musicStateId = resolutionMusicStateId(resolution.envelope)", self.app)
    self.assertIn("audioClient.setMusicState(musicStateId, resolution.envelope.after)", self.app)
    self.assertIn("audioClient.setMusicFromVisible(resolution.envelope.after)", self.app)
    for state in (
      "debrief",
      "regulatory_scrutiny",
      "affiliation_negotiation",
      "competitive_escalation",
      "pressure",
      "stable_operations",
    ):
      self.assertIn(state, self.resolution)
      self.assertIn(state, self.music)
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
    for path in (MUSIC, APP):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
