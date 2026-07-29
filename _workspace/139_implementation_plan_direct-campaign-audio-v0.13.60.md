# Implementation Plan — Direct campaign audio projection v0.13.60

## Task restatement

Add host-sourced, actor-visible audio metadata to the existing
`campaign-coverage-v1` envelope for stabilization and regional affiliation, and
make the live browser honor it while preserving legacy text classification and
written/audio-off fallbacks.

## Current understanding

- `src/mcp/campaign_coverage.rs` owns the typed campaign-coverage envelope but
  currently emits no explicit music or event-cue metadata.
- `gui/app.mjs` derives campaign audio from visible briefing/actor/process text
  through `campaignAudioInput`; its submit path has a legacy hard-coded
  affiliation cue fallback.
- Existing `music-stem-contract.mjs` and `audio.mjs` already provide the
  allowlisted music/cue vocabulary, written equivalents, mute behavior, and
  unknown-content fallback.
- The Phase 12 stabilization and regional-affiliation audio ledgers explicitly
  leave direct campaign-envelope audio integration open.
- The existing typed `campaign-coverage-v1` route is the correct host boundary;
  an additive optional field preserves older browser fixtures and envelopes.

## Assumptions

- Campaign audio metadata can be derived deterministically from actor-visible
  stage/briefing/actor/process text and committed visible transition summaries;
  no hidden state or resolved input is needed.
- `music_state_id` and `audio_cue_ids` use only existing catalog IDs.
- An explicit empty host cue list means no cue; an omitted audio projection
  keeps the existing browser fallback behavior.
- Audio remains optional presentation metadata and is not stored in simulation
  history, hashes, or transition state.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Inspect the campaign-coverage constructors, transition-summary fields, and
   existing audio catalog allowlists; confirm there is no second campaign
   coverage envelope constructor.
2. Add a typed additive campaign-audio projection with host-selected music and
   event-cue IDs derived only from visible campaign text and committed visible
   history. Keep `campaign-coverage-v1` and all existing fields stable.
3. Update the browser campaign client to prefer explicit host music, play an
   explicit host cue list only after a successful host refresh, and use the
   existing affiliation/text fallback when the field is omitted.
4. Add Rust, Node, and Python contract tests for catalog allowlists, direct
   mapping, explicit-empty cues, legacy fallback, audio-off behavior, and the
   unchanged hidden-state/authority boundary.
5. Update both Phase 12 audio ledgers, the roadmap checklist/evidence, guides,
   spec/changelog/lessons, package version to `0.13.60`, generated metadata,
   and request/contract/QA/handoff records.
6. Run the full validation suite, perform exactly one medium-effort code review,
   fix directly relevant findings, and prepare the PR handoff.

## Files and functions likely to change

- `src/mcp/campaign_coverage.rs`: typed audio projection and deterministic
  visible-source mapping in both campaign constructors.
- `src/mcp/session.rs`: Rust projection assertions for audio metadata and
  hidden-state exclusion.
- `gui/app.mjs`: campaign audio input/ID helpers, host-metadata preference,
  post-refresh cue routing, and explicit-empty/legacy behavior.
- `tests/test_phase12_live_campaign_coverage.py`,
  `tests/test_gui_campaign_coverage.py`, and focused audio tests: contract and
  browser behavior.
- `docs/evaluation/phase12-live-campaign-coverage.json`,
  `docs/evaluation/phase12-stabilization-audio-state-mapping.json`,
  `docs/evaluation/phase12-regional-affiliation-audio-motif.json`, and their
  tests: evidence and open-work closure for the technical integration only.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, generated credits,
  device policy, release metadata, and `_workspace` current records.

Avoid editing files outside this list unless a generated check requires a
derived file. If a new route, schema version, asset, or authority path appears
necessary, stop and report before broadening scope.

## Tests and checks

- `cargo fmt --check`
- focused Rust campaign-coverage tests
- `python3 -m unittest tests.test_phase12_live_campaign_coverage tests.test_gui_campaign_coverage tests.test_phase12_stabilization_audio_state_mapping tests.test_phase12_regional_affiliation_audio_motif`
- Node syntax and direct/legacy/audio-off probes
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- release metadata, documentation links, asset registry/credits/release,
  security/generation, device-performance, offline, browser-compatibility,
  visual/audio contract, and `git diff --check` checks.

Expected results:

- Both campaigns emit only existing music/cue IDs from visible sources.
- An explicit empty cue list does not trigger a legacy cue; omitted metadata
  retains the old visible classifier/affiliation fallback.
- Audio-off or unavailable audio preserves the same written campaign content.
- No simulation transition, hash, history, true-state, or local authority
  changes.

## Acceptance criteria

- The typed campaign envelope exposes a documented additive audio projection for
  stabilization and regional affiliation without exposing forbidden fields.
- The browser honors host music state and post-refresh cue IDs, including an
  explicit empty cue list, while supporting older envelopes without audio.
- Rust/Python/Node evidence proves allowlist parity, deterministic mapping,
  audio-off fallback, and unchanged host authority.
- Phase 12 ledgers no longer mark direct technical campaign-envelope audio
  integration as open; campaign-specific quality and human listening review
  remain open.
- Full checks pass at v0.13.60.

## Non-goals

- Do not add recorded audio, a new catalog ID, asset, registry entry, route,
  schema version, simulation rule, transition, persistence, or true-state view.
- Do not infer severity, agreement, intent, probability, causality, or future
  outcome from audio metadata.
- Do not make audio required for play or remove written equivalents.
- Do not refactor the shared audio contracts or competitive resolution audio.
- Do not claim human listening, accessibility, educational, legal, or release
  approval.

## Stop conditions

Stop and report if:

- the additive field cannot remain optional for existing fixtures;
- any mapping requires private state, resolved inputs, or a new transition;
- more than two production modules beyond the named host/browser files require
  changes;
- a new audio asset/catalog ID or schema version becomes necessary;
- unrelated test failures cannot be isolated from this slice.

## Review checklist

- Verify every host ID is present in the existing music/cue catalog.
- Verify direct mapping reads only visible stage/briefing/actor/process/history
  summary text and does not enter history/hash/simulation state.
- Verify explicit empty cues differ from omitted legacy metadata.
- Verify rejected submissions and failed refreshes do not play host cues.
- Verify audio-off, unavailable, reduced, and written-equivalent behavior.
- Verify competitive resolution audio and action flow remain unchanged.
- Verify the diff matches this plan and records deviations and unresolved risks.

## Risk label

Risk: medium

Reason: this changes a typed host projection and browser audio routing across
two campaigns, while preserving the existing schema, catalog, and authority
boundaries.

## Execution record

- Host projection, browser routing, current evaluation ledgers, roadmap/spec,
  guides, lessons, generated release records, and v0.13.60 metadata were
  implemented within the planned file boundary.
- Full validation passed: 344 Rust tests, 763 Python tests, focused campaign/
  audio tests, Clippy, formatting, release/asset/documentation/device/offline/
  browser/visual-audio checks.
- The sole medium-effort review found one High compatibility issue (required
  audio field) and one Low record-state issue. The field is now optional with
  `Some(...)` emitted by current constructors, a legacy deserialization test
  was added, and the QA/handoff records are finalized. No other actionable
  findings remained.
