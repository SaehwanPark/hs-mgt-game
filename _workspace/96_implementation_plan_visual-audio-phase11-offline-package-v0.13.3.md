# Implementation Plan — Visual/audio Phase 11.2 offline package completeness v0.13.3

## Task restatement

Make the live loopback GUI host serve the complete repository-embedded module
graph and catalogs required by the live desktop, then add a deterministic audit
that fails closed on missing route coverage, external sources, path escapes, or
non-loopback binding.

## Current understanding

- `gui/index.html` is served with an injected local `host-adapter.mjs` script.
- The v0.13.2 loading policy declares the entrypoint and its complete local
  module graph, but `src/gui_server.rs` currently exposes only a subset of
  those modules and two catalogs.
- The host API is same-origin and the GUI server is intended to bind only to a
  loopback address.
- The target is offline package completeness, not a service worker or browser
  cache feature.

## Assumptions

- The v0.13.2 loading-policy graph is the authoritative live module set.
- The host adapter and audio/visual catalogs are additional embedded live
  resources because the Rust server injects or serves them outside the HTML
  graph.
- Route/source closure plus loopback-server tests are sufficient bounded
  technical evidence for the current offline gate; browser/device/human gates
  remain separate.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Add `assets/offline-policy.json` describing the live entrypoint, embedded
   resources, same-origin API boundary, loopback requirement, and forbidden
   external/path markers.
2. Add `scripts/check_offline_availability.py` to validate the policy, compare
   every declared resource to an `include_str!` route in `src/gui_server.rs`,
   reuse the live loading-policy report, and emit `offline-policy-report-v1`.
3. Expand `src/gui_server.rs` static routes for every live module, the host
   adapter, and the two live catalogs; add a route-closure test.
4. Add focused Python tests for the current report/CLI, missing route/source,
   external source, path/schema, and loopback-policy failures.
5. Update roadmap, README, SPEC, ARCHITECTURE, LESSONS, CHANGELOG, asset
   guidance, version projections, request/contract/QA, and handoff to v0.13.3.
6. Run focused/full checks; stop if the work reaches service workers, browser
   cache persistence, deployment, device compatibility, or human evaluation.

## Files and functions likely to change

- `src/gui_server.rs`: `static_asset` route table and focused server test.
- `assets/offline-policy.json`: embedded offline scope and requirements.
- `scripts/check_offline_availability.py`: policy/route/source report.
- `tests/test_offline_availability.py`: green and fail-closed cases.
- `_workspace` request/contract/QA/plan/handoff records.
- Roadmap, canonical docs, lessons, changelog, asset guidance, and version
  projections.

## Tests and checks

- `python3 -m unittest tests.test_offline_availability`
- `python3 -m unittest discover -s tests`
- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- loading/audio/asset/security/release/metadata/documentation/visual-audio
  audits.

Expected result: the report passes, every live resource has an embedded local
route, and the loopback GUI server's route-closure test passes.

## Acceptance criteria

- Every current live module, host adapter, and catalog is served from a local
  repository-embedded route.
- A missing route, external source, path escape, or non-loopback policy fails
  closed.
- The same-origin API boundary remains explicit and host-authoritative.
- No simulation, history/hash, replay, debrief, audio, or asset semantics
  change.
- Only the Phase 11.2 offline-operation checklist item is closed; low-power and
  browser-compatibility gates remain open.

## Non-goals

- No service worker, CDN, browser cache, external dependency, or deployment.
- No screenshots, browser/device matrix, or human-quality claim.
- No unrelated Rust or presentation refactor.

## Stop conditions

Stop and report if the live graph is broader than the v0.13.2 policy, the host
uses a non-loopback API boundary, route coverage requires runtime filesystem
access, or implementation reaches browser cache/deployment behavior.

## Review checklist

- Route/source mapping is explicit, repository-local, and fail-closed.
- The offline report reuses or agrees with the loading-policy graph.
- Loopback binding and same-origin API assumptions remain tested.
- Current visual/audio semantics and authority boundaries are unchanged.
- Version, roadmap, canonical docs, QA, and handoff agree.

## Risk label

Risk: medium-low

Reason: The slice changes a Rust static delivery table and adds read-only
policy/tests; it does not change simulation transitions or host projections.
