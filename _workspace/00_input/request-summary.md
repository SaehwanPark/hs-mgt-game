# Request Summary

## Scope

Continue development with a documentation-first Phase 3 slice: add the
actor-card template and first scenario brief for the current fictional regional
US market prototype, and align the evidence registry and project-state files.

## Roadmap Phase

Phase 3 game and educational design — actor cards, scenario concept, learning
objectives, strategic tensions, observation use, and debrief hooks.

## Expected Outputs

- New `docs/actor-cards.md`
- New `docs/first-scenario-brief.md`
- Updated `docs/system-boundary.md` and `docs/evidence-registry.md` links
- Corrected `SPEC.md` state for the merged Phase 2 boundary slice
- Version bump to `0.1.11`
- Updated changelog, lessons, and workspace handoff artifacts

## Non-Goals

- No runtime behavior changes
- No scenario or ruleset file loader
- No command parser or save format
- No module split
- No new Cargo dependencies
- No empirical calibration or policy forecasting claim

## Validation Target

- Actor-card template clearly identifies objectives, authority, constraints,
  observations, private information, outside options, decision procedure,
  rationale output, debrief use, and evidence status
- First scenario brief clearly identifies player role, included interactions,
  learning objectives, strategic tensions, observation use, debrief hooks, and
  scenario non-goals
- Existing deterministic CLI demo remains unchanged
- `cargo fmt --check`, `cargo test`, and default `cargo run` pass

## Generic Skills Needed

- `spec-driven-developer` for project state sync
- `simple-code-writer` for keeping the diff minimal
- `code-reviewer` for PR review loop
