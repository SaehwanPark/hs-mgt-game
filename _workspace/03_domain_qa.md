# Domain QA — Visual/audio Phase 12 visual identity and marker provenance v0.12.28

## Status

pass

## Reviewed Inputs

- `SPEC.md` product contract, visual/motion language, presentation/action
  boundary, asset/accessibility rules, Phase 11 closure, and Phase 12 entry.
- `docs/visual_audio_upgrade_proposal.md` first vertical slice, visual identity,
  asset registry, accessibility, and testing sections.
- `_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`,
  `_workspace/02_mechanism_design.md`, and the Phase 12 implementation plan.
- `gui/visual.mjs`, `gui/visual-catalog.json`, `gui/app.mjs`,
  `gui/index.html`, `gui/ASSET_CREDITS.md`, and focused tests.
- Canonical README, proposal, roadmap, design principles, and harness team
  spec.

## Findings

- The change is presentation-only. The catalog maps visible IDs/names/kinds/
  labels to tokens and does not add actors, policy levers, utilities,
  measurements, formulas, or transition behavior.
- Owned Riverside and public Northlake/Summit identity labels remain distinct;
  the generic fallback makes unknown or missing visible identity explicit.
- Facility, demand, capacity, project, staffing, payer/policy, timeline, and
  generic markers are category labels, not claims about severity or outcome.
- Existing host status text, status symbols/patterns, source labels, public
  rival limitation text, and unavailable detail remain rendered alongside the
  new tokens. No private rival state or unsupported geography is exposed.
- Lookup is deterministic pure browser code. It does not enter commands,
  transitions, stochastic inputs, history, hashes, replay, audio classification,
  or debrief output.
- Registry and credits explicitly record project-generated glyph/CSS primitives
  and no third-party/downloaded assets. No Rust/MCP DTO change is present.

## Required Fixes

None for domain scope, observation boundaries, determinism, or educational
claim discipline.

## Residual Risks

- Name aliases could be too permissive for a future campaign; the current
  aliases are limited to the three known competitive systems and unknown values
  fall back explicitly.
- Unicode glyph appearance and visual comfort vary by font/platform; human
  recognition and lived accessibility remain unevaluated.
- The registry proves provenance for generated primitives, not visual polish or
  license readiness for future external assets.
- Browser transport, real host integration, and human first-session outcomes
  remain outside this technical slice.

## Verification Evidence

- Focused visual identity plus existing GUI/audio/accessibility/regional/static/
  release tests: 32 passed.
- Full Python discovery: 299 passed.
- `node --check gui/app.mjs` and `node --check gui/visual.mjs` passed.
- `cargo fmt -- --check`, `cargo clippy --all-targets -- -D warnings`, and
  serial `cargo test --all -- --test-threads=1` passed: 322 library tests,
  3 competitive-AI tests, 2 competitive golden tests, 1 stabilization golden
  test, 7 scenario tests, and no doctest failures.
- Release metadata and `git diff --check` passed for v0.12.28.
