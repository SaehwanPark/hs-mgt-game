const MUSIC_ENTRIES = [
  {
    id: "menu",
    channel: "music",
    visible_source: "explicit page stage",
    equivalent: "menu heading and start/load controls",
    recipe: { waveform: "sine", frequency: 196, duration_ms: 1800 },
  },
  {
    id: "stable_operations",
    channel: "music",
    visible_source: "PlayerObservation.operations and visible status",
    equivalent: "stable operating summary and status label",
    recipe: { waveform: "triangle", frequency: 261.63, duration_ms: 2200 },
  },
  {
    id: "pressure",
    channel: "music",
    visible_source: "visible margin, unmet demand, runway, or pressure label",
    equivalent: "source-linked pressure banner and affected metric",
    recipe: { waveform: "sawtooth", frequency: 146.83, duration_ms: 1400 },
  },
  {
    id: "debrief",
    channel: "music",
    visible_source: "explicit debrief page stage",
    equivalent: "debrief heading and retrospective timeline",
    recipe: { waveform: "sine", frequency: 329.63, duration_ms: 2600 },
  },
];

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
}));

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
}));

const AMBIENCE_ENTRIES = [{
  id: "regional_ambience",
  channel: "ambience",
  visible_source: "active competitive month",
  equivalent: "regional market panel and current date",
  cooldown_ms: 0,
  recipe: { waveform: "sine", frequency: 110, duration_ms: 4200 },
}];

export const AUDIO_CATALOG = Object.freeze({
  schema_version: "audio-catalog-v1",
  music: Object.freeze(MUSIC_ENTRIES),
  cues: Object.freeze([...INTERFACE_CUES, ...EVENT_CUES]),
  ambience: Object.freeze(AMBIENCE_ENTRIES),
});

const MUSIC_BY_ID = new Map(MUSIC_ENTRIES.map((entry) => [entry.id, entry]));
const CUE_BY_ID = new Map(AUDIO_CATALOG.cues.map((entry) => [entry.id, entry]));
const AMBIENCE_BY_ID = new Map(AMBIENCE_ENTRIES.map((entry) => [entry.id, entry]));
const PRESSURE_WORDS = /watch|strained|pressure|shortage|constraint|unmet|negative/i;

function visibleString(value) {
  return JSON.stringify(value ?? "").toLowerCase();
}

export function classifyMusicState(input = {}) {
  const stage = input.stage ?? input.page_stage ?? input.session?.stage;
  if (stage === "menu" || stage === "debrief") return stage;
  if (input.done === true || input.session?.done === true) return "debrief";
  const observation = input.observation ?? input.after?.observation ?? {};
  const operations = observation.operations ?? {};
  const visibleSummary = visibleString({
    cash_runway_signal: observation.cash_runway_signal,
    workforce_trust: observation.workforce_trust,
    in_flight_projects: observation.in_flight_projects,
    market_bullets: observation.market_bullets,
    policy_bullets: observation.policy_bullets,
  });
  if (
    Number(operations.margin) < 0
    || Number(operations.unmet_demand) > 0
    || PRESSURE_WORDS.test(visibleSummary)
  ) return "pressure";
  return "stable_operations";
}

export function cueEntry(cueId) {
  return CUE_BY_ID.get(cueId) ?? null;
}

export function musicEntry(state) {
  return MUSIC_BY_ID.get(state) ?? null;
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
  let focused = true;
  let reducedNotifications = false;
  let currentMusic = "menu";
  let musicTimer = null;
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
  }

  function gainValue(channel) {
    if (muted || !focused) return 0;
    return volumes.master * (channel === "master" ? 1 : volumes[channel]);
  }

  function playTone(entry, channel) {
    if (!context || gainValue(channel) === 0) return false;
    const now = context.currentTime;
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    const recipe = entry.recipe;
    oscillator.type = recipe.waveform;
    oscillator.frequency.value = recipe.frequency;
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(Math.max(0.0001, gainValue(channel) * 0.08), now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + recipe.duration_ms / 1000);
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start(now);
    oscillator.stop(now + recipe.duration_ms / 1000);
    return true;
  }

  function stopMusic() {
    if (musicTimer != null) globalThis.clearTimeout(musicTimer);
    musicTimer = null;
  }

  function stopAmbience() {
    if (ambienceTimer != null) globalThis.clearTimeout(ambienceTimer);
    ambienceTimer = null;
  }

  function scheduleMusic() {
    stopMusic();
    const entry = musicEntry(currentMusic);
    if (!entry || !enabled || !context || muted || !focused) return;
    playTone(entry, "music");
    musicTimer = globalThis.setTimeout(scheduleMusic, entry.recipe.duration_ms);
  }

  function scheduleAmbience() {
    stopAmbience();
    const entry = AMBIENCE_BY_ID.get("regional_ambience");
    if (!entry || !enabled || !context || muted || !focused) return;
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

  function state() {
    return { enabled, muted, focused, reducedNotifications, music: currentMusic, volumes: { ...volumes } };
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
  root?.querySelector?.("#audio-reduced-notifications")?.addEventListener("change", (event) => setReducedNotifications(event.target.checked));
  for (const channel of Object.keys(volumes)) {
    root?.querySelector?.(`#audio-${channel}-volume`)?.addEventListener("input", (event) => setVolume(channel, event.target.value));
  }
  updateDom();

  return {
    enable,
    setMusicState,
    setMusicFromVisible,
    playCue,
    setVolume,
    setMuted,
    setFocused,
    setReducedNotifications,
    state,
    destroy,
    sink,
  };
}
