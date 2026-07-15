# Implementation Plan — Visual and Audio Phase 4 Resolution/Causal Feedback v0.12.20

Status: Implemented and ready for the single code-review pass.

## Task restatement

Implement one read-only, replayable competitive-month resolution presentation
over committed `CompetitiveTransition` history while preserving the existing
transition, stochastic-input, observation, replay, hash, CLI, MCP action, and
submit behavior.

## Current understanding

- `CompetitiveTransition` already stores prior/next world snapshots, committed
  events/effects, aggregated actions, and a state hash in
  `src/model/competitive_history.rs`.
- `src/mcp/presentation.rs` already projects actor-visible observation,
  resources, pending processes, history, and replay metadata.
- `submit_turn` is the only mutation path; Phase 3's action client currently
  refreshes the read-only presentation after a successful submit.
- The desired Phase 4 sequence is eight presentation homes: submitted batch,
  visible responses, process advancement, operating result, resources, direct
  effects, new information, and updated pending processes.
- Main uncertainty: whether existing transition event/effect strings are
  sufficiently clear for the first slice without promoting a richer structured
  causal model. The implementation must reuse them and stop short of inferred
  causal graphs.

## Assumptions

- `observe_for_human` can safely project both `CompetitiveTransition.prior` and
  `.next` with the appropriate prior-month aggregate, without exposing true
  world state.
- A new read-only `get_resolution(session_id, turn?)` tool can locate an
  immutable committed transition without adding session mutation or persistence.
- The accepted `TransitionSummary` event/effect surface is already within the
  player's observation boundary; Phase 4 will not add private rival fields.
- CSS/DOM pacing and native `prefers-reduced-motion` are sufficient; no new
  dependency or audio playback is required in Phase 4.

If any assumption is false, stop and report the mismatch before editing core or
adding a broader causal abstraction.

## Minimal implementation plan

1. Inspect the transition/history and observation helpers to confirm the safe
   prior/next projection and turn lookup described above.
2. Add `competitive-resolution-v1` DTOs in `src/mcp/resolution.rs` for safe
   before/after snapshots, ordered steps, committed event/effect text,
   operating/resource values, pending processes, and replay/hash metadata.
3. Add `GetResolutionRequest`, `GameSessionStore::get_resolution`, and the
   non-mutating MCP `get_resolution` tool; reject unsupported campaigns,
   missing history, and unavailable turns without touching the session.
4. Add focused Rust tests for latest resolution, historical lookup, exact state
   hash, no-transition behavior, unsupported/missing turns, and hidden-field
   exclusion.
5. Add `createResolutionClient`/rendering in `gui/app.mjs`, and integrate the
   action client's successful-submit path with optional `getResolution` before
   the read-only refresh. Keep every step's text in the DOM immediately while
   local controls change only highlighting/pacing.
6. Add play/pause/skip/review controls, a committed-month review selector, and
   reduced-motion CSS/semantic state in `gui/index.html`. Use no timer or
   presentation state that can call `submitTurn`.
7. Add GUI contract tests for eight step IDs, before/after labels, direct
   effect/source rendering, all controls, adapter errors, replay reads,
   reduced-motion markers, no formulas, and no assets/network calls.
8. Update the Phase 4 contract, SPEC/architecture/README/changelog/lessons,
   evidence/mechanism/QA/handoff records, and package metadata to `0.12.20`.
9. Run focused and full checks, perform exactly one code-review pass, push a
   feature branch, open the PR, wait for CI, merge into `main`, and record the
   next Phase 5 audio gate.

## Files and functions likely to change

- `src/mcp/resolution.rs`: new typed resolution envelope, snapshot, step, and
  direct-effect DTOs plus safe projection helpers.
- `src/mcp/session.rs`: `GetResolutionRequest`, immutable turn lookup, and
  tests for read-only/replay/hidden-field behavior.
- `src/mcp/server.rs`, `src/mcp/mod.rs`: expose the read-only tool and DTOs.
- `gui/app.mjs`: resolution projection, local pacing controls, replay lookup,
  and successful-submit integration.
- `gui/index.html`: resolution panel, step/review controls, semantic status,
  and reduced-motion presentation styles.
- `gui/README.md`: Phase 4 adapter contract and review checklist.
- `tests/test_gui_resolution.py`: static browser/adapter/source-boundary tests.
- `docs/visual-audio-phase4-resolution-causal-v0.12.20.md`: contract, source
  map, user checklist, evidence limits, and Phase 5 gate.
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `CHANGELOG.md`, `LESSONS.md`,
  `_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`,
  `_workspace/02_mechanism_design.md`, `_workspace/03_domain_qa.md`,
  `_workspace/final/handoff.md`, `Cargo.toml`, `Cargo.lock`, and affected
  contract tests: phase promotion and project records.

Avoid editing transition, resolver, randomness, scenario, replay verification,
audio, or asset files. If the safe presentation requires one of those paths,
stop and explain why.

## Tests and checks

Run:

- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest tests/test_gui_resolution.py tests/test_gui_contextual_actions.py tests/test_gui_live_read_only.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `node --check gui/app.mjs`
- `python3 scripts/check_release_metadata.py`
- `git diff --check`

Expected result:

- The host can read the latest and historical committed month without a turn
  change; JSON omits true state, resolved inputs, private rival fields, and
  effect queues.
- The GUI contains the complete textual resolution immediately, supports
  pause/skip/review/reduced motion, and uses `submitTurn` only through the
  existing validated action path.
- Existing Phase 0–3, CLI, MCP, replay, golden, and metadata tests remain green.

If tests fail, fix only failures directly caused by this slice and report any
unrelated failure separately.

## Acceptance criteria

- A successful graphical submit can load one typed `competitive-resolution-v1`
  envelope and present all eight ordered resolution steps.
- Before/after actor-visible operations and resources are labeled as changes;
  direct causal/effect text is host-sourced and no inferred graph is shown.
- The full textual result remains available when paused, skipped, reviewed, or
  `prefers-reduced-motion` is active; animation never gates access to results.
- `get_resolution` for the latest or a historical turn does not mutate session
  turn, resources, history, replay count, or state hash.
- Missing, unsupported, invalid-turn, and adapter-refresh failures are explicit
  and recoverable; a committed submit is not mislabeled as rejected if only the
  optional refresh fails.
- No transition formulas, stochastic inputs, hidden-state fields, new command
  families, audio playback, asset/network behavior, or other campaigns change.

## Non-goals

- Do not add audio, downloaded/generated assets, audio cues, or a Phase 5 music
  system.
- Do not add a causal inference engine, new formulas, recommendation model,
  true-state/instructor view, or private rival reveal.
- Do not create a general multi-month replay editor, campaign-general DTO
  framework, browser simulation, or second parser.
- Do not change command legality, transition semantics, randomness, replay
  artifacts, state hashes, scenario rules, or debrief generation.
- Do not claim human comprehension, accessibility, learning, engagement,
  calibration, balance, or policy validity from technical checks.

## Stop conditions

Stop and request direction if:

- the existing actor-visible projection cannot safely produce before/after
  snapshots without adding hidden state;
- resolution requires changing transition or stochastic-input semantics;
- event/effect text cannot be scoped to the accepted player-visible boundary;
- replay lookup needs persistence or migration changes;
- more than the listed presentation/MCP/GUI/docs files need production edits; or
- a proposed animation delays, hides, or changes the textual result.

## Review checklist

Before finalizing, verify:

- The DTO is derived from committed history and has no true-state or private
  rival fields.
- Latest and historical resolution reads are non-mutating and hash-stable.
- Each step maps to one existing committed source; no inferred causal edge or
  client formula is introduced.
- Textual results are present before animation and controls work with keyboard,
  pause, skip, review, and reduced motion.
- The action path still submits only unchanged host-validated canonical batches.
- Focused tests cover missing/unsupported/replay/error states and avoid fixture-
  only claims.
- Exactly one code-review pass occurs, and the final handoff lists files,
  tests, deviations, and unresolved risks.

## Risk label

Risk: high

Reason: This adds a public MCP presentation contract and browser replay-facing
behavior, so observation-boundary and historical-state semantics require domain
QA plus the requested single code-review pass even though simulation semantics
remain unchanged.
