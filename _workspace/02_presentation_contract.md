# Presentation Contract — Host autosave after committed GUI decisions v0.13.68

## Goal and authorization

Make the existing host checkpoint path automatic after an accepted GUI
decision while keeping the current browser presentation, save envelope, and
opaque-session boundary unchanged.

## Player questions and consequences

The player question is: “Will my accepted decision have a current host restart
point?” A successful autosave reports the committed count. A failed autosave
reports a written recovery message; the accepted host transition remains the
current session and can be retried with the manual Save host checkpoint
control.

## Actor-visible source ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Autosave trigger | Successful host `submitTurn` response | Only after the host accepts the decision | Do not submit, retry, or synthesize a transition in JavaScript |
| Autosave result | Existing `SaveEnvelope` metadata or host error | Written after each accepted decision when the adapter supports save | Do not expose the save artifact or true state |
| Recovery action | Existing manual Save/Restore controls and load path | Available after success, failure, refresh, or restart | Do not claim durable success when the host save failed |

## Visual, motion, and audio semantics

No new visual asset or motion behavior is introduced. Autosave success uses the
existing written session status and approved `ui.save-complete` cue when audio
is available. Audio-off, reduced-motion, and blocked-audio paths retain the
same written status. Autosave failure remains written and recoverable.

## Accessibility and fallbacks

The status is exposed through the existing live session-status region and is
not color-only. The current committed presentation remains available if
autosave fails. Missing save capability is a safe no-op for adapters that do
not support checkpoints; it does not block a host transition.

## Authority and persistence boundary

The host owns save serialization, verification, durable file replacement,
history, hashes, and continuation. The browser calls only the existing save
adapter and stores no serialized state. Autosave does not add a route, schema,
transition, or client authority.

## Asset provenance and release requirements

No asset, audio file, registry entry, provenance record, or release binary is
added. The existing approved save-complete cue is reused.

## Verification and evidence limits

Focused tests must prove autosave is exposed by the shared checkpoint client,
is invoked after accepted competitive and campaign decisions, reports failure
without rejecting the committed decision, and preserves the authority boundary.
The checks do not establish human accessibility, educational usefulness,
device/browser certification, provenance/legal approval, or public release.

## Non-goals and open questions

- No new route/schema, browser serialization, service worker, simulation rule,
  replay redesign, fresh AI search, screenshot, human review, or release claim.
- Open: full-campaign placement/screenshots, human evaluation, device/browser
  certification, provenance/legal review, and public-release approval.

# Presentation Contract — Host deterministic replay regeneration v0.13.67

## Goal and Authorization

Keep the existing `competitive-replay-v1` visible replay projection backed by a
host/core deterministic regeneration check over immutable recorded action
batches. This is a host integrity boundary, not a new browser presentation or
simulation surface.

## Player Questions and Consequences

The player question remains: “Can I trust that the committed replay rows and
hashes are internally reproducible?” A valid replay continues to show the same
local written playback rail. A failed verification produces a recoverable host
error rather than a partial or client-authored trace.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Regeneration inputs | Host-owned seed, genesis, and recorded `AggregatedMonthlyActions` in the immutable competitive history | Used only during host verification before a replay projection is returned | Do not expose resolved stochastic inputs or infer private actor rationale |
| Regenerated transition | Deterministic core month-start, transition, and institution phases | Compared to the recorded transition; mismatch fails closed | Do not return regenerated true state or let the browser calculate it |
| Visible replay rows | Existing `ReplayEnvelope` summary projection after successful verification | Same schema, fields, and missingness as the current replay read | Do not add a regenerated trace, hidden field, or new outcome |
| Failure status | Existing MCP/GUI host error boundary | Malformed or tampered history is rejected in written form | Do not silently fall back to unverified rows |

## Visual, Motion, and Audio Semantics

No new visual, motion, or audio signal is introduced. The existing local replay
cursor, written row detail, reduced-motion behavior, muted-audio behavior, and
empty/failure fallbacks remain unchanged. Verification status is represented by
the existing host read success/error boundary, not by a severity cue.

## Accessibility and Fallbacks

The existing native replay controls and written summaries remain the complete
understanding path. A failed host verification must be written and recoverable;
it must not leave a stale successful projection presented as current. Missing
or empty history retains the existing explicit empty state. No color, motion,
audio, asset, browser storage, or client computation is required.

## Authority, History, and Replay Boundaries

The host/core owns deterministic regeneration, immutable history, seeds, action
batches, state hashes, and rejection of tampered traces. The browser continues
to validate and locally play back only the visible `ReplayEnvelope`; it never
regenerates, serializes, mutates, submits, or accesses true state. Regeneration
uses recorded explicit action batches, not a fresh AI decision search.

## Asset Provenance and Release Requirements

No asset, audio file, registry entry, provenance record, or release binary is
added or modified by this slice.

## Verification and Evidence Limits

Focused Rust tests must prove exact regeneration of an untampered history and
fail-closed rejection of tampered action, event/effect, state, and hash data.
Session replay and durable-save tests must exercise the same verifier. Existing
browser/transport tests must show no route/schema or authority expansion. These
checks do not establish human accessibility, educational replay comprehension,
calibration, device/browser certification, provenance/legal approval, or public
release readiness.

## Non-Goals and Open Questions

- No new route/schema, browser simulation, client-side replay regeneration,
  true-state/resolved-input field, private rationale, fresh AI search, save
  format, autosave, asset/audio behavior, screenshot, or human review.
- Open: fresh policy/AI decision regeneration, full-campaign replay placement,
  screenshots, human evaluation, and public-release approval.

# Presentation Contract — Host-envelope replay playback rail v0.13.66

## Goal and Authorization

Let a player review committed replay rows through previous/next/play/pause
controls backed only by the existing host `ReplayEnvelope`.

## Player Questions and Consequences

The player question is: “What did I commit, what visible context accompanied it,
and what hash/effects were recorded?” Selecting a row changes only the local
review cursor. It never submits a command, changes host state, or fabricates a
missing result.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Replay rows | Existing host `ReplayEnvelope.transitions` | After a successful replay read; empty when no rows exist | Do not reconstruct true state or regenerate a trace |
| Selected row | Local cursor over validated visible summaries | Previous/next/play/pause only | Do not call a transition or imply an unrecorded outcome |
| Row detail | Existing command, optional observation, events, effects, and state hash | Written with the selected row; absent fields remain absent | Do not reveal resolved inputs or private actor rationale |
| Recovery status | Existing replay adapter response/failure | Failed reads preserve the last valid view | Do not replace a failed read with client-authored data |

## Visual, Motion, and Audio Semantics

Playback is a local written review state. Animation and audio are optional
presentation layers; reduced motion, muted audio, and no-audio environments keep
the same selected-row text and controls.

## Accessibility, Authority, and Evidence Limits

Controls are native buttons with written status and keyboard activation. The
browser validates and displays host-sourced summaries; it never serializes,
deserializes, mutates, or regenerates simulation state. Technical checks do not
establish human usability, accessibility, educational value, device
certification, legal/provenance approval, or public release.

## Non-Goals and Open Questions

- No replay regeneration, new route/schema, state transfer, simulation,
  persistence, autosave, asset/audio behavior, or screenshot is included.
- Open: deterministic regeneration, full-campaign placement/use and
  screenshots, and human review remain separate roadmap gates.

# Presentation Contract — Durable regional-affiliation host checkpoint v0.13.65

## Goal and Authorization

Let a player explicitly save a `regional-affiliation-v1` GUI checkpoint,
restart the loopback host, and recover the same host-owned session through the
opaque ID already held by browser storage.

## Player Questions and Consequences

The player question is: “Can I recover my explicitly saved affiliation session
after the local host restarts?” A matching durable checkpoint restores the
visible stage, history, hash, and continuation. Missing, malformed, or
colliding data produces written recovery guidance and never overwrites a live
session or invents an outcome.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Durable checkpoint identity | Host-only wrapper containing opaque `session_id` and existing `AffiliationReplayArtifact` text | Written only after explicit save; loaded only for matching ID | Do not display or expose serialized true state, resolved inputs, or private rationale |
| Recovery status | Existing host load response plus repeated actor-visible reads | Success, missing file, malformed file, collision, or adapter failure | Do not infer a replacement session, transition, or outcome |
| Restored visible surface | Existing campaign-coverage, history, replay, and session responses | After host hydration and ordinary reads | Do not reconstruct the projection in JavaScript |

## Visual, Motion, and Audio Semantics

No new semantic visual, motion, or audio signal is introduced. Existing
affiliation stage, written history, optional audio, audio-off, and reduced-motion
fallbacks remain the complete understanding path.

## Accessibility, Authority, and Evidence Limits

The browser stores only the opaque session ID. The host owns file I/O, replay
verification, hydration, and transitions; the browser never serializes,
deserializes, mutates, or regenerates affiliation state. Technical checks do
not establish human usability, accessibility, educational value, device
certification, legal/provenance approval, or public release.

## Non-Goals and Open Questions

- No autosave, browser serialization, replay playback/regeneration, new
  route/schema, asset, audio behavior, or screenshot is included.
- The configured path stores one latest explicit checkpoint; a later
  affiliation save replaces the prior file through the temporary-sibling host
  operation.
- Open: replay playback/regeneration, full-campaign placement/use and
  screenshots, and human review remain separate roadmap gates.

# Presentation Contract — Durable stabilization host checkpoint v0.13.64

## Goal and Authorization

Let a player explicitly save a `stabilization-v1` GUI checkpoint, stop/restart
the loopback host, and recover the same host-owned campaign session through the
opaque ID already held by browser storage.

## Player Questions and Consequences

The player question is: “Can I recover my explicitly saved stabilization
session after the local host restarts?” A matching durable checkpoint restores
the visible campaign stage, history, hash, and continuation. Missing, malformed,
or colliding data produces written recovery guidance and never overwrites a
live session or invents a replacement outcome.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Durable checkpoint identity | Host-only wrapper containing opaque `session_id` and the existing stabilization `SessionSave` fields | Written only after explicit save; loaded only for matching ID | Do not display or expose serialized true state, resolved inputs, or private rationale |
| Recovery status | Existing host load response plus repeated actor-visible reads | Success, missing file, malformed file, collision, or adapter failure | Do not infer a replacement session, transition, or outcome |
| Restored visible surface | Existing campaign-coverage, history, replay, and session responses | After host hydration and ordinary reads | Do not reconstruct the projection in JavaScript |

## Visual, Motion, and Audio Semantics

No new semantic visual, motion, or audio signal is introduced. Existing
campaign stage, written history, optional audio, audio-off, and reduced-motion
fallbacks remain the complete understanding path.

## Accessibility, Authority, and Evidence Limits

The browser continues to store only the opaque session ID. The host owns file
I/O, replay verification, hydration, and transitions; the browser never
serializes, deserializes, mutates, or regenerates stabilization state. Technical
checks do not establish human usability, accessibility, educational value,
device certification, legal/provenance approval, or public release.

## Non-Goals and Open Questions

- No durable regional-affiliation checkpoint, autosave, browser serialization,
  replay playback/regeneration, new route/schema, asset, audio behavior, or
  screenshot is included.
- The configured path stores one latest explicit checkpoint; a later
  stabilization save replaces the prior file through a temporary-sibling host
  operation.
- Open: regional-affiliation durability, full-campaign save/load/replay
  continuity, screenshots, and human review remain separate roadmap gates.

# Presentation Contract — Campaign decision-time observation recovery v0.13.61

## Goal and Authorization

Let a player revisit the visible observation that preceded each committed
stabilization or regional-affiliation decision. The host remains authoritative;
the browser renders optional written observation lines alongside immutable
turn/command/hash summaries.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Decision-time observation | Existing host `Transition.observation` / `AffiliationTransition.observation` formatted through visible session helpers | Optional on `TransitionSummary`; absent for older/competitive summaries | Do not expose resolved inputs, private rationale, true state, or future outcome |
| Turn and command | Existing immutable `TransitionSummary` | Paired with the committed entry | Do not allow local edits or inferred command results |
| State hash | Existing host transition summary | Existing hash remains host-owned | Do not recalculate or use it as causal proof |
| Written fallback | Existing history/command/effect/debrief text | Always available if disclosure is absent or audio is unavailable | Do not make decoration or audio required |

## Visual, Motion, and Audio Semantics

The browser uses native written `<details>`/`<summary>` disclosure semantics
for observation lines. No new image, animation, audio cue, or color-only state
is introduced. Reduced motion and audio-off behavior remain unchanged.

## Accessibility, Authority, and Evidence Limits

The disclosure is text-first and tied to a committed history item. Technical
keyboard/DOM/source checks do not establish human comprehension, accessibility,
educational usefulness, causal understanding, or visual quality.

## Non-Goals

- No route, schema version, simulation rule, persistence, replay regeneration,
  true-state view, resolved-input field, private rationale, or causal graph.
- No instructor-only or competitive-path redesign.

# Presentation Contract — Direct campaign audio projection v0.13.60

## Goal and Authorization

Expose optional host-selected campaign music/cue metadata through the existing
typed `campaign-coverage-v1` envelope and let the browser use it without
changing simulation authority. Existing written campaign content remains the
primary equivalent when audio is unavailable, muted, reduced, or omitted.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Campaign music state | Host `CampaignCoverageAudio.music_state_id` | Optional; browser falls back to visible text when omitted | Do not infer hidden severity, intent, agreement, or future outcome |
| Campaign event cues | Host `CampaignCoverageAudio.audio_cue_ids` and existing catalog | Optional; explicit empty means no campaign cue; omitted preserves legacy fallback | Do not invent cues or treat a cue as causal proof |
| Music/cue vocabulary | Existing `AUDIO_CATALOG` | IDs must already be catalog entries | Do not create or accept new runtime IDs |
| Written meaning | Existing campaign stage, briefing, actor, process, decision, history, and debrief fields | Always retained independent of audio | Do not make audio required for play |

## Visual, Motion, and Audio Semantics

Host metadata selects existing optional Web Audio recipes only. The browser
filters cue IDs, applies explicit music after a valid coverage refresh, and
plays campaign cues only after a successful canonical host submission and
refresh. Audio-off and reduced-notification settings continue to preserve the
same written stage and decision meaning.

## Accessibility, Authority, and Evidence Limits

The projection must not contain true state, resolved inputs, private rationale,
or local transition authority. Technical routing and allowlist tests do not
establish human listening quality, comprehension, accessibility, educational
value, fatigue, legal clearance, device certification, or public-release
readiness.

## Non-Goals

- No new audio asset, catalog ID, route, schema version, simulation rule,
  transition, persistence, or registry entry.
- No campaign-specific motif redesign or human listening approval.

# Presentation Contract — Phase 13.1 AI-generation metadata boundary v0.13.57

## Goal and Authorization

The authorized outcome is a technical provenance/readiness ledger for the
existing fictional portrait-preview candidates. It must make the release
boundary inspectable without treating missing model/seed data as known. This
is a governance and evidence surface, not a new player-facing portrait or
browser route.

## Player Questions and Consequences

There is no new player-facing semantic signal in this slice. The contributor
question is: “Can this candidate be regenerated or promoted with complete,
auditable provenance?” The safe consequence of an incomplete answer is the
existing generic actor marker and written role label; no preview may become a
runtime asset by implication.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Approved model identity/revision | `assets/generation/approved-models.json` | Current registry record; no record means unavailable | Do not infer the model used for an existing preview |
| Required metadata vocabulary | `assets/generation/generation-workflow.json` | Capture-time contract | Do not treat a field name as a captured value |
| Captured record validation | `scripts/capture_generation_metadata.py`, `scripts/validate_generation_metadata.py` | Pre-manifest/release check | Do not bypass the validator for a preview |
| Preview source/hash/role/equivalent | `assets/generation/portrait-previews.json` and preserved PNGs | Current preview inventory | Do not infer model, seed, quality, identity, or outcome meaning |
| Human review status | `assets/generation/portrait-review-queue.json` | Pending until a named human review occurs | Do not convert technical checks into human approval |
| Release/runtime eligibility | generation manifest and visual registry | Must remain empty/unregistered for current previews | Do not infer release eligibility from source hashes alone |

## Visual, Motion, and Audio Semantics

The ledger is text/JSON-only and has no visual, motion, or audio cue. The
meaningful states are written explicitly: `technical-ready`,
`missing-preview-provenance`, `pending-human-review`, and `release-blocked`.
The generic actor marker and written role label remain the complete fallback if
portraits are unavailable. No color, motion, sound, or image is required to
understand the boundary.

## Accessibility and Fallbacks

The evidence is machine-readable and text-first. Missing model, revision, seed,
sampler, or review data must remain visible as unavailable/pending rather than
being replaced with a guessed value. No audio or motion capability is used;
the existing generic fallback and written equivalent remain available at all
times.

## Authority, History, and Replay Boundaries

The ledger and validators operate outside the simulation and presentation
runtime. They must not read or write commands, transitions, stochastic inputs,
observations, state hashes, immutable history, replay artifacts, checkpoints,
or debrief facts. No browser state, asset status, or provenance field may
enter host authority.

## Asset Provenance and Release Requirements

Existing preview hashes may prove byte preservation only. A future promoted
portrait requires an approved model ID and immutable revision, license/card
metadata, actual seed and sampler/settings, preserved source output, release
derivative/hash, complete human-review gates, an asset registry entry, and
manifest/credits parity. Until then, preview status, approval, release path,
registry ID, and manifest entry remain blocked/null.

## Verification and Evidence Limits

The focused test will validate the ledger's source paths and statuses, run the
current generation validator, assert all seven previews have null model/seed
provenance and pending review, and mutate one preview into a promotion-shaped
state to prove validation fails closed. This cannot establish human
resemblance, artifact quality, lived accessibility, legal clearance,
training-data provenance, educational value, or public-release readiness.

## Non-Goals and Open Questions

- No portrait regeneration, model download, image editing, asset promotion,
  runtime integration, or screenshot is authorized.
- Open: an authorized contributor must regenerate or replace each candidate
  through the approved local workflow with real model/seed data.
- Open: a named human must complete identity, resemblance, marks, artifact,
  accessibility, small-size, grayscale, and release-derivative review.

--- Historical presentation contracts ---

# Presentation Contract — Durable host checkpoint recovery v0.13.63

## Goal and Authorization

Let a player explicitly save a competitive GUI checkpoint, stop/restart the
loopback host, and recover the same host-owned session through the opaque ID
already held by browser storage.

## Player Questions and Consequences

The player question is: “Can I recover my explicitly saved competitive session
after the local host restarts?” A matching durable checkpoint restores the same
visible board, action catalog, history, replay metadata, and regional-world
reads. Missing or invalid durable data produces written recovery guidance and
does not invent a new campaign or outcome.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Durable checkpoint identity | Host-only save wrapper containing the opaque `session_id` and existing `CompetitiveSessionSave` | Written only after explicit save; loaded only for a matching ID | Do not display or expose serialized true state, resolved inputs, or private rationale |
| Recovery status | Existing host load response plus repeated actor-visible reads | Success, missing file, malformed file, or adapter failure | Do not infer a replacement session, transition, or outcome |
| Restored visible surface | Existing presentation/action/history/replay/regional-world responses | After host hydration and ordinary read refresh | Do not reconstruct the projection in JavaScript |

## Visual, Motion, and Audio Semantics

No new semantic visual, motion, or audio signal is introduced. Existing
checkpoint status, written recovery, history, replay metadata, resolution,
regional-world, optional audio, and reduced-motion fallbacks remain the complete
understanding path.

## Accessibility and Fallbacks

The browser continues to store only the opaque session ID. A missing or
malformed host file leaves the current view recoverable, exposes written
status, and permits manual start/load. Persistence is not required for audio,
color, motion, or browser storage.

## Authority, History, and Replay Boundaries

Rust owns serialization, file I/O, session hydration, immutable history,
state hashes, stochastic inputs, transitions, and debrief facts. The browser
may request `loadSession` after an unknown live session and then re-read host
projections; it does not serialize, deserialize, mutate, regenerate, or play
back simulation state.

## Asset Provenance and Release Requirements

No asset, audio file, registry entry, or release path is added.

## Verification and Evidence Limits

Focused tests must cover explicit save, new-store load, matching identity,
hash/count alignment, deterministic continuation, missing/malformed files,
browser retry, and authority exclusions. These checks do not establish human
usability, device/browser certification, replay playback, educational value,
legal/provenance approval, or public-release readiness.

## Non-Goals and Open Questions

- No autosave, durable stabilization/affiliation checkpoint, browser
  serialization, service worker, replay playback/regeneration, or new visual/
  audio asset is included.
- The configured application path stores one latest explicit competitive
  checkpoint; a later save replaces that file, and concurrent-session archive
  management is out of scope.
- Open: full-campaign presentation placement, replay playback/regeneration,
  and human review remain separate roadmap gates.

# Presentation Contract — Phase 11.1 live history handoff v0.12.94

## Goal and Authorization

Define the bounded live history handoff needed for the Phase 11.1 history-view
item. The host may expose its existing immutable transition summaries through a
versioned non-mutating route; the browser may validate and render those
summaries through the existing history list. This slice does not authorize
replay regeneration, save/load, or full campaign continuity.

## Player Questions and Consequences

The history view should answer: “Which committed visible transitions occurred,
in what order, and what state hash identifies each summary?” It must not reveal
hidden rival actions, true state, future results, or client-reconstructed
causality.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| History list | Host `HistoryEnvelope.transitions` from `GameSessionStore::get_history` | Keep presentation-provided history; show explicit empty state | No local history synthesis |
| Transition count | Host `HistoryEnvelope.transition_count` equal to list length | Reject envelope and retain current view | No inferred missing turns |
| Turn/command/events/effects | Existing visible `TransitionSummary` fields | Render written fields or existing empty text | No hidden actor outcomes |
| State hash | Existing host `TransitionSummary.state_hash` | Render visible hash text; do not recalculate | No client hash authority |
| Unknown session | Existing structured host error/404 | Preserve current history and recovery status | No retry loop or local replacement |
| Missing adapter capability | Existing presentation history | Continue without dedicated refresh | No second data source or simulation |

## Visual, Motion, and Audio Semantics

The existing text-first `renderHistory` surface remains the meaning-bearing
presentation. History refresh adds no animation, audio, asset, or motion path;
existing optional audio and reduced-motion behavior remain unchanged.

## Accessibility and Fallbacks

Each committed summary remains written DOM content with turn, command, event,
effect, and state-hash text. Empty history and failed/missing history reads
retain explicit current-view/recovery behavior. Automated checks do not
establish human screen-reader, focus, contrast, device, or usability quality.

## Authority, History, and Replay Boundaries

The route calls only the existing non-mutating `GameSessionStore::get_history`.
The response does not enter commands, transitions, stochastic inputs, hashes,
replay verification, save files, or debrief facts. The browser does not mutate,
reconstruct, rehash, or regenerate the history.

## Asset Provenance and Release Requirements

No asset is added or promoted. Existing presentation/history text and current
credits, registry, release, metadata, and security checks remain the boundary.

## Verification and Evidence Limits

Rust/session/transport tests must cover schema, count/hash alignment, one live
turn, unknown-session errors, and non-mutation. Node/Python tests must cover
validation, text rendering, capability/failure fallback, syntax, and forbidden
authority/network markers. Full Rust, Python, asset, replay, documentation,
and release checks remain required.

## Non-Goals and Open Questions

- No replay playback/regeneration, save/load, terminal redesign, screenshot
  suite, performance benchmark, browser matrix, or new campaign path.
- Open: later full-campaign save/load/replay continuity needs a separate host
  contract and evidence campaign.
- Open: human history comprehension and educational usefulness remain external
  evaluation gates.

---

# Presentation Contract — Phase 11.1 live music-state projection v0.12.93

## Goal and Authorization

Define the live competitive resolution music-state projection needed for the
bounded Phase 11.1 music item. The host may add one existing catalog state from
committed actor-visible data; the browser may use it for optional music and
retain visible-only classification for older/malformed envelopes. This slice
does not authorize full campaign coverage or new assets.

## Player Questions and Consequences

Music may reinforce the visible context of a committed resolution: completed
session, regulatory scrutiny, affiliation/negotiation, competitive escalation,
operating pressure, or stable operations. Written resolution and source text
remain authoritative. Music must not reveal hidden severity, private intent,
probability, causality, or future outcome.

## Actor-Visible Source Ledger

| State | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| `debrief` | Explicit terminal transition boundary | Fall back to visible classifier | No victory/quality claim |
| `regulatory_scrutiny` | Visible committed text containing regulatory, oversight, mandate, or policy-review language | Fall back to next visible state | No predicted review result |
| `affiliation_negotiation` | Visible committed text containing affiliation, partner, coalition, negotiation, or commitment-review language | Fall back to next visible state | No agreement or partner intent |
| `competitive_escalation` | Visible committed text containing rival, competitive, competition, market escalation, or public expansion | Fall back to next visible state | No private rival action |
| `pressure` | After visible margin `< 0`, unmet demand `> 0`, or catalog pressure language | Fall back to stable operations | No hidden severity or solvency forecast |
| `stable_operations` | No stronger visible state marker | Always safe fallback | No claim of favorable outcome |
| Legacy/malformed envelope | Existing `classifyVisibleMusicState` over visible input | Use browser classifier | No hidden-field read or client transition |
| Unknown explicit state | Existing audio client validation/fallback | Keep written resolution and use visible fallback | No local reinterpretation as a new state |

## Visual, Motion, and Audio Semantics

`music_state_id` uses the existing `MUSIC_STEM_CONTRACT` IDs and their visible
source/equivalent text. Stem roles, crossfade, normalization, reduced-audio,
mute, unavailable-audio, and cues-only policies remain unchanged. No new music
asset or playback path is introduced.

## Accessibility and Fallbacks

Music remains optional atmospheric support. Resolution text, visible status,
source, and result remain complete when muted, unavailable, reduced, or
malformed. A non-array/non-string or unknown host value does not suppress the
existing visible classifier or written fallback. Automated checks do not
establish human accessibility or audio usefulness/fatigue.

## Authority, History, and Replay Boundaries

The field is additive presentation metadata generated after a committed
transition. It is derived from `TransitionSummary`, actor-visible after
observation, and the explicit terminal boundary; it does not enter commands,
transition evaluation, stochastic inputs, immutable history, state hashes,
replay verification, or debrief facts. The browser does not fetch, simulate,
or reconstruct the transition.

## Asset Provenance and Release Requirements

No asset is added or promoted. Existing music-stem catalog, audio credits,
registry, release, metadata, and security checks remain the provenance boundary.

## Verification and Evidence Limits

Rust tests must cover each live-selectable state, deterministic priority, and
stable fallback. Node/Python tests must cover catalog parity, explicit valid,
malformed, unknown, and legacy behavior, syntax, and no-authority markers.
Existing full Rust, Python, asset, replay, documentation, and release checks
remain required.

## Non-Goals and Open Questions

- No new audio asset, event taxonomy, history/debrief redesign, save/load/
  replay continuity, screenshot suite, performance benchmark, or browser
  matrix in this slice.
- Open: which later host-committed event/history fields can support additional
  music states without duplicating transition logic?
- Open: full-campaign visual/audio continuity and human evaluation remain
  separate gates.

---

# Presentation Contract — Phase 11.1 live event-cue projection v0.12.92

## Goal and Authorization

Define the live competitive resolution event-cue projection needed for the
bounded Phase 11.1 event-cue slice. The host may add explicit cue IDs derived
from committed actor-visible transition data; the browser may play catalog
cues and retain the existing visible-only fallback for legacy envelopes. This
slice does not authorize full campaign coverage or new assets.

## Player Questions and Consequences

The resolution view may reinforce: “Which visible event or operating change
was just committed, and what written explanation remains available?” A cue
must not reveal hidden severity, actor intent, private rival action, causality
not present in the envelope, probability, or future outcome.

## Actor-Visible Source Ledger

| Cue | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| `event.project-complete` | Visible committed event/effect or in-flight project text containing project + complete | Omit cue | No inferred completion from a project name alone |
| `event.staffing-constraint` | Visible event/effect, workforce text, or staffing metric label containing a supported staffing term | Omit cue | No hidden vacancy severity or labor intent |
| `event.operating-loss` | After actor-visible operations margin `< 0` | Omit cue when absent/nonnegative | No forecast or solvency claim |
| `event.operating-recovery` | After visible margin is greater than before visible margin | Omit cue when unchanged/worse | No causal attribution beyond visible results |
| `event.payer-decision` | Visible committed event/effect text containing payer | Omit cue | No private payer intent |
| `event.regulatory-decision` | Visible committed event/effect text containing regulatory/policy decision | Omit cue | No hidden regulatory posture |
| `event.rival-expansion` | Visible text containing rival and expand/expansion | Omit cue | No private rival action or intent |
| `event.affiliation-milestone` | Visible text containing affiliation/integration milestone | Omit cue | No unobserved partner stage |
| Legacy envelope without `audio_cue_ids` | Existing `visibleEventCues` classifier over visible envelope data | Use legacy classifier | No client transition or hidden-state read |
| Explicit empty `audio_cue_ids` | Host-provided empty list | Play no event cue | Do not locally reinterpret absence as a trigger |

## Visual, Motion, and Audio Semantics

`audio_cue_ids` uses the existing `AUDIO_CUE_CONTRACT` IDs and their written
equivalents. Cue priority, duration, cooldown, reduced-audio behavior, and
unavailable-audio fallback remain catalog/client presentation policy. No new
audio or motion is introduced, and text-first resolution remains complete when
audio is muted or unavailable.

## Accessibility and Fallbacks

Each supported cue retains a visible source and text equivalent in the catalog.
An omitted field is a backward-compatible legacy envelope; a present empty
list is authoritative for that response. Unknown playback remains governed by
the existing unavailable-audio fallback. Automated checks do not establish
human accessibility or audio usefulness/fatigue.

## Authority, History, and Replay Boundaries

The host-shaped list is additive presentation metadata. It is derived from
`TransitionSummary`, before/after `ReadOnlyObservation` data, and no hidden
world state; it does not enter simulation transitions, commands, stochastic
inputs, immutable history, state hashes, replay verification, or debrief
facts. The browser does not fetch, simulate, or reconstruct the transition.

## Asset Provenance and Release Requirements

No asset is added or promoted. Existing audio catalog IDs, credits, registry,
release, metadata, and security checks remain the provenance boundary.

## Verification and Evidence Limits

Rust tests must cover every supported event cue plus recovery and empty cases.
Node/Python tests must cover catalog parity, explicit-list preference,
legacy fallback, syntax, and the no-authority boundary. Existing full Rust,
Python, asset, replay, documentation, and release checks remain required.

## Non-Goals and Open Questions

- No full campaign event taxonomy, music-state binding, history/debrief
  redesign, save/load/replay continuity, screenshot suite, performance
  benchmark, or browser matrix in this slice.
- Open: which later host-committed event/history fields can safely support
  additional cues without duplicating transition logic?
- Open: full-campaign visual/audio continuity and human evaluation remain
  separate gates.

---

# Presentation Contract — Phase 11.1 live operational overlays v0.12.90

## Goal and Authorization

Define the live regional-world overlay binding needed to advance the Phase 11.1
overlay-coverage slice. The host may add an optional catalog ID derived from a
directly actor-visible condition; the browser may render that ID and its
registered semantics. This slice does not authorize full campaign coverage or
new assets.

## Player Questions and Consequences

The board should answer: “Which visible operational condition is currently
reported, what source supports it, and what information remains unavailable?”
The overlay must not answer hidden severity, actor intent, causal attribution,
probability, or future outcome.

## Actor-Visible Source Ledger

| Binding | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| `operational-demand-pressure` | `PlayerObservation.monthly_unmet_demand > 0` | No binding when the reported value is zero; raw metric remains visible | No severity beyond the reported nonzero condition |
| `operational-active-capital-project` | Non-empty `PlayerObservation.in_flight_projects` | No binding for `none`/empty | No completion, delay cause, or future result |
| `operational-financial-distress` | `CashRunwaySignal::Strained` or reported margin `< 0` | No binding when neither condition is reported | No solvency or forecast claim |
| `operational-community-trust-concern` | `PlayerObservation.community_trust_summary == "watch"` | No binding for stable/unknown | No latent sentiment or causal claim |
| `operational-uncertain-stale-intelligence` | Non-empty `intel_gaps` or `prior_access_revision` | No binding when neither is present | No probability, truth, or hidden risk estimate |
| Unknown explicit catalog ID | Host-shaped optional field | Browser uses `operational-overlay-generic` | No local reinterpretation |
| Raw metric overlay | Existing actor-visible metric value | Keep existing label/value/source/equivalent | Do not relabel as an operational category |

## Visual, Motion, and Audio Semantics

The catalog supplies stable label, glyph, non-color pattern, text equivalent,
source, and static reduced-motion semantics. The live board renders the
explicit catalog ID alongside the raw value. Catalog priority remains display
ordering only and never encodes severity. No new audio or motion is introduced.

## Accessibility and Fallbacks

Every bound overlay retains text, source, and equivalent content. Unknown IDs
resolve to the registered generic overlay with an explicit unavailable label.
Absent conditions are omitted as categories but retain raw metric/report text.
Mute, reduced-motion, missing-asset, text-scaling, and unsupported-browser
behavior remain unchanged because the slice adds no playback or asset load.

## Authority, History, and Replay Boundaries

The optional catalog ID is a host-shaped projection of `PlayerObservation`; it
does not enter commands, transition evaluation, stochastic inputs, state hashes,
immutable history, replay artifacts, or debrief facts. Browser normalization,
selection, and DOM attributes remain reversible presentation state.

## Asset Provenance and Release Requirements

No asset is added or promoted. The existing operational-overlay module remains
the registry source and the changed regional-board adapter must keep its
repository-authored hash current. Generic fallback remains registry-backed and
release-free.

## Verification and Evidence Limits

Focused Rust tests must prove supported condition projection and unchanged
observation reads. Node/Python tests must prove catalog resolution, fallback,
DOM/source/equivalent exposure, and JavaScript syntax. Existing asset, replay,
documentation, and full Rust/Python checks remain required. These checks do not
establish human accessibility, audio usefulness, asset quality, legal clearance,
educational benefit, or full campaign coverage.

## Non-Goals and Open Questions

- No event-cue/music mapping, history/debrief redesign, save/load/replay
  screenshot suite, performance benchmark, or browser matrix in this slice.
- Open: which later host-committed event/history fields can safely support the
  remaining operational categories without duplicating transition logic?
- Open: full-campaign visual continuity and human evaluation remain separate
  gates.

---

# Historical Presentation Contract — Phase 11.1 live facility binding v0.12.89

## Goal and Authorization

Bind the current actor-visible player facility groups to stable registered
visual-component IDs across the regional board and selected-detail view. This
is a bounded presentation binding; it does not establish full campaign asset
coverage or change simulation authority.

## Player Questions and Consequences

The player may identify the current facility group, its registered visual
component equivalent, and the visible source of that presentation. A missing
or unknown component remains a generic facility. The component label must not
imply hidden capacity, geography, severity, intent, causality, or future
outcome; the combined emergency/ICU group is explicitly only an
`emergency-department` presentation equivalent.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Player facilities | `PlayerObservation` capacity groups projected by `RegionalWorldFacility.component_id` | Existing `generic-facility` catalog descriptor | No hidden facility topology or private state |
| Component metadata | `FACILITY_COMPONENTS` via pure board/scene adapters | Generic label, source, and written equivalent | No claim that a catalog equivalent is an exact asset match |
| Rival facilities | No facility DTO emitted for public rivals | Private detail remains unavailable | No rival capacity, projects, or facility inference |
| Board accessibility | `data-component-id`, component-aware label/title, written detail | Generic component metadata remains readable | No color, motion, or audio-only meaning |
| Selected detail | `component_label`, `component_source`, `component_equivalent` | Generic detail text | No client transition or simulation authority |

## Visual, Motion, and Audio Semantics

The board remains a schematic SVG. Component IDs and catalog equivalents add
semantic identity and source text; they do not load a new asset or create a
second rendering path. Existing reduced-motion, written, and optional-audio
behavior remains authoritative for presentation.

## Accessibility and Fallbacks

Facility anchors expose the component ID and component-aware accessible label;
the SVG title carries source/equivalent semantics, and selected detail repeats
them as text. Missing or unknown IDs resolve to the registered generic
descriptor. This is automated contract evidence, not human accessibility or
browser-compatibility approval.

## Authority, History, and Replay Boundaries

The component ID is host-shaped presentation vocabulary derived from the
actor-visible `PlayerObservation` projection. It is not true simulation state,
does not expose rival facilities, and cannot submit commands, advance a
session, mutate history, alter replay hashes, or authorize transitions.

## Provenance/Release

No new asset bytes or registry entries are added. Existing registry hashes are
refreshed for the changed hand-authored adapter/renderer sources; known IDs
reuse existing catalog source/release metadata, and generic fallback has no
release path. Existing asset validators, credits, hashes, provenance, and
human-review gates remain authoritative.

## Verification/Evidence Limits

`tests/test_phase11_live_facility_binding.py` and the Rust projection assertion
prove exact current IDs, catalog fallback, visible source/equivalent semantics,
and forbidden authority/network markers. They do not prove full campaign
facility coverage, registry completeness, screenshots, performance,
compatibility, accessibility quality, audio usefulness, legal clearance,
educational benefit, or human review.

## Non-goals

- No new assets, runtime network path, simulation, stochastic, history, replay,
  debrief, rival-private, or client-authority change.
- No closure of the full Phase 11.1 facility checklist.

---

# Historical Presentation Contract — Phase 11.1 campaign-coverage evidence v0.12.88

## Goal and Authorization

Bind the current competitive presentation catalog to exact, inspectable
coverage evidence without presenting a bounded catalog ledger as full-campaign
completion. This slice records pure module exports and fallback semantics; it
does not add a runtime path or approve quality.

## Player Questions and Consequences

The ledger supports visible identity, facility, overlay, event, cue, and music
labels with written equivalents. It must not imply severity, intent, causality,
probability, future outcome, or hidden rival information from a catalog entry or
fallback.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Facilities | `FACILITY_COMPONENTS` and visible facility context | Generic facility label/marker | No hidden facility state or true geography |
| Operational overlays | `OPERATIONAL_OVERLAY_SET` and explicit visible fields | Generic overlay with text and no severity encoding | No inferred severity, intent, or causality |
| Actor families | `ACTOR_FAMILIES` and visible family ID | Generic actor marker, frame, and written notification | No private actor identity or intent |
| Event markers | `EVENT_MARKER_SET` and visible category | Generic unknown-category marker | No urgency or resolution meaning |
| Event cues/music | Audio cue/music contracts and visible trigger source | Unknown cue/music is absent; written UI/result remains authoritative | No audio-only outcome channel |
| Continuity | Existing first-month/history/debrief/replay presentation references | Host/core retains history and hash authority | No ledger-derived state transition |

## Visual, Motion, and Audio Semantics

The ledger covers existing static catalog semantics and optional audio states.
It does not add a facility, overlay, event, cue, music stem, screenshot, or
animation. Existing written equivalents, reduced-audio behavior, and generic
fallbacks remain required.

## Accessibility and Fallbacks

The regression test requires visible source/equivalent fields and exercises
unknown facility, actor, overlay, event-marker, and asset paths. It does not
establish human accessibility quality or browser compatibility.

## Authority, History, and Replay Boundaries

The test imports pure browser modules only. It cannot submit commands, advance a
session, read true state, mutate history, alter replay hashes, or authorize a
client transition. First-month/history/debrief/replay references remain
presentation-only evidence of existing host/core-owned surfaces.

## Provenance/Release

No asset or registry entry changes. Existing asset validators, release hashes,
credits, provenance, and human-review gates remain authoritative.

## Verification/Evidence Limits

`tests/test_phase11_campaign_coverage.py` compares the JSON ledger with live
module exports and checks fallback/equivalent semantics. It does not prove full
campaign coverage, screenshot completion, performance, compatibility, asset
quality, audio usefulness, accessibility quality, legal clearance, or
educational benefit.

## Non-goals

- No runtime, host, simulation, stochastic, history, replay, debrief, or asset
  change.
- No full-campaign screenshot suite, device benchmark, browser matrix, or human
  quality finding.

---

# Historical Presentation Contract — Phase 10.2 evaluation preparation v0.12.87

## Goal and Authorization

Define a reproducible, privacy-bounded human-evaluation preparation slice for
the existing Phase 10.1 first-month visual/audio presentation. The repository
may define tasks, instruments, evidence categories, and decision boundaries;
it may not invent participant evidence or authorize release.

## Player Questions and Consequences

The protocol asks whether participants can identify institutions, facilities,
visible pressures, source/status labels, and committed consequence chains; use
keyboard, text-scale, reduced-motion, skip/review, mute, cues-only, and written
equivalents; and distinguish public, uncertain, missing, and committed
information. It does not teach an intended answer or expose hidden state.

## Actor-Visible Source Ledger

| Evaluation surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| First-month tasks | Existing seeded host-connected presentation | Record not-observed when a task is skipped or uninterpretable | No private rival action or hidden outcome |
| Recognition tasks | Visible labels, tokens, facilities, pressures, and source/status text | Preserve missingness and generic fallback text | No inference from color alone or from true state |
| Consequence tasks | Host-committed resolution, history, replay, and written equivalents | Keep uncertain, stale, missing, and committed states distinct | No predicted or recomputed consequence |
| Accessibility/audio tasks | Existing local controls and equivalent written content | Audio is optional; unavailable playback remains reviewable in text | No audio-only meaning or severity channel |
| Findings/decision | Anonymized bounded feedback and authorized review | Empty/pending until human evidence exists | No automated go/no-go or legal approval |

## Visual, Motion, and Audio Semantics

The protocol evaluates existing visuals, motion, music/cues, fallback status,
and written equivalents. It adds no asset, playback path, animation, or
runtime behavior. Ratings describe participant experience and are not policy
outcomes or simulation validation.

## Accessibility and Fallbacks

Tasks explicitly cover keyboard navigation, larger text, reduced motion,
skip/review, mute, cues-only mode, reduced notifications, unavailable audio,
and equivalent written content. The protocol records no conclusion about
universal accessibility; it only defines what an authorized evaluator may
observe.

## Authority, History, and Replay Boundaries

Participants interact with the existing host-authoritative path. The protocol
must not add commands, transition logic, stochastic inputs, hidden-state
projections, history mutations, replay mutations, or client authority.

## Provenance/Release

No asset or registry entry is added or promoted. Existing provenance, credits,
security, release, and human-review gates remain authoritative. Evaluation
artifacts are repository documentation and bounded JSON, not release approval.

## Verification/Evidence Limits

`tests/test_phase10_evaluation_prep.py` binds the JSON protocol, guide,
revision-log blank state, privacy restrictions, and exact Phase 10.2
preparation checklist. No participant results, legal conclusion, accessibility
claim, educational claim, or go/no-go decision may be inferred from the test.

## Non-goals

- No sessions, participant recruitment, interviews, recordings, personal data,
  private game state, or fabricated findings.
- No runtime, asset, host, simulation, history, replay, or debrief change.
- No automatic release, legal, accessibility, or educational approval.

---

# Historical Presentation Contract — Phase 10.1 first-month slice v0.12.86

## Goal and Authorization

Bind the existing first-month `competitive-regional-v1` path to a deterministic
technical acceptance contract across the regional board, executive desktop,
host resolution, optional audio, replay, accessibility, fallback, and
provenance surfaces. This slice adds evidence, not a second runtime path.

## Player Questions and Consequences

The technical path must make these visible without inventing hidden state:

- Which three systems, facilities, projects, pressures, and rival observations
  are visible at the current point in the first month?
- What was drafted, validated, submitted, committed, and refreshed by the host?
- Which resolution stages, written consequences, audio equivalents, replay
  hashes, and uncertain/missing values remain reviewable?

First-time-user comprehension, game feel, audio usefulness/fatigue, and
educational usability are not inferred from these contracts.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Regional board | Actor-visible regional-world DTO and observed public signals | Preserve source, lag, missingness, and generic identity/facility fallback | No true geography or private rival detail |
| Executive desktop | Presentation DTO, action catalog, and local selection state | Keep text/source/status labels visible | No simulation transition or client command authority |
| Resolution | Host-committed resolution envelope, history, and replay metadata | Preserve written stages, skip/review, and stable hashes | No predicted effects or recomputed outcomes |
| Audio | Existing visible classifier, catalog, priority, and fallback contracts | Keep mute/cues-only/text equivalents available | No hidden intent, severity, or outcome channel |
| Provenance | Existing registries, manifest, credits, and generation gates | Fail closed when records are incomplete | No automatic legal or human approval |

## Visual, Motion, and Audio Semantics

The integrated first-month path uses the existing schematic regional board,
institution/facility tokens, semantic containers, eight-stage resolution
sequence, optional ambience/cues/adaptive music, and written equivalents.
Skip/reduced-motion/review modes preserve committed text and replay order.

## Accessibility and Fallbacks

Keyboard landmarks, non-color status language, text scale, reduced motion,
mute/cues-only modes, written audio equivalents, missingness labels, and
generic unknown content fallbacks remain required. Technical presence does not
establish human accessibility quality.

## Authority, History, and Replay Boundaries

The browser consumes actor-visible host DTOs and local presentation state only.
Commands, transitions, stochastic inputs, true state, immutable history, state
hashes, replay artifacts, and debrief facts remain host/core-owned. Selection,
animation, audio, skip, and first-month stage state cannot advance the session.

## Asset Provenance and Release Requirements

The slice uses existing registered assets/catalog projections and does not add
or promote an asset. Existing hash, license, provenance, fallback, and human
review gates remain authoritative for release changes.

## Verification and Evidence Limits

`tests/test_phase10_first_month.py` must assert every Phase 10.1 technical label,
live mount/source marker, no-authority boundary, deterministic first-month
stage path, visible music sequence, skip behavior, and JavaScript syntax.
Existing GUI, host, replay, audio, accessibility, asset, and Rust checks remain
required. No check establishes first-time-user comprehension, audio quality or
fatigue, educational usability, legal clearance, ownership, or human review.

## Non-Goals and Open Questions

- No new asset, dependency, host field, simulation rule, hidden-state projection,
  or duplicate proof runtime.
- No Phase 10.2 participant protocol, human evaluation, or go/no-go decision.
- How the first-month slice performs with new players remains an open gate.

---

# Presentation Contract — Phase 9 technical closure v0.12.85

## Goal and Authorization

Record the completed automated Phase 9.1/9.2 release gates in the roadmap and
protect their evidence limits. This slice is a contributor/release audit of
existing validators, generated projections, manifests, fallbacks, and the SVG
derivative check. It does not approve assets or add a player-facing signal.

## Player Questions and Consequences

There is no new player-facing behavior. Contributor-facing questions are:

- Are the automated license, provenance, security, hash, reproducibility,
  metadata, fallback, and credits gates present and passing?
- Does the roadmap distinguish technical evidence from human legal, portrait,
  accessibility, quality, decoder, and ownership review?

No policy outcome, actor identity, severity, intent, or simulation state is
derived from a checklist or validator result.

## Actor-Visible Source Ledger

| Artifact | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| License/provenance record | Canonical visual/audio registries | Validator fails on missing, invalid, or incompatible fields | No inference of legal clearance or ownership |
| Release integrity | Security scanner, sanitizer, registry hashes, and manifest | Fail closed on unsafe content, metadata, missing files, or changed bytes | No automatic approval or promotion |
| Presentation fallback | Existing local availability/playback contracts | Preserve written equivalents and generic fallbacks | No hidden-state or host inference |
| Roadmap evidence | Passing tests and committed documentation | Keep unresolved human gates explicit | A checked technical item is not human review |

## Visual, Motion, and Audio Semantics

No runtime visual, motion, or audio behavior changes. Existing identity,
facility, resolution, audio, fallback, and credits surfaces remain authoritative
only for their existing actor-visible or local presentation contracts.

## Accessibility and Fallbacks

The audit requires existing written equivalents, mute/reduced-audio behavior,
generic missing-asset fallback, and explicit missingness language to remain
documented. It does not claim human accessibility quality.

## Authority, History, and Replay Boundaries

The audit reads repository files and test evidence only. It never changes host
DTOs, commands, transitions, stochastic inputs, observations, history, hashes,
replay artifacts, debrief facts, or runtime state.

## Asset Provenance and Release Requirements

Technical completion does not approve a current or future asset. Registry,
source/release hash, license, provenance, accessibility, and human approval
gates remain required for any release change.

## Verification and Evidence Limits

The roadmap closure test, asset validators, release manifest/credits checks,
SVG release check, full Python/Rust/JavaScript checks, formatting, Clippy, and
documentation checks are required. They establish automated technical evidence
only, not legal clearance, decoder safety, quality, accessibility, ownership,
or human review.

## Non-Goals and Open Questions

- No asset, dependency, registry, manifest, runtime, host, or simulation change.
- No portrait approval, legal audit, browser/decoder study, or user evaluation.
- Future human and product gates remain open until separately authorized.

---

# Presentation Contract — Phase 9.2 SVG metadata sanitizer v0.12.84

## Goal and Authorization

Provide a deterministic, dependency-free transformation for an explicit SVG
derivative that removes `<metadata>` elements while preserving accessible
`<title>` and `<desc>` content. The release check must confirm current
registry-controlled SVGs are already sanitized without rewriting them. This is
asset-governance work, not runtime presentation or simulation work.

## Player Questions and Consequences

There is no new player-facing signal. The contributor/release questions are:

- Can metadata be removed from a proposed SVG derivative deterministically?
- Are title/description accessibility elements and visible geometry preserved?
- Does the check fail closed without changing approved bytes or hashes?

No player outcome, institution identity, severity, intent, or policy meaning is
derived from metadata presence or removal.

## Actor-Visible Source Ledger

| Artifact | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| SVG bytes | Explicit contributor-provided local input | Malformed XML or unbalanced metadata fails without output | No reconstruction from screenshots or runtime state |
| Metadata element | `<metadata>` element in the supplied SVG | Remove only the metadata element and its contents | Do not remove `<title>`/`<desc>` or infer whether metadata is legally safe |
| Release check | Approved registry release paths under `assets/release/` | Any removable metadata or unsafe path is a deterministic check failure | No auto-promotion, hash update, or approval inference |

## Visual, Motion, and Audio Semantics

The transform has no visual/audio runtime semantics. It preserves all non-
metadata SVG markup byte-for-byte where possible and leaves the existing asset
security, accessibility, and release-manifest contracts authoritative.

## Accessibility and Fallbacks

- `<title>` and `<desc>` remain present and unchanged in sanitized output.
- Malformed XML, missing input, unbalanced metadata, output collisions, and
  paths outside the explicit derivative boundary fail closed.
- Runtime fallback behavior remains the existing generic/text contract; the
  sanitizer does not remove an asset from the GUI or change its label.

## Authority, History, and Replay Boundaries

The sanitizer reads local files and optionally writes only a caller-selected
derivative path. It never reads host/session payloads, commands, observations,
simulation state, stochastic inputs, history, hashes, replay artifacts, or
debrief facts. The `--check-release` path is read-only.

## Asset Provenance and Release Requirements

Sanitized output is not approved automatically. If a contributor uses the
output as a future release derivative, the existing registry source/release
hash, provenance, license, accessibility, and human approval gates still apply.
No current registry entry or release hash is changed by this slice.

## Verification and Evidence Limits

Focused tests must cover removal, title/description preservation, malformed and
unbalanced input, safe output paths, and current release-root parity. Existing
security, manifest, registry, credits, release, Python, Rust, formatting,
Clippy, JavaScript, and documentation checks remain required. These checks do
not establish decoder safety, legal clearance, ownership, accessibility,
quality, or human review.

## Non-Goals and Open Questions

- No raster, audio, EXIF, ID3, or other non-SVG metadata transformation.
- No canonical asset rewrite, registry mutation, release promotion, or new
  dependency.
- Whether a sanitized derivative should replace any future source/release file
  remains a separately approved asset-review decision.

---

# Presentation Contract — Phase 9.2 audio playback fallback v0.12.83

## Goal and Authorization

When optional Web Audio setup or generated cue playback is unavailable, the
client must expose a deterministic local fallback descriptor and preserve the
cue's visible source and written equivalent. This is the bounded v0.12.83
Phase 9.2 runtime slice; it does not add recorded audio or change host
authority.

## Player Questions and Consequences

- Is audio available, muted, unsupported, or failed?
- What visible event or interface meaning remains available when sound cannot
  play?
- Does a playback exception stop only optional audio while the current visual,
  text, and session presentation remains usable?

The player consequence is presentation-only: unavailable sound never hides or
changes the host-reported event, action, observation, or outcome.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Cue/music/ambience identity | Existing local audio catalog entry | Preserve `visible_source` and `equivalent`; use generic audio fallback when the ID is unknown | No inference of severity, intent, or outcome from a sound failure |
| Playback availability | Local Web Audio setup/playback result | Normalize unsupported, missing, failed, malformed, contradictory, and unknown results as unavailable | No host/session or decoder state is synthesized |
| Failure status | Local presentation state and `#audio-state` text | Announce that visual and written equivalents remain active | No command, transition, history, hash, or debrief mutation |

## Visual, Motion, and Audio Semantics

Successful generated tones retain the existing catalog identity and priority
rules. Unsupported setup or thrown playback switches to a visible text status
and an explicit fallback descriptor; no meaning depends on hearing the sound.
Mute, cues-only, reduced-notification, unfocused-page, and missing-audio states
retain the existing visible controls and text equivalents.

## Accessibility and Fallbacks

- Unsupported context creation returns an unavailable fallback without
  throwing through the client.
- Cue playback exceptions clear optional audio work and report the cue's written
  equivalent through the existing status region.
- Unknown or malformed catalog IDs use a generic “Audio unavailable” marker and
  never expose a release path.
- Color, motion, and sound are never the only channel for event meaning.

## Authority, History, and Replay Boundaries

Audio context, timers, playback failures, fallback descriptors, and status text
remain local browser presentation state. They never enter commands, host DTOs,
simulation transitions, stochastic inputs, observations, immutable history,
state hashes, replay artifacts, or debrief facts. A playback failure cannot
replace or retry a host transition.

## Asset Provenance and Release Requirements

No new asset or registry entry is authorized. Existing generated recipes and
written equivalents remain the sole local catalog inputs; pending portraits and
all external/license questions remain unchanged.

## Verification and Evidence Limits

Focused tests must cover unsupported setup, thrown cue playback, successful
recording, fallback descriptor fields, visible status text, and no-authority
markers. Existing audio, asset, release, documentation, Python, Rust,
formatting, Clippy, JavaScript, and diff checks remain required. Automated
checks do not establish measured loudness, browser compatibility, human
accessibility, fatigue, audio quality, learning, or policy validity.

## Non-Goals and Open Questions

- No recorded audio, file decoder, network fetch, audio download, or new audio
  asset is in scope.
- No catalog taxonomy, priority policy, music-state classifier, or host API is
  redesigned.
- Human listening and classroom/accessibility review remain open evidence gates.

---

# Presentation Contract — Phase 8.2 review-ready fictional actor portrait approval worksheet

## Goal and Authorization

Fictional actor portraits must be traceable from an approved local model and
prompt request through preserved source output, post-processing, human review,
and release-asset registry entry. This slice prepares a review-ready worksheet
for all seven preserved previews; it does not perform human review or promote
unverified outputs into the runtime or release manifest.

## Player Questions and Consequences

Portraits add only a bounded identity aid. Contributor-facing questions are:

- Can a contributor reproduce how an asset was created?
- Can a reviewer identify the model/license, prompt, seed, settings, source
  output, post-processing, and release derivative?
- Can the project reject resemblance, protected marks, clinical implausibility,
  missing alt text, incomplete provenance, or unreviewed release state?
- Can each portrait be disabled without losing written actor identity or role?
- Does a future asset fail closed when source/release hashes or registry links
  are missing?

## Actor-Visible Source Ledger

| Workflow element | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Model and license | Approved local model registry and primary model card | Capture is rejected if model is not listed or license is not allowlisted | No assumption that model-card license clears training data or every output |
| Prompt/settings | Contributor request file and captured command metadata | Required prompt, negative prompt, seed, sampler, dimensions, and settings must be explicit | No reconstruction from an image or filename |
| Source output | Preserved local source file and hash | No release record without an existing hashed source output | No claim that a release derivative is the original |
| Human review | Checklist fields for resemblance, marks, plausibility, accessibility, and release | Approval remains pending until every required review field is true | No automated proxy for human approval |
| Registry bridge | Existing visual/audio asset registry ID | Approved output must point to a matching registry entry | No asset becomes release-safe merely by being generated |
| Review queue | Per-role worksheet bound to preview ID/path/hash | Reviewer identity, date, decision, and every required gate must be explicit | A checked schema is not human approval |
| Portrait meaning | Explicit actor family/role and written label | Use generic actor marker and role text when the image is absent | No inference of score, severity, intent, outcome, or private action |

## Visual, Motion, and Audio Semantics

The portrait is an optional decorative identity aid, not a new authority or
information channel. The shared set uses non-photorealistic editorial,
chest-up, consistent-crop, neutral-institutional-background output with no
public-figure resemblance, protected marks, readable text, or clinical claim.
Generated assets must retain written labels, alt text, generic fallback,
disabled-asset behavior, small-size behavior, and grayscale behavior. They must
not encode hidden simulation state, future outcomes, clinical severity,
real-person identity, protected logos, or exact simulation parameters.

## Accessibility and Fallbacks

- Every portrait record requires an accessible equivalent/alt-text field and a
  generic actor-marker fallback plan.
- Every portrait must be checked at small size and grayscale before approval.
- Every future audio record requires a written equivalent, mute/unavailable
  fallback, and safe reduced-audio behavior.
- Missing source output, metadata, review, or release derivative blocks release;
  the application uses the existing generic/project-authored fallback.
- Prompt and post-processing records remain readable without an image viewer.

## Authority, History, and Replay Boundaries

Generation requests, seeds, outputs, hashes, approvals, and local model files
are contributor/release artifacts. They never enter simulation transitions,
actor observations, commands, history, state hashes, replay artifacts, or
debrief facts. A future asset may decorate a host-authoritative presentation
only after its asset-registry entry is approved.

## Asset Provenance and Release Requirements

The workflow records model name/version or immutable revision, model license and
source URL, generation application/version, prompt, negative prompt, seed,
sampler/settings, dimensions, date, contributor, post-processing, source image
references, source hash, optional release path/hash, human-review checklist,
approval status, and target visual/audio registry ID. The approved-model file
records the model-card review date, immutable repository revision, and scope
limitations. No model weights or hosted inference outputs are committed by
this bounded preview slice.

## Verification and Evidence Limits

Focused tests must cover the role/style contract, prompt constraints, fallback
fields, review-queue bindings, and pending-review release gate. A fixture proof
must show all seven roles, per-role review gates, accessible equivalents,
small/grayscale checks, and the fail-closed release rule. Existing
generation, asset, credits, release, docs, Python, Rust, formatting, and
Clippy checks remain required. These checks do not establish legal clearance,
training-data provenance, output ownership, human resemblance, clinical
plausibility, accessibility, learning, or policy validity.

## Non-Goals and Open Questions

- No runtime portrait set or approved output asset is in scope until each
  per-portrait generation and human-review gate passes.
- `FLUX.1-schnell` is listed only as a local prototype candidate under its
  model-card license statement and access conditions; legal review remains
  required before release use.
- Future audio generation needs the same metadata schema but may require extra
  model/license fields and an acoustic human-review track.
# Presentation Contract — Phase 11.1 live debrief handoff v0.12.91

## Goal and Authorization

Define the terminal live-session presentation needed to expose the host's
final debrief while preserving immutable history and replay metadata. The
browser may render host-provided final text and hashes; it may not generate
debrief facts or continue a terminated session.

## Player Questions and Consequences

The terminal view should answer: “What was committed, what history/hash can I
review, and what host-authored lessons are available?” It must not answer
unreported causality, hidden rival state, probability, or outcome quality by
itself.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Final history | `EndSessionEnvelope.history` / `TransitionSummary` | Empty-history text remains visible | No local reconstruction of transitions |
| Replay continuity | `EndSessionEnvelope.replay` | Unavailable hash/count text | No hash generation or replay validation in browser |
| Debrief | `EndSessionEnvelope.debrief` | Explicit unavailable debrief text | No JavaScript debrief synthesis or scoring |
| Terminal status | `EndSessionEnvelope.done`, turn, and max turns | Host-response error preserves current view | No local session completion |

## Visual, Motion, and Audio Semantics

The final screen is text-first: committed history, state hash, transition
count, and debrief lines remain in the DOM. The optional audio client may select
the existing `debrief` music state after a successful host terminal response;
audio adds atmosphere only and never carries a terminal fact alone. No new
asset or motion behavior is introduced.

## Accessibility and Fallbacks

The terminal control has a descriptive label and is disabled after successful
termination. Empty history, missing replay values, and empty debrief arrays
use explicit written messages. Existing reduced-motion, text scaling, mute,
and focus behavior remain the source of truth; automated checks do not claim
human screen-reader, contrast, or device approval.

## Authority, History, and Replay Boundaries

`end_session` remains the only terminal mutation and host debrief authority.
The server removes the session after creating the final envelope. The browser
does not call a transition function, infer from hashes, mutate history, or
retry a successful terminal call. A failed request leaves the active view and
session ID unchanged.

## Asset Provenance and Release Requirements

No asset is added or promoted. Changed JavaScript source hashes must be
synchronized in the visual registry; generated credits and release checks must
remain green.

## Verification and Evidence Limits

Rust and transport tests must prove terminal history/replay/debrief alignment,
session removal, and structured unknown-session errors. Node/Python tests must
prove schema validation, text rendering, disabled controls, failure
preservation, syntax, and forbidden hidden-state/network markers. These checks
do not establish full campaign continuity, persistence, screenshots,
performance, compatibility, audio usefulness, human accessibility, legal
clearance, or educational benefit.

## Non-goals and Open Questions

- No save/load format, replay regeneration, screenshot suite, new audio, or
  additional campaign surface is included.
- Open: full campaign save/load and replay continuity still requires a later
  host contract and evidence campaign.

---
# Presentation Contract — Phase 11.1 live replay continuity v0.12.95

## Goal and Authorization

Define the bounded live replay handoff needed for the Phase 11.1 replay-view
item. The host may expose immutable actor-visible transition summaries with
replay metadata; the browser may validate and render them through the existing
history surface. This slice does not authorize replay regeneration, playback
simulation, save/load, or full campaign continuity.

## Player Questions and Consequences

The replay view should answer: “Which committed visible transitions can I
review, and what final hash identifies this retained sequence?” It must not
recompute outcomes, reveal hidden rival actions, or imply unobserved causality.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Replay list | Host `ReplayEnvelope.transitions` from existing history | Keep current history; show explicit empty state | No local replay synthesis |
| Replay metadata | Host schema, seed, count, latest visible hash | Reject envelope and preserve current view | No browser-authored replay identity |
| Transition turn/command/events/effects | Existing visible `TransitionSummary` fields | Render written fields or existing empty text | No hidden actor outcomes |
| State hash | Existing host `TransitionSummary.state_hash` | Reject missing/blank values | No client hash calculation |
| Unknown session | Existing structured host error/404 | Preserve current view and recovery state | No retry loop or replacement simulation |

## Visual, Motion, and Audio Semantics

The existing text-first committed-history list remains the meaning-bearing
replay surface. This handoff adds no animation, audio, asset, or local playback
state; historical resolution review remains the existing host read.

## Accessibility and Fallbacks

Each retained summary remains written DOM content with turn, command, and state
hash text. Empty history and failed/missing replay reads preserve explicit
current-view/recovery behavior. Automated checks do not establish human
screen-reader, focus, contrast, device, or comprehension quality.

## Authority, History, and Replay Boundaries

The route calls only `GameSessionStore::get_history` through a typed replay
projection. The response does not enter commands, transitions, stochastic
inputs, hashes, save files, or debrief facts. The browser does not mutate,
recalculate, rehash, regenerate, or simulate the replay.

## Asset Provenance and Release Requirements

No asset is added or promoted. Existing text, current credits, registry,
release, metadata, and security checks remain the provenance boundary.

## Verification and Evidence Limits

Rust/session/MCP/transport tests must cover empty and committed replay reads,
latest-hash/count alignment, unknown sessions, and non-mutation. Node/Python
tests must cover validation, text rendering, capability/failure fallback,
syntax, and forbidden authority/network markers. Full Rust, Python, asset,
replay, documentation, and release checks remain required.

## Non-Goals and Open Questions

- No replay playback/regeneration, save/load, terminal redesign, screenshot
  suite, performance benchmark, browser matrix, or new campaign path.
- Open: persistence-backed save/load and full replay continuity need separate
  host contracts and evidence campaigns.
- Open: human replay comprehension and educational usefulness remain external
  evaluation gates.

---
# Presentation Contract — Phase 11.1 live checkpoint continuity v0.12.96

## Goal and Authorization

Define the bounded live checkpoint save/restore handoff for the Phase 11.1
save/load item. The host may clone and restore the current in-memory session;
the browser may request the operation and reload typed host reads. This slice
does not authorize durable persistence, browser serialization, or full campaign
continuity.

## Player Questions and Consequences

The controls should answer: “Was the host checkpoint saved or restored, and
what visible transition count/hash now identifies the current session?” They
must not suggest that browser state or hidden outcomes were independently
saved.

## Actor-Visible Source Ledger

| Surface | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Save status | Host `SaveEnvelope` operation and visible count/hash | Show recoverable error; keep current view | No local save confirmation |
| Restore status | Host `SaveEnvelope` plus refreshed host reads | Preserve current session/view on failure | No browser snapshot restore |
| History/replay after restore | `get_presentation`, `get_history`, `get_replay` | Keep last valid view if a refresh fails | No local history/replay synthesis |
| Action catalog after restore | Host `get_action_catalog` | Keep current catalog/session if unavailable | No browser legality reconstruction |
| Checkpoint identity | Host session ID/campaign/seed | Reject malformed envelope | No inferred durability or cross-process identity |

## Visual, Motion, and Audio Semantics

Save and restore add status text and existing recovery messaging only. A
successful restore reuses the existing text-first presentation, history,
replay, action, and regional-world renderers; no new animation/audio/asset
path is needed.

## Accessibility and Fallbacks

Controls have explicit labels, disabled/busy states, and live status text.
Failed, unsupported, missing-checkpoint, and unknown-session operations preserve
the current rendered session and offer the existing recoverable read path.
Automated checks do not establish human screen-reader, focus, contrast, device,
or comprehension quality.

## Authority, History, and Replay Boundaries

Only the host clones/restores `GameSession` values. The browser sends a named
operation and then requests host reads; it does not serialize state, mutate
history, calculate hashes, resolve transitions, or restore hidden fields.
Checkpoint metadata does not enter simulation state or transition hashes.

## Asset Provenance and Release Requirements

No asset is added or promoted. Existing text, current credits, registry,
release, metadata, and security checks remain the provenance boundary.

## Verification and Evidence Limits

Rust/session/MCP/transport tests must cover save/restore clone behavior,
count/hash continuity, missing checkpoints, and unknown sessions. Node/Python
tests must cover envelope validation, controls, refresh/failure preservation,
syntax, and forbidden authority/network markers. Full Rust, Python, asset,
replay, documentation, and release checks remain required.

## Non-Goals and Open Questions

- No durable save file, browser refresh persistence, cross-process recovery,
  replay playback/regeneration, screenshot suite, performance benchmark,
  browser matrix, or new campaign path.
- Open: the existing CLI durable save artifact and future GUI persistence need
  a separate storage/locking contract.
- Open: human save/restore comprehension and educational usefulness remain
  external evaluation gates.

---
# Presentation Contract — Phase 11.2 asset-size budget v0.12.97

## Goal and authorization

Define the first Phase 11.2 packaging-hardening contract: explicit byte and
file-count limits for tracked release assets, with a deterministic report that
can be checked in a normal checkout. This is an engineering budget, not a
runtime benchmark or a visual-quality approval.

## Budget classes

| Class | Scope | Per-file limit | Total limit | File-count limit |
| --- | --- | ---: | ---: | ---: |
| `release-visual-svg` | `assets/release/visual/svg/*.svg` | 4 KiB | 32 KiB | 32 |
| `release-package` | all tracked files under `assets/release` except README | 8 KiB | 64 KiB | 64 |

The checker reports observed file count, total bytes, and largest file for
each class. Limits are intentionally explicit and conservative for the
current small release package; later asset additions must update the budget in
the same reviewed change.

## Source and authority ledger

| Field | Authorized source | Missing/invalid behavior | Prohibited inference |
| --- | --- | --- | --- |
| Budget class | `assets/asset-budget.json` | Checker fails closed | No implicit glob or limit |
| Files | Resolved in-repository paths under declared root | Checker fails on escaped/missing root | No network or generated download |
| Bytes | Filesystem byte length at check time | Checker reports limit failure | No compressed-size estimate |
| Report | Deterministic checker output | Nonzero exit on failure | No performance conclusion |

## Accessibility and presentation boundary

The budget is documentation/tooling evidence and adds no player-facing visual,
audio, motion, or interaction path. Existing text equivalents, fallback rules,
and provenance checks remain unchanged.

## Explicit non-goals and evidence limits

- No asset optimization, raster derivative generation, audio compression,
  lazy-loading, preload policy, browser cache measurement, SVG render timing,
  audio decode timing, memory measurement, offline verification, low-power test,
  browser matrix, screenshot suite, or human evaluation.
- A passing report proves only that the named tracked files are within the
  declared byte/file-count limits at check time.

## Verification

Tests must cover schema/report shape, current counts and bytes, escaped paths,
empty classes, exceeded limits, and deterministic CLI output. Full project
quality/release gates remain required.

---
# Presentation Contract — Phase 11.2 SVG optimization v0.12.98

## Goal and authorization

Define the SVG optimization boundary for tracked release derivatives. The
optimizer may remove formatting whitespace between XML tags and outer document
whitespace only. The resulting release bytes must remain registry/manifest
hash-aligned and idempotent under the same pass.

## Source and transformation ledger

| Surface | Authorized source | Allowed transformation | Prohibited change |
| --- | --- | --- | --- |
| Release SVG bytes | `assets/release/visual/svg/*.svg` | Outer/inter-tag whitespace normalization | Geometry, attributes, styles, URLs |
| Accessible text | Existing `<title>`, `<desc>`, and text nodes | Byte placement only | Text removal or rewrite |
| Registry | `assets/registry/visual-assets.json` | Matching `release_hash` refresh | Source/original hash changes |
| Manifest | `assets/ASSET_RELEASE_MANIFEST.json` | Deterministic regeneration | Unregistered or extra release files |
| Check report | Optimizer/checker output | File/count/byte/hash status | Runtime performance inference |

## Player-facing and accessibility semantics

No player-facing route, visual catalog, audio cue, motion, or host projection
changes. Existing SVG titles, descriptions, written equivalents, non-color
semantics, and fallback behavior remain the meaning-bearing boundary.

## Fail-closed behavior

The checker fails on missing/non-relative roots, malformed SVG/XML, missing
release files, non-idempotent output, stale registry hashes, or stale release
manifest data. It must not fetch, rewrite source files, or silently accept an
untracked release derivative.

## Explicit non-goals and evidence limits

- No geometry simplification, path conversion, style minification, raster
  derivative work, audio compression, lazy loading, preload policy, browser
  measurement, render/decode benchmark, offline test, device matrix,
  screenshot suite, or human evaluation.
- A passing check proves repository-level normalization and hash alignment, not
  visual equivalence on every browser or measurable runtime improvement.

## Verification

Tests must cover idempotence, text/attribute preservation, current release
count/bytes, malformed/path failures, and registry/manifest alignment. Full
project release gates remain required.

---
# Presentation Contract — Phase 11.2 missing-asset fallback v0.12.99

## Goal and authorization

Define the missing-asset fallback evidence boundary for all current facility
and fictional institution release descriptors. The existing
`assetPresentationFor`/catalog helpers remain authoritative; tests may invoke
them with missing, failed, or malformed availability and inspect their written
fallback output.

## Source and coverage ledger

| Surface | Authorized source | Required evidence | Prohibited inference |
| --- | --- | --- | --- |
| Facility descriptor | `FACILITY_COMPONENTS` | Every release path is registry-backed and fallback-tested | No new facility inference |
| Institution descriptor | `IDENTITY_KITS` | Every release path is registry-backed and fallback-tested | No identity substitution |
| Availability | `asset-availability.mjs` | Missing/failed/malformed becomes explicit fallback | No silent asset success |
| Fallback view | Existing descriptor fallback | Non-empty label/equivalent, null release path | No hidden-state or outcome claim |
| Registry | `assets/registry/visual-assets.json` | Catalog release-path set aligns exactly | No unregistered file acceptance |

## Accessibility and presentation semantics

Fallback output remains written text with explicit status, reason, source, and
equivalent fields. No color-only signal, audio cue, animation, network fetch,
or host/session read is introduced. Existing generic facility and institution
labels remain the meaning-bearing fallback.

## Fail-closed behavior

Coverage fails if a catalog descriptor lacks a fallback, emits an asset release
path while unavailable, has an empty equivalent, or references a release path
absent from the canonical registry. Unknown/contradictory availability remains
malformed fallback behavior.

## Explicit non-goals and evidence limits

- No new fallback code, asset mutation, registry change, source/release hash
  change, browser matrix, device test, screenshot, runtime performance test,
  human accessibility evaluation, or full-campaign asset claim.
- Passing tests prove only the current enumerated catalog contract under Node;
  they do not establish browser rendering or human comprehension.

## Verification

Focused Node/Python tests must enumerate all current facility/institution
descriptors and preserve the no-network/no-authority boundary. Full project
release gates remain required.

---
# Presentation Contract — Phase 11.2 raster scope and bounds v0.13.0

## Goal and authorization

Define the raster packaging boundary for the current repository. The checker
may inspect release files and the existing unverified portrait-preview
metadata/PNGs, but may not rewrite, promote, resize, compress, or load them in
the browser.

## Source and budget ledger

| Surface | Authorized source | Required boundary | Prohibited inference |
| --- | --- | --- | --- |
| Release package | `assets/release` | Zero supported raster files | No future raster absence claim |
| Portrait previews | `assets/generation/portrait-previews` | 2048×2048 max, 3 MiB/file, 24 MiB total | No release eligibility |
| Preview metadata | `portrait-previews.json` | Seven exact roles, `release_eligible: false`, no release path/registry ID | No provenance completion |
| Report | `raster-scope-v1` output | Count, bytes, dimensions, status | No decode/render/memory claim |

The preview bounds are an explicit repository review limit, not an assertion
that 1254×1254 previews are suitable runtime derivatives.

## Accessibility and presentation boundary

No visual/audio runtime surface changes. Existing written equivalents,
generic fallbacks, pending review status, and preview-only provenance remain
authoritative.

## Fail-closed behavior

The checker fails on release raster files, missing/malformed PNG headers,
oversized preview dimensions/bytes/totals, missing preview metadata, promoted
release paths/registry IDs, or path escapes. It does not silently skip files.

## Explicit non-goals and evidence limits

- No image edit, raster derivative promotion, compression, lazy loading,
  preload, browser matrix, offline test, device test, decode/render benchmark,
  memory measurement, screenshot, legal clearance, or human evaluation.
- Passing proves only current file/scope bounds and metadata separation.

## Verification

Tests must cover current counts/bytes/dimensions, release prohibition,
oversize/malformed/promotion failures, and deterministic CLI output. Full
project release gates remain required.

---
# Presentation Contract — Phase 11.2 audio packaging review v0.13.1

## Goal and Authorization

Record and machine-check the current audio packaging boundary. This slice is
authorized only to review whether compression applies to the current release
surface and to add a fail-closed scope report. The current answer is
`not-applicable-runtime-generated`: browser audio is synthesized from local
recipes after user gesture, and no audio file is distributed.

## Player Questions and Consequences

The player should be able to understand that optional audio is a presentation
layer, not a source of additional game facts. Visible cue text, event text,
history, and debrief content remain complete when audio is muted, unsupported,
unavailable, or absent from the release package.

## Actor-Visible Source Ledger

| Semantic element | Source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| UI/event cue recipe | `gui/audio.mjs` and `gui/audio-cue-contract.mjs` | Explicit visible interaction or committed visible event; playback can be unavailable | Do not infer an outcome from a sound that is not visible in the host response |
| Music state recipe | `gui/music-stem-contract.mjs` and host-shaped visible resolution context | Active visible page/resolution context; malformed or absent state uses written fallback | Do not encode hidden state, intent, severity, or future outcome |
| Ambience recipe | `gui/ambience-contract.mjs` and explicit visible presentation setting | Optional, reduced, muted, or unsupported | Do not imply clinical acuity, geography, or real institution identity |
| Release packaging status | `assets/audio-packaging-scope.json` and audio registries | Read-only package inspection | Do not treat package absence as a simulation state |

## Visual, Motion, and Audio Semantics

- The report uses explicit text fields for `runtime-generated` and
  `compression-not-applicable`; no visual or auditory signal is required to
  interpret the packaging result.
- The checker accepts no file-backed release audio in the current scope. A
  future file-backed asset requires a separately reviewed codec, source,
  release derivative, hash, license, size, decode, and accessibility contract.
- No playback timing, cue priority, volume, music state, or ambience behavior
  changes in this slice.

## Accessibility and Fallbacks

Mute, cues-only, reduced-audio, unsupported-Web-Audio, failed-playback, and
missing-audio paths preserve written equivalents and visible source/status
language. The packaging report itself is text-first. Reduced motion is not
relevant because no animation is added.

## Authority, History, and Replay Boundaries

The packaging document and checker are read-only presentation/release
governance. They do not enter commands, transition evaluation, stochastic
inputs, state hashes, immutable history, replay, or debrief facts. The Rust
host remains authoritative for all game state and outcomes; the browser remains
responsible only for optional presentation playback and local preferences.

## Asset Provenance and Release Requirements

Current runtime-generated recipes remain registered with `release_path: null`,
project-generated provenance, and written equivalents. The scope checker scans
the release tree for known audio suffixes and requires zero matches. If a
future file is introduced, it must not be silently covered by this decision;
the scope document, registry, credits, hashes, security checks, and compression
evidence must be updated in a new reviewed slice.

## Verification and Evidence Limits

`tests/test_audio_packaging.py` covers the current green report, CLI output,
release-file rejection, path/schema validation, and registry/catalog release
path semantics. Automated evidence establishes only the current packaging
boundary. It does not establish codec quality, loudness, decode latency,
fatigue, lived accessibility, device performance, browser compatibility,
human comprehension, licensing counsel, or educational effectiveness.

## Non-Goals and Open Questions

- No audio file is added or compressed.
- Lazy loading, preload policy, offline operation, low-power testing, browser
  compatibility, screenshots, and human review remain open roadmap work.
- If recorded or pre-rendered audio becomes necessary, choose a codec and
  compression target through a separate plan with actual browser/device
  evidence rather than changing this report's meaning.

---
# Presentation Contract — Phase 11.2 loading-policy audit v0.13.2

## Goal and Authorization

Define and machine-check the current live GUI loading boundary. The current
decision is `no-lazy-loading-needed` and `no-preload-directives`: the live
regional scene is serialized inline from actor-visible DTOs, runtime audio is
generated locally, and no file-backed presentation asset is loaded by the live
entrypoint. This slice may add governance evidence only.

## Player Questions and Consequences

The player should receive the same visible board, reports, metrics, written
audio equivalents, and recovery states whether optional file-backed assets are
absent. Loading policy must never become a hidden source of strategic
information, timing-dependent outcome, or severity signal.

## Actor-Visible Source Ledger

| Surface | Current source | Loading decision | Prohibited inference |
| --- | --- | --- | --- |
| Regional board and facility scene | `gui/scene.mjs` and actor-visible host DTOs | Inline/generated SVG; no file-backed lazy or preload path | Do not load or infer hidden facility, rival, or future-outcome data |
| Executive desktop | `gui/index.html` and local modules | Static HTML/CSS/module graph; no media tags or preload directives | Do not use load timing to signal state or priority |
| Optional UI/event audio | `gui/audio.mjs` and registered runtime recipes | Generated after user gesture; no file decode or preload | Do not infer a result from audio availability or timing |
| Release assets | `assets/registry/*.json` and `assets/release` | No current live-entrypoint references; future paths require policy metadata | Do not treat an unlisted asset as approved or actor-visible |

## Visual, Motion, and Audio Semantics

- The checker reports explicit text decisions for no-lazy and no-preload
  behavior; no color, motion, or sound conveys loading status.
- A future high-value asset must declare a stable registry ID, live consumer,
  load trigger, preload justification or lazy trigger, byte budget, fallback,
  written equivalent, and provenance before entering the live surface.
- No loading spinner, animation, audio cue, or timing behavior changes here.

## Accessibility and Fallbacks

The current no-file policy preserves keyboard navigation, visible source/status
text, text scaling, reduced motion, mute/reduced-audio behavior, unsupported
audio fallback, and missing-asset fallback. A future loading failure must
preserve the existing generic visual/audio descriptor and written equivalent.

## Authority, History, and Replay Boundaries

The loading policy is a read-only presentation/release contract. It cannot
enter commands, transition evaluation, stochastic inputs, host projections,
state hashes, immutable history, replay, or debrief facts. The browser remains
presentation-only and the Rust host remains authoritative.

## Asset Provenance and Release Requirements

The current report requires the live files to contain no file-backed media
reference, runtime file-load expression, or preload directive and requires all
declared policy paths to remain repository-relative. Registry metadata may
retain release paths without loading them. Future file-backed assets must join
the existing visual or audio registry, include provenance/hash/fallback metadata, and pass security,
credits, release, and loading-policy checks. A policy exception is not an
implicit release approval.

## Verification and Evidence Limits

`tests/test_loading_policy.py` covers the current green report and CLI,
preload/media-marker rejection, unlisted source and path/schema failures, and
policy metadata requirements. This is static contract evidence only; it does
not establish browser loading order, cache behavior, decode/render latency,
memory use, offline operation, device suitability, compatibility, lived
accessibility, or human comprehension.

## Non-Goals and Open Questions

- Do not add a loader, preload tag, media file, browser network call, or runtime
  behavior in this slice.
- Offline operation, low-power devices, browser compatibility, screenshot
  coverage, full campaign continuity, asset quality, and human evaluation
  remain open.
- If file-backed audio or raster assets become runtime-required, revisit the
  loading decision with actual browser/device measurements.

---

# Presentation Contract — Phase 11.2 browser compatibility matrix v0.13.5

## Goal and Authorization

This slice authorizes a versioned technical compatibility matrix for the
existing dependency-free GUI and its loopback host. It does not authorize a
new browser framework, runtime asset loader, or simulation change.

## Player Questions and Consequences

The player should be able to launch the documented GUI, read the current
actor-visible board and executive surfaces, use keyboard and text controls,
and receive complete written feedback when optional SVG/audio/browser
capabilities are unavailable. Compatibility evidence answers whether the
presentation remains decision-complete across the documented target.

## Actor-Visible Source Ledger

| Semantic surface | Source | Timing | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- | --- |
| Board, facilities, overlays, reports | Existing host-projected DTOs and committed history consumed by `gui/` | Current host read or committed resolution | Existing generic marker, source label, written equivalent, or unavailable state | No browser-derived severity, intent, outcome, or geography |
| Audio cues and music | Existing host-shaped visible cue/state IDs with legacy visible-only fallback | Committed resolution or local presentation outcome | Mute, reduced-audio, unsupported-audio, or written equivalent | No private rival/true-state classifier |
| Compatibility status | Versioned local policy/checker inputs and observed browser capability result | Before/while loading the page | Unsupported/unknown environment is explicit and does not become a support claim | No support inference from user-agent string alone |

## Visual, Motion, and Audio Semantics

Compatibility metadata is non-informational presentation evidence. It must not
alter visual or audio meaning. Text, symbols, labels, and written resolution
content remain the required equivalents for color, motion, and audio.

## Accessibility and Fallbacks

- Keyboard navigation and semantic HTML remain required on the supported target.
- Reduced motion, mute, cues-only, text scaling, unavailable audio, missing
  assets, and failed adapter reads retain existing written content.
- Unsupported capability combinations report a recoverable status and use the
  existing generic/disabled fallback; they do not block the simulation host.

## Authority, History, and Replay Boundaries

The compatibility checker is read-only. Browser capability results, viewport
measurements, and fallback decisions never enter commands, transition
evaluation, stochastic inputs, state hashes, immutable history, replay
artifacts, or debrief facts. The host remains authoritative.

## Asset Provenance and Release Requirements

This slice adds no assets. Existing registry, release hashes, credits, and
offline route policy remain the source of truth. The checker rejects a
compatibility declaration that references an undeclared local policy or route.

## Verification and Evidence Limits

Automated policy checks establish documented capability requirements, route
closure, syntax, and fallback contracts. A local browser smoke check establishes
only the observed environment and visible page state. It does not establish
all browser versions, device performance, contrast, screen-reader behavior, or
lived accessibility.

## Non-Goals and Open Questions

- No universal browser/device certification.
- No low-power benchmark in this slice.
- Open: measured low-power device behavior, additional browser engines, and
  human accessibility evaluation.

---
# Presentation Contract — Phase 11.2 offline package completeness v0.13.3

## Goal and Authorization

Make the live GUI usable from a normal repository checkout without external
asset or module sources. The loopback Rust host must embed the complete local
entrypoint graph, host adapter, and catalogs required by the live desktop. This
slice may add route coverage and static governance evidence only.

## Player Questions and Consequences

The player should receive the same actor-visible board, reports, actions,
history, replay, debrief, written audio equivalents, and recovery states when
the machine has no external network access. Offline package completeness must
never become a hidden source of strategic information or a timing-dependent
outcome signal.

## Actor-Visible Source Ledger

| Surface | Current source | Offline contract | Prohibited inference |
| --- | --- | --- | --- |
| Executive desktop | `gui/index.html` and embedded local modules | Served from the loopback host with no external module source | Do not infer state from missing network or route timing |
| Host boundary | `gui/host-adapter.mjs` and `/api/v1/sessions` | Same-origin loopback API only | Do not move authority into the browser |
| Catalogs | `gui/audio-catalog.json` and `gui/visual-catalog.json` | Embedded local JSON routes | Do not infer asset approval from route presence |

## Visual, Motion, and Audio Semantics

- No visual, motion, or audio cue changes in this slice.
- Static route completeness does not establish decode, render, memory, device,
  or browser-performance behavior.
- Missing route or offline host failures remain written, recoverable errors;
  they do not alter game state.

## Accessibility and Fallbacks

Existing keyboard, scaling, reduced-motion, mute/reduced-audio, written
equivalent, and missing-asset fallbacks remain authoritative. The offline
package audit adds no loading spinner, timing cue, or new visual state.

## Authority, History, and Replay Boundaries

The server continues to own session state, command validation, transitions,
stochastic inputs, history, hashes, replay, and debrief facts. The offline
policy and route table are delivery evidence; they cannot enter a transition
or expose hidden state.

## Asset Provenance and Release Requirements

The embedded route table may serve only repository-local, reviewed source files.
It does not promote release assets, change registry provenance, or authorize
external URLs. A future external or file-backed dependency requires a new
loading/offline review with explicit fallback and evidence.

## Verification and Evidence Limits

`tests/test_offline_availability.py` and the Rust GUI-server tests establish
route/source closure, loopback binding, and current policy shape. They do not
establish browser behavior, cache persistence, low-power suitability,
compatibility, screen-reader behavior, lived accessibility, or human
comprehension.

## Non-Goals and Open Questions

- Do not add a service worker, CDN, external module, or production deployment.
- Do not treat proof pages or external documentation as the live offline
  surface.
- Low-power-device and browser-compatibility gates remain open.

---

# Presentation Contract — Phase 11.1 facility asset coverage v0.13.6

## Goal and authorization

Prove that the live file-backed facility vocabulary has complete source and
release asset wiring. This is a registry/catalog evidence slice only.

## Player questions and consequences

The player should see a stable facility label or the explicit generic facility
fallback. Asset coverage must not create a new strategic fact, imply a facility
outcome, or alter campaign placement.

## Actor-visible source ledger

| Surface | Source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Facility catalog | `gui/facility-components.mjs` | `generic-facility` with no asset paths | No browser- or registry-derived severity, capacity, ownership, or outcome |
| Source/release assets | Catalog paths and `assets/release/visual/svg/` | Fail the coverage check if a declared path or hash is absent | No promotion of an unregistered or unapproved asset |
| Registry evidence | `assets/registry/visual-assets.json` entries named `visual.facility.<id>` | Fail closed on missing, duplicate, mismatched, or unapproved entries | Registry presence is not a claim of visual quality or campaign placement |

## Visual, motion, and audio semantics

No visual geometry, motion, audio cue, or metric meaning changes. The coverage
test validates existing bytes and metadata only.

## Accessibility and fallbacks

Existing facility labels, layer text, generic markers, and unavailable/error
states remain authoritative. `generic-facility` is deliberately excluded from
file-backed asset coverage and remains the safe fallback.

## Authority, history, and replay boundaries

The ledger and test are read-only governance evidence. They cannot enter
commands, transitions, stochastic inputs, state hashes, immutable history,
replay artifacts, or debrief facts. The host remains authoritative.

## Asset provenance and release requirements

Each file-backed facility must have matching source/release paths, approved
status, and exact original/release hashes. Existing asset-registry,
release-manifest, credits, and license validators remain required.

## Verification and evidence limits

The focused test proves catalog-to-registry wiring and byte hashes. It does not
prove facility placement in every campaign month, screenshot completeness,
render quality, device/browser performance, lived accessibility, or human
visual-quality review.

## Non-goals and open questions

- No new facility asset or runtime renderer.
- Open: full campaign placement/use, screenshot suite, continuity, performance,
  compatibility, and human evaluation gates.

---

# Presentation Contract — Phase 11.1 event-cue coverage v0.13.7

## Goal and authorization

Prove exact parity among the current event-channel audio cue catalog, the
host-shaped visible event-cue projection, and the legacy browser fallback. This
is a presentation evidence slice only.

## Player questions and consequences

When a committed visible event is reported, the player may receive an optional
cue with the same written source/equivalent. A missing, muted, unknown, or
explicitly empty cue list must leave the visible report intact and must not
signal a hidden outcome.

## Actor-visible source ledger

| Surface | Source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Event cue contract | `gui/audio-cue-contract.mjs` event-channel entries | Keep source/equivalent text and cues-only metadata | No cue intensity as severity, intent, probability, or outcome |
| Host projection | `src/mcp/resolution.rs: visible_event_cue_ids` | Empty list is valid; host remains authoritative | No private rival, true-state, stochastic, or effect-queue data |
| Legacy browser fallback | `gui/audio.mjs: visibleEventCues` | Use visible text only for older envelopes; unknown IDs remain non-authoritative | No browser-derived event classification outside visible text |

## Visual, motion, and audio semantics

No audio recipe, timing, loudness, cue priority, or visual rendering changes.
The audit verifies the existing cues-only and written-equivalent contracts.

## Accessibility and fallbacks

Mute, cues-only mode, written event text, explicit empty lists, malformed
legacy inputs, and unknown cue IDs remain recoverable. Audio is supplementary;
the visible report is the required semantic channel.

## Authority, history, and replay boundaries

The catalog/projection test is read-only. Cue IDs cannot enter commands,
transitions, stochastic inputs, state hashes, immutable history, replay
artifacts, or debrief facts. The host remains authoritative.

## Asset provenance and release requirements

No audio asset or registry entry is added. Existing generated-audio provenance,
credits, normalization, and release checks remain authoritative.

## Verification and evidence limits

Parity tests prove current ID wiring and visible-only fallbacks. They do not
prove full campaign event taxonomy, loudness, fatigue, musical quality,
hardware/browser behavior, lived accessibility, or human usefulness.

## Non-goals and open questions

- No new cue, recorded audio, host event, simulation rule, or client-owned
  authority.
- Open: broader event taxonomy, music continuity, screenshot/device/browser
evidence, audio quality, and human evaluation.

---

# Presentation Contract — Phase 11.1 music-state coverage v0.13.8

## Goal and authorization

Prove the current music-state catalog is consistent across the host resolution
projection and browser classifier, with the browser-only menu state kept
separate from host resolution.

## Player questions and consequences

Music may gently reflect a visible planning, operating, pressure, policy,
competitive, affiliation, or debrief context. It must never reveal a private
intent, hidden outcome, severity certainty, or future result.

## Actor-visible source ledger

| Surface | Source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Music catalog | `gui/music-stem-contract.mjs` | Retain heading/status/source/result text when unavailable or suppressed | No music state as hidden severity, intent, probability, or outcome |
| Host resolution state | `src/mcp/resolution.rs: visible_music_state_id` | Explicit debrief/visible priority; existing browser fallback for missing/malformed values | No private rival, true-state, stochastic, or effect-queue data |
| Menu/planning state | `classifyVisibleMusicState` local stage | Browser-only `menu` state; no host resolution claim | No local stage inference about simulation outcome |

## Visual, motion, and audio semantics

No stem recipe, loop duration, crossfade, gain, or visual rendering changes.
The audit verifies existing ordered stem metadata and visible-source rules.

## Accessibility and fallbacks

Mute, music-only controls, cues-only mode, reduced-audio behavior, written
headings/status/source/result text, and unknown/malformed state fallback remain
authoritative. Audio is supplementary.

## Authority, history, and replay boundaries

The catalog/projection tests are read-only. Music state cannot enter commands,
transitions, stochastic inputs, state hashes, immutable history, replay
artifacts, or debrief facts. The host remains authoritative.

## Asset provenance and release requirements

No stem or audio asset is added. Existing generated-audio registry, credits,
normalization, and release checks remain authoritative.

## Verification and evidence limits

Parity tests prove current state wiring, priority, and visible-only fallback.
They do not prove full campaign continuity, loudness, fatigue, musical quality,
hardware/browser behavior, lived accessibility, or human usefulness.

## Non-goals and open questions

- No new stem, audio asset, host event, simulation rule, or browser-owned music
  authority.
- Open: broader campaign taxonomy/continuity, screenshots/device/browser
  evidence, audio quality, and human evaluation.

---

# Presentation Contract — Phase 11.1 history-view coverage v0.13.9

## Goal and authorization

Document the current live history-view handoff from the host-owned immutable
history to the existing text-first browser surface. This bounded contract closes
only the current history-view checklist item.

## Player questions and consequences

The view should answer: “Which committed visible transitions occurred, in what
turn order, and what state hash identifies each row?” It must not imply hidden
causes, private rival detail, severity, future outcomes, or replay authority.

## Actor-visible source ledger

| Surface | Source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Host history | `src/mcp/session.rs: get_history` with `competitive-history-v1` | Return the host error; do not synthesize rows | No true state, private detail, or local history |
| Loopback route | `src/gui_server.rs: GET /api/v1/sessions/{session_id}/history` via `get_competitive_history` | Preserve structured failure for the adapter; reject noncompetitive sessions | No network or alternate data source |
| Browser adapter | `gui/host-adapter.mjs: getHistory` | Expose recoverable adapter error | No command submission or simulation read |
| History renderer | `gui/app.mjs: renderHistoryEnvelope` / `#history-list` | Keep the last valid view and show recovery status | No browser-derived causality or outcome |

## Visual and semantic behavior

Rows remain text-first and pair each committed `turn` with its corresponding
`state_hash`. Valid data requires an aligned transition count and transition
rows. Empty history is explicit; malformed, unsupported, missing, and failed
reads fail closed without replacing valid content with invented data.

## Accessibility and fallbacks

The text list and visible recovery status are the meaning-bearing channels.
Missing or throwing adapters preserve the last valid view and expose a
recoverable error. Contrast, focus, screen-reader behavior, device behavior,
and human comprehension remain unverified.

## Authority, history, and replay boundaries

The route calls only the existing non-mutating `GameSessionStore::get_history`.
The browser validates and renders host-shaped data; it cannot submit commands,
advance a session, reconstruct history, alter hashes, or regenerate replay.

## Evidence limits and deferred work

Focused tests establish current source parity, row alignment, validation, and
failure preservation. They do not establish full campaign history/debrief,
durable save/load/replay continuity, screenshots, browser/device compatibility,
accessibility, or human educational usefulness.

# Presentation Contract — Phase 11.1 operational-overlay coverage v0.13.12

## Goal and Authorization

Complete the current twelve-entry operational-overlay catalog in the live
competitive regional-world read-only projection. Authorized changes are direct
host bindings, catalog source/equivalent alignment, ledger evidence, and tests.
No simulation rule, hidden-state projection, browser authority, new asset, or
human-quality claim is authorized.

## Player Questions and Consequences

The overlay should answer: “Which explicitly reported operational field or
visible text needs attention?” It may identify staffing, capacity, demand,
projects, payer/policy signals, community trust, cash/runway, recovery, or
uncertainty only when that source is present. It must not answer why an outcome
occurred, predict what will happen, or rank a strategy.

## Actor-Visible Source Ledger

| Catalog ID | Direct host condition | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| staffing constraint | `PlayerObservation.workforce_trust_summary` contains visible strained status | No overlay when status is absent/non-strained | No staffing-cause or labor-outcome inference |
| capacity constraint | Explicit player facility capacity field is zero/unavailable | No overlay when all reported capacities are positive | No hidden utilization or demand forecast |
| demand pressure | `PlayerObservation.monthly_unmet_demand > 0` | Raw metric remains visible without category when zero | No severity or future demand claim |
| active/delayed project | Explicit `in_flight_projects` text, with delayed wording for delayed state | No overlay for empty/none text | No inferred delay cause |
| project completion | Visible project text contains explicit completion wording | No overlay when text is absent | No transition reconstruction |
| payer/network change | Visible market bullet contains payer, carrier, network, or renewal signal | No overlay when signal is absent | No payer forecast or negotiation advice |
| regulatory review | Visible regulatory policy bullet or annual review exists | No overlay when absent | No legal/compliance conclusion |
| community trust | `PlayerObservation.community_trust_summary` is `watch` | No overlay for stable/absent status | No population judgment |
| financial distress | Visible negative margin or strained cash runway | No overlay when neither is present | No solvency prediction |
| operational recovery | Positive monthly margin plus explicit visible recovery text | No overlay when either is absent | No durable recovery claim |
| uncertain/stale intelligence | Visible information gaps or prior access revision exists | No overlay when both are absent | No probability/truth estimate |

## Visual, Motion, and Audio Semantics

The browser continues to use the existing registered non-color patterns, glyphs,
stable priority/order, written equivalents, static reduced-motion behavior, and
optional audio. The host only adds `operational_overlay_id` values to existing
actor-visible regional-world rows; raw demand/access/capacity/process rows stay
raw and unclassified.

## Accessibility and Fallbacks

Every bound entry retains source text and a written equivalent. Unknown IDs
resolve to `operational-overlay-generic`; missing conditions omit the optional
operational binding without deleting the raw metric. Meaning does not depend on
color, motion, or audio. This slice does not establish contrast, screen-reader,
device, or lived accessibility quality.

## Authority, History, and Replay Boundaries

Conditions read only `PlayerObservation` fields and explicit visible bullets.
They do not read true world state, transition inputs, effect queues, hidden rival
state, stochastic inputs, commands, hashes, history, replay, debrief facts, or
client-owned authority. The browser resolver remains a presentation fallback,
not a source of truth.

## Asset Provenance and Release Requirements

No asset or audio bytes are added or changed. Existing catalog provenance,
registry, release, credits, security, and offline checks remain authoritative.

## Verification and Evidence Limits

Rust fixture tests and Python live/ledger tests must cover all twelve IDs,
absence behavior, raw metric preservation, generic fallback, source/equivalent
text, syntax, and forbidden authority markers. Catalog-to-host parity does not
establish full campaign placement/use, screenshots, asset quality, human
accessibility, audio usefulness, or educational benefit.

## Non-Goals and Open Questions

- No new overlay categories, screenshot suite, durable save/load, replay
  regeneration, runtime telemetry, or simulation mechanism is included.
- Open: full campaign placement/use and visual continuity across durable
  save/load/replay remain separate Phase 11.1 gates.

# Presentation Contract — Phase 11.1 terminal debrief coverage v0.13.13

## Goal and Authorization

Document the current competitive terminal debrief presentation as a bounded
host/browser contract. Authorized evidence covers the existing end-session
envelope, aligned history/replay metadata, host-authored debrief text, terminal
controls, and failure handling. No new debrief content or authority is added.

## Player Questions and Consequences

The terminal view should answer: “What committed history, replay identity, and
host-authored lessons can I inspect after this session ends?” It must not imply
that a debrief line is a forecast, an instructor-only true-state view, a
counterfactual, a causal proof, or evidence of learning.

## Actor-Visible Source Ledger

| Surface | Authorized source | Required behavior | Prohibited inference |
| --- | --- | --- | --- |
| Schema/session | `EndSessionEnvelope` from host end-session route | Reject unknown/incomplete schema | No browser-created terminal state |
| History rows | Host immutable history with turn/command/hash | Render aligned rows | No replay regeneration or mutation |
| Replay metadata | Host seed, transition count, latest hash | Require count/hash alignment | No hidden state or future outcome |
| Debrief text | Host-authored `debrief` lines | Render written lines completely | No browser-authored lesson or quality claim |
| Terminal controls | Valid host terminal result | Disable further session actions | No client authority over session end |

## Visual, Motion, and Audio Semantics

The existing text-first history/debrief view remains authoritative for meaning.
Terminal debrief music is optional and atmospheric; muting it does not remove
history, hashes, replay metadata, or written debrief lines. No new motion or
asset is introduced.

## Accessibility and Fallbacks

Missing, malformed, unknown-schema, count-mismatched, and hash-mismatched
envelopes fail closed and preserve the current presentation. Written history,
replay, and debrief content remain present when audio is unavailable. This
contract does not establish contrast, screen-reader, lived accessibility,
usability, or learning quality.

## Authority, History, and Replay Boundaries

The host/core owns session history, state hashes, replay metadata, and debrief
facts. The browser validates and renders the supplied projection only. No
commands, transitions, stochastic inputs, hidden fields, or client-owned
history/replay/debrief facts are introduced.

## Verification and Evidence Limits

`tests/test_phase11_live_debrief.py` covers valid rendering, aligned rows,
count/hash/schema rejection, terminal controls, route/source markers, syntax,
and authority exclusions. The ledger links those checks to the exact host,
route, adapter, and renderer sources. Evidence is limited to the current
competitive terminal view; full-campaign debrief taxonomy, instructor views,
counterfactuals, screenshots, and human learning remain open.

## Non-Goals and Open Questions

- No new debrief mechanics, instructor export, counterfactual, durable
  persistence, replay playback, screenshot tooling, asset, or audio file.
- Open: which broader campaign/instructor debrief surfaces need separate
  information-boundary and usability evidence?
# Presentation Contract — Phase 11.2 low-power profile evidence v0.13.11

## Goal and Authorization

Define the narrow technical presentation contract for the Phase 11.2
low-power-device checklist item. The authorized output is a read-only,
emulated reduced-capability profile for the current loopback GUI and a
fail-closed report over its source/DOM/SVG/time observations. This does not
authorize runtime optimization, new assets, browser dependencies, or a real
device-certification claim.

## Player Questions and Consequences

The evidence should answer: “Does the current first-session presentation retain
its written meaning and bounded structural surface when motion and audio are
reduced at a smaller viewport?” It must not imply that a device has a specific
battery, thermal, frame-rate, or accessibility outcome.

## Actor-Visible Source Ledger

| Signal | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Live source bytes | `assets/loading-policy.json` `live_files` and repository file sizes | Fail the report if a declared path is missing or escapes | No download, cache, or decode estimate |
| DOM/SVG counts | Local browser smoke observation of the static/live shell | Fail the captured report if the values are absent or non-integers | No frame-rate or render-time claim |
| Shell/start/adapter time | Local loopback browser smoke wall-clock observations | Fail if values are missing, negative, or above the declared proxy limit | No hardware, thermal, battery, or network claim |
| Written equivalent | Visible text in `gui/index.html` during the smoke | Fail if text fallback is absent | No claim about human comprehension |
| Audio-off behavior | Existing visible `Audio off` state and audio fallback text | Fail if the captured surface omits it | No claim about loudness or fatigue |
| Reduced-motion setting | Existing visible settings language and control | Preserve the current text contract; do not infer runtime preference support | No claim about lived accessibility |

## Visual, Motion, and Audio Semantics

The profile uses a 1024×768 viewport, reduced-motion preference, audio off,
optional local storage unavailable, and loopback-only host access. These are
test conditions, not simulation inputs or presentation state. The policy checks
that the current written and audio-off fallbacks are present; it does not add
new animation, audio, visual classification, or asset loading.

## Accessibility and Fallbacks

The test retains written results, source/status language, visible symbols, and
fallback text when audio is off. Reduced-motion is a declared preference in
the profile. Missing policy fields or unsupported measurements fail closed;
they do not receive a generic “pass.” The evidence does not establish contrast,
screen-reader behavior, device compatibility, battery life, or lived
accessibility.

## Authority, History, and Replay Boundaries

The policy and report are outside simulation state. They do not enter commands,
transition evaluation, stochastic inputs, hashes, immutable history, replay,
debrief facts, or host projections. The browser smoke only reads the existing
loopback presentation and does not reconstruct or mutate simulation state.

## Asset Provenance and Release Requirements

No asset bytes, registry entries, release paths, or external dependencies are
added. The checker reuses the existing loading and offline policies; all
provenance and release gates remain unchanged.

## Verification and Evidence Limits

Focused tests must cover green report/CLI output, live-source drift, limit
violations, malformed profiles, path escapes, and an attempted real-device
claim. Full release, documentation, Rust, and Python checks remain required.
The smoke values are local wall-clock measurements from an emulated profile,
not repeatable hardware benchmarks. They do not establish low-power device
performance, browser-engine support, cache behavior, memory/thermal behavior,
human usability, accessibility quality, audio quality, or learning.

## Non-Goals and Open Questions

- No browser automation dependency, device farm, runtime telemetry, or visual
  optimization is included.
- No real low-power device is available in this slice; a physical-device
  check remains an external follow-up if the project needs certification.
- Open: which named hardware/browser targets should be tested before public
  release, and what representative workload should be used for each?

# Presentation Contract — Phase 11.1 checkpoint visual continuity v0.13.14

## Contract status

Complete for the current in-memory host checkpoint view. This is a technical
presentation contract, not evidence of durable save/load, cross-process
recovery, browser-refresh recovery, replay playback, accessibility quality, or
human learning.

## Source and visible behavior

- Host source: `src/mcp/session.rs` owns one cloned checkpoint per active
  session and returns `competitive-save-v1` operation, campaign, seed,
  transition-count, and latest-state-hash metadata.
- Boundary sources: `src/mcp/server.rs`, `src/gui_server.rs`, and
  `gui/host-adapter.mjs` expose explicit save/load operations; `gui/app.mjs`
  validates the envelope and refreshes the actor-visible read-only view after
  a successful load.
- The visible contract keeps the save/restore controls host-gated and retains
  the current view with a recoverable message when the checkpoint is missing or
  the adapter/refresh path fails.

## Fallback, authority, and provenance

The host/core remains authoritative for checkpoint state, transition count, and
state hash. The browser receives metadata and refreshes projections; it does not
serialize or reconstruct true state. No asset or audio source is introduced.
Missing or malformed envelopes fail closed, while current presentation remains
available when recovery is possible.

## Verification and limits

`tests/test_phase11_live_checkpoint.py` and the ledger parity test cover schema,
metadata alignment, adapter calls, refresh, missing/failing recovery, controls,
routes, syntax, and authority exclusions. Existing Rust session tests cover
cloned restore without a new transition. Durable file/browser persistence,
cross-process/browser-refresh recovery, replay, screenshots, and human review
remain separately gated.

# Presentation Contract — Phase 11.1 replay visual continuity v0.13.15

## Contract status

Complete for the current live host replay projection. This is a technical
presentation contract, not evidence of playback, regenerated simulation traces,
durable persistence, screenshots, accessibility quality, or human learning.

## Source and visible behavior

- Host source: `src/mcp/session.rs` derives `competitive-replay-v1` from
  immutable visible history and returns session/campaign/seed,
  transition-count, latest-state-hash, and visible transition rows.
- Boundary sources: `src/mcp/server.rs`, `src/gui_server.rs`, and
  `gui/host-adapter.mjs` expose the read-only replay operation;
  `gui/app.mjs` validates aligned metadata and renders the projection through
  the existing text-first history surface.
- Empty and committed views render as host-supplied history; a missing adapter,
  failed read, unsupported schema, or misaligned envelope fails closed while
  preserving the last valid view and exposing a recoverable error.

## Fallback, authority, and provenance

The host/core remains authoritative for immutable rows, transition count, seed,
and state hashes. The browser does not calculate transitions, regenerate a
trace, author hashes, or control simulation state. No asset or audio source is
introduced.

## Verification and limits

`tests/test_phase11_live_replay.py` and the ledger parity test cover source
closure, empty/committed validation, row/count/hash alignment, adapter fallback,
rendering preservation, syntax, and authority exclusions. Existing Rust/MCP/
transport tests cover the immutable history source. Playback, regeneration,
durable persistence, screenshots, and human review remain separately gated.

# Presentation Contract — Phase 11.1 current asset-registry coverage v0.13.16

## Contract status

Complete for the current tracked visual and audio registries. This is a
technical registry/release contract, not evidence of future campaign inventory,
asset/audio quality, placement/use, screenshots, accessibility quality, or
human review.

## Source and visible behavior

- `assets/registry/visual-assets.json` and `assets/registry/audio-assets.json`
  are the source documents for the current 38 visual and 7 audio entries.
- Every current entry is approved, unique within its registry, and validated for
  required schema, provenance, license, hash, visible-source, and accessible-
  equivalent fields.
- Fifteen file-backed entries require approved release paths and manifest hashes;
  30 runtime-generated or catalog/documentation entries intentionally retain
  null release paths and are not missing release files.

## Fallback, authority, and provenance

Registry metadata does not enter simulation state, commands, transitions,
stochastic inputs, hashes, history, replay, debrief facts, or client authority.
Existing generic presentation fallbacks remain the behavior for unknown asset
IDs. Credits and third-party notices remain generated from the registries.

## Verification and limits

The ledger parity test links both registries to `tests/test_asset_registry.py`,
the asset validator, release-manifest checker, security validator, and credits
generator; the full asset/security/release/credits checks pass. Future assets,
campaign placement/use, quality, screenshots, accessibility, and human review
remain separately gated.

# Presentation Contract — Phase 11.1 current screenshot-surface contract v0.13.17

## Contract status

Complete for the current supported actor-visible GUI screenshot surface. This
is a source/structural/SVG/local-smoke contract, not a full-campaign raster,
cross-browser/device, pixel-quality, accessibility-quality, or human-review
approval.

## Source and visible behavior

- The ledger names the executive desktop shell, briefing/regional board,
  deterministic regional scene, decision/consequence views, and
  resolution/history/replay/debrief views.
- `gui/index.html`, `gui/app.mjs`, and `gui/regional-board.mjs` provide the
  current source markers; the browser renders actor-visible metrics, briefing,
  campaign controls, settings, first-month path, and the live presentation
  surfaces without inventing hidden state.
- The deterministic regional SVG remains protected by
  `tests/fixtures/regional_board_snapshot.sha256`; structural, live-handoff,
  accessibility, audio, and playtest checks remain the repeatable evidence.

## Fallback, authority, and provenance

The browser remains a read-only presentation client for simulation facts. A
local viewport screenshot is inspection-only evidence and is not a source of
state, a hash authority, a persisted asset, or a cross-browser guarantee.
Written and reduced-audio fallbacks remain part of the visible surface.

## Verification and limits

`tests/test_phase11_campaign_coverage.py` requires the named surfaces, source
markers, SVG snapshot test, structural/live-handoff tests, playtest marker, and
local smoke policy. Full-campaign state-by-state raster goldens,
cross-browser/device capture, pixel-level visual quality, accessibility
quality, usability, asset/audio quality, and human review remain separate
gates.

## Status

`pass` for the current supported screenshot-surface contract. No screenshot
artifact or runtime behavior was added.

# Presentation Contract — Phase 8.2 current portrait-preview inventory integrity v0.13.18

## Contract status

Complete for the current preserved preview inventory and source/hash boundary.
This is not portrait approval, human quality/accessibility review, legal
clearance, release readiness, or runtime integration.

## Source and visible behavior

- `docs/evaluation/portrait-preview-coverage.json` records the seven canonical
  fictional actor roles, seven preserved square source previews, seven pending
  review entries, and empty generation manifest.
- The source previews retain repository-relative paths, SHA-256 bindings,
  prompts/settings, written equivalents, and generic fallbacks; the preview
  proof remains fixture-only and the candidates are not runtime consumers.

## Fallback, authority, and provenance

Portrait preview metadata is generation/release evidence only. It does not
enter simulation state, commands, transitions, observations, history, replay,
debrief facts, or client authority. Missing approved model/seed provenance,
human review, and release data remain explicit blockers.

## Verification and limits

`tests/test_portrait_workflow.py` requires ledger parity and retains hash,
dimension, pending-review, empty-manifest, fallback, and release-block checks.
Human identity/role, resemblance, protected marks, artifact quality, lived
accessibility, small-size/grayscale review, legal/ownership, release
derivative, registry bridge, and runtime-use evidence remain open.

# Presentation Contract — Phase 8.2 current portrait metadata gates v0.13.19

## Contract status

Complete for current machine-checkable portrait role/source/equivalent fields.
This is not human identity, quality, lived accessibility, legal, release, or
runtime approval.

## Source and visible behavior

- The ledger marks role definition, source preservation, and written
  identity-only equivalent/generic fallback fields complete for all seven
  preview candidates.
- The role set provides labels, families, alt-text guidance, and fallbacks;
  the preview set provides existing hash-bound source PNGs and non-empty
  accessible-equivalent/fallback fields.

## Fallback, authority, and provenance

These metadata fields remain generation/release evidence only. They do not
enter simulation state, commands, observations, history, replay, debrief, or
client authority. Generic actor fallbacks remain the runtime-safe boundary.

## Verification and limits

`tests/test_portrait_workflow.py` requires parity for role label/family,
source existence/hash, and written equivalent/fallback fields. Prompt/seed,
crop/derivative, human identity/resemblance, protected marks, artifact
quality, lived accessibility, small-size/grayscale, legal, release, registry,
and runtime-use gates remain open.

# Presentation Contract — Phase 13.1 current technical-release coverage v0.13.20

## Contract status

Complete for current source-checkout technical evidence. This is not a public
release, product/content, full-campaign, durable-persistence,
cross-browser/device, human-quality, or educational-readiness approval.

## Source and visible behavior

- The ledger joins existing Rust/GUI, source/structural/SVG,
  asset/license/hash/security, accessibility-contract, offline, Chromium,
  replay, and in-memory checkpoint checks.
- No new presentation surface or behavior is introduced; existing written,
  fallback, read-only, and bounded continuity contracts remain authoritative.

## Fallback, authority, and provenance

This is governance evidence only. It cannot enter simulation state, commands,
observations, history, replay, debrief, or client authority. The narrower
limits of each referenced ledger remain in force.

## Verification and limits

`tests/test_phase13_technical_coverage.py` requires each check to retain a
source path, command, pass marker, and explicit limits. Product/content
completion, full-campaign raster, durable save/load/replay, additional browser
engines/real devices, human quality/accessibility/legal review, educational
readiness, and public-release approval remain open.

# Presentation Contract — Phase 12 campaign-specific presentation inventory v0.13.21

## Contract status

Complete for the current campaign-coverage inventory only. This is not
campaign-specific art/audio implementation, human review, educational
usability, or Phase 12.3 instructor-view approval.

## Source and visible behavior

- The ledger binds `stabilization-v1` and `regional-affiliation-v1` to the
  existing shared briefing, metric, actor, process, decision, history/replay,
  debrief, and optional-audio host/browser presentation surfaces.
- The current abstract stabilization and stage-based affiliation contracts
  require no new map or facility asset; current written equivalents remain
  visible and source-bound.

## Fallback, authority, and provenance

Campaign coverage remains a read-only host-adapter projection. The inventory
does not enter simulation state, commands, transitions, history, replay,
debrief facts, or client authority. Existing asset/audio provenance checks
remain the relevant technical gates; no new asset was introduced.

## Verification and limits

`tests/test_phase12_campaign_presentation_coverage.py` requires source parity,
written-equivalent fields, supporting evidence paths, and the host-adapter
boundary. Tutorial, pressure-state, stage-specific art/audio, replay/debrief,
instructor, human comprehension, and educational usability remain open.

# Presentation Contract — Phase 12 campaign presentation reuse matrix v0.13.22

## Contract status

Complete for current reusable-asset decisions only. This is not direct
campaign audio mapping, campaign-specific art/stage completion, quality review,
human evaluation, or educational usability approval.

## Source and visible behavior

- The matrix binds both campaigns to exact existing visual catalog IDs,
  generated-audio IDs, the facility fallback registry, and written-equivalent
  metadata.
- Shared identity, marker, status, fallback, and UI primitives are eligible
  for reuse; campaign audio rows are eligible but explicitly not direct
  mappings into the current campaign-coverage envelope.

## Fallback, authority, and provenance

No catalog entry, asset bytes, runtime field, or authority path changes. The
browser remains optional-audio and host-projection driven; missing visual or
audio primitives retain written/fallback presentation.

## Verification and limits

`tests/test_phase12_campaign_reuse_matrix.py` checks IDs, source markers,
approval/provenance, generated-audio null release paths, written equivalents,
and the no-new-asset boundary. Direct mapping, quality, partner/stage art,
replay/debrief, instructor, human, and educational gates remain open.

# Presentation Contract — Phase 12 campaign map/facility asset-need decision v0.13.23

## Contract status

Complete for the current map/facility need decision only. This is not asset
placement/use, visual quality, screenshot coverage, human review, or future
campaign-art approval.

## Source and visible behavior

- The decision joins both campaign IDs to the typed campaign inventory, reuse
  matrix, facility catalog, and generic-facility fallback test.
- Current abstract/stage surfaces remain text-complete without new map or
  facility illustration; future geography, placement, and causal-legibility
  triggers are explicitly recorded.

## Fallback, authority, and provenance

No asset, registry entry, runtime field, transition, or authority path changes.
The generic-facility descriptor remains fallback-only, and written equivalents
remain the presentation boundary.

## Verification and limits

`tests/test_phase12_campaign_asset_need_decision.py` checks source parity,
campaign parity, fallback identity, written equivalents, reopen triggers, and
bounded limits. Placement/use, quality, screenshots, audio, replay/debrief,
instructor, human, and educational gates remain open.

# Presentation Contract — Phase 12 current pressure-state registration v0.13.24

## Contract status

Complete for the current actor-visible shared pressure/recovery taxonomy only.
This is not campaign-specific pressure design, direct audio mapping, quality,
human review, or educational usability approval.

## Source and visible behavior

- The ledger registers eight current categories against operational overlays,
  visual statuses, optional event-cue candidates, and optional music states.
- Each category retains visible trigger fields, text equivalents, non-color
  patterns, reduced-motion behavior, and explicit fallback/audio boundaries.

## Fallback, authority, and provenance

No hidden severity, intent, probability, causality, pressure mechanic, asset,
runtime field, or authority path is added. Campaign-specific registration is
empty, and existing unknown/fallback behavior remains authoritative.

## Verification and limits

`tests/test_phase12_pressure_state_registration.py` checks source/catalog parity,
exact IDs, empty campaign-specific sets, optional audio, and no-new-asset/
hidden-state limits. Tutorial, direct mapping, quality, replay/debrief,
instructor, human, and educational gates remain open.

# Presentation Contract — Phase 12 stabilization tutorial presentation v0.13.25

## Contract status

Complete for the current CLI beginner/tutorial contract only. This is not
browser-native stabilization integration, direct audio, campaign-specific
content, quality, human review, or educational usability approval.

## Source and visible behavior

- The ledger binds the five-turn beginner menu, three written choices per
  turn, choice labels/pros/cons/trade-offs/recommendability, player guide, and
  beginner-test sources.
- Shared campaign coverage can render supplied stabilization projections, while
  the current live GUI launcher remains competitive-only.

## Fallback, authority, and provenance

Beginner recommendations are explanatory metadata, not optimal policy claims;
commands and outcomes remain host/core-owned. No route, asset, audio, runtime
field, transition, or authority path changes.

## Verification and limits

`tests/test_phase12_stabilization_tutorial_presentation.py` checks source
markers, field counts, host ownership, written equivalents, and explicit
no-browser-tutorial/no-human-learning limits. Browser integration, direct
audio, content/pacing, quality, replay/debrief, human, and educational gates
remain open.

# Presentation Contract — Phase 12 stabilization audio-state mapping v0.13.26

## Contract status

Complete for current shared visible audio mapping only. Direct stabilization
campaign-envelope audio, browser-native integration, audio quality, human
review, and educational usability remain separately gated.

## Source and visible behavior

- The ledger joins eight pressure/recovery categories to existing music-state,
  event-cue, and audio-direction IDs with visible trigger and written fields.
- Audio remains optional; the stabilization CLI is text-first and the live GUI
  launcher remains competitive-regional-v1 only.

## Fallback, authority, and provenance

Mute, unavailable, reduced, or unsupported audio preserves written meaning.
No new route, asset, audio ID, runtime field, transition, or authority path
changes; mappings do not infer hidden severity or future outcomes.

## Verification and limits

`tests/test_phase12_stabilization_audio_state_mapping.py` checks exact parity
with pressure registration and current catalogs, plus direct-integration and
human-quality boundaries. Browser integration, direct campaign audio, motif
quality, replay/debrief, human, and educational gates remain open.

# Presentation Contract — Phase 12 stabilization debrief presentation v0.13.27

## Contract status

Complete for the current deterministic CLI/host/shared-renderer debrief
contract only. Browser-native stabilization presentation, quality,
instructor-surface decisions, human review, and educational usability remain
separately gated.

## Source and visible behavior

- The ledger binds the stabilization CLI's tradeoff, rationale, attributed
  effect, reflection, decision/outcome, revision, and existing instructor
  appendix sections to committed history/replay sources.
- Host campaign/end-session envelopes supply debrief lines only after
  completion; shared browser renderers display supplied text, while the live
  GUI launcher remains competitive-regional-v1 only.

## Fallback, authority, and provenance

Debrief text, history, hashes, source-linked effects, and controls remain
complete without audio or motion. The existing CLI instructor appendix is
recorded as a boundary, not a new true-state view, route, or authority path.

## Verification and limits

`tests/test_phase12_stabilization_debrief_presentation.py` checks source
markers, section identity, completion gating, written fallback, live GUI scope,
and the instructor/true-state boundary. Browser-native stabilization quality,
instructor-surface decisions, replay/debrief expansion, human, and educational
gates remain open.

# Presentation Contract — Phase 12 stabilization accessibility evidence v0.13.28

## Contract status

Complete for current shared technical accessibility-contract evidence only.
Browser-native stabilization integration, contrast/screen-reader/device
certification, lived accessibility, human review, and educational usability
remain separately gated.

## Source and visible behavior

- The ledger joins existing keyboard/focus, text/non-color status, text-scale,
  reduced-motion, written-equivalent, optional-audio fallback, and semantic
  campaign coverage checks.
- The stabilization CLI remains text-first and the live GUI launcher remains
  competitive-regional-v1 only; no browser-native stabilization flow is
  certified.

## Fallback, authority, and provenance

Text scale, reduced motion, and written-equivalent preferences remain local
presentation state and do not enter commands, transitions, randomness, history,
hashes, or debrief output. Written meaning remains available when audio or
motion is unavailable.

## Verification and limits

`tests/test_phase12_stabilization_accessibility_evidence.py` checks source
markers, six passing technical entries, local-settings ownership, the
text-first/competitive-only boundary, and human-accessibility limits. Human
accessibility, assistive technology, device, fatigue, and educational gates
remain open.

# Presentation Contract — Phase 12 stabilization provenance audit v0.13.29

## Contract status

Complete for current technical stabilization provenance evidence only. Future
asset/legal provenance, portrait review, human quality, educational, and
public-release review remain separately gated.

## Source and visible behavior

- The ledger joins current repository-authored/project-generated visual and
  audio catalogs, reusable facility fallback, registry/release/credits checks,
  the no-new-asset decision, and the unreleased portrait-preview boundary.
- Runtime-generated audio has no file-backed release path; written equivalents
  and optional mapping remain explicit.

## Fallback, authority, and provenance

No new asset, registry entry, route, runtime field, or authority path changes.
Machine provenance fields and generated credits establish a technical release
boundary only; they do not establish legal clearance, training-data provenance,
output quality, or human approval.

## Verification and limits

`tests/test_phase12_stabilization_provenance_audit.py` checks source markers,
six passing audit entries, catalog/release scope, zero third-party release
count, no-new-asset decision, and unreleased preview limits. Future assets,
portraits, legal, human-quality, and public-release gates remain open.

# Presentation Contract — Phase 12 regional-affiliation partner identity v0.13.30

## Contract status

Complete for current host-reported partner identity and shared fallback only.
Browser-native regional-affiliation presentation, partner-specific visual/audio
treatment, and human identity, quality, accessibility, legal, educational, and
public-release review remain separately gated.

## Source and visible behavior

- The ledger binds partner name, reported condition, stage, and status to the
  current host campaign-coverage projection and preserves written uncertainty.
- The shared renderer may display supplied partner identity and coverage fields
  with a written fallback; the actor-family catalog separately retains the
  generic-actor marker, neutral frame, and written-notification equivalent.
- The `affiliation-partner-executive` portrait is identity decoration only and
  remains an unverified/unreleased preview.

## Fallback, authority, and provenance

The live GUI launcher remains competitive-regional-v1 only; no browser-native
regional-affiliation route is claimed. No new asset is required by the current
stage contract, and no partner-specific audio identity, runtime authority path,
private intent, true condition, or future commitment is exposed.

## Verification and limits

`tests/test_phase12_regional_affiliation_partner_identity.py` checks source
markers, host fields, fallback, portrait status, shared/live GUI boundaries,
and the no-new-asset decision. Partner-specific visual/audio integration and
human review remain open.

# Presentation Contract — Phase 12 regional-affiliation negotiation-stage visualization v0.13.31

## Contract status

Complete for current `NegotiateCommitments` presentation evidence only.
Browser-native affiliation integration, stage-specific art/audio,
commitment/review/integration completion, and human quality, accessibility,
legal, educational, and public-release review remain separately gated.

## Source and visible behavior

- The ledger binds the typed stage, active institutional-stage process, and
  host-owned `set-commitments` decision with community, workforce, and
  continuity fields and written uncertainty.
- The shared renderer can display supplied process and decision fields and
  preserves canonical-command submission through the host boundary.
- Visible commitment values and reported partner/stakeholder signals remain
  host-projected; hidden intent, thresholds, review state, and true responses
  are not presented.

## Fallback, authority, and provenance

Written stage, process, parameter, uncertainty, validation, and status text
remains complete. The reusable `affiliation_negotiation` music state is
optional and visible-trigger based. The live GUI remains competitive-regional-
v1 only; no new asset, route, runtime authority path, or registry entry is
introduced.

## Verification and limits

`tests/test_phase12_regional_affiliation_negotiation_stage.py` checks source
markers, stage/process identity, commitment fields, renderer and canonical
command boundaries, live scope, optional audio, and the no-new-asset decision.
Stage-specific art/audio, replay/debrief, and human review remain open.

# Presentation Contract — Phase 12 regional-affiliation commitment and review states v0.13.32

## Contract status

Complete for current host-projected commitment/review evidence only.
Browser-native affiliation integration, state-specific art/audio,
integration-state visualization, replay/debrief updates, and human quality,
accessibility, legal, educational, and public-release review remain separately
gated.

## Source and visible behavior

- The ledger binds community, workforce, and continuity commitment metrics and
  reported partner response statuses to the pending `institutional-review`
  process and `submit-review`/`await-review` decisions.
- Reported review response/status values remain host-resolved observations with
  written timing and outcome uncertainty; they are not legal or predictive
  claims.
- Shared process/decision renderers preserve supplied fields and canonical host
  submission while written labels, values, status, and uncertainty remain
  complete.

## Fallback, authority, and provenance

The reusable `affiliation_negotiation` music state remains optional and
visible-trigger based. The live GUI remains competitive-regional-v1 only; no
browser-native review route, new asset, runtime authority path, hidden review
deliberation, or registry entry is introduced.

## Verification and limits

`tests/test_phase12_regional_affiliation_commitment_review.py` checks source
markers, commitment/review fields and statuses, renderers, canonical-command
and written-fallback boundaries, live scope, optional audio, and the no-new-
asset decision. State-specific art/audio, integration, replay/debrief, and
human review remain open.

# Presentation Contract — Phase 12 regional-affiliation integration-state visualization v0.13.33

## Contract status

Complete for current host-projected integration-state evidence only.
Browser-native integration, state-specific art/audio, stage transitions,
replay/debrief updates, persistence, and human quality, accessibility, legal,
educational, and public-release review remain separately gated.

## Source and visible behavior

- The ledger binds the `IntegrateOrDecline` stage, visible
  `integration-obligation` process, begin/decline decision, and
  `Integrated`/`IntegrationDeclined` statuses.
- Host-projected status, metrics, events, effects, commitments, stakeholder
  responses, written consequence text, and uncertainty remain visible; resolved
  integration drag and continuity shock remain outside actor observation.
- Shared process/decision renderers preserve supplied fields and canonical host
  submission with complete written equivalents.

## Fallback, authority, and provenance

The reusable `affiliation_negotiation` music state remains optional and
visible-trigger based. The live GUI remains competitive-regional-v1 only; no
browser-native integration route, new asset, runtime authority path, hidden
input, or registry entry is introduced.

## Verification and limits

`tests/test_phase12_regional_affiliation_integration_state.py` checks source
markers, stage/process/decision identity, outcomes, hidden-input exclusions,
renderers, canonical-command and written-fallback boundaries, live scope,
optional audio, and the no-new-asset decision. State-specific art/audio,
transitions, replay/debrief, persistence, and human review remain open.

# Presentation Contract — Phase 12 regional-affiliation audio motif v0.13.34

## Contract status

Complete for the current reusable affiliation-audio motif evidence only.
Direct browser-native campaign audio integration, new/stage-specific audio,
human listening/quality/accessibility/legal/educational review, and public
release remain separately gated.

## Source and visible behavior

- The ledger binds the existing `affiliation_negotiation` music state and
  `event.affiliation-milestone` cue to explicit visible affiliation,
  partner, coalition, negotiation, commitment, and committed milestone text.
- Generated loop/cue properties and shared audio routing are recorded without
  adding an audio file, release path, or direct campaign route.
- Audio remains optional and cannot imply agreement, severity, success, private
  intent, or future outcome.

## Fallback, authority, and provenance

Written headings, statuses, sources, results, stage markers, and notifications
remain complete when audio is unavailable, muted, reduced, or unsupported.
The live GUI remains competitive-regional-v1 only; no runtime authority,
registry, or new asset boundary changes.

## Verification and limits

`tests/test_phase12_regional_affiliation_audio_motif.py` checks source markers,
IDs/properties, visible routing, written/audio-off fallback, live scope, and
the no-new-asset boundary. Direct campaign audio integration and human
listening/quality review remain open.

# Presentation Contract — Phase 12 regional-affiliation stage-transition sequence v0.13.35

## Contract status

Complete for current host-projected deterministic stage-sequence evidence only.
Browser-native affiliation sequencing, stage-specific presentation,
persistence, instructor views, and human visual/audio/accessibility/
educational/legal/public-release review remain separately gated.

## Source and visible behavior

- The ledger binds the typed six-stage successor chain and terminal completion
  to host command validation, one-transition advancement, visible labels, and
  the `affiliation-stage` process.
- Each committed step retains the command/result, source, status, effects,
  uncertainty, and aligned history/replay metadata; resolved stochastic inputs,
  private rationale, and future outcomes remain outside the actor view.
- The existing browser resolution sequence is explicitly competitive-first-
  month only and is not promoted as affiliation coverage.

## Fallback, authority, and provenance

Written stage labels, process status, command/result, source, uncertainty, and
committed history remain complete without animation or audio. The host owns
validation, stochastic resolution, state hashing, and replay; the presentation
surface remains read-only. No new asset, route, runtime authority path, or
registry entry is introduced.

## Verification and limits

`tests/test_phase12_regional_affiliation_stage_transition_sequence.py` checks
source markers, exact order/successors, command/uncertainty coverage,
history/replay and read-only boundaries, shared-sequence scope, optional audio,
live scope, and the no-new-asset decision. Browser sequencing and human review
remain open.

# Presentation Contract — Phase 12 regional-affiliation replay/debrief views v0.13.36

## Contract status

Complete for current technical replay/debrief evidence only. Browser-native
affiliation replay/debrief views, durable persistence/playback,
instructor/true-state distinction, human visual/audio/accessibility/
educational/legal review, and public release remain separately gated.

## Source and visible behavior

- The ledger binds the versioned replay artifact, serializer, ruleset and
  state/observation/hash verification, host history/replay envelopes, and
  terminal affiliation debrief.
- The debrief records stage count, final status, outcomes, commitments,
  decision quality under reported observations, social-welfare distinction,
  alternatives, and per-stage response detail as existing host/CLI text.
- Shared campaign renderers preserve committed history, state hashes, debrief
  lines, source/uncertainty text, and completion fallback without visual
  decoration or new authority.

## Fallback, authority, and provenance

The host owns replay serialization/verification, state hashes, history, and
debrief construction; presentation remains read-only. Post-resolution detail
stays within existing typed replay/CLI terminal-debrief contracts and is not a
live browser actor-view claim. No new asset, route, runtime authority path, or
registry entry is introduced.

## Verification and limits

`tests/test_phase12_regional_affiliation_replay_debrief.py` checks source
markers, replay fields/integrity, debrief content, written history/debrief
renderers, optional audio, live scope, resolved-detail boundaries, and the
no-new-asset decision. Browser views, persistence, and human review remain
open.

## Technical Attribution Boundary Addendum — v0.13.52

The current canonical visual/audio registries, generated static credits and
third-party notices, runtime credits projection, and release manifest are
joined by a focused technical attribution ledger/test. Every current registry
entry retains source/generation attribution, legal-basis reference, accessible
equivalent, approval status, and hash fields; release entries remain manifest-
bound. Unverified portrait previews remain outside registry, release, and
runtime attribution surfaces.

This addendum records a provenance projection boundary only. It does not
authorize portrait promotion or establish legal, ownership, training-data,
resemblance, accessibility, educational, or public-release approval. Portrait
AI-generation metadata remains open because the current preview tool did not
expose approved model and seed data.

# Presentation Contract — Phase 12 regional-affiliation provenance audit v0.13.37

## Contract status

Complete for current machine-checkable technical provenance evidence only.
Direct partner/stage assets, recorded audio, legal/training-data review,
human visual/audio/accessibility/educational quality, and public release remain
separately gated.

## Source and visible behavior

- The ledger binds reusable visual/audio/fallback catalogs, registry policy,
  generated credits, portrait review queue, and passing registry/security/
  release/generation/credits/reuse/asset-need/audio-packaging checks.
- The current regional-affiliation asset-need decision remains
  `none-required-by-current-stage-contract`; generic fallback and written
  equivalents remain available without promoting partner/stage assets.
- Runtime-generated audio has no file-backed release path, and unreleased
  portrait previews remain outside the release surface.

## Fallback, authority, and provenance

Catalog and registry evidence is technical and read-only; it does not grant
asset authority, direct campaign mapping, legal clearance, training-data
provenance, human approval, or public-release status. No new asset, route,
runtime authority path, or registry entry is introduced.

## Verification and limits

`tests/test_phase12_regional_affiliation_provenance_audit.py` checks source
markers, all audit statuses/coverage, release counts, portrait gates, and
legal/training-data/human/public-release limits. Direct assets, recorded audio,
and human review remain open.

# Presentation Contract — Phase 12.3 instructor-only authority boundaries v0.13.38

## Contract status

Complete for current authority-boundary documentation only. True-state visual
language, instructor-surface design, decision-time recovery, causal,
counterfactual, distributional, export, human educational, and public-release
work remain separately gated.

## Source and visible behavior

- The ledger distinguishes existing stabilization CLI appendix, competitive
  instructor summary, and regional-affiliation typed/CLI post-run detail from
  player-visible observations.
- Host/core debrief functions own post-run detail; shared renderers display
  supplied text, history, hashes, and notices without authoring outcomes.
- No regional-affiliation instructor route or browser true-state surface is
  implemented or claimed; resolved inputs remain outside live controls.

## Fallback, authority, and provenance

Written observation labels, source attribution, committed history, hashes,
debrief text, and authority notices remain readable without audio or visual
decoration. The host remains authoritative and presentation remains read-only;
no new asset, route, runtime field, or registry entry is introduced.

## Verification and limits

`tests/test_phase12_instructor_authority_boundaries.py` checks source markers,
all three campaign boundaries, written fallback, live scope, and no-authority/
no-true-state/counterfactual/human-review limits. Instructor design and human
educational review remain open.

# Presentation Contract — Phase 12.3 true-state language boundary v0.13.39

## Contract status

Complete for current textual language-boundary evidence only. Browser-native
true-state visual design, decision-time recovery, causal, counterfactual,
distributional, export, instructor-surface, accessibility, human educational,
and public-release work remain separately gated.

## Source and visible behavior

- The ledger binds explicit `Observed`, `True Prior`, `True Outcome`, and
  instructor-reveal labels in the existing debrief report, plus the separate
  decision-quality/outcome-quality statement.
- Host/core functions own labels and post-run detail; shared renderers display
  supplied text without authoring state, outcomes, or authority.
- The live GUI remains `competitive-regional-v1` only, and no browser-native
  true-state route or control is implemented or claimed.

## Fallback, authority, and provenance

Text labels, committed history, hashes, debrief text, and authority notices
remain readable without audio or visual decoration. The true-state distinction
is a current textual contract, not a visual-quality or educational result.

## Verification and limits

`tests/test_phase12_true_state_language_boundary.py` checks source markers,
language labels, written fallback, live scope, and no-expansion limits. Visual
language, export, causal/counterfactual/distributional views, and human review
remain open.

# Presentation Contract — Phase 12.3 decision-time recovery boundary v0.13.40

## Contract status

Complete for current technical recovery-boundary evidence only. Full browser
per-decision observation playback, causal, counterfactual, distributional,
export, instructor-surface, accessibility, human educational, and public-
release work remain separately gated.

## Source and visible behavior

- The ledger binds immutable core observation/command retention, debrief
  before-command and revision language, host history/replay summaries, and
  text-first turn/command/hash rendering.
- Core/host functions own recovery and hash alignment; shared renderers display
  supplied summaries without authoring observations, outcomes, or authority.
- The live GUI remains `competitive-regional-v1` only; it does not claim a
  browser-native full decision-time observation timeline.

## Fallback, authority, and provenance

Commands, history, hashes, source/status text, and debrief lines remain
readable without audio or visual decoration. Host summaries remain narrower
than core history and do not expose resolved inputs or private rationale.

## Verification and limits

`tests/test_phase12_decision_time_recovery_boundary.py` checks source markers,
recovery contracts, the narrower host/browser boundary, written fallback, and
no-expansion limits. Full browser recovery and human review remain open.

# Presentation Contract — Phase 12.3 counterfactual difference view v0.13.42

## Goal and Authorization

This slice closes the current “Counterfactual differences visualized” item as
a deterministic, text-first, post-run comparison of existing stabilization
histories. The existing preset CLI demo displays the selected preset against a
deterministic alternative. It is not a browser or instructor authority
surface.

## Source Ledger and Semantics

- Commands come from committed `Transition.command` values.
- State differences come from committed `Transition.next` values.
- Effect differences come from committed `AttributedEffect` values.
- Resolved-input equality is reported without printing resolved-input values.
- Same genesis is required; mismatches receive a written fallback.

The output uses stable baseline/alternative/unchanged/different labels. It does
not infer intent, severity, future outcomes, causal graphs, or strategy value.

## Accessibility, Authority, and Provenance

The view is fully text-first and requires no color, motion, audio, asset, or
browser capability. It reads immutable histories without mutating commands,
transitions, hashes, replay artifacts, or debrief state. No new asset or audio
provenance record is needed.

## Verification and Open Questions

Focused Rust tests cover equal histories, changed command/state/effect values,
unequal inputs, and incompatible genesis. A source-linked Python ledger test
checks the boundary. Causal validity, distributional outcomes, export behavior,
browser instructor presentation, and human educational review remain open.

# Presentation Contract — Phase 12.3 causal attribution boundary v0.13.41

## Contract status

Complete for current host-sourced direct-attribution evidence only. Inferred
causal graphs, causal certainty, counterfactual, distributional, export,
instructor-surface, accessibility, human educational, and public-release work
remain separately gated.

## Source and visible behavior

- The ledger binds typed `ResolutionEffect` source/metric/delta/text fields,
  ordered direct-effect resolution stages, descriptive debrief attribution,
  and source-linked consequence rendering.
- Host/core resolution owns effect source, magnitude, text, and ordering;
  shared renderers display supplied evidence without calculating new outcomes.
- The live GUI remains `competitive-regional-v1` only; direct attribution is a
  descriptive source-linked layer, not a browser causal model.

## Fallback, authority, and provenance

Effect text, source labels, before/after values, hashes, consequence text, and
debrief lines remain readable without audio or decorative motion. Before/after
comparison does not authorize causal certainty or future-outcome inference.

## Verification and limits

`tests/test_phase12_causal_attribution_boundary.py` checks source markers,
attribution contracts, read-only/live scope, written fallback, and no-inference
limits. Broader causal design and human review remain open.

# Presentation Contract — Phase 12.3 distributional outcome summary v0.13.43

## Goal and Authorization

This slice addresses “Distributional outcomes represented responsibly” using
the existing post-run competitive instructor-summary renderer. It adds no new
authority path and does not promote the summary into the player observation.

## Source Ledger and Semantics

| Element | Source | Meaning | Prohibited inference |
| --- | --- | --- | --- |
| System identity | committed `CompetitiveWorldState.systems` | stable system label | ownership beyond host label |
| Outcome change | genesis and final committed system fields | per-system descriptive delta | welfare, rank, or causal value |
| Visibility | existing instructor-summary boundary | post-run review context | live rival knowledge |

The renderer reports access, quality, workforce trust, community trust, and
market share changes independently. It does not sum, normalize, rank, or label
one metric as the objective.

## Accessibility, Authority, and Provenance

The view is text-first, with no color, motion, audio, or asset requirement. It
reads committed history snapshots and does not change commands, transitions,
hashes, replay, or observation DTOs. No new asset provenance is required.

## Verification and Open Questions

Focused Rust tests cover multiple systems, metric deltas, deterministic order,
and no-transition fallback. A source-linked Python ledger test checks the
instructor boundary and no-ranking language. Human educational interpretation,
policy validity, and distributional fairness review remain open.
## Export Boundary Addendum — v0.13.44

The current export contract is documentation-only in this slice. Stabilization
uses the versioned `replay-artifact-0.1.15` writer; the separate
`verify_replay_artifact` function is available for validation but is not invoked
by the export command. Regional affiliation uses its versioned replay writer;
competitive CLI export currently writes the existing serialized competitive
history JSON. Empty export input skips writing. These outputs may serialize
commands, transitions, hashes, and resolved inputs, but they are post-run
analysis artifacts rather than browser state, mid-run saves, or new authority
paths.

## Player-Facing Settings and Help Addendum — v0.13.45

The existing GUI guide is the player-facing source for the settings panel,
optional audio controls, credits disclosure, and troubleshooting. It documents
reduced motion, optional cue explanations, Standard/Large text, browser-local
storage with session-local fallback, mute/cues-only/channel controls, and
written recovery paths. These controls remain presentation-only: they do not
enter host commands, validation, transitions, stochastic inputs, immutable
history, replay verification, or simulation authority.

The guide is written for a first-time local Chromium player and a facilitator
helping with a bounded session. It does not claim human accessibility,
educational usability, audio quality, classroom readiness, or public-release
approval.

## Pilot Preparation Addendum — v0.13.46

The existing structured-evaluation guide now carries a preparation-only pilot
contract: facilitator preflight, fictional seeded runs, loopback/local-host
assumptions, optional audio, existing reduced-motion/Large-text/written
equivalent controls, accommodation categories, and explicit screenshot/
recording consent. The feedback instrument stores only anonymized bounded
responses and keeps the human decision pending.

This preparation does not create classroom multiplayer, a runtime
low-distraction mode, a new observation or debrief route, participant data,
media storage, or host authority. It does not establish accessibility,
educational, audio-quality, legal, or public-release approval.

## Low-Distraction Mode Addendum — v0.13.47

The GUI now exposes a local **Low-distraction mode** toggle. When enabled, the
presentation layer forces reduced motion, Large text, written cue explanations,
muted audio, and reduced notifications; it temporarily locks conflicting
presentation/audio controls and restores their prior local values when disabled.
The mode preference uses the existing browser-local/session-local settings
boundary.

The mode does not enter commands, host validation, stochastic inputs,
transitions, immutable history, replay, host persistence, or simulation
authority. It is not a new host game mode and does not establish human
accessibility, educational usability, or classroom approval.

## Limitations Statement Addendum — v0.13.48

The GUI guide now places the fictional educational-simulation boundary beside
first-session instructions. It states that the game is not a calibrated policy
forecast or real-world operational, clinical, financial, regulatory, or legal
decision tool, while preserving actor-visible and host-authoritative limits.
Remaining human, provenance, browser/device, full-campaign, persistence, and
public-release gates remain explicit.

## Vertical-Slice Technical Evidence Addendum — v0.13.49

Current live host/browser contracts support the actor-visible regional board,
facility/report linkage, visible project overlays, first-month consequence
handoffs, and planning/pressure music states from visible inputs. The evidence
remains bounded to supported current conditions and does not expose hidden state
or claim full-campaign, provenance, first-time-user, or human-review completion.

## Hidden-State Boundary Addendum — v0.13.50

Current browser presentation modules and read-only DTO tests reject simulation
world, resolved-input, and effect-queue fields at the presentation boundary.
This is a technical source-checkout contract only; it does not approve content,
clinical implications, institutional resemblance, accessibility, educational
usability, or public release.

## Bounded Content Boundary Addendum — v0.13.51

The current player guide, README, metric visualization proof, semantic
container catalog, and browser modules were reviewed for unsupported clinical
implications and information-boundary drift. The source/content QA records
the fictional/non-forecast boundary, absence of diagnosis/prescribing/
treatment-plan/patient-specific/clinical-recommendation claims, text-first
precision rules, and host-authorized source/status semantics.

This contract closes only a current repository-owned wording and source-boundary
check. It does not authorize new assets, audio, browser routes, host fields,
simulation changes, or clinical/policy claims. Human domain, accessibility,
educational, provenance, resemblance, legal, and public-release review remain
open.

## Technical First-Session Boundary Addendum — v0.13.53

The current presentation contract now records the technical path from
host-bound launch/load through actor-visible inspection, contextual drafting and
validation, committed resolution review, continuation, and written recovery.
The seven-stage first-month rail remains source-bound and presentation-only;
browser-local draft/preferences state does not become session or simulation
authority.

This addendum does not establish first-time-user comprehension, human
accessibility, educational usability, classroom readiness, or broader campaign
coverage. No new route, asset, audio, persistence, or replay behavior is added.

## Technical Competitive Campaign Boundary Addendum — v0.13.54

The current presentation contract now records the technical
`competitive-regional-v1` campaign boundary: host-owned 24-month completion,
current actor-visible board/facility/overlay/event/music/history/replay/
checkpoint/debrief surfaces, host-owned resolution continuity, and written
fallbacks. The shared `campaign-coverage-v1` envelope remains limited to
stabilization and regional-affiliation. Presentation code remains a renderer of
supplied competitive projections; it does not own campaign transitions, history,
replay, checkpoint state, resolution, or debrief authority.

This addendum does not establish full-campaign facility placement/use coverage,
campaign-specific visual or audio quality, screenshot completeness,
cross-browser/device certification, human comprehension, educational value, or
expansion approval. No new route, asset, audio, persistence, or runtime
simulation behavior is added.

## Technical Debrief Visual Boundary Addendum — v0.13.55

The current presentation contract records the host-supplied terminal debrief
path: history/replay/hash alignment, written debrief lines, before/after
snapshots, direct committed effects, consequence links, read-only terminal
controls, and written fallbacks when audio or motion is unavailable. The browser
validates and renders supplied fields; it does not author outcomes, infer a
causal graph, or retain terminal mutation authority.

This addendum does not establish visual hierarchy or quality, human
comprehension, accessibility quality, educational effectiveness, classroom
readiness, causal certainty, or public-release approval. No new route, asset,
audio, persistence, replay regeneration, or runtime simulation behavior is
added.
# Presentation Contract — Direct campaign audio projection v0.13.60

## Contract status

Bounded technical host-to-browser audio contract for the existing
`campaign-coverage-v1` envelope. The projection is additive and optional.

## Actor-visible behavior

- Stabilization and regional-affiliation coverage may include an existing
  catalog `music_state_id` and a list of existing visible event-cue IDs.
- Music is applied on coverage load; event cues play only after a successful
  canonical host decision and refreshed envelope.
- An explicit empty cue list means no cue. An omitted audio projection uses the
  existing visible text classifier and affiliation fallback for older envelopes.

## Authority and fallback

- The Rust host derives metadata from visible campaign presentation fields and
  committed visible transition summaries; it does not expose private rationale,
  resolved inputs, true state, or future outcomes.
- The browser validates/uses catalog vocabulary only for presentation. Audio
  never changes commands, transitions, history, hashes, or debrief facts.
- Mute, unavailable audio, reduced notifications, malformed IDs, and missing
  metadata retain written stage, decision, consequence, and debrief content.

## Non-goals and evidence limits

No new audio asset, catalog entry, route, schema version, simulation behavior,
audio-quality claim, human listening result, accessibility approval, educational
result, legal clearance, or public-release approval is claimed.

---

# Presentation Contract — Campaign-aware first-month rail v0.13.59

## Contract status

Bounded technical presentation contract for the first-session rail only. The
competitive rail remains `competitive-first-month-v1`; the two existing
campaign-coverage campaigns use `campaign-coverage-first-session-v1`.

## Actor-visible behavior

- Competitive sessions retain Start/load → inspect → draft → validate → submit
  → resolution → continue.
- Stabilization and regional-affiliation sessions show Start/load → inspect
  coverage → choose a host decision → review the committed stage → continue.
- Campaign-coverage text remains sourced from the existing typed host envelope;
  the rail labels presentation handoffs and never claims a strategy or outcome.
- A rejected campaign decision leaves the current stage and visible envelope
  recoverable. A successful decision advances only after the existing coverage
  refresh succeeds.

## Authority and fallback

- `first-month.mjs` owns only local stage labels, state, and semantic markup.
- `app.mjs` updates campaign stages from successful adapter reads/writes;
  `adapter.submitTurn(command)` remains the only mutation path.
- Missing, malformed, or failed coverage preserves the current valid surface
  and shows a written recovery message.
- No true state, resolved input, private rationale, effect queue, forecast, or
  client-side legality is introduced.

## Non-goals and evidence limits

No new host schema, simulation transition, asset, audio file, persistence,
screenshot, browser certification, human accessibility review, educational
usability result, or public-release approval is claimed.

---

# Presentation Contract — Live campaign-coverage handoff v0.13.58

## Goal and authorization

Expose the existing host-owned `campaign-coverage-v1` envelope through the
loopback GUI for stabilization and regional-affiliation sessions. Reuse the
existing text-first campaign panel and canonical host decision route. This is
an integration slice, not a new campaign presentation system.

## Player questions and visible consequences

The browser should answer: “What campaign stage, actor-visible metrics,
processes, decisions, committed history, and debrief are currently available?”
A selected decision is submitted as the host-provided canonical command and
the next panel is fetched from the host. A failed read or submit preserves the
current view and reports a recoverable error.

## Source and visibility contract

| Surface | Source | Allowed browser behavior | Prohibited inference |
| --- | --- | --- | --- |
| Campaign launch | `GameSessionStore::start_session` | Send campaign, seed, and competitive difficulty when relevant | Do not create a local session or outcome |
| Existing-session identity | Host session-envelope read | Resolve the campaign before selecting the competitive or campaign-coverage renderer | Do not infer campaign identity from a stale browser value |
| Stage/metrics/actors/processes | `get_campaign_coverage` | Render the typed envelope and source labels | Do not reconstruct true state, intent, probability, or future response |
| Decisions | Envelope `command_template` and parameters | Fill visible fields and submit the resulting canonical command | Do not invent commands or validate locally as authoritative |
| History/debrief/replay metadata | Same host envelope | Render committed summaries and hashes | Do not regenerate transitions or debrief facts |
| Session end | Existing `end_session` route | Show the host terminal envelope | Do not mark a session complete locally |

## Visual, motion, and audio semantics

The existing campaign-coverage panel, text/status language, optional audio
classifier, and written equivalents are reused. No new cue, music state, asset,
motion effect, or color-only signal is introduced. Stabilization and affiliation
remain distinguishable through host-provided campaign role/stage text and
source-linked fields.

## Accessibility and recovery

Keyboard forms, text equivalents, reduced-motion behavior, optional audio, and
existing recovery controls remain the fallback. Missing or malformed campaign
coverage must not erase a successfully rendered prior session. Adapter and
host failures remain visible as recoverable status messages.

## Authority, history, and provenance boundary

The Rust host remains authoritative for campaign creation, command acceptance,
transition resolution, history, hashes, and debrief. The browser stores only
the active session ID, campaign selection, and presentation/draft UI state.
No asset or release registry entry changes in this slice.

## Evidence limits and non-goals

This contract does not establish campaign-specific art/audio quality,
human comprehension, accessibility, educational usefulness, screenshots,
durable persistence, replay playback, legal/provenance approval, or public
release. No new visual/audio asset or hidden-state route is authorized.

--- Historical presentation contracts ---

# Presentation Contract — Phase 13.1 AI-generation metadata boundary v0.13.57
# Presentation Contract — Browser-refresh session continuity v0.13.62

## Goal and Authorization

Let a player return to a still-running local host session after refreshing the
browser. The browser may retain only the opaque host-issued session ID as
presentation state, then request the existing actor-visible envelope again.

## Player Questions and Consequences

The player question is: “Can I resume the session I was viewing after the page
reloads?” A valid host response restores the same visible campaign/action
surface; an unavailable session produces written recovery guidance and does
not invent a replacement outcome.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Timing/missingness | Prohibited inference |
| --- | --- | --- | --- |
| Active session identity | Host-issued `session_id` from start/load/read responses | Optional best-effort browser storage; absent storage means manual load | Do not store or derive true state, command, outcome, observation, hash, or intent |
| Recovery result | Existing host `getSession`/presentation/campaign-coverage/action reads | Valid host response, unknown session, or adapter failure | Do not infer a new session or local outcome from failure |
| Terminal cleanup | Successful host `end_session` response | Clear only after confirmed end; retain on failure | Do not mark a session ended locally |
| Written fallback | Existing launcher status/recovery messages and current valid view | Always available without storage or audio | Do not make storage required for play |

## Visual, Motion, and Audio Semantics

No new semantic visual, motion, or audio signal is introduced. The existing
session launcher status is the written recovery surface. Current rendered
history, observations, commands, results, mute behavior, and reduced-motion
behavior remain unchanged.

## Accessibility and Fallbacks

Storage read/write/clear failures are swallowed as optional-capability failures.
The existing session-ID field remains keyboard-visible, and a player can load a
session manually. Unknown IDs are cleared with written guidance; transient
errors retain the ID for retry. No color, motion, sound, or storage is required
to understand or continue the session.

## Authority, History, and Replay Boundaries

The browser stores one opaque ID only. Recovery calls the existing host reads;
the browser does not serialize or recreate simulation state, submit commands,
mutate history, recalculate hashes, regenerate replay, or change authority.
Cross-process and durable file recovery remain outside this contract.

## Asset Provenance and Release Requirements

No asset, registry, release path, audio file, or provenance record is added.

## Verification and Evidence Limits

Focused source/Node/Python checks must cover optional storage, successful and
failed recovery, stale cleanup, end cleanup, written fallback, and forbidden
authority fields. These checks do not establish human usability, accessibility,
device/browser certification, durable persistence, or educational benefit.

## Non-Goals and Open Questions

- No durable file persistence, cross-process store, browser serialization,
  service worker/cache, replay playback/regeneration, new host route/schema,
  simulation change, asset, audio change, or human review is included.
- Open: durable file/cross-process recovery and full-campaign continuity require
  a separately designed host persistence slice.
