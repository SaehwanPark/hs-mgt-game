# Release assets

Only approved distributable derivatives belong here. The asset validator scans
all non-README files and requires an exact registry entry, an approved status,
license/provenance metadata, and a matching `release_hash`. Regenerate
`assets/ASSET_CREDITS.md` and `assets/THIRD_PARTY_NOTICES.md` before packaging.
Run `python3 scripts/validate_asset_security.py` to reject unsafe SVG content,
oversized files, excessive dimensions, mismatched audio signatures, and
release metadata. Run `python3 scripts/verify_asset_release.py --check` to
verify the deterministic approved-release manifest before packaging.
