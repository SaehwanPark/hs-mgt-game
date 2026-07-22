import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "gui" / "audio-priority-contract.mjs"
AUDIO = ROOT / "gui" / "audio.mjs"
HTML = ROOT / "gui" / "index.html"
PROOF = ROOT / "gui" / "audio-priority-proof.html"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class AudioPriorityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.contract = CONTRACT.read_text(encoding="utf-8")
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")

  def test_policy_plans_priority_critical_limit_and_aggregation(self):
    result = run_node(
      """
      import { AUDIO_PRIORITY_POLICY, planAudioCueBatch, validateAudioPriorityPolicy } from './gui/audio-priority-contract.mjs';
      if (validateAudioPriorityPolicy().length || AUDIO_PRIORITY_POLICY.maximum_simultaneous_cue_voices !== 1) process.exit(1);
      const plan = planAudioCueBatch([
        'event.operating-loss',
        'event.regulatory-decision',
        'event.project-complete',
        'ui.action-add',
        'ui.action-confirm',
        'ui.action-confirm',
      ]);
      if (plan.selected[0].id !== 'event.operating-loss') process.exit(2);
      if (plan.critical_suppressed_count !== 1 || plan.routine_aggregated_count !== 2 || plan.duplicate_ids.length !== 1) process.exit(3);
      if (plan.selected.some((request, index) => index > 0 && request.priority === 'critical')) process.exit(4);
      if (plan.selected.length > AUDIO_PRIORITY_POLICY.maximum_batch_cues) process.exit(5);
      console.log(JSON.stringify({ selected: plan.selected.map((request) => request.id), plan }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(json.loads(result.stdout)["selected"][0], "event.operating-loss")

  def test_runtime_queue_ducking_stress_and_preference_round_trip(self):
    result = run_node(
      """
      import { createAudioClient } from './gui/audio.mjs';
      const timers = [];
      const started = [];
      const ramps = [];
      const recorderEvents = [];
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
              setValueAtTime: () => {},
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
            stop: () => {},
            onended: null,
          };
          return source;
        }
      }
      class FailingContext extends FakeContext {
        createGain() {
          if (FailingContext.fail) throw new Error('audio context failure');
          return super.createGain();
        }
      }
      FailingContext.fail = false;
      const root = { hidden: false, addEventListener() {}, removeEventListener() {}, querySelector() { return null; } };
      const recorder = { record(type, fields) { recorderEvents.push({ type, fields }); } };
      const storage = {
        value: null,
        getItem() { return this.value; },
        setItem(key, value) { this.value = value; },
      };
      try {
        const client = createAudioClient({ root, AudioContextCtor: FakeContext, storage, recorder });
        await client.enable();
        const musicStarts = started.length;
        client.playCue('event.operating-loss');
        await Promise.resolve();
        if (client.state().active_cue_voices !== 1 || client.state().ducking !== 'critical') process.exit(1);
        if (started.length !== musicStarts + 1 || !ramps.some((event) => Math.abs(event.time - 10.04) < 0.001 && event.value < 0.02)) process.exit(2);
        const duckTimer = timers.find((timer) => timer.delay === 320);
        if (!duckTimer) process.exit(3);
        duckTimer.callback();
        if (client.state().ducking !== null || !ramps.some((event) => Math.abs(event.time - 10.04) < 0.001 && event.value > 0.02)) process.exit(4);
        for (const id of ['event.regulatory-decision', 'event.payer-decision', 'event.rival-expansion', 'ui.action-add', 'ui.action-remove']) client.playCue(id);
        await Promise.resolve();
        if (client.state().active_cue_voices !== 1 || client.state().queued_cues > 4 || !recorderEvents.some((event) => event.type === 'audio_queue_bounded')) process.exit(5);
        const burstResults = ['ui.submit', 'ui.advance-month', 'ui.report-received', 'ui.save-complete', 'event.staffing-constraint'].map((id) => client.playCue(id));
        if (burstResults.some((result) => result.queue_size > 4)) process.exit(6);
        const cueTimer = timers.find((timer) => timer.delay === 180);
        if (!cueTimer) process.exit(7);
        cueTimer.callback();
        if (client.state().active_cue_voices > 1) process.exit(8);
        const failing = createAudioClient({ root, AudioContextCtor: FailingContext, storage: null, recorder });
        await failing.enable();
        FailingContext.fail = true;
        failing.playCue('event.operating-loss');
        await Promise.resolve();
        if (failing.state().queued_cues !== 0 || !recorderEvents.some((event) => event.type === 'audio_playback_failed')) process.exit(9);
        FailingContext.fail = false;
        failing.playCue('event.regulatory-decision');
        await Promise.resolve();
        if (failing.state().active_cue_voices !== 1) process.exit(10);
        failing.destroy();
        client.setVolume('music', 0.25);
        client.setMode('cues-only');
        client.setMusicMuted(true);
        client.setReducedNotifications(true);
        client.setMuted(true);
        const restored = createAudioClient({ root, AudioContextCtor: null, storage }).state();
        if (restored.mode !== 'cues-only' || !restored.musicMuted || !restored.muted || !restored.reducedNotifications || restored.volumes.music !== 0.25) process.exit(11);
        storage.value = JSON.stringify({ muted: 'false', musicMuted: 'false', reducedNotifications: 'false', mode: 'full', volumes: { music: 0.25 } });
        const malformed = createAudioClient({ root, AudioContextCtor: null, storage }).state();
        if (malformed.muted || malformed.musicMuted || malformed.reducedNotifications) process.exit(12);
        const brokenStorage = { getItem() { throw new Error('blocked'); }, setItem() { throw new Error('blocked'); } };
        const safe = createAudioClient({ root, AudioContextCtor: null, storage: brokenStorage });
        safe.setVolume('event', 0.4);
        safe.setMuted(true);
        safe.destroy();
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

  def test_live_region_proof_and_forbidden_authority_markers(self):
    for marker in (
      "audio-priority-manager-v1",
      "maximum_critical_per_batch",
      "maximum_queued_cues",
      "maximum_simultaneous_cue_voices",
      "routine_aggregation_minimum",
      "duck_attack_ms",
      "storage_key",
      "audio_queue_bounded",
      "audio_batch_planned",
      "aria-live=\"polite\"",
      "audio-equivalent",
      "Fixture-only",
      "Written equivalent",
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
