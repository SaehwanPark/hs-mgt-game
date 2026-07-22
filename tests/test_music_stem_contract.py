import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "gui" / "music-stem-contract.mjs"
AUDIO = ROOT / "gui" / "audio.mjs"
HTML = ROOT / "gui" / "index.html"
PROOF = ROOT / "gui" / "music-stem-proof.html"
GUI_CATALOG = ROOT / "gui" / "audio-catalog.json"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class MusicStemContractTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.contract = CONTRACT.read_text(encoding="utf-8")
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.gui_catalog = json.loads(GUI_CATALOG.read_text(encoding="utf-8"))

  def test_seven_states_and_five_stems_have_complete_contracts(self):
    result = run_node(
      """
      import { MUSIC_STEM_CONTRACT, MUSIC_STEM_ROLES, musicStateFor, validateMusicStemContracts } from './gui/music-stem-contract.mjs';
      const expected = ['menu', 'stable_operations', 'pressure', 'regulatory_scrutiny', 'competitive_escalation', 'affiliation_negotiation', 'debrief'];
      if (MUSIC_STEM_CONTRACT.schema_version !== 'adaptive-music-stem-contract-v1' || MUSIC_STEM_CONTRACT.entries.length !== 7) process.exit(1);
      if (JSON.stringify(MUSIC_STEM_CONTRACT.stem_roles) !== JSON.stringify(['base_pulse', 'institutional_motif', 'pressure_layer', 'policy_layer', 'transition_cadence'])) process.exit(2);
      if (JSON.stringify(MUSIC_STEM_CONTRACT.entries.map((entry) => entry.id)) !== JSON.stringify(expected)) process.exit(3);
      if (validateMusicStemContracts().length || musicStateFor('unknown') !== null) process.exit(4);
      for (const entry of MUSIC_STEM_CONTRACT.entries) {
        if (entry.stem_order.length !== 5 || entry.stem_order.some((role) => !entry.stems[role])) process.exit(5);
        if (!entry.visible_trigger_source || !entry.text_equivalent || !entry.fallback || entry.crossfade_ms <= 0) process.exit(6);
      }
      console.log(JSON.stringify({ count: MUSIC_STEM_CONTRACT.entries.length, roles: MUSIC_STEM_ROLES.length }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    payload = json.loads(result.stdout)
    self.assertEqual(payload["count"], 7)
    self.assertEqual(payload["roles"], 5)

  def test_visible_classifier_and_replay_sequence_use_only_visible_inputs(self):
    result = run_node(
      """
      import { classifyVisibleMusicState, musicPlanFromVisible, musicReplaySequence } from './gui/music-stem-contract.mjs';
      const inputs = [
        { stage: 'menu' },
        { observation: { policy_bullets: ['Regulatory oversight review is visible'] } },
        { reports: ['Public rival expansion observed in the market'] },
        { decisions: ['Affiliation negotiation review is visible'] },
        { observation: { operations: { margin: -1, unmet_demand: 2 } } },
        { stage: 'planning' },
        { done: true },
      ];
      const expected = ['menu', 'regulatory_scrutiny', 'competitive_escalation', 'affiliation_negotiation', 'pressure', 'menu', 'debrief'];
      if (JSON.stringify(musicReplaySequence(inputs)) !== JSON.stringify(expected)) process.exit(1);
      if (musicPlanFromVisible(inputs[2]).state !== 'competitive_escalation') process.exit(2);
      if (classifyVisibleMusicState({ true_state: { hidden: 'pressure' }, observation: {} }) !== 'stable_operations') process.exit(3);
      if (classifyVisibleMusicState({ campaign: 'competitive-regional-v1', observation: {} }) !== 'stable_operations') process.exit(4);
      const hiddenNested = {
        actors: [{ private_intent: 'negotiation', hidden_outcome: 'regulatory review' }],
        reports: [{ private_intent: 'rival expansion' }],
        processes: [{ hidden_status: 'pressure' }],
        decisions: [{ private_intent: 'affiliation' }],
      };
      if (classifyVisibleMusicState(hiddenNested) !== 'stable_operations') process.exit(5);
      console.log(JSON.stringify({ sequence: musicReplaySequence(inputs) }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(json.loads(result.stdout)["sequence"][0], "menu")

  def test_runtime_catalog_and_music_only_mute_remain_optional(self):
    result = run_node(
      """
      import { AUDIO_CATALOG, createAudioClient } from './gui/audio.mjs';
      if (AUDIO_CATALOG.music.length !== 7) process.exit(1);
      if (AUDIO_CATALOG.music.some((entry) => entry.stem_order.length !== 5 || !entry.stems.transition_cadence || !entry.text_equivalent)) process.exit(2);
      const nodes = new Map();
      const root = {
        hidden: false,
        addEventListener() {},
        removeEventListener() {},
        querySelector(selector) {
          if (!nodes.has(selector)) nodes.set(selector, { value: '', checked: false, textContent: '', addEventListener() {}, setAttribute() {} });
          return nodes.get(selector);
        },
      };
      const client = createAudioClient({ root, AudioContextCtor: null });
      if (client.setMusicState('regulatory_scrutiny').state !== 'regulatory_scrutiny') process.exit(3);
      if (client.setMusicMuted(true).musicMuted !== true || client.state().musicMuted !== true) process.exit(4);
      if (client.setMusicMuted(false).musicMuted !== false) process.exit(5);
      if (client.setMode('cues-only').mode !== 'cues-only') process.exit(6);
      client.destroy();
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_runtime_music_stems_release_with_bounded_crossfade(self):
    result = run_node(
      """
      import { createAudioClient } from './gui/audio.mjs';
      const timers = [];
      const started = [];
      const stopped = [];
      const ramps = [];
      const originalSetTimeout = globalThis.setTimeout;
      const originalClearTimeout = globalThis.clearTimeout;
      globalThis.setTimeout = (callback, delay) => {
        const timer = { callback, delay, cleared: false };
        timers.push(timer);
        return timer;
      };
      globalThis.clearTimeout = (timer) => { if (timer) timer.cleared = true; };
      class FakeContext {
        constructor() { this.currentTime = 10; this.destination = {}; }
        async resume() {}
        async close() {}
        createGain() {
          return {
            gain: {
              value: 0.0001,
              setValueAtTime: (value) => { this.lastGain = value; },
              exponentialRampToValueAtTime: (value, time) => ramps.push({ value, time }),
              cancelScheduledValues: () => {},
            },
            connect: () => {},
          };
        }
        createOscillator() {
          const source = {
            type: '',
            frequency: { value: 0 },
            connect: () => {},
            start: (time) => started.push({ source, time }),
            stop: (time) => stopped.push({ source, time }),
            onended: null,
          };
          return source;
        }
      }
      const root = {
        hidden: false,
        addEventListener() {},
        removeEventListener() {},
        querySelector() { return null; },
      };
      try {
        const client = createAudioClient({ root, AudioContextCtor: FakeContext });
        await client.enable();
        if (started.length !== 4 || !timers.some((timer) => timer.delay === 2700) || !timers.some((timer) => timer.delay === 3600)) process.exit(1);
        client.setMusicState('pressure');
        if (stopped.length < 4 || !stopped.some((event) => Math.abs(event.time - 10.26) < 0.001)) process.exit(2);
        if (!ramps.some((event) => Math.abs(event.time - 10.26) < 0.001 && event.value === 0.0001)) process.exit(3);
        const startsBeforeCue = started.length;
        client.setMusicMuted(true);
        client.playCue('ui.action-confirm');
        await Promise.resolve();
        if (started.length !== startsBeforeCue + 1) process.exit(4);
        const startsBeforeFullMute = started.length;
        client.setMuted(true);
        client.playCue('ui.action-confirm');
        await Promise.resolve();
        if (started.length !== startsBeforeFullMute) process.exit(5);
        client.destroy();
        console.log('pass');
      } finally {
        globalThis.setTimeout = originalSetTimeout;
        globalThis.clearTimeout = originalClearTimeout;
      }
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_proof_catalog_and_controls_preserve_visible_fallbacks(self):
    for marker in (
      "adaptive-music-stem-contract-v1",
      "base_pulse",
      "institutional_motif",
      "pressure_layer",
      "policy_layer",
      "transition_cadence",
      "crossfade_ms",
      "visible_trigger_source",
      "text_equivalent",
      "music-only",
      "audio-music-mute",
      "MUSIC_STEM_CONTRACT",
      "validation errors",
    ):
      self.assertIn(marker, self.contract + self.audio + self.html + self.proof)
    for forbidden in (
      "CompetitiveWorldState",
      "resolved_inputs",
      "effect_queue",
      "private_rival",
      "fetch(",
      "WebSocket",
      "Math.random",
      "http://",
      "https://",
    ):
      self.assertNotIn(forbidden, self.contract + self.audio + self.proof)
    music_entries = [entry for entry in self.gui_catalog["entries"] if entry["id"] in {
      "menu",
      "stable_operations",
      "pressure",
      "regulatory_scrutiny",
      "competitive_escalation",
      "affiliation_negotiation",
      "debrief",
    }]
    self.assertEqual(len(music_entries), 7)
    self.assertEqual({entry["original_hash"] for entry in music_entries}, {"sha256:61743c70ee86c5004e6474d07a12b3b7f42a9dcd646151574aa2e4e267059a35"})
    self.assertTrue(all(entry["release_hash"] is None for entry in music_entries))

  def test_javascript_syntax_is_valid(self):
    for path in (CONTRACT, AUDIO):
      result = subprocess.run(
        ["node", "--check", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
