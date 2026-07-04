# Versioning Policy

**Status:** Phase 0 governance artifact  
**Audience:** Contributors and release maintainers

## Package Version (Cargo)

The `hs-mgt-game` crate follows the versioning policy defined in [`AGENTS.md`](../AGENTS.md):

The project follows a modified semantic versioning format: `x.y.z`, where **x**, **y**, and **z** are integers.

### Increment Rules

* **Patch (`z`):** Increment by `1` for every Pull Request (PR) or PR-equivalent change.
* **Minor (`y`):** Increment by `1` when the project receives significant improvements or feature updates.
* **Major (`x`):** Increment by `1` for categorical, architectural, or structurally different changes.

### Reset & Carrying Rules

* **No Automatic Carry-Over:** Lower digits do **not** automatically roll over or carry over when a higher digit is incremented, nor do they roll over when reaching `10` (e.g., version `0.1.9` increments to `0.1.10`, not `0.2.0`).
* **Digit Initialization:** When a higher-order digit (**x** or **y**) is incremented, all lower-order digits are explicitly reset to `0` (e.g., incrementing `y` resets `z` to `0`; incrementing `x` resets both `y` and `z` to `0`).

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
