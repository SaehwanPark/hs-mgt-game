# Access Evidence Synthesis v0.10.25

- **Status:** Phase 7 simulated-agent evidence synthesis
- **Date:** 2026-07-08
- **Code version:** 0.10.25
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.10.21.md`
  - `docs/playtest-findings-v0.10.22.md`
  - `docs/playtest-findings-v0.10.23.md`
  - `docs/playtest-findings-v0.10.24.md`
- **Validation artifact:** `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This synthesis closes the access-heavy follow-through mini-loop that began in
`v0.10.21`. The evidence supports explanatory debrief and guidance work, but it
does not justify runtime tuning, command-cost changes, access-pledge cooldowns,
difficulty changes, scenario schema changes, MCP DTO changes, replay format
changes, state hash changes, or balance changes.

## Evidence Chain

| Version | Evidence shape | Main signal | Runtime change |
| --- | --- | --- | --- |
| `v0.10.21` | Live-capture synthesis | Retry visibility was sufficient; next question was access-heavy understanding | No |
| `v0.10.22` | Access-heavy comprehension review | Existing surfaces were reviewable but the player-facing explanation was distributed | No |
| `v0.10.23` | Debrief wording slice | Added a student-facing access follow-through note for low-cash under-followed pledge runs | No mechanics |
| `v0.10.24` | Bounded MCP trigger/control validation | The note appears in targeted trigger runs and stays absent in nearby controls | No |

## Synthesis Findings

1. The access-heavy evidence path has produced a bounded product explanation,
   not a mechanics finding. The relevant intervention is now covered in the
   competitive debrief surface.
2. The `v0.10.24` trigger/control artifact validates the debrief note's surface
   behavior for deterministic policies at seed `42`, across Normal and Hard
   difficulty.
3. The evidence still does not show that access pledges are overpowered,
   underpriced, too available, or mechanically defective. The accepted command
   streams remain valid and replayable.
4. Future access-related work should start from a broader evidence question:
   whether players can connect public commitments, cash limits, operational
   follow-through, payer strategy, and final outcomes across repeated play.
5. Additional runtime changes should require a later artifact that names a
   concrete mechanics problem rather than relying on repeated pledge counts,
   retry metadata, or debrief visibility alone.

## Recommended Routing

For the next PR-sized slice, prefer one of these evidence-led paths:

- a broader Phase 7 synthesis comparing multiple recent competitive playtest
  findings for teachability, debrief coherence, and repeated-play interest;
- a guidance or command-surface review only if a new artifact identifies a
  concrete player-facing comprehension gap;
- a runtime mechanics investigation only if a later artifact identifies a
  specific command-cost, balance, validation, or strategic-behavior defect.

Do not promote access-pledge cooldowns, effect tuning, action-cost changes,
difficulty adjustment, or new runtime validation from the current evidence.

## Evidence Limits

- The access evidence is simulated-agent, deterministic-policy, and
  operator-authored evidence, not human play or classroom evidence.
- The `v0.10.24` validation matrix is bounded to seed `42`, Normal/Hard
  difficulty, and trigger/control policies designed to exercise the debrief
  condition.
- The validation artifact is MCP wrapper evidence, not a full replay artifact
  or a measurement of learning.
- This synthesis supports development routing, not empirical calibration,
  policy validity, human-learning claims, or balance validation.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.25-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
