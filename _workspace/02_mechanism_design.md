# Mechanism Design — Release Metadata Check v0.12.13

The check is a pure repository-boundary function:

1. read the package version from the `[package]` section of `Cargo.toml`;
2. read the `hs-mgt-game` package version from `Cargo.lock`;
3. read the public milestone version from the README;
4. read the first version heading from `CHANGELOG.md`;
5. validate the modified `x.y.z` integer format and equality; and
6. return a non-zero exit status with file-specific errors when a value is
   missing or inconsistent.

The checker never imports the Rust crate, runs a simulation, edits files,
contacts a registry, creates a tag, or publishes an artifact. CI and local
contributors invoke the same command, so the quality signal is reproducible
at the repository boundary.

## Boundary decision

The package version remains the expected source value. The lockfile, README,
and changelog are checked projections. `SPEC.md` and the versioning policy
remain human-maintained design/governance records and are updated in the same
PR, but they are not parsed as package metadata by this lightweight check.
