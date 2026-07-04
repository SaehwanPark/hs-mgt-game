# Versioning Policy

**Status:** Phase 0 governance artifact  
**Audience:** Contributors and release maintainers

## Package Version (Cargo)

The `hs-mgt-game` crate uses the following versioning policy:

- Increase version number by `0.0.1` for each PR or PR-equivalent change.
- Increase version number by `0.1.0` (increase `0.1` of the minor digit and reset lower digits to `0`) for major feature releases or meaningful accumulated changes.
- Reset lower digits when bumping a higher digit (e.g. `0.2.0` not `0.2.21`).
- No need to carry over the patch digit when bumping up higher digits.

Record all user-visible changes in [`CHANGELOG.md`](../CHANGELOG.md).

## Ruleset Version

- Ruleset versions are string identifiers on the `Ruleset` struct (e.g.
  `demo-ruleset-0.1.9`).
- Bump the ruleset version when validation bounds or transition semantics change
  in ways that affect replay compatibility.
- Replay artifacts record the ruleset version at export time.

## Scenario Format Version

- Format prefix: `scenario-toml-<package-version>` at time of introduction
  (current: `scenario-toml-0.1.40`).
- Scenario files record `scenario_id`, `scenario_version`, and `ruleset_id`.
- New runtime scenario format versions require an ADR and focused validation
  tests.
- The first runtime format supports only the bundled `stabilization-v1`
  scenario; competitive scenario loading is deferred.

## Replay Artifact Version

- Format prefix: `replay-artifact-<package-version>` at time of introduction
  (current: `replay-artifact-0.1.15`).
- New optional fields may be added with backward-compatible parsing.
- Breaking layout changes require a new artifact version string and CHANGELOG note.

## Golden Trajectory

- Integration test [`tests/golden_seed42.rs`](../tests/golden_seed42.rs) pins the
  canonical seed-42 preset path.
- Changing turn count, commands, or transition semantics requires updating the
  golden hash and documenting the break in `CHANGELOG.md`.

## Documentation

- Bump `README.md` status line when shipping a tagged slice.
- Update [`SPEC.md`](../SPEC.md) `Past` / `Present` / `Future` per
  spec-driven-development rules.

## Related Documents

- [`glossary.md`](glossary.md)
- [`decision-records/README.md`](decision-records/README.md)
