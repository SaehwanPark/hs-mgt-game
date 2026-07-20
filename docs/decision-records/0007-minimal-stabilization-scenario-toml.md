# ADR-0007: Minimal Stabilization Scenario TOML

**Status:** Accepted  
**Date:** 2026-06-26  
**Deciders:** Project contributors

## Context

`docs/design/scenario-format-draft.md` required an ADR before adding a runtime
scenario loader. Phase 6.2 calls for versioned, validated scenario files that
compose known mechanisms without arbitrary executable logic.

The current executable already has a stable five-turn `stabilization-v1`
scenario. The next useful step is to load that existing scenario metadata from
data while preserving deterministic transition, replay, and save boundaries.

## Decision

1. Adopt `scenario-toml-0.1.40` as the first runtime scenario format.
2. Use TOML parsed through `serde` and `toml`.
3. Ship one bundled runtime scenario at `scenarios/stabilization-v1.toml`.
4. Support only `campaign_id = "stabilization-v1"` and `turn_unit = "abstract"`.
5. Validate the scenario's ruleset id, initial turn, learning objectives, five
   fixed turn schedule entries, and actor-stub references before starting a new
   stabilization run.
6. Keep presets as CLI conveniences rather than scenario data.

## Consequences

### Positive

- Contributors can inspect the stabilization scenario without reading Rust code.
- Scenario loading starts at the CLI/config boundary and does not enter
  deterministic transition logic.
- Golden replay hashes remain stable because the bundled scenario reproduces
  the existing genesis state and schedule.

### Negative / tradeoffs

- Adds `serde` and `toml` dependencies.
- The first format is intentionally narrow and rejects competitive scenarios.
- There is not yet a CLI option for arbitrary scenario paths.

### Follow-ups

- Add explicit scenario-path selection only after authoring and validation needs
  are proven.
- Extend the format for competitive campaigns in a separate ADR.
- Decide when session saves and replay artifacts should record scenario id.

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| JSON + serde | Better for some tools, but less friendly for hand-authored scenario files |
| Custom text format | Avoids dependencies but creates parser maintenance risk |
| Load competitive scenarios now | Broader than the current slice and would couple Phase 6.2 to competitive campaign expansion |

## Verification

- Bundled TOML parses and validates against `default_ruleset()`.
- Scenario initial state equals current `genesis_state()`.
- Turn schedule is exactly the current five-turn stabilization sequence.
- Unsupported campaign, unsupported turn unit, malformed TOML, missing stubs,
  and ruleset mismatch are rejected.
- `cargo fmt --check` and `cargo test` must pass with stabilization and
  competitive golden hashes unchanged.

## Related Documents

- [`scenario-format-draft.md`](../design/scenario-format-draft.md)
- [ADR-0001](0001-deterministic-transition-and-stochastic-input-boundary.md)
- [ADR-0002](0002-mid-run-session-save.md)
