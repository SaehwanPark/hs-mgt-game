# Implementation Plan — Phase 8.3 Reproducible Distribution v0.13.10

## Goal

Document and verify the exact Git source checkout as the canonical
distribution unit without adding a package/archive format or changing runtime
behavior.

## Changes

- Add `docs/guides/reproducible-distribution.md` with required tracked inputs,
  stable Rust/Cargo setup, read-only checks, CLI/GUI run commands, current
  Chromium evidence, first-build network caveat, and deferred release paths.
- Link the guide from the README, contributor documentation index, and release
  metadata guide.
- Bump package projections from v0.13.9 to v0.13.10 and synchronize the
  changelog, roadmap, SPEC, and lessons.
- Append this request/plan context and a final handoff under `_workspace/`.

## Verification and handoff

Run the complete release, documentation, asset, offline, browser, Python, and
Rust command set from the request summary. Confirm no generated tracked diff,
commit as `docs: establish reproducible distribution path`, push, open a PR
against `main`, complete three independent review passes plus any required
follow-up, merge with a merge commit, and verify local/remote branch cleanup.

## Explicit boundaries

No simulation, GUI runtime, MCP, history, replay, asset, CI, public API,
binary, archive, installer, registry, deployment, release-tag, or human-quality
change is part of this slice.
