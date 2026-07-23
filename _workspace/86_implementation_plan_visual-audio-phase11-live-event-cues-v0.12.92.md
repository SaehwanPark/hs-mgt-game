# Phase 11.1 Live Event-Cue Binding — Implementation Plan v0.12.92

## Task restatement

Advance the bounded Phase 11.1 event-cue item by making live competitive
resolution event-cue selection an explicit host-shaped projection from the
committed transition summary and actor-visible before/after snapshots.

## Current understanding

- `ResolutionEnvelope` already carries host-owned visible steps, effects, and
  before/after observations, while `gui/audio.mjs` has an approved cue catalog.
- The browser currently calls `visibleEventCues`, which classifies visible
  resolution text and reported operating values locally with regular
  expressions.
- The browser must not infer hidden intent, severity, or outcome from a cue;
  explicit host cue IDs can preserve the same visible-only boundary and make
  the event-cue source inspectable.
- The smallest useful slice is an additive `audio_cue_ids` array on the live
  resolution envelope. It is derived only from `TransitionSummary.events`/
  `effects` and `ReadOnlyObservation` before/after values; the existing browser
  classifier remains a compatibility fallback for older recorded envelopes.

## Assumptions

- Stable cue IDs are presentation vocabulary and may be emitted by the host
  without entering simulation state, transition evaluation, stochastic input,
  history hashes, or debrief facts.
- The existing cue catalog IDs remain public and stable; unknown IDs are passed
  through to the audio client, which already records an unavailable/fallback
  result without making audio authoritative.
- Visible text and reported operating values are sufficient for the currently
  supported event categories: project completion, staffing constraint,
  operating loss/recovery, payer decision, regulatory decision, public rival
  expansion, and affiliation milestone.
- Full campaign event taxonomy and human audio usefulness remain separate
  roadmap gates.

## Minimal implementation plan

1. Add deterministic host-side cue selection to `src/mcp/resolution.rs` using
   only committed transition summaries and actor-visible before/after DTO
   values; include the IDs in `ResolutionEnvelope`.
2. Update the live resolution client to prefer the explicit host cue list and
   retain `visibleEventCues` only when a legacy envelope omits the additive
   field. Keep audio optional and written resolution text complete.
3. Add Rust and Node/Python tests covering every currently supported event cue,
   absent conditions, deterministic ordering, malformed/unknown IDs, legacy
   fallback, and forbidden hidden-state/network markers.
4. Update the roadmap evidence, coverage ledger, README/GUI README, SPEC,
   ARCHITECTURE, CHANGELOG, version projections, lessons, request/contract/QA/
   handoff artifacts, and registry/hash projections.

## Files and functions likely to change

- `src/mcp/resolution.rs`: envelope field, visible cue projection, and tests.
- `gui/app.mjs`: explicit host cue preference in resolution submission flow.
- `tests/test_phase11_live_event_cues.py`, `tests/test_gui_resolution.py`, and
  existing resolution/audio tests: focused contract evidence.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: bounded live
  event-cue continuity surface and limits.
- `assets/registry/visual-assets.json`, generated credits, and release
  projections: changed registered presentation sources where applicable.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`,
  `ARCHITECTURE.md`, `LESSONS.md`, and the roadmap: project records.
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, and `_workspace/final/handoff.md`:
  durable handoffs.

## Tests and checks

- `python3 -m unittest tests/test_phase11_live_event_cues.py tests/test_gui_resolution.py tests/test_gui_audio.py`
- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- `python3 scripts/generate_asset_credits.py --check`
- `python3 scripts/audit_visual_audio_contract.py`
- JavaScript syntax checks for changed modules.

Expected result: the live host returns deterministic explicit cue IDs for
currently supported visible event conditions, the browser plays only those
host-provided IDs for current envelopes, legacy fixtures remain readable, and
all written/reduced-audio fallbacks remain complete.

## Acceptance criteria

- `ResolutionEnvelope.audio_cue_ids` is deterministic, deduplicated, ordered,
  and derived only from visible committed summaries and snapshots.
- Each supported cue ID has an existing catalog contract and written
  equivalent; no cue is emitted from private rival intent or true state.
- The browser prefers the explicit field, uses the existing classifier only for
  envelopes that omit it, and does not create a second transition path.
- Replaying the same resolution envelope yields the same cue sequence; omitted
  or unknown IDs remain safe and text-complete.
- The roadmap records only bounded current live resolution event-cue evidence;
  full campaign event coverage, screenshots, performance, compatibility,
  audio usefulness, and human gates remain open.

## Non-goals

- Do not add recorded audio, new assets, dependencies, music-state changes,
  screenshots, save/load, or a new simulation mechanism.
- Do not infer private intent, event severity, causality, probability, or future
  outcomes from visible cue IDs or textual matches.
- Do not mark broad Phase 11.1 event-cue or full-campaign coverage complete.

## Stop conditions

- Stop if a cue requires true state, hidden rival action, or unresolved event
  taxonomy rather than the visible transition summary/snapshots.
- Stop if the field changes state hashes, history, command validation, or
  deterministic transition evaluation.
- Stop if legacy envelopes would lose written output or if the change broadens
  into music, screenshot, or performance work.

## Review checklist

- Every emitted ID traces to a visible source and existing cue contract.
- Host ordering is deterministic and cue selection is presentation-only.
- Legacy fallback is retained without overriding an explicit empty host list.
- Unknown/missing audio remains text-complete and optional.
- One code-reviewer skill performs the required review passes; findings are
  fixed before merge.

## Risk label

Risk: medium

Reason: this adds an additive host presentation field and changes live cue
selection, but does not alter simulation authority, history, replay hashes, or
audio assets.
