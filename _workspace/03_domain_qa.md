# Domain QA - Gameplay Playtest (v0.1.42)

**Status:** pass

## Reviewed Inputs

- User request to test and review gameplay.
- 3 subagent playtest logs and feedback reports in `scratch/`.
- Playtest findings report: `docs/playtest-findings-v0.1.42.md`.
- Canonical docs: `README.md`, `docs/design_principles.md`, `docs/external-playtest-protocol.md`.

## Findings

- **Strategic Tension Validation:** Checked that insurer negotiations and competitor capacity expansions create real tradeoffs. The rejections of rate requests under "adequate" access (71 index) conform to the rule that actor observations and utility functions are distinct from player desires.
- **Winnability Check:** The game is winnable under conservative play (fiscal cautions), but extremely difficult and high-risk under aggressive growth. This matches the project's strategic goals of teaching that hospital expansion consumes cash faster than commercial rate relief can offset, illustrating systemic dynamics rather than single-metric optimization.
- **Fog of War / Observability:** Confirmed that rival public actions are correctly lagged by 1 month, and that `monitor` commands retrieve accurate hidden states, reinforcing the separation of true state from actor beliefs.
- **Determinism Boundary:** Tested that runs are reproducible. Seed 42 runs for each strategy profile yielded the same final state hashes across multiple subagent invocations, verifying that the stochastic inputs boundary works correctly.

## Required Fixes

None. The simulation and interface logic operated without failure. However, we note that insurer rate negotiation leverage and workforce salary inflation dynamics should be documented more clearly in future player manuals.

## Residual Risks

- **Short Bounded Preview:** The competitive campaign is currently limited to a 3-month preview. Longer 24-month campaigns could expose scaling issues or compounding cash runway strains not visible in the first three months.
- **Rival AI Calibration:** AI behavior is currently deterministic based on seed and difficulty. Future work must verify that CPU systems do not have a single trivial exploit or lock the player into defensive bed expansions indefinitely.

## Verification Evidence

- Run log for `player_fiscal` completed both campaigns with final state hashes:
  - Stabilization: `78c0a130398a6b0b`
  - Competitive: `3c0634b870c2d0cd`
- Run log for `player_growth` completed with cash = 5 (critical risk).
- Run log for `player_balanced` completed with cash = 25.
- All cargo tests pass.
