# Evidence Map — Release Metadata Check v0.12.13

| Requirement | Authority | Result | Limit |
| --- | --- | --- | --- |
| Package metadata is authoritative | `Cargo.toml` `[package]` version | Checker reads the package version as the expected value | It does not validate every Cargo field |
| Lockfile stays aligned | `Cargo.lock` package block | Checker compares the `hs-mgt-game` package version | It does not regenerate or edit the lockfile |
| User-facing version is aligned | README milestone line and `CHANGELOG.md` first version heading | Checker catches stale visible release metadata | It does not judge release-note completeness |
| Local contributor usage | `docs/contributor-release-check.md`, README | One copyable Python command is documented | It assumes the repository's existing `python3` command is available |
| CI coverage | `.github/workflows/ci.yml` | CI runs the same read-only check before Rust checks | It is not a package publication or deployment gate |
| Runtime safety | no `src/` or scenario changes | Simulation, replay, and ruleset behavior are untouched | The check cannot prove all semantic behavior is unchanged |

## Conclusion

This is a narrow metadata consistency check appropriate for the final release
readiness queue item. It adds no release automation beyond the existing
versioning policy and leaves publication, packaging, licensing, and deployment
for a later explicitly authorized slice.
