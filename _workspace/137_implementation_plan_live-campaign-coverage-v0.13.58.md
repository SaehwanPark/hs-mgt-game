# Implementation Plan — Live campaign-coverage handoff v0.13.58

## Target slice

Connect the existing host-owned `campaign-coverage-v1` projection to the
loopback GUI launcher for `stabilization-v1` and `regional-affiliation-v1`.
The slice is limited to transport, adapter, launcher, and browser fallback
integration; it does not create new simulation, visual/audio assets, or hidden
state.

## Request summary

- Add `GET /api/v1/sessions/{session_id}/campaign-coverage` to the Rust GUI
  server using `GameSessionStore::get_campaign_coverage`.
- Add a non-mutating host session-envelope read so loading an existing session
  after a fresh page can resolve its campaign before choosing a renderer.
- Accept the two existing campaign-coverage campaigns in the live launcher;
  retain competitive difficulty validation and competitive action flow.
- Add `getCampaignCoverage` and active-campaign tracking to the local host
  adapter.
- Let the action client fail over to the typed campaign-coverage renderer when
  a noncompetitive session has no competitive presentation/action catalog.
- Preserve host ownership: campaign decisions still submit through the
  existing `submit_turn` route and refresh from the host envelope.
- Add focused Rust transport, JavaScript, and Python contract evidence, then
  update roadmap/spec/changelog/lessons and version to `0.13.58`.
- Preserve the currently rendered campaign envelope when a replacement read is
  malformed or unavailable.

## Explicit non-goals

- No new campaign rules, commands, transitions, state fields, or authority.
- No regional-world, competitive history, action-catalog, validation, or
  resolution projection for noncompetitive campaigns.
- No new visual/audio asset, portrait, screenshot, persistence mechanism, or
  browser true-state view.
- No claim of campaign-specific visual/audio quality, human accessibility,
  educational usability, legal/provenance approval, or public release.

## Implementation sequence

1. Extend the GUI route and Rust tests for campaign coverage and supported
   campaign launch boundaries.
2. Extend the host adapter and launcher validation/status language.
3. Add action-client fallback to campaign coverage while preserving existing
   competitive tests and controls.
4. Add focused contract tests and update current user-facing documentation
   and evidence ledgers.
5. Run the focused and full validation suites, perform one medium-effort code
   review, then address any Critical/High findings before handoff.

## Verification target

- `cargo fmt --check`
- focused Rust GUI transport tests
- focused Python campaign-coverage/session-launch tests
- Node syntax and fallback behavior probes
- full Python suite, `cargo clippy --all-targets -- -D warnings`, and
  `cargo test --all -- --test-threads=1`
- release metadata, asset, security, credits, documentation-link, and
  `git diff --check` validation

## Completion boundary

The technical browser-integration item is complete only when a loopback host
can start each campaign, expose the existing typed envelope, render its
actor-visible decisions/history/debrief, and submit through the canonical host
route. Human review and broader campaign-quality gates remain explicitly open.
