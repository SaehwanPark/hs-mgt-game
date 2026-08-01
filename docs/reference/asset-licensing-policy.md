# Asset licensing policy

This repository keeps visual and audio provenance in the canonical registries
under `assets/registry/`. The policy is an automated release-safety check and
documentation aid, not legal advice or a substitute for a human legal
conclusion.

## Default allowlist

The validator accepts project-authored or otherwise explicitly registered
entries using `project-generated`, `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`,
`MIT`, `Apache-2.0`, `GPL-3.0-or-later`, or `OFL-1.1`. GPL and other
third-party-compatible entries still carry a visible rights/provenance limit;
uncertain entries are excluded rather than approved by inference.

The validator rejects noncommercial, no-derivatives, personal-use-only,
unclear, proprietary, unattributed-aggregator, screenshot, and protected-art
provenance markers. A license string outside the allowlist fails closed.

## Provenance kinds

Every registry entry contains:

- `repository-authored`: source is in this repository, license is
  `project-generated`, and external URL/retrieval fields are null.
- `local-generation`: a contributor generated the source locally; the model
  or workflow source URL, retrieval date, and license reference are required.
- `external`: the source came from elsewhere; an HTTPS source URL, retrieval
  date, and license reference are required.

`license_reference` may be an HTTPS URL or a repository-relative file that
preserves or explains the original license basis. Source bytes and approved
derivatives remain hash-bound by `scripts/validate_assets.py`.

## Release practice

Only entries that pass automated policy checks and have a registered
`release_path` are distributable.
`assets/ASSET_CREDITS.md` and `assets/THIRD_PARTY_NOTICES.md` are generated
from registry data. Before a release, contributors must rerun the registry,
credits, notices, security, and release checks and retain any external license
text or archive reference available. Automated conformance does not establish
legal clearance; unresolved rights fail closed to exclusion and fallback.
