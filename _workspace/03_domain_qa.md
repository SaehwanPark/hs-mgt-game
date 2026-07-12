# Domain QA — Release Metadata Check v0.12.13

## Decision

Pass for a bounded contributor-readiness check.

## Checks

- The check enforces the repository's documented modified semantic-version
  shape without inventing a new release convention.
- It catches the common failure mode where a package bump leaves the lockfile,
  README milestone, or changelog heading stale.
- It is read-only and has no access to simulation state, scenario data, replay
  artifacts, or external registries.
- The same command is documented for local use and executed in CI.
- A focused test covers both the current repository and a deliberate mismatch.

## Reopening condition

Reopen release-readiness work only for a separately authorized packaging,
publication, licensing, deployment, or contributor workflow need. Do not grow
this check into a release platform without a concrete requirement.
