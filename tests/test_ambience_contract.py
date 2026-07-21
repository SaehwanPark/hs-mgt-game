import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "gui" / "ambience-contract.mjs"
AUDIO = ROOT / "gui" / "audio.mjs"
PROOF = ROOT / "gui" / "ambience-proof.html"
GUI_CATALOG = ROOT / "gui" / "audio-catalog.json"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class AmbienceContractTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.contract = CONTRACT.read_text(encoding="utf-8")
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.gui_catalog = json.loads(GUI_CATALOG.read_text(encoding="utf-8"))

  def test_all_seven_settings_have_provenance_levels_and_safety_metadata(self):
    result = run_node(
      """
      import { AMBIENCE_CONTRACT, defaultAmbience, validateAmbienceContracts } from './gui/ambience-contract.mjs';
      const expected = [
        'ambience.executive-office',
        'ambience.hospital-lobby',
        'ambience.hospital-campus-exterior',
        'ambience.construction-site',
        'ambience.boardroom',
        'ambience.press-policy-event',
        'ambience.regional-city-bed',
      ];
      if (AMBIENCE_CONTRACT.schema_version !== 'ambience-library-v1' || AMBIENCE_CONTRACT.entries.length !== 7) process.exit(1);
      if (JSON.stringify(AMBIENCE_CONTRACT.entries.map((entry) => entry.id)) !== JSON.stringify(expected)) process.exit(2);
      if (AMBIENCE_CONTRACT.default_id !== 'ambience.regional-city-bed' || defaultAmbience()?.id !== AMBIENCE_CONTRACT.default_id) process.exit(3);
      if (validateAmbienceContracts().length) process.exit(4);
      for (const entry of AMBIENCE_CONTRACT.entries) {
        if (!entry.source_or_generation || entry.license !== 'project-generated' || !entry.source_hash_basis || !entry.release_derivative) process.exit(5);
        if (!Number.isFinite(entry.noise_floor_db) || entry.loudness_target_db !== -24 || entry.peak_ceiling_dbfs !== -6) process.exit(6);
        if (!entry.loop.seamless || !entry.loop.reviewed || entry.loop.end_ms <= entry.loop.start_ms || entry.loop.crossfade_ms <= 0) process.exit(7);
        if (entry.recipe.waveform !== 'noise' || entry.recipe.filter !== 'lowpass' || entry.recipe.noise_floor_db !== entry.noise_floor_db || entry.recipe.crossfade_ms !== entry.loop.crossfade_ms || !Number.isFinite(entry.recipe.seed)) process.exit(8);
        if (!entry.no_identifying_speech || !entry.no_copyrighted_music || !entry.no_real_institution_names || !entry.no_clinical_alarm) process.exit(9);
        if (!entry.reduced_audio || !entry.text_equivalent || !entry.visible_source || !entry.fallback) process.exit(10);
      }
      console.log(JSON.stringify({ count: AMBIENCE_CONTRACT.entries.length, default_id: AMBIENCE_CONTRACT.default_id }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(json.loads(result.stdout)["count"], 7)

  def test_runtime_catalog_contains_all_settings_and_uses_regional_bed_default(self):
    result = run_node(
      """
      import { AUDIO_CATALOG, createAudioClient } from './gui/audio.mjs';
      if (AUDIO_CATALOG.ambience.length !== 7) process.exit(1);
      if (AUDIO_CATALOG.ambience.some((entry) => entry.channel !== 'ambience' || !entry.recipe || !entry.text_equivalent || !entry.release_derivative)) process.exit(2);
      if (!AUDIO_CATALOG.ambience.some((entry) => entry.id === 'ambience.regional-city-bed')) process.exit(3);
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
      if (client.setMode('cues-only').mode !== 'cues-only' || client.state().mode !== 'cues-only') process.exit(4);
      if (client.setMode('unknown').ok) process.exit(5);
      if (client.state().ambience !== null) process.exit(6);
      if (client.setAmbienceFromVisible({ campaign: 'competitive-regional-v1' }).id !== 'ambience.regional-city-bed') process.exit(7);
      if (client.setAmbienceFromVisible({ campaign: 'stabilization-v1' }).id !== null) process.exit(8);
      client.destroy();
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_runtime_waits_for_visible_context_and_uses_filtered_noise_path(self):
    result = run_node(
      """
      import { createAudioClient } from './gui/audio.mjs';
      const calls = [];
      const nativeSetTimeout = globalThis.setTimeout;
      const nativeClearTimeout = globalThis.clearTimeout;
      globalThis.setTimeout = (callback, duration) => { calls.push(['timer', duration]); return calls.length; };
      globalThis.clearTimeout = () => {};
      const gainNode = () => ({ gain: { setValueAtTime() {}, exponentialRampToValueAtTime() {} }, connect() {} });
      class FakeContext {
        currentTime = 0;
        sampleRate = 8000;
        destination = {};
        async resume() {}
        close() {}
        createGain() { return gainNode(); }
        createBiquadFilter() { return { type: '', frequency: { value: 0 }, connect() {} }; }
        createBuffer(channels, frames) { return { getChannelData() { return new Float32Array(frames); } }; }
        createBufferSource() { calls.push(['buffer-source']); return { buffer: null, connect() {}, start() {}, stop() {} }; }
        createOscillator() { calls.push(['oscillator']); return { type: '', frequency: { value: 0 }, connect() {}, start() {}, stop() {} }; }
      }
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
      const client = createAudioClient({ root, AudioContextCtor: FakeContext });
      await client.enable();
      if (calls.some(([kind]) => kind === 'buffer-source')) process.exit(1);
      client.setAmbienceFromVisible({ campaign: 'competitive-regional-v1' });
      if (!calls.some(([kind]) => kind === 'buffer-source')) process.exit(2);
      if (client.state().ambience !== 'ambience.regional-city-bed') process.exit(3);
      client.destroy();
      globalThis.setTimeout = nativeSetTimeout;
      globalThis.clearTimeout = nativeClearTimeout;
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_registry_catalog_and_proof_keep_ambience_optional_and_visible_only(self):
    for marker in (
      "ambience-library-v1",
      "source_or_generation",
      "source_hash_basis",
      "release_derivative",
      "noise_floor_db",
      "loop",
      "crossfade_ms",
      "loudness_target_db",
      "peak_ceiling_dbfs",
      "no_identifying_speech",
      "no_copyrighted_music",
      "no_real_institution_names",
      "no_clinical_alarm",
      "reduced_audio",
      "noise_amplitude",
      "setAmbienceFromVisible",
      "text_equivalent",
      "validation errors",
      "ambience.regional-city-bed",
    ):
      self.assertIn(marker, self.contract + self.audio + self.proof)
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
    ambience_entries = [entry for entry in self.gui_catalog["entries"] if entry["id"].startswith("ambience.")]
    self.assertEqual(len(ambience_entries), 7)
    self.assertEqual(self.gui_catalog["third_party_assets"], [])
    self.assertEqual({entry["original_hash"] for entry in ambience_entries}, {"sha256:8e0d18d9d91ee8d00386a75965ee8589bb40066ad581c81d00dfcc0cc43eb82e"})
    self.assertTrue(all(entry["release_hash"] is None for entry in ambience_entries))

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
