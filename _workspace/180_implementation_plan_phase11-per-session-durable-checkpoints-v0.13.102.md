# Implementation Plan — Per-session durable GUI checkpoints v0.13.102

## Target slice

Replace the single latest GUI checkpoint slot with a small host-owned archive
of per-session files. Preserve the current public save/load routes, opaque
session-ID browser storage, deterministic artifact validators, and legacy
single-file recovery path.

## Acceptance criteria

1. A competitive, stabilization, and regional-affiliation save each resolves
   to a distinct archive file keyed by its validated session ID.
2. A fresh `GameSessionStore` can hydrate each saved campaign independently
   after the in-memory store is gone.
3. Ending one session removes only that session's archive/legacy checkpoint;
   another campaign's durable checkpoint remains recoverable.
4. Existing single-file GUI checkpoints remain loadable and removable for
   migration compatibility.
5. Invalid session IDs cannot escape the archive directory.
6. The browser still stores only an opaque session ID and uses the existing
   host load route; no save artifact or authority moves into JavaScript.
7. Focused and full verification pass, with package version v0.13.102 and
   roadmap/spec/handoff state synchronized.

## Planned files

- `src/mcp/persistence.rs`
- `src/mcp/session.rs`
- `src/gui_server.rs`, `gui/README.md`
- `tests/test_phase11_browser_refresh_recovery.py`
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`,
  `gui/asset-credits.mjs`, `tests/test_release_metadata.py`
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `LESSONS.md`
- `_workspace/final/handoff.md`

## Design boundaries

- Use the standard library and the existing atomic temporary-sibling write
  pattern; do not add a dependency or invent a checkpoint database.
- Treat generated session IDs as opaque path components and reject traversal or
  unsupported path characters before constructing archive paths.
- Keep legacy single-file loading as a fallback only when the per-session file
  is absent; a present but invalid archive file must fail closed.
- Keep all checkpoint serialization and validation host-side. The browser
  receives only the existing `SaveEnvelope` metadata and stores only the
  opaque session ID.

## Verification

- Run focused persistence/session/browser-boundary tests and new archive tests.
- Run the full Python suite, serial Rust tests, Clippy, formatting, CLI smoke,
  release, asset, browser/device, documentation, syntax, and diff checks.
- Complete the one-reviewer PR loop and re-run archive/legacy/cross-campaign
  checks on clean `main` after merge.
