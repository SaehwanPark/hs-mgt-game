# Implementation Plan — Terminal-debrief runtime-boundary evidence v0.13.99

## Target slice

Capture and validate one fresh host-backed competitive terminal debrief in the
live GUI. The slice closes only the current technical observation boundary for
the existing `competitive-end-session-v1` projection; it does not close the
human debrief or educational review gate.

## Acceptance criteria

1. A fresh Chromium loopback session starts through the host, not the demo
   fixture.
2. The existing end-session control returns a terminal host envelope with
   `done: true`, non-empty committed history, non-empty written debrief, and
   replay metadata aligned to history count and latest state hash.
3. The visible terminal surface shows final session metadata, history rows,
   debrief rows, an explicit terminal status, no placeholder debrief, no
   further action submission, and a disabled end-session control.
4. The terminal onboarding action directs the player to review the debrief.
5. The evidence packet records written fallback and optional-debrief-audio
   boundaries without claiming playback, listening quality, accessibility,
   educational usability, or human review.
6. The validator fails closed on schema/source/host/history/debrief/replay/
   control drift, type coercion, privacy drift, and premature promotion.

## Planned files

- `docs/evaluation/phase13.2-terminal-debrief-runtime-evidence.json`
- `scripts/validate_terminal_debrief_runtime_evidence.py`
- `tests/test_phase13_2_terminal_debrief_runtime_evidence.py`
- `src/debrief/report.rs`, `src/debrief/mod.rs`, and `src/mcp/session.rs`
- `_workspace/00_input/request-summary.md`
- `_workspace/02_presentation_contract.md`
- `_workspace/03_domain_qa.md`
- `_workspace/03_presentation_qa.md`
- `docs/visual_audio_enhancement_roadmap.md`
- `SPEC.md`, `README.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`, and
  `tests/test_release_metadata.py`
- `_workspace/final/handoff.md`

## Design boundaries

- Use only actor-visible host output and committed history fields.
- Do not render, infer, or store true state, private rival actions, future
  outcomes, causal claims, or participant data.
- Keep terminal history and debrief immutable/read-only in the browser.
- Keep written content complete when audio is muted, reduced, unavailable, or
  not verified.
- Keep human debrief, education, accessibility, browser/device, provenance,
  revision, expansion, and release statuses false/pending.
- Preserve the separate instructor/CLI debrief path while removing its
  instructor-only appendix from the player-facing end-session projection.

## Verification

- Run the live in-app Browser smoke and record exact observed values.
- Run focused packet/validator and existing terminal debrief tests.
- Run the full Python suite, serial Rust tests, Clippy, formatting, metadata,
  asset, browser, device, and remaining-gate validators.
- Complete one medium-effort code review on the PR and record the outcome.
