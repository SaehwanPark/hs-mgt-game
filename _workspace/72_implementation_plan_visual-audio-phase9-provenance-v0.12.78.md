# Implementation Plan — Visual/audio Phase 9.1 provenance and notices v0.12.78

## Target slice

Implement the first bounded Phase 9.1 licensing/release-hardening slice:
make the canonical visual/audio registries carry machine-checked provenance
metadata, and generate both human-readable asset credits and a third-party
notice projection from those registries.

## Scope

- Add a per-entry provenance object with a constrained provenance kind,
  source URL, retrieval date, and license-reference fields.
- Require repository-authored entries to point at the repository licensing
  policy and require future external/local-generation entries to provide
  source and license references with retrieval dates.
- Keep every current registry entry project-authored; do not invent external
  source URLs, licenses, dates, or third-party assets.
- Validate provenance paths/URLs, date shape, license-policy compatibility,
  and denylisted provenance text fail-closed.
- Extend deterministic credits generation with provenance columns and add a
  generated `assets/THIRD_PARTY_NOTICES.md` projection.
- Add focused malformed-provenance, stale-output, external-entry, and
  denylist tests; wire the checks into CI and contributor release guidance.

## Non-goals

- No portrait approval, model/seed claim, release derivative, or registry
  promotion for the pending Phase 8.2 candidates.
- No download, network retrieval, license acquisition, or third-party asset
  addition.
- No host DTO, simulation transition, actor observation, history, replay,
  debrief, or runtime authority changes.
- No claim that registry validation is legal advice or a substitute for a
  human license audit.

## Acceptance checks

- Both canonical registries validate with complete provenance metadata and
  no external release assets.
- Credits and third-party notices are reproducible from registry data and
  stale generated files fail CI.
- External entries require HTTPS source/license references, an ISO retrieval
  date, an allowlisted license, and an existing local license reference when
  a repository copy is claimed.
- Repository-authored entries cannot silently carry an external URL/date or
  a non-project-generated license.
- Full Python/Rust/JavaScript, asset, release, documentation, formatting,
  and diff checks pass.

## Evidence limits

This slice makes provenance auditable and release projections reproducible;
it does not establish legal clearance, ownership, output provenance, human
accessibility, educational benefit, or policy validity.

## Review disposition

The single designated read-only code reviewer identified three medium findings:
non-repository entries could retain `project-generated`, malformed HTTPS
authority values were not fully rejected, and generated notices did not
independently filter approval status. All three were fixed with regression
coverage before handoff.
