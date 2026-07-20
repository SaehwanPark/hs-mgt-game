import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "gui" / "audio-direction.mjs"
PROOF = ROOT / "gui" / "audio-proof.html"
README = ROOT / "gui" / "README.md"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class AudioDirectionTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.audio = AUDIO.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")

  def test_standards_and_prototypes_cover_phase_direction_slice(self):
    result = run_node(
      """
      import { AUDIO_DIRECTION, audioDirectionSummary } from "./gui/audio-direction.mjs";
      const standards = AUDIO_DIRECTION.standards;
      const entries = audioDirectionSummary();
      const required = [
        "audio.direction-confirm", "audio.direction-reject", "audio.direction-report",
        "audio.direction-riverside-motif", "audio.direction-neutral-bed",
        "audio.direction-pressure-layer", "audio.direction-environmental-loop",
      ];
      if (entries.length !== required.length || !required.every((id) => entries.some((entry) => entry.id === id))) process.exit(1);
      if (standards.loudness_target_lufs !== -24 || standards.peak_ceiling_dbfs !== -6) process.exit(2);
      if (standards.cue_duration_ms.min !== 80 || standards.cue_duration_ms.max !== 500) process.exit(3);
      console.log(JSON.stringify({ standards, entries }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    payload = json.loads(result.stdout)
    self.assertEqual(len(payload["entries"]), 7)

  def test_cues_are_distinguishable_and_loops_are_bounded(self):
    result = run_node(
      """
      import { AUDIO_DIRECTION } from "./gui/audio-direction.mjs";
      const cues = AUDIO_DIRECTION.prototypes.filter((entry) => entry.channel === "interface" || entry.channel === "event");
      if (new Set(cues.map((entry) => entry.pattern)).size !== cues.length) process.exit(1);
      for (const entry of AUDIO_DIRECTION.prototypes) {
        if (entry.peak_dbfs > AUDIO_DIRECTION.standards.peak_ceiling_dbfs) process.exit(2);
        if (entry.loopable && (entry.duration_ms < AUDIO_DIRECTION.standards.loop_duration_ms.min || entry.duration_ms > AUDIO_DIRECTION.standards.loop_duration_ms.max)) process.exit(3);
        if (entry.loopable && AUDIO_DIRECTION.standards.loop_crossfade_ms >= entry.duration_ms / 2) process.exit(4);
        if (!entry.visible_source || !entry.equivalent) process.exit(4);
      }
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_priority_cooldown_modes_and_reduced_audio_policy(self):
    result = run_node(
      """
      import { AUDIO_MODES, audioPriorityOrder, createAudioDirectionPolicy } from "./gui/audio-direction.mjs";
      let now = 1000;
      const policy = createAudioDirectionPolicy({ clock: () => now });
      const first = policy.request("audio.direction-confirm");
      const repeated = policy.request("audio.direction-confirm");
      now += 701;
      const afterCooldown = policy.request("audio.direction-confirm");
      if (!first.ok || first.priority !== 2 || first.duck_music_db !== -8) process.exit(1);
      if (repeated.ok || repeated.code !== "throttled" || !repeated.equivalent) process.exit(2);
      if (!afterCooldown.ok) process.exit(3);
      if (audioPriorityOrder()[0] !== "audio.direction-report") process.exit(4);
      policy.setMode(AUDIO_MODES.CUES_ONLY);
      if (policy.request("audio.direction-neutral-bed").code !== "visual_only") process.exit(5);
      if (!policy.request("audio.direction-reject").ok) process.exit(6);
      policy.setMode(AUDIO_MODES.FULL_AUDIO);
      policy.setReducedAudio(true);
      if (policy.request("audio.direction-pressure-layer").code !== "visual_only") process.exit(7);
      if (!policy.request("audio.direction-report").equivalent) process.exit(8);
      policy.setMode(AUDIO_MODES.MUTED);
      if (policy.request("audio.direction-report").code !== "visual_only") process.exit(9);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_loop_crossfade_reduces_boundary_delta(self):
    result = run_node(
      """
      import { AUDIO_DIRECTION, loopBoundaryDelta } from "./gui/audio-direction.mjs";
      const delta = loopBoundaryDelta({ durationMs: 6000, toneHz: 110, toneGain: 0.12 });
      if (AUDIO_DIRECTION.standards.loop_crossfade_ms !== 120 || delta >= 0.02) process.exit(1);
      console.log(delta);
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertLess(float(result.stdout.strip()), 0.02)

  def test_preview_player_has_visual_only_fallback(self):
    result = run_node(
      """
      import { createAudioDirectionPlayer } from "./gui/audio-direction.mjs";
      const player = createAudioDirectionPlayer({ AudioContextCtor: null });
      const result = await player.play("audio.direction-confirm");
      if (result.ok || result.code !== "audio_unsupported" || !result.entry.equivalent) process.exit(1);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_failed_playback_does_not_consume_cooldown(self):
    result = run_node(
      """
      import { createAudioDirectionPlayer } from "./gui/audio-direction.mjs";
      const player = createAudioDirectionPlayer({ AudioContextCtor: null });
      const first = await player.play("audio.direction-confirm");
      const second = await player.play("audio.direction-confirm");
      if (first.code !== "audio_unsupported" || second.code !== "audio_unsupported") process.exit(1);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_preview_player_catches_audio_context_failure(self):
    result = run_node(
      """
      import { createAudioDirectionPlayer } from "./gui/audio-direction.mjs";
      class RejectingContext {
        async resume() { throw new Error("blocked"); }
      }
      const player = createAudioDirectionPlayer({ AudioContextCtor: RejectingContext });
      const preview = await player.play("audio.direction-confirm");
      if (preview.ok || preview.code !== "audio_unsupported" || !preview.entry.equivalent) process.exit(1);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_preview_player_catches_node_construction_failure(self):
    result = run_node(
      """
      import { createAudioDirectionPlayer } from "./gui/audio-direction.mjs";
      class BrokenContext {
        get currentTime() { return 0; }
        async resume() {}
        createOscillator() { throw new Error("device failure"); }
        close() {}
      }
      const player = createAudioDirectionPlayer({ AudioContextCtor: BrokenContext });
      const preview = await player.play("audio.direction-confirm");
      if (preview.ok || preview.code !== "audio_unsupported" || !preview.entry.equivalent) process.exit(1);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_proof_page_and_module_are_presentation_only(self):
    for marker in ("AUDIO_DIRECTION", "audio-direction-v1", "audio-policy-v1", "loudness_target_lufs", "peak_ceiling_dbfs", "loopable", "cooldown_ms"):
      self.assertIn(marker, self.audio + self.proof)
    for marker in ("visible_source", "equivalent", "Play preview", "Audio is optional", "text equivalent", "data-mode", "cues-only", "reduced-audio", "audioPriorityOrder", "duck_music_db"):
      self.assertIn(marker, self.proof)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "effect_queue", "private_rival", "transition_competitive", "fetch(", "WebSocket"):
      self.assertNotIn(forbidden, self.audio + self.proof)
    self.assertIn("Audio direction proof", self.readme)
    self.assertNotRegex(self.audio, re.compile(r"https?://"))

  def test_javascript_syntax_is_valid(self):
    for path in (AUDIO, PROOF):
      if path.suffix == ".mjs":
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
