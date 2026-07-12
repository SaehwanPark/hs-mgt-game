# Request Summary - Regional Affiliation Runtime Proposal v0.11.14

## Scope

- Continue from merged PR #151 and the v0.11.13 affiliation-first design gate.
- Define an opt-in `regional-affiliation-v1` runtime proposal using existing
  competitive transition, observation, history, replay, and debrief concepts.
- Specify the minimum true-state, actor-observation, command, resolved-input,
  replay, and educational-debrief contracts needed by a later implementation.
- Preserve the default `competitive-regional-v1` campaign and its seed-42
  golden path.

## Non-goals

- No Rust runtime mechanics, public commands, scenario TOML, scenario-loader
  changes, replay format, MCP schema, ruleset, or state-hash changes.
- No direct acquisition, national deal market, private-equity rollup, detailed
  transaction finance, calibrated legal outcome, or policy forecast.
- No generic actor framework, AI rival expansion, GUI work, balance change, new
  playtest matrix, human-learning claim, or policy-validity claim.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.
- `docs/expansion-proposal-review.md`, `docs/system-boundary.md`,
  `docs/scenario-format-draft.md`, and the v0.11.13 workspace artifacts.
- Existing DOJ/FTC and HHS consolidation sources cited by the expansion review;
  no new external evidence is introduced.

## Expected files

- ADR-0010 and synchronized expansion, roadmap, architecture, boundary,
  scenario, specification, changelog, README, lesson, and workspace handoff
  documents.
- `Cargo.toml` and `Cargo.lock` for the required `0.11.14` patch bump.

## Validation target

- Domain QA returns `Pass`.
- The proposal distinguishes actor authority, observations, actor utility,
  organizational outcomes, social welfare, community effects, and educational
  evaluation.
- Partner, review, labor, payer, community, and integration uncertainty is
  represented as explicit resolved input before deterministic transition.
- Existing Rust, Python, formatting, clippy, golden, and diff checks pass.
