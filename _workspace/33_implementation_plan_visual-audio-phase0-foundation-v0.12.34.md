# Implementation Plan — Visual/audio Phase 0 foundation v0.12.34

## Task restatement

Close the first two roadmap milestones with a bounded product brief and a
dependency-free asset registry/release validation boundary. Preserve the
existing host-authoritative GUI and generated visual/audio catalog behavior.

## Minimal slice

1. Record product/style/audio/accessibility/license/AI/ownership decisions.
2. Add separated source, generated, release, and registry asset paths.
3. Add visual/audio registry schemas and project-generated baseline manifests.
4. Add validation for IDs, roles, metadata, licenses, approvals, hashes, and
   release coverage.
5. Add deterministic credits rendering and focused tests.
6. Align roadmap, SPEC, architecture, changelog, lessons, docs index, release
   metadata, and handoff records.

## Acceptance criteria

- Phase 0.1 and 0.2 deliverable/checklist evidence is present.
- Invalid registry fixtures fail closed with actionable messages.
- Existing catalogs remain unchanged and no host/runtime boundary changes.
- Full proportional verification passes.

## Non-goals and stop conditions

No asset acquisition, image/audio generation, GUI redesign, host schema, new
dependency, human evaluation, or Phase 1 promotion. Stop if registry validation
requires a package dependency or if current generated catalogs cannot be
represented without changing runtime semantics.
