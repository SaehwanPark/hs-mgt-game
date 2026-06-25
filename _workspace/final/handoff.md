# Handoff — Competitive Campaign Runtime I8 (v0.1.35)

## Summary

Implemented Stata-like competitive command parser and interactive human monthly
batch entry in the competitive campaign preview. Non-TTY contexts (tests, CI)
use the preset human batch without blocking on stdin.

## Changed files

### New

- `src/cli/competitive_parse.rs`

### Updated

- `src/cli/campaign.rs`, `src/cli/mod.rs`
- `Cargo.toml`, `CHANGELOG.md`

## Verification

- `cargo fmt --check`, `cargo test` (192 tests)
- Competitive golden hash unchanged (`88d07f9e1bbd6f04`)

## Known limits

- Single-line batch entry (semicolon-separated); no multi-line submit loop yet
- Full 24-month interactive campaign and competitive autosave remain deferred
