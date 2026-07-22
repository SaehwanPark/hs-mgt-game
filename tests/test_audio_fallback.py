import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "gui" / "audio.mjs"


class AudioFallbackTests(unittest.TestCase):
  def test_audio_projection_and_runtime_failures_preserve_visible_equivalents(self):
    script = r'''
      import { audioPresentationFor, createAudioClient } from './gui/audio.mjs';

      const loaded = audioPresentationFor('event.operating-loss', 'loaded');
      const failed = audioPresentationFor('event.operating-loss', 'failed');
      const contradictory = audioPresentationFor('event.operating-loss', { ok: true, status: 'failed' });
      const unknown = audioPresentationFor('unknown-audio', 'malformed');
      const unknownLoaded = audioPresentationFor('unknown-audio', 'loaded');
      if (loaded.display_mode !== 'asset' || loaded.equivalent !== 'Margin/cost result with direct contributors') process.exit(1);
      for (const outcome of [failed, contradictory, unknown, unknownLoaded]) {
        if (outcome.display_mode !== 'fallback' || outcome.release_path !== null || !outcome.equivalent) process.exit(2);
      }
      if (contradictory.asset_status !== 'malformed' || unknownLoaded.asset_status !== 'malformed' || unknown.rendered_label !== 'Audio unavailable') process.exit(3);

      const originalSetTimeout = globalThis.setTimeout;
      const originalClearTimeout = globalThis.clearTimeout;
      const timers = [];
      globalThis.setTimeout = (callback, delay) => {
        const timer = { callback, delay, cleared: false };
        timers.push(timer);
        return timer;
      };
      globalThis.clearTimeout = (timer) => { if (timer) timer.cleared = true; };

      function makeRoot() {
        const nodes = new Map();
        return {
          hidden: false,
          addEventListener() {},
          removeEventListener() {},
          querySelector(selector) {
            if (!nodes.has(selector)) nodes.set(selector, {
              textContent: '',
              value: '',
              checked: false,
              setAttribute() {},
              addEventListener() {},
            });
            return nodes.get(selector);
          },
        };
      }

      function gainNode() {
        return {
          gain: {
            value: 0.0001,
            setValueAtTime() {},
            exponentialRampToValueAtTime() {},
            cancelScheduledValues() {},
          },
          connect() {},
        };
      }

      class FakeContext {
        static fail = false;
        currentTime = 10;
        destination = {};
        async resume() {}
        async close() {}
        createGain() {
          if (FakeContext.fail) throw new Error('simulated playback failure');
          return gainNode();
        }
        createOscillator() {
          return {
            type: '',
            frequency: { value: 0 },
            connect() {},
            start() {},
            stop() {},
            onended: null,
          };
        }
      }

      const recorderEvents = [];
      const recorder = { record(type, fields) { recorderEvents.push({ type, fields }); } };
      const root = makeRoot();
      const client = createAudioClient({ root, AudioContextCtor: FakeContext, recorder });
      if (!(await client.enable()).ok || client.state().audio_status !== 'loaded') process.exit(4);
      FakeContext.fail = true;
      client.playCue('event.operating-loss');
      await Promise.resolve();
      if (client.state().audio_status !== 'failed' || client.state().queued_cues !== 0) process.exit(5);
      if (!recorderEvents.some((event) => event.type === 'audio_fallback') || !recorderEvents.some((event) => event.type === 'audio_playback_failed')) process.exit(6);
      if (!root.querySelector('#audio-state').textContent.includes('visual and written equivalent')) process.exit(7);
      FakeContext.fail = false;
      client.playCue('event.regulatory-decision');
      await Promise.resolve();
      if (client.state().audio_status !== 'loaded' || client.state().last_fallback !== null || client.state().active_cue_voices !== 1) process.exit(8);
      if (!root.querySelector('#audio-state').textContent.includes('Audio enabled')) process.exit(14);
      client.destroy();

      const unsupportedRoot = makeRoot();
      const unsupported = createAudioClient({ root: unsupportedRoot, AudioContextCtor: null });
      const unavailable = await unsupported.enable();
      if (unavailable.ok || unavailable.code !== 'audio_unsupported' || unavailable.presentation.display_mode !== 'fallback') process.exit(9);
      if (!unsupportedRoot.querySelector('#audio-state').textContent.includes('Audio unavailable')) process.exit(10);
      if (unsupported.playCue('ui.submit').code !== 'audio_unavailable') process.exit(11);
      unsupported.destroy();

      class SetupFailureContext extends FakeContext {
        createGain() { throw new Error('setup failure'); }
      }
      const setupFailure = createAudioClient({ root: makeRoot(), AudioContextCtor: SetupFailureContext });
      const setupResult = await setupFailure.enable();
      if (setupResult.ok || setupResult.code !== 'audio_playback_failed' || setupResult.presentation.asset_status !== 'failed') process.exit(12);
      setupFailure.destroy();
      if (JSON.stringify({ loaded, failed, contradictory, unknown }).match(/CompetitiveWorldState|resolved_inputs|private_rival|effect_queue|fetch\(|WebSocket|Math\.random/)) process.exit(13);
      globalThis.setTimeout = originalSetTimeout;
      globalThis.clearTimeout = originalClearTimeout;
      console.log('audio fallback contract passed');
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(AUDIO)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
