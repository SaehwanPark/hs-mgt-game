# Request Summary — Release Metadata Check v0.12.13

## Decision

Implement one lightweight contributor/release-readiness check that validates
version metadata locally and in CI, then close the final release Future item.

## Target slice

- Check the package version in `Cargo.toml` and `Cargo.lock`.
- Check the README milestone and latest changelog heading.
- Document `python3 scripts/check_release_metadata.py` for contributors.
- Add the same command to the existing CI workflow.

## Explicit non-goals

No packaging, publishing, tag automation, registry access, dependency
installation, broad CI redesign, or simulation/runtime behavior change.
