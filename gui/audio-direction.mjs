const AUDIO_STANDARDS = Object.freeze({
  schema_version: "audio-direction-v1",
  sample_rate_hz: 48000,
  loudness_target_lufs: -24,
  loudness_tolerance_lufs: 2,
  peak_ceiling_dbfs: -6,
  cue_duration_ms: Object.freeze({ min: 80, max: 500 }),
  loop_duration_ms: Object.freeze({ min: 4000, max: 8000 }),
  loop_crossfade_ms: 120,
  speech_duck_db: -8,
  minimum_preview_gain: 0.25,
});

export const AUDIO_MODES = Object.freeze({
  FULL_AUDIO: "full-audio",
  CUES_ONLY: "cues-only",
  MUTED: "muted",
});

export const AUDIO_POLICY = Object.freeze({
  schema_version: "audio-policy-v1",
  priority_order: Object.freeze(["event", "interface", "music", "ambience"]),
  ducking_db: -8,
  reduced_audio_channels: Object.freeze(["music", "ambience"]),
});

const PROTOTYPES = Object.freeze([
  {
    id: "audio.direction-confirm",
    label: "Confirmation",
    channel: "interface",
    semantic_role: "ui-cue",
    visible_source: "Local confirmation result or host validation response",
    equivalent: "Confirmation status and affected control text",
    purpose: "A short ascending two-note acknowledgement without urgency.",
    duration_ms: 240,
    peak_dbfs: -12,
    loopable: false,
    priority: 2,
    cooldown_ms: 700,
    pattern: "ascending-major-second",
    recipe: Object.freeze({
      kind: "partials",
      attack_ms: 12,
      release_ms: 80,
      partials: Object.freeze([
        Object.freeze({ waveform: "sine", frequency_hz: 523.25, gain: 0.7 }),
        Object.freeze({ waveform: "sine", frequency_hz: 659.25, gain: 0.55 }),
      ]),
    }),
  },
  {
    id: "audio.direction-reject",
    label: "Rejection",
    channel: "interface",
    semantic_role: "ui-cue",
    visible_source: "Host rejection or failed visible validation",
    equivalent: "Error text and unchanged-session marker",
    purpose: "A compact descending minor-second signal that is distinct but not punitive.",
    duration_ms: 280,
    peak_dbfs: -12,
    loopable: false,
    priority: 2,
    cooldown_ms: 700,
    pattern: "descending-minor-second",
    recipe: Object.freeze({
      kind: "partials",
      attack_ms: 12,
      release_ms: 100,
      partials: Object.freeze([
        Object.freeze({ waveform: "triangle", frequency_hz: 311.13, gain: 0.65 }),
        Object.freeze({ waveform: "triangle", frequency_hz: 277.18, gain: 0.6 }),
      ]),
    }),
  },
  {
    id: "audio.direction-report",
    label: "Report arrival",
    channel: "event",
    semantic_role: "event-cue",
    visible_source: "New visible report or briefing item",
    equivalent: "Report heading, source label, and timing text",
    purpose: "A soft three-note arrival that invites reading rather than demanding attention.",
    duration_ms: 420,
    peak_dbfs: -15,
    loopable: false,
    priority: 3,
    cooldown_ms: 1500,
    pattern: "soft-open-triad",
    recipe: Object.freeze({
      kind: "partials",
      attack_ms: 20,
      release_ms: 160,
      partials: Object.freeze([
        Object.freeze({ waveform: "sine", frequency_hz: 392, gain: 0.6 }),
        Object.freeze({ waveform: "sine", frequency_hz: 493.88, gain: 0.45 }),
        Object.freeze({ waveform: "sine", frequency_hz: 587.33, gain: 0.3 }),
      ]),
    }),
  },
  {
    id: "audio.direction-riverside-motif",
    label: "Riverside motif",
    channel: "music",
    semantic_role: "music-state",
    visible_source: "Visible Riverside institution identity",
    equivalent: "Riverside name, marker, and report-header treatment",
    purpose: "A restrained open-fifth motif for the fictional player system identity.",
    duration_ms: 1800,
    peak_dbfs: -24,
    loopable: false,
    priority: 1,
    cooldown_ms: 0,
    pattern: "open-fifth-pulse",
    recipe: Object.freeze({
      kind: "partials",
      attack_ms: 80,
      release_ms: 240,
      partials: Object.freeze([
        Object.freeze({ waveform: "sine", frequency_hz: 261.63, gain: 0.45 }),
        Object.freeze({ waveform: "triangle", frequency_hz: 392, gain: 0.25 }),
      ]),
    }),
  },
  {
    id: "audio.direction-northlake-motif",
    label: "Northlake motif",
    channel: "music",
    semantic_role: "music-state",
    visible_source: "Visible Northlake institution identity",
    equivalent: "Northlake name, marker, and report-header treatment",
    purpose: "A restrained layered-fourth motif for the fictional public rival identity.",
    duration_ms: 1800,
    peak_dbfs: -24,
    loopable: false,
    priority: 1,
    cooldown_ms: 0,
    pattern: "layered-fourth-pulse",
    recipe: Object.freeze({
      kind: "partials",
      attack_ms: 80,
      release_ms: 240,
      partials: Object.freeze([
        Object.freeze({ waveform: "sine", frequency_hz: 293.66, gain: 0.45 }),
        Object.freeze({ waveform: "triangle", frequency_hz: 391.995, gain: 0.25 }),
      ]),
    }),
  },
  {
    id: "audio.direction-summit-motif",
    label: "Summit motif",
    channel: "music",
    semantic_role: "music-state",
    visible_source: "Visible Summit institution identity",
    equivalent: "Summit name, marker, and report-header treatment",
    purpose: "A restrained rising minor-third motif for the fictional market system identity.",
    duration_ms: 1800,
    peak_dbfs: -24,
    loopable: false,
    priority: 1,
    cooldown_ms: 0,
    pattern: "rising-minor-third",
    recipe: Object.freeze({
      kind: "partials",
      attack_ms: 80,
      release_ms: 240,
      partials: Object.freeze([
        Object.freeze({ waveform: "sine", frequency_hz: 329.63, gain: 0.45 }),
        Object.freeze({ waveform: "triangle", frequency_hz: 392, gain: 0.25 }),
      ]),
    }),
  },
  {
    id: "audio.direction-neutral-bed",
    label: "Neutral ambient bed",
    channel: "ambience",
    semantic_role: "ambience",
    visible_source: "Optional active competitive-month presentation ambience",
    equivalent: "Current month, regional market heading, and written operating summary",
    purpose: "A low-level non-semantic bed that does not encode status or outcome.",
    duration_ms: 6000,
    peak_dbfs: -30,
    loopable: true,
    priority: 0,
    cooldown_ms: 0,
    pattern: "filtered-neutral-noise",
    recipe: Object.freeze({ kind: "filtered-noise", filter_hz: 700, tone_hz: 110, tone_gain: 0.12 }),
  },
  {
    id: "audio.direction-pressure-layer",
    label: "Pressure layer",
    channel: "music",
    semantic_role: "music-state",
    visible_source: "Actor-visible margin, unmet-demand, runway, or pressure signal",
    equivalent: "Visible pressure banner and affected metric text",
    purpose: "A bounded low-register layer that responds only to visible pressure categories.",
    duration_ms: 6000,
    peak_dbfs: -28,
    loopable: true,
    priority: 1,
    cooldown_ms: 0,
    pattern: "slow-low-pulse",
    recipe: Object.freeze({ kind: "filtered-noise", filter_hz: 420, tone_hz: 146.83, tone_gain: 0.16 }),
  },
  {
    id: "audio.direction-environmental-loop",
    label: "Environmental loop",
    channel: "ambience",
    semantic_role: "ambience",
    visible_source: "Optional non-semantic regional operating environment",
    equivalent: "Regional board, current date, and written operating context",
    purpose: "A generated filtered-noise loop with no speech, names, sirens, or decision signal.",
    duration_ms: 6000,
    peak_dbfs: -32,
    loopable: true,
    priority: 0,
    cooldown_ms: 0,
    pattern: "filtered-environmental-noise",
    recipe: Object.freeze({ kind: "filtered-noise", filter_hz: 900, tone_hz: 73.42, tone_gain: 0.08 }),
  },
]);

export const AUDIO_DIRECTION = Object.freeze({
  standards: AUDIO_STANDARDS,
  policy: AUDIO_POLICY,
  prototypes: PROTOTYPES,
});

const PROTOTYPE_BY_ID = new Map(PROTOTYPES.map((entry) => [entry.id, entry]));

export function audioDirectionEntry(id) {
  return PROTOTYPE_BY_ID.get(id) ?? null;
}

export function audioDirectionSummary() {
  return PROTOTYPES.map(({ id, label, channel, visible_source, equivalent, purpose, duration_ms, peak_dbfs, loopable, pattern, priority, cooldown_ms }) => ({
    id,
    label,
    channel,
    visible_source,
    equivalent,
    purpose,
    duration_ms,
    peak_dbfs,
    loopable,
    pattern,
    priority,
    cooldown_ms,
  }));
}

export function audioPriorityOrder(ids = PROTOTYPES.map((entry) => entry.id)) {
  return ids
    .map((id) => audioDirectionEntry(id))
    .filter(Boolean)
    .sort((left, right) => right.priority - left.priority || left.id.localeCompare(right.id))
    .map((entry) => entry.id);
}

export function createAudioDirectionPolicy({ clock = () => Date.now() } = {}) {
  let mode = AUDIO_MODES.FULL_AUDIO;
  let reducedAudio = false;
  const lastRequestedAt = new Map();

  function decision(entry, ok, code = null) {
    return {
      ok,
      code,
      id: entry.id,
      entry,
      equivalent: entry.equivalent,
      priority: entry.priority,
      duck_music_db: entry.priority >= 2 ? AUDIO_POLICY.ducking_db : 0,
      mode,
      reducedAudio,
    };
  }

  function request(id, { commit = true } = {}) {
    const entry = audioDirectionEntry(id);
    if (!entry) return { ok: false, code: "unknown_audio_direction_id" };
    const modeBlocks = mode === AUDIO_MODES.MUTED
      || (mode === AUDIO_MODES.CUES_ONLY && !["interface", "event"].includes(entry.channel));
    const preferenceBlocks = reducedAudio && AUDIO_POLICY.reduced_audio_channels.includes(entry.channel);
    if (modeBlocks || preferenceBlocks) return decision(entry, false, "visual_only");
    const now = Number(clock());
    const previous = lastRequestedAt.get(entry.id);
    if (previous != null && now - previous < entry.cooldown_ms) return decision(entry, false, "throttled");
    if (commit) lastRequestedAt.set(entry.id, now);
    return decision(entry, true);
  }

  function commit(id) {
    const entry = audioDirectionEntry(id);
    if (!entry) return { ok: false, code: "unknown_audio_direction_id" };
    lastRequestedAt.set(entry.id, Number(clock()));
    return { ok: true, id: entry.id };
  }

  function setMode(next) {
    if (!Object.values(AUDIO_MODES).includes(next)) return { ok: false, code: "unknown_audio_mode", mode };
    mode = next;
    return { ok: true, mode };
  }

  function setReducedAudio(value) {
    reducedAudio = Boolean(value);
    return { ok: true, reducedAudio };
  }

  function state() {
    return { mode, reducedAudio };
  }

  return { request, commit, setMode, setReducedAudio, state };
}

function linearGain(decibels) {
  return 10 ** (decibels / 20);
}

function scheduleEnvelope(gain, now, duration, attack, release, peak) {
  const attackAt = now + attack / 1000;
  const releaseAt = Math.max(attackAt, now + duration / 1000 - release / 1000);
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(Math.max(0.0001, peak), attackAt);
  gain.gain.exponentialRampToValueAtTime(0.0001, releaseAt + release / 1000);
}

function createLoopSamples(frameCount, sampleRate, toneHz, toneGain, crossfadeMs) {
  const samples = new Float32Array(frameCount);
  const durationSeconds = frameCount / sampleRate;
  const toneCycles = Math.max(1, Math.round(toneHz * durationSeconds));
  for (let index = 0; index < samples.length; index += 1) {
    const phase = (index / samples.length) * Math.PI * 2;
    const tone = Math.sin(phase * toneCycles) * toneGain;
    const texture = (Math.sin(phase * 17 + toneHz * 0.001) * 0.35)
      + (Math.sin(phase * 31) * 0.1);
    samples[index] = tone + texture;
  }
  const crossfadeFrames = Math.min(
    Math.max(1, Math.floor(sampleRate * crossfadeMs / 1000)),
    Math.floor(samples.length / 2),
  );
  const seam = (samples[0] + samples[samples.length - 1]) / 2;
  for (let index = 0; index < crossfadeFrames; index += 1) {
    const blend = index / Math.max(1, crossfadeFrames - 1);
    const head = samples[index];
    const tail = samples[samples.length - crossfadeFrames + index];
    samples[index] = seam * (1 - blend) + head * blend;
    samples[samples.length - crossfadeFrames + index] = tail * (1 - blend) + seam * blend;
  }
  return samples;
}

export function loopBoundaryDelta({ durationMs = 6000, sampleRate = AUDIO_STANDARDS.sample_rate_hz, toneHz = 110, toneGain = 0.1, crossfadeMs = AUDIO_STANDARDS.loop_crossfade_ms } = {}) {
  const frameCount = Math.max(1, Math.ceil(sampleRate * durationMs / 1000));
  const samples = createLoopSamples(frameCount, sampleRate, toneHz, toneGain, crossfadeMs);
  return Math.abs(samples[0] - samples[samples.length - 1]);
}

function createNoiseBuffer(context, entry) {
  const frameCount = Math.max(1, Math.ceil(context.sampleRate * entry.duration_ms / 1000));
  const buffer = context.createBuffer(1, frameCount, context.sampleRate);
  const channel = buffer.getChannelData(0);
  channel.set(createLoopSamples(
    frameCount,
    context.sampleRate,
    entry.recipe.tone_hz,
    entry.recipe.tone_gain,
    AUDIO_STANDARDS.loop_crossfade_ms,
  ));
  return buffer;
}

export function createAudioDirectionPlayer({ AudioContextCtor, sink = { record() {} }, policy = createAudioDirectionPolicy() } = {}) {
  const contextConstructor = AudioContextCtor ?? globalThis.AudioContext ?? globalThis.webkitAudioContext ?? null;
  let context = null;
  let activeNodes = [];

  function stop() {
    for (const node of activeNodes) {
      try {
        node.stop?.();
      } catch {
        // A preview may already have reached its scheduled stop time.
      }
    }
    activeNodes = [];
    return { ok: true };
  }

  async function play(id) {
    const entry = audioDirectionEntry(id);
    if (!entry) return { ok: false, code: "unknown_audio_direction_id" };
    const admission = policy.request(id, { commit: false });
    if (!admission.ok) return admission;
    if (!contextConstructor) return { ok: false, code: "audio_unsupported", entry };
    try {
      context ??= new contextConstructor();
      await context.resume?.();
    } catch {
      context = null;
      return { ok: false, code: "audio_unsupported", entry };
    }
    try {
      stop();
      const now = context.currentTime;
      const peak = linearGain(entry.peak_dbfs);
      if (entry.recipe.kind === "filtered-noise") {
        const source = context.createBufferSource();
        const filter = context.createBiquadFilter();
        const gain = context.createGain();
        source.buffer = createNoiseBuffer(context, entry);
        source.loop = entry.loopable;
        source.loopStart = 0;
        source.loopEnd = entry.duration_ms / 1000;
        filter.type = "lowpass";
        filter.frequency.value = entry.recipe.filter_hz;
        gain.gain.value = peak;
        source.connect(filter);
        filter.connect(gain);
        gain.connect(context.destination);
        source.start(now);
        source.stop(now + entry.duration_ms / 1000);
        activeNodes = [source];
      } else {
        activeNodes = entry.recipe.partials.map((partial) => {
          const oscillator = context.createOscillator();
          const gain = context.createGain();
          oscillator.type = partial.waveform;
          oscillator.frequency.value = partial.frequency_hz;
          oscillator.connect(gain);
          gain.connect(context.destination);
          scheduleEnvelope(
            gain,
            now,
            entry.duration_ms,
            entry.recipe.attack_ms,
            entry.recipe.release_ms,
            peak * partial.gain,
          );
          oscillator.start(now);
          oscillator.stop(now + entry.duration_ms / 1000);
          return oscillator;
        });
      }
      policy.commit(entry.id);
      sink.record?.({ type: "audio-direction-preview", id: entry.id, source: entry.visible_source, equivalent: entry.equivalent, priority: admission.priority, duck_music_db: admission.duck_music_db });
      return { ...admission, ok: true };
    } catch {
      stop();
      try {
        context?.close?.();
      } catch {
        // The context may already be closed after a device failure.
      }
      context = null;
      return { ...admission, ok: false, code: "audio_unsupported" };
    }
  }

  function destroy() {
    stop();
    context?.close?.();
    context = null;
  }

  return { play, stop, destroy, policy };
}
