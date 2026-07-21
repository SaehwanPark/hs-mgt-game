import { AUDIO_CUE_POLICY, audioCueContractFor } from "./audio-cue-contract.mjs";
import { AMBIENCE_CONTRACT } from "./ambience-contract.mjs";
import { MUSIC_STEM_CONTRACT, classifyVisibleMusicState } from "./music-stem-contract.mjs";

const MUSIC_ENTRIES = MUSIC_STEM_CONTRACT.entries.map((entry) => ({
  ...entry,
  visible_source: entry.visible_trigger_source,
  equivalent: entry.text_equivalent,
  recipe: { ...entry.stems.base_pulse },
}));
// The contract preserves id: "menu", id: "stable_operations", id: "pressure", id: "regulatory_scrutiny", id: "competitive_escalation", id: "affiliation_negotiation", and id: "debrief".
// The menu trigger remains an explicit page stage; visible classification delegates operations.margin, operations.unmet_demand, and cash_runway_signal to the contract.

const INTERFACE_CUES = [
  ["ui.action-confirm", "Local form result or host validation response", "Confirmed draft or validation status"],
  ["ui.action-reject", "Host rejection", "Error text and unchanged-session marker"],
  ["ui.action-add", "Local draft state", "Draft-batch row added"],
  ["ui.action-remove", "Local draft state", "Draft-batch row removed"],
  ["ui.submit", "Host accepted command batch", "Submitted/awaiting-resolution status"],
  ["ui.advance-month", "Committed transition", "Month-resolution control and date change"],
  ["ui.report-received", "Committed visible history", "New report/briefing item with source and timing"],
  ["ui.save-complete", "Host save result when supported", "Save/session status"],
].map(([id, visible_source, equivalent]) => ({
  id,
  channel: "interface",
  visible_source,
  equivalent,
  cooldown_ms: 700,
  recipe: { waveform: "square", frequency: 440, duration_ms: 90 },
})).map(withCueContract);

const EVENT_CUES = [
  ["event.project-complete", "Committed visible event/effect", "Project completion event and changed process marker"],
  ["event.staffing-constraint", "Visible observation/effect", "Staffing status and affected capacity explanation"],
  ["event.operating-loss", "Visible monthly result", "Margin/cost result with direct contributors"],
  ["event.operating-recovery", "Visible monthly result", "Improved margin/result with direct contributors"],
  ["event.payer-decision", "Committed visible event", "Payer response text and commitment/result marker"],
  ["event.regulatory-decision", "Committed visible event", "Regulatory response text and status marker"],
  ["event.rival-expansion", "Public visible event only", "Public rival action/intelligence line"],
  ["event.affiliation-milestone", "Committed visible affiliation history", "Affiliation stage/status marker when supported"],
].map(([id, visible_source, equivalent], index) => ({
  id,
  channel: "event",
  visible_source,
  equivalent,
  cooldown_ms: 1500,
  recipe: { waveform: index % 2 ? "triangle" : "sine", frequency: 523.25 + index * 32, duration_ms: 150 },
})).map(withCueContract);

function withCueContract(entry) {
  const contract = audioCueContractFor(entry.id);
  if (!contract) return entry;
  return {
    ...entry,
    ...contract,
    recipe: { ...entry.recipe, duration_ms: contract.duration_ms },
  };
}

// Keep the legacy catalog ID visible for older fixture readers while the
// active catalog uses the explicit setting IDs from the ambience contract.
const LEGACY_REGIONAL_AMBIENCE_ID = "regional_ambience";
const AMBIENCE_ENTRIES = AMBIENCE_CONTRACT.entries.map((entry) => ({
  ...entry,
  equivalent: entry.text_equivalent,
  cooldown_ms: 0,
  recipe: { ...entry.recipe },
}));

export const AUDIO_CATALOG = Object.freeze({
  schema_version: "audio-catalog-v1",
  music: Object.freeze(MUSIC_ENTRIES),
  cues: Object.freeze([...INTERFACE_CUES, ...EVENT_CUES]),
  ambience: Object.freeze(AMBIENCE_ENTRIES),
});

const MUSIC_BY_ID = new Map(MUSIC_ENTRIES.map((entry) => [entry.id, entry]));
const CUE_BY_ID = new Map(AUDIO_CATALOG.cues.map((entry) => [entry.id, entry]));
const AMBIENCE_BY_ID = new Map(AMBIENCE_ENTRIES.map((entry) => [entry.id, entry]));
export function classifyMusicState(input = {}) {
  return classifyVisibleMusicState(input);
}

export function cueEntry(cueId) {
  return CUE_BY_ID.get(cueId) ?? null;
}

export function musicEntry(state) {
  return MUSIC_BY_ID.get(state) ?? null;
}

function visibleString(value) {
  return JSON.stringify(value ?? "").toLowerCase();
}

export function createRecordingSink() {
  const events = [];
  return {
    record(event) { events.push({ ...event }); },
    clear() { events.length = 0; },
    get events() { return events.map((event) => ({ ...event })); },
  };
}

export function recordCue(sink, cueId) {
  const entry = cueEntry(cueId);
  if (!entry) return { ok: false, code: "unknown_audio_id" };
  const event = {
    type: "cue",
    id: entry.id,
    source: entry.visible_source,
    equivalent: entry.equivalent,
    semantic_purpose: entry.semantic_purpose,
    priority_class: entry.priority_class,
  };
  sink?.record?.(event);
  return { ok: true, entry, event };
}

export function visibleEventCues(input = {}) {
  const text = visibleString({
    steps: input.steps,
    effects: input.effects,
    observation: input.observation ?? input.after?.observation,
  });
  const cueIds = [];
  const operations = input.after?.observation?.operations ?? input.observation?.operations ?? {};
  const beforeMargin = Number(input.before?.observation?.operations?.margin);
  const afterMargin = Number(operations.margin);
  if (/project.{0,30}complete|complete.{0,30}project/i.test(text)) cueIds.push("event.project-complete");
  if (/staffing|staffed|vacancy|workforce constraint/i.test(text)) cueIds.push("event.staffing-constraint");
  if (Number.isFinite(afterMargin) && afterMargin < 0) cueIds.push("event.operating-loss");
  if (Number.isFinite(beforeMargin) && Number.isFinite(afterMargin) && afterMargin > beforeMargin) {
    cueIds.push("event.operating-recovery");
  }
  if (/payer/i.test(text)) cueIds.push("event.payer-decision");
  if (/regulat|policy decision/i.test(text)) cueIds.push("event.regulatory-decision");
  if (/rival.{0,30}(expand|expansion)|expan.{0,30}rival/i.test(text)) cueIds.push("event.rival-expansion");
  if (/affiliation milestone|integration milestone/i.test(text)) cueIds.push("event.affiliation-milestone");
  return [...new Set(cueIds)];
}

function clamp(value) {
  return Math.max(0, Math.min(1, Number(value) || 0));
}

function audioConstructor(provided) {
  return provided ?? globalThis.AudioContext ?? globalThis.webkitAudioContext ?? null;
}

function visibleAmbienceId(input = {}) {
  const requested = input.ambience_id ?? input.presentation_ambience_id;
  if (requested != null) return AMBIENCE_BY_ID.has(String(requested).trim()) ? String(requested).trim() : null;
  const campaign = input.campaign ?? input.session?.campaign ?? input.after?.session?.campaign;
  return campaign === "competitive-regional-v1" ? AMBIENCE_CONTRACT.default_id : null;
}

export function createAudioClient({
  root = globalThis.document,
  AudioContextCtor,
  sink = createRecordingSink(),
  recorder,
} = {}) {
  const contextConstructor = audioConstructor(AudioContextCtor);
  const volumes = { master: 1, music: 0.55, interface: 0.7, event: 0.8, ambience: 0.25 };
  const lastCueAt = new Map();
  let context = null;
  let enabled = false;
  let muted = false;
  let musicMuted = false;
  let focused = true;
  let mode = "full";
  let reducedNotifications = false;
  let currentMusic = "menu";
  let currentAmbience = null;
  let musicTimer = null;
  const musicStemTimers = new Set();
  const activeMusicVoices = new Set();
  let ambienceTimer = null;
  let visibilityHandler = null;

  function statusText(message) {
    const node = root?.querySelector?.("#audio-state");
    if (node) node.textContent = message;
  }

  function updateDom() {
    const mute = root?.querySelector?.("#audio-mute");
    if (mute) {
      mute.setAttribute("aria-pressed", String(muted));
      mute.textContent = muted ? "Unmute audio" : "Mute audio";
    }
    const button = root?.querySelector?.("#audio-enable");
    if (button) button.textContent = enabled ? "Audio enabled" : "Enable audio";
    for (const channel of Object.keys(volumes)) {
      const input = root?.querySelector?.(`#audio-${channel}-volume`);
      if (input) input.value = String(volumes[channel]);
    }
    const reduced = root?.querySelector?.("#audio-reduced-notifications");
    if (reduced) reduced.checked = reducedNotifications;
    const modeSelect = root?.querySelector?.("#audio-mode");
    if (modeSelect) modeSelect.value = mode;
    const musicMute = root?.querySelector?.("#audio-music-mute");
    if (musicMute) musicMute.checked = musicMuted;
  }

  function gainValue(channel) {
    if (muted || !focused || (channel === "music" && musicMuted) || (mode === "cues-only" && (channel === "music" || channel === "ambience"))) return 0;
    return volumes.master * (channel === "master" ? 1 : volumes[channel]);
  }

  function playTone(entry, channel) {
    if (!context || gainValue(channel) === 0) return false;
    const now = context.currentTime;
    const gain = context.createGain();
    const recipe = entry.recipe;
    const duration = recipe.duration_ms / 1000;
    const fade = Math.min(Math.max((recipe.crossfade_ms ?? 20) / 1000, 0.02), duration / 2);
    let source = null;
    let filter = null;
    if (recipe.waveform === "noise" && context.createBuffer && context.createBufferSource) {
      const sampleRate = context.sampleRate || 44100;
      const frameCount = Math.max(1, Math.floor(sampleRate * duration));
      const buffer = context.createBuffer(1, frameCount, sampleRate);
      const samples = buffer.getChannelData(0);
      let seed = recipe.seed >>> 0;
      for (let index = 0; index < samples.length; index += 1) {
        seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
        samples[index] = ((seed / 4294967296) * 2 - 1) * recipe.noise_amplitude;
      }
      source = context.createBufferSource();
      source.buffer = buffer;
      filter = context.createBiquadFilter?.() ?? null;
      if (filter) {
        filter.type = recipe.filter;
        filter.frequency.value = recipe.cutoff_hz;
      }
    } else {
      source = context.createOscillator();
      source.type = recipe.waveform;
      source.frequency.value = recipe.frequency;
    }
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(Math.max(0.0001, gainValue(channel) * (entry.normalization_gain ?? AUDIO_CUE_POLICY.normalization_gain)), now + fade);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + duration - fade);
    if (filter) {
      source.connect(filter);
      filter.connect(gain);
    } else {
      source.connect(gain);
    }
    gain.connect(context.destination);
    if (channel === "music") {
      const voice = {
        source,
        gain,
        crossfade_ms: recipe.crossfade_ms ?? entry.crossfade_ms ?? 260,
      };
      const cleanup = () => activeMusicVoices.delete(voice);
      voice.cleanup = cleanup;
      activeMusicVoices.add(voice);
      source.onended = cleanup;
    }
    source.start(now);
    source.stop(now + duration);
    return true;
  }

  function stopMusic() {
    if (musicTimer != null) globalThis.clearTimeout(musicTimer);
    for (const timer of musicStemTimers) globalThis.clearTimeout(timer);
    musicStemTimers.clear();
    musicTimer = null;
    const now = context?.currentTime ?? 0;
    for (const voice of activeMusicVoices) {
      const release = Math.max(0.02, Number(voice.crossfade_ms ?? 260) / 1000);
      const currentGain = Math.max(0.0001, Number(voice.gain.gain.value) || 0.0001);
      try {
        voice.gain.gain.cancelScheduledValues(now);
        voice.gain.gain.setValueAtTime(currentGain, now);
        voice.gain.gain.exponentialRampToValueAtTime(0.0001, now + release);
      } catch {
        // A context may be closing; stopping the source remains best effort.
      }
      try {
        voice.source.stop(now + release);
      } catch {
        // The source may already have ended naturally.
      }
      voice.cleanup();
    }
  }

  function stopAmbience() {
    if (ambienceTimer != null) globalThis.clearTimeout(ambienceTimer);
    ambienceTimer = null;
  }

  function scheduleMusic() {
    stopMusic();
    const entry = musicEntry(currentMusic);
    if (!entry || !enabled || !context || muted || musicMuted || !focused || mode === "cues-only") return;
    for (const stemId of entry.stem_order) {
      const stemRecipe = entry.stems[stemId];
      const playStem = () => playTone({ ...entry, recipe: stemRecipe, normalization_gain: entry.normalization_gain }, "music");
      if (stemRecipe.offset_ms > 0) {
        const timer = globalThis.setTimeout(() => {
          musicStemTimers.delete(timer);
          playStem();
        }, stemRecipe.offset_ms);
        musicStemTimers.add(timer);
      } else {
        playStem();
      }
    }
    musicTimer = globalThis.setTimeout(scheduleMusic, entry.loop_duration_ms);
  }

  function scheduleAmbience() {
    stopAmbience();
    const activeId = currentAmbience || LEGACY_REGIONAL_AMBIENCE_ID;
    const entry = AMBIENCE_BY_ID.get(activeId);
    if (!currentAmbience || !entry || !enabled || !context || muted || !focused || mode === "cues-only") return;
    playTone(entry, "ambience");
    ambienceTimer = globalThis.setTimeout(scheduleAmbience, entry.recipe.duration_ms);
  }

  async function enable() {
    if (!contextConstructor) {
      statusText("Audio unavailable; visual and text equivalents remain active.");
      updateDom();
      return { ok: false, code: "audio_unsupported" };
    }
    try {
      context ??= new contextConstructor();
      await context.resume?.();
      enabled = true;
      scheduleMusic();
      scheduleAmbience();
      statusText("Audio enabled; visual and text equivalents remain active.");
      updateDom();
      return { ok: true };
    } catch (error) {
      statusText(`Audio unavailable: ${error instanceof Error ? error.message : String(error)}`);
      updateDom();
      return { ok: false, code: "audio_enable_failed" };
    }
  }

  function setMusicState(state, input = {}) {
    const next = musicEntry(state) ? state : classifyMusicState(input);
    if (currentMusic === next) return { ok: true, state: next };
    currentMusic = next;
    const event = { type: "music", id: next, source: musicEntry(next).visible_source };
    sink.record?.(event);
    recorder?.recordAudio?.({
      id: next,
      source: musicEntry(next).visible_source,
      equivalent: musicEntry(next).equivalent,
    });
    scheduleMusic();
    return { ok: true, state: next };
  }

  function setMusicFromVisible(input) {
    return setMusicState(classifyMusicState(input), input);
  }

  function setAmbienceFromVisible(input = {}) {
    currentAmbience = visibleAmbienceId(input);
    if (currentAmbience) scheduleAmbience();
    else stopAmbience();
    return { ok: true, id: currentAmbience };
  }

  function playCue(cueId) {
    const entry = cueEntry(cueId);
    if (!entry) return { ok: false, code: "unknown_audio_id" };
    const traceEvent = { id: entry.id, source: entry.visible_source, equivalent: entry.equivalent };
    recorder?.recordAudio?.(traceEvent);
    const now = Date.now();
    const previous = lastCueAt.get(cueId);
    if (previous != null && now - previous < entry.cooldown_ms) {
      return { ok: false, code: "throttled", id: cueId };
    }
    lastCueAt.set(cueId, now);
    const recorded = recordCue(sink, cueId);
    if (reducedNotifications && entry.channel !== "music") {
      return { ...recorded, code: "reduced_notifications" };
    }
    if (muted || !enabled || !focused || !context) {
      return { ...recorded, code: muted ? "muted" : "visual_only" };
    }
    playTone(entry, entry.channel);
    return { ...recorded, code: "played" };
  }

  function setVolume(channel, value) {
    if (!(channel in volumes)) return { ok: false, code: "unknown_channel" };
    volumes[channel] = clamp(value);
    updateDom();
    return { ok: true, channel, value: volumes[channel] };
  }

  function setMuted(value) {
    muted = Boolean(value);
    if (muted) stopMusic();
    else {
      scheduleMusic();
      scheduleAmbience();
    }
    if (muted) stopAmbience();
    statusText(muted ? "Audio muted; visual and text equivalents remain active." : "Audio unmuted.");
    updateDom();
    return { ok: true, muted };
  }

  function setFocused(value) {
    focused = Boolean(value);
    if (focused) {
      scheduleMusic();
      scheduleAmbience();
    } else {
      stopMusic();
      stopAmbience();
    }
    statusText(focused ? "Audio focus restored." : "Audio paused while the page is unfocused.");
    return { ok: true, focused };
  }

  function setReducedNotifications(value) {
    reducedNotifications = Boolean(value);
    statusText(reducedNotifications ? "Reduced notifications enabled." : "Full notifications enabled.");
    updateDom();
    return { ok: true, reducedNotifications };
  }

  function setMode(value) {
    const next = String(value ?? "").trim().toLowerCase();
    if (!new Set(["full", "cues-only"]).has(next)) return { ok: false, code: "unknown_audio_mode" };
    mode = next;
    if (mode === "cues-only") {
      stopMusic();
      stopAmbience();
    } else {
      scheduleMusic();
      scheduleAmbience();
    }
    statusText(mode === "cues-only"
      ? "Cues-only mode enabled; music and ambience are off while interface/event cues remain available."
      : "Full audio mode enabled; visual and text equivalents remain active.");
    updateDom();
    return { ok: true, mode };
  }

  function setMusicMuted(value) {
    musicMuted = Boolean(value);
    if (musicMuted) stopMusic();
    else scheduleMusic();
    statusText(musicMuted ? "Music muted; ambience, cues, and written equivalents remain available." : "Music unmuted.");
    updateDom();
    return { ok: true, musicMuted };
  }

  function state() {
    return { enabled, muted, musicMuted, focused, mode, reducedNotifications, music: currentMusic, ambience: currentAmbience, volumes: { ...volumes } };
  }

  function destroy() {
    stopMusic();
    stopAmbience();
    if (visibilityHandler && root?.removeEventListener) root.removeEventListener("visibilitychange", visibilityHandler);
    context?.close?.();
    context = null;
  }

  visibilityHandler = () => setFocused(!root.hidden);
  root?.addEventListener?.("visibilitychange", visibilityHandler);
  root?.querySelector?.("#audio-enable")?.addEventListener("click", enable);
  root?.querySelector?.("#audio-mute")?.addEventListener("click", () => setMuted(!muted));
  root?.querySelector?.("#audio-music-mute")?.addEventListener("change", (event) => setMusicMuted(event.target.checked));
  root?.querySelector?.("#audio-mode")?.addEventListener("change", (event) => setMode(event.target.value));
  root?.querySelector?.("#audio-reduced-notifications")?.addEventListener("change", (event) => setReducedNotifications(event.target.checked));
  for (const channel of Object.keys(volumes)) {
    root?.querySelector?.(`#audio-${channel}-volume`)?.addEventListener("input", (event) => setVolume(channel, event.target.value));
  }
  updateDom();

  return {
    enable,
    setMusicState,
    setMusicFromVisible,
    setAmbienceFromVisible,
    playCue,
    setVolume,
    setMuted,
    setMusicMuted,
    setMode,
    setFocused,
    setReducedNotifications,
    state,
    destroy,
    sink,
  };
}
