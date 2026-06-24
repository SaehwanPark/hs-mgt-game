# Request Summary

## Scope

Continue development with a documentation-first Phase 2 slice: expand the
system-boundary and ontology draft for the current fictional regional US market
prototype, and align the evidence registry and project-state files.

## Roadmap Phase

Phase 2 conceptual and domain design — system boundary, domain ontology, actor
classes, observation boundary, causal categories, and assumption visibility.

## Expected Outputs

- Expanded `docs/system-boundary.md`
- Updated `docs/evidence-registry.md`
- Corrected `SPEC.md` state for the merged coalition slice
- Version bump to `0.1.10`
- Updated changelog, lessons, and workspace handoff artifacts

## Non-Goals

- No runtime behavior changes
- No scenario or ruleset file loader
- No command parser or save format
- No module split
- No new Cargo dependencies
- No empirical calibration or policy forecasting claim

## Validation Target

- Phase 2 docs clearly identify included and excluded actors, authority,
  observation boundaries, command vocabulary, causal categories, and evidence
  gaps
- Existing deterministic CLI demo remains unchanged
- `cargo fmt --check`, `cargo test`, and default `cargo run` pass

## Generic Skills Needed

- `spec-driven-developer` for project state sync
- `simple-code-writer` for keeping the diff minimal
- `code-reviewer` for PR review loop
