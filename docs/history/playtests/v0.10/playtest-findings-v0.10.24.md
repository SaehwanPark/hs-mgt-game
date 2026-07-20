# Access Debrief Validation v0.10.24

- **Status:** Phase 7 bounded debrief validation
- **Date:** 2026-07-08
- **Code version:** 0.10.24
- **Campaign:** `competitive-regional-v1`
- **Prior routing:** `docs/history/playtests/v0.10/playtest-findings-v0.10.23.md`
- **Artifact:** `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This slice validates that the `v0.10.23` access follow-through debrief note is
visible through the MCP end-session debrief surface for bounded trigger runs
and absent from nearby control runs.

## Validation Runs

All runs used seed `42`, completed 24 committed months, and had no final
validation failures.

| Profile | Difficulty | Access pledges | Durable follow-through | Final cash | Note present | Final hash |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Access Pledge Under-Followed | Normal | 3 | 2 | 15 | yes | `5182804a50a8dd9c` |
| Single Access Pledge Low-Cash Control | Normal | 1 | 2 | 15 | no | `67c868c18ac592ad` |
| Access Pledge Followed Control | Normal | 2 | 2 | 15 | no | `2b27f8e457178deb` |
| Access Pledge Under-Followed | Hard | 3 | 2 | 15 | yes | `beb0e684156c93aa` |
| Single Access Pledge Low-Cash Control | Hard | 1 | 2 | 15 | no | `0e2325e243937d14` |
| Access Pledge Followed Control | Hard | 2 | 2 | 15 | no | `b4636bcb7db45c0d` |

## Findings

1. The note appears in both targeted trigger runs where public access pledges
   outnumber durable follow-through actions and final cash is below `20`.
2. The note stays absent when low cash is present but repeated access pledges
   are not present.
3. The note stays absent when repeated access pledges are paired with at least
   as many durable follow-through actions.
4. Existing diagnostics can consume the artifact, so this slice does not need
   new parser fields, MCP DTOs, or diagnostic tooling.

## Routing

No runtime tuning is justified by this validation slice. The access
follow-through note is now covered by focused unit tests and by bounded MCP
surface evidence. The next access-related work should remain in guidance,
debrief review, or broader playtest synthesis unless a later artifact identifies
a concrete mechanics problem.

## Evidence Limits

- These are deterministic trigger/control policies, not organic human play.
- The runs validate debrief-surface visibility, not educational effectiveness.
- The artifact is MCP wrapper evidence, not a full replay artifact.
- Do not use this slice to justify access-pledge cooldowns, action-cost tuning,
  difficulty changes, or balance changes.

## Verification

```bash
python3 _workspace/experiments/v0.10.24-access-debrief-validation/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.24-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
