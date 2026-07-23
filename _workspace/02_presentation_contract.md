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
