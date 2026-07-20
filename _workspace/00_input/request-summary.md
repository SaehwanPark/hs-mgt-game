# Request Summary — Documentation information architecture v0.12.32

## Classification and scope

- Roadmap/output: cross-phase documentation governance and contributor
  navigation; behavior-preserving document production and relocation.
- Reorganize `docs/` around equal software, design/research, and validation
  contributor paths.
- Preserve canonical documents and immutable evidence, consolidate playtest
  protocols, repair references, add a dependency-free link checker, and align
  release metadata at v0.12.32.

## Sources

- `README.md`, `SPEC.md`, `ARCHITECTURE.md`, and `CHANGELOG.md`.
- `docs/proposal.md`, `docs/roadmap.md`, `docs/design_principles.md`, and the
  harness team spec.
- Repository instructions and the approved implementation plan.

## Expected files

- Contributor and history indexes plus relocated documentation.
- Consolidated playtesting guidance.
- Documentation checker, CI integration, and updated reference tests.
- Project-state documentation and final handoff.

## Non-goals

- No simulation, scenario, command, replay, GUI, calibration, policy-validity,
  research-conclusion, or evidence-conclusion changes.
- No compatibility stubs for moved document paths.

## Validation target

- Four Markdown files at the `docs/` root.
- All current documents reachable within two links.
- All versioned evidence preserved.
- No broken or machine-local Markdown links.
- Visual/audio, release, Python, and Rust checks pass.

Global preferred-workflow, spec-driven-developer, and simple-code-writer skills
apply. Project-specific mechanism or evidence redesign does not.
