import { AUDIO_CUE_POLICY, audioCueContractFor } from "./audio-cue-contract.mjs";
import { AUDIO_PRIORITY_POLICY, planAudioCueBatch, priorityValue } from "./audio-priority-contract.mjs";
import { AMBIENCE_CONTRACT } from "./ambience-contract.mjs";
import { MUSIC_STEM_CONTRACT, classifyVisibleMusicState } from "./music-stem-contract.mjs";

// AUDIO_PRIORITY_POLICY follows audio-priority-manager-v1; its pure batch plan
// keeps visible cue ordering separate from host transitions and written output.

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

function resolveAudioStorage(storage) {
  if (storage !== undefined) return storage;
  try {
    return globalThis.localStorage;
  } catch {
    return null;
  }
}

function readAudioPreferences(storage) {
  try {
    const parsed = JSON.parse(storage?.getItem?.(AUDIO_PRIORITY_POLICY.storage_key) ?? "{}");
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function persistedBoolean(value, fallback = false) {
  return typeof value === "boolean" ? value : fallback;
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
  storage,
} = {}) {
  const contextConstructor = audioConstructor(AudioContextCtor);
  const audioStorage = resolveAudioStorage(storage);
  const persisted = readAudioPreferences(audioStorage);
  const volumes = { master: 1, music: 0.55, interface: 0.7, event: 0.8, ambience: 0.25 };
  for (const channel of Object.keys(volumes)) {
    if (Number.isFinite(Number(persisted.volumes?.[channel]))) volumes[channel] = clamp(persisted.volumes[channel]);
  }
  const lastCueAt = new Map();
  const pendingCueRequests = [];
  const queuedCueRequests = [];
  let context = null;
  let enabled = false;
  let muted = persistedBoolean(persisted.muted);
  let musicMuted = persistedBoolean(persisted.musicMuted);
  let focused = true;
  let mode = ["full", "cues-only"].includes(persisted.mode) ? persisted.mode : "full";
  let reducedNotifications = persistedBoolean(persisted.reducedNotifications);
  let currentMusic = "menu";
  let currentAmbience = null;
  let musicTimer = null;
  const musicStemTimers = new Set();
  const activeMusicVoices = new Set();
  const activeAmbienceVoices = new Set();
  const activeCueVoices = new Set();
  let cueBatchTimer = null;
  let cueDrainTimer = null;
  let cueBusy = false;
  let duckTimer = null;
  let duckingPriority = null;
  let ambienceTimer = null;
  let visibilityHandler = null;

  function persistAudioPreferences() {
    try {
      audioStorage?.setItem?.(AUDIO_PRIORITY_POLICY.storage_key, JSON.stringify({
        muted,
        musicMuted,
        mode,
        reducedNotifications,
        volumes,
      }));
    } catch {
      // Preferences remain session-local when browser storage is unavailable.
    }
  }

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

  function linearGain(decibels) {
    return 10 ** (Number(decibels) / 20);
  }

  function duckFactor(channel) {
    if (channel === "music" && duckingPriority === "critical") return linearGain(AUDIO_PRIORITY_POLICY.ducking_db.critical);
    if (channel === "ambience" && duckingPriority) return linearGain(AUDIO_PRIORITY_POLICY.ducking_db[duckingPriority]);
    return 1;
  }

  function backgroundVoices() {
    return [...activeMusicVoices, ...activeAmbienceVoices];
  }

  function scheduleVoiceTarget(voice, factor) {
    if (!context || voice.released) return;
    const now = context.currentTime;
    const attack = Math.max(0.02, AUDIO_PRIORITY_POLICY.duck_attack_ms / 1000);
    const target = Math.max(0.0001, voice.base_gain * factor);
    const releaseAt = Math.max(now + attack, voice.end_time - voice.fade_seconds);
    try {
      const currentGain = Math.max(0.0001, Number(voice.gain.gain.value) || 0.0001);
      voice.gain.gain.cancelScheduledValues(now);
      voice.gain.gain.setValueAtTime(currentGain, now);
      voice.gain.gain.exponentialRampToValueAtTime(target, now + attack);
      voice.gain.gain.exponentialRampToValueAtTime(0.0001, releaseAt);
    } catch {
      // A closing or unsupported context keeps the visible fallback complete.
    }
  }

  function applyDucking() {
    for (const voice of backgroundVoices()) scheduleVoiceTarget(voice, duckFactor(voice.channel));
  }

  function beginDucking(priority, durationMs) {
    if (!(priority === "critical" || priority === "major")) return;
    if (!duckingPriority || priorityValue(priority) > priorityValue(duckingPriority)) duckingPriority = priority;
    applyDucking();
    if (duckTimer != null) globalThis.clearTimeout(duckTimer);
    duckTimer = globalThis.setTimeout(() => {
      duckTimer = null;
      duckingPriority = null;
      applyDucking();
    }, Math.max(0, Number(durationMs) || 0) + AUDIO_PRIORITY_POLICY.duck_release_ms);
  }

  function releaseVoice(voice, releaseMs = voice.crossfade_ms ?? 40) {
    if (!voice || voice.released) return;
    voice.released = true;
    const now = context?.currentTime ?? 0;
    const release = Math.max(0.02, Number(releaseMs) / 1000);
    try {
      const currentGain = Math.max(0.0001, Number(voice.gain.gain.value) || 0.0001);
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

  function stopVoiceSet(voices, releaseMs) {
    for (const voice of [...voices]) releaseVoice(voice, releaseMs);
  }

  function playTone(entry, channel) {
    if (!context || gainValue(channel) === 0) return false;
    const now = context.currentTime;
    const gain = context.createGain();
    const recipe = entry.recipe;
    const duration = recipe.duration_ms / 1000;
    const fade = Math.min(Math.max((recipe.crossfade_ms ?? 20) / 1000, 0.02), duration / 2);
    const baseGain = Math.max(0.0001, gainValue(channel) * (entry.normalization_gain ?? AUDIO_CUE_POLICY.normalization_gain));
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
    gain.gain.exponentialRampToValueAtTime(Math.max(0.0001, baseGain * duckFactor(channel)), now + fade);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + duration - fade);
    if (filter) {
      source.connect(filter);
      filter.connect(gain);
    } else {
      source.connect(gain);
    }
    gain.connect(context.destination);
    if (channel === "music" || channel === "ambience" || channel === "interface" || channel === "event") {
      const voiceSet = channel === "music" ? activeMusicVoices
        : channel === "ambience" ? activeAmbienceVoices : activeCueVoices;
      const voice = {
        source,
        gain,
        channel,
        base_gain: baseGain,
        end_time: now + duration,
        fade_seconds: fade,
        crossfade_ms: recipe.crossfade_ms ?? entry.crossfade_ms ?? 260,
      };
      const cleanup = () => voiceSet.delete(voice);
      voice.cleanup = cleanup;
      voiceSet.add(voice);
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
    stopVoiceSet(activeMusicVoices, 260);
  }

  function stopAmbience() {
    if (ambienceTimer != null) globalThis.clearTimeout(ambienceTimer);
    ambienceTimer = null;
    stopVoiceSet(activeAmbienceVoices, 260);
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

  function dispatchCue(request) {
    const played = playTone(request.entry, request.entry.channel);
    if (played) beginDucking(request.entry.priority_class, request.entry.duration_ms);
    return played;
  }

  function enqueuePendingCue(entry) {
    const request = { id: entry.id };
    const currentSize = pendingCueRequests.length + queuedCueRequests.length;
    if (currentSize < AUDIO_PRIORITY_POLICY.maximum_queued_cues) {
      pendingCueRequests.push(request);
      return true;
    }
    const replaceableIndex = pendingCueRequests.findIndex((pending) => {
      const pendingEntry = cueEntry(pending.id);
      return pendingEntry && priorityValue(entry.priority_class) > priorityValue(pendingEntry.priority_class);
    });
    if (replaceableIndex >= 0) {
      pendingCueRequests[replaceableIndex] = request;
      return true;
    }
    recorder?.record?.("audio_queue_bounded", {
      id: entry.id,
      priority: entry.priority_class,
      overflow_count: 1,
    });
    return false;
  }

  function finishCueVoices() {
    for (const voice of [...activeCueVoices]) voice.cleanup();
  }

  function drainCueQueue() {
    cueDrainTimer = null;
    if (cueBusy || muted || !enabled || !focused || !context || !queuedCueRequests.length) return;
    const request = queuedCueRequests.shift();
    cueBusy = true;
    try {
      if (!dispatchCue(request)) {
        cueBusy = false;
        drainCueQueue();
        return;
      }
    } catch {
      stopVoiceSet(activeCueVoices, 40);
      cueBusy = false;
      recorder?.record?.("audio_playback_failed", { id: request.id, message: "Optional audio cue playback failed." });
      drainCueQueue();
      return;
    }
    cueDrainTimer = globalThis.setTimeout(() => {
      finishCueVoices();
      cueBusy = false;
      drainCueQueue();
    }, request.entry.duration_ms);
  }

  function flushCueBatch() {
    cueBatchTimer = null;
    if (!pendingCueRequests.length) return;
    const requests = pendingCueRequests.splice(0, pendingCueRequests.length);
    const plan = planAudioCueBatch(requests, AUDIO_CATALOG.cues);
    for (const request of plan.selected) {
      if (queuedCueRequests.length >= AUDIO_PRIORITY_POLICY.maximum_queued_cues) {
        recorder?.record?.("audio_queue_bounded", {
          id: request.id,
          priority: request.priority,
          overflow_count: plan.overflow_count + 1,
        });
        continue;
      }
      queuedCueRequests.push(request);
    }
    if (plan.duplicate_ids.length || plan.routine_aggregated_count || plan.overflow_count) {
      recorder?.record?.("audio_batch_planned", {
        request_count: plan.request_count,
        duplicate_count: plan.duplicate_ids.length,
        routine_aggregated_count: plan.routine_aggregated_count,
        overflow_count: plan.overflow_count,
      });
    }
    drainCueQueue();
  }

  function scheduleCueBatchFlush() {
    if (cueBatchTimer != null) return;
    cueBatchTimer = true;
    if (globalThis.queueMicrotask) globalThis.queueMicrotask(flushCueBatch);
    else globalThis.setTimeout(flushCueBatch, 0);
  }

  function stopCueVoices() {
    if (cueDrainTimer != null) globalThis.clearTimeout(cueDrainTimer);
    cueDrainTimer = null;
    cueBusy = false;
    stopVoiceSet(activeCueVoices, 40);
  }

  function clearCueQueue() {
    pendingCueRequests.length = 0;
    queuedCueRequests.length = 0;
    stopCueVoices();
  }

  function clearDucking() {
    if (duckTimer != null) globalThis.clearTimeout(duckTimer);
    duckTimer = null;
    duckingPriority = null;
    applyDucking();
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
    const duplicatePending = pendingCueRequests.some((request) => request.id === entry.id)
      || queuedCueRequests.some((request) => request.id === entry.id);
    lastCueAt.set(cueId, now);
    const recorded = recordCue(sink, cueId);
    if (duplicatePending) return { ...recorded, code: "duplicate_suppressed", id: cueId };
    if (reducedNotifications && entry.channel !== "music") {
      return { ...recorded, code: "reduced_notifications" };
    }
    if (muted || !enabled || !focused || !context) {
      return { ...recorded, code: muted ? "muted" : "visual_only" };
    }
    const enqueued = enqueuePendingCue(entry);
    if (!enqueued) return { ...recorded, code: "queue_bounded", queue_size: pendingCueRequests.length + queuedCueRequests.length };
    scheduleCueBatchFlush();
    return { ...recorded, code: "queued", queue_size: pendingCueRequests.length + queuedCueRequests.length };
  }

  function setVolume(channel, value) {
    if (!(channel in volumes)) return { ok: false, code: "unknown_channel" };
    volumes[channel] = clamp(value);
    persistAudioPreferences();
    updateDom();
    return { ok: true, channel, value: volumes[channel] };
  }

  function setMuted(value) {
    muted = Boolean(value);
    if (muted) {
      clearCueQueue();
      stopMusic();
      stopAmbience();
      stopCueVoices();
      clearDucking();
    }
    else {
      scheduleMusic();
      scheduleAmbience();
    }
    persistAudioPreferences();
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
      clearCueQueue();
      stopMusic();
      stopAmbience();
      clearDucking();
    }
    statusText(focused ? "Audio focus restored." : "Audio paused while the page is unfocused.");
    return { ok: true, focused };
  }

  function setReducedNotifications(value) {
    reducedNotifications = Boolean(value);
    persistAudioPreferences();
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
      clearDucking();
    } else {
      scheduleMusic();
      scheduleAmbience();
    }
    persistAudioPreferences();
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
    persistAudioPreferences();
    statusText(musicMuted ? "Music muted; ambience, cues, and written equivalents remain available." : "Music unmuted.");
    updateDom();
    return { ok: true, musicMuted };
  }

  function state() {
    return {
      enabled,
      muted,
      musicMuted,
      focused,
      mode,
      reducedNotifications,
      music: currentMusic,
      ambience: currentAmbience,
      queued_cues: pendingCueRequests.length + queuedCueRequests.length,
      active_cue_voices: activeCueVoices.size,
      ducking: duckingPriority,
      volumes: { ...volumes },
    };
  }

  function destroy() {
    clearCueQueue();
    stopMusic();
    stopAmbience();
    clearDucking();
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
