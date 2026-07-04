# Domain QA - Nursing Workforce & Retention Ledger (Phase 4)

## Status
**FIX**

## Reviewed Inputs
- [docs/workforce-ledger.md](file:///home/saehwan/repos/hs-mgt-game/docs/workforce-ledger.md)
- [docs/evidence-registry.md](file:///home/saehwan/repos/hs-mgt-game/docs/evidence-registry.md)
- [src/actors/labor.rs](file:///home/saehwan/repos/hs-mgt-game/src/actors/labor.rs)
- [src/sim/transition.rs](file:///home/saehwan/repos/hs-mgt-game/src/sim/transition.rs)
- [src/sim/transition_competitive.rs](file:///home/saehwan/repos/hs-mgt-game/src/sim/transition_competitive.rs)
- [src/sim/effects_competitive.rs](file:///home/saehwan/repos/hs-mgt-game/src/sim/effects_competitive.rs)
- [src/model/competitive_command.rs](file:///home/saehwan/repos/hs-mgt-game/src/model/competitive_command.rs)
- [src/model/ruleset.rs](file:///home/saehwan/repos/hs-mgt-game/src/model/ruleset.rs)

---

## Findings

### Finding 1: Timing and Semantic Contradiction in `Pending Hire Trust Drop`
- **Severity:** **MAJOR**
- **Parameter/Formula:** `workforce_trust -= headcount` (Row 7 in [docs/workforce-ledger.md](file:///home/saehwan/repos/hs-mgt-game/docs/workforce-ledger.md))
- **Reference File:** [effects_competitive.rs:L61](file:///home/saehwan/repos/hs-mgt-game/src/sim/effects_competitive.rs#L61)
- **Description:** 
  The ledger states: *"Trust declines temporarily when staff are recruited but not yet on board, reflecting immediate workload pressure on existing staff."*
  However, in the codebase:
  1. The trust penalty of `-headcount` is applied in `apply_pending_effect` when the `PendingEffectKind::Recruit` resolves (meaning the staff *are* now on board and `staffed_beds` increases). No penalty is applied when the command is queued (the "pending" state).
  2. This timing is reversed: trust is unchanged while pending, but drops permanently when they arrive.
  3. The effect direction is counter-intuitive: hiring nurses *reduces* trust permanently, and there is no competitive command or mechanism in the codebase to increase or recover `workforce_trust`.
  4. While this doesn't break tests because the labor actor is not active in competitive mode, it represents a broken simulation logic for workforce dynamics in the competitive campaign.

### Finding 2: Line Reference Mismatch in `Nurse Recruitment Cost`
- **Severity:** **LOW**
- **Parameter/Formula:** `$5` per nurse unit (AP cost = 1) (Row 3 in [docs/workforce-ledger.md](file:///home/saehwan/repos/hs-mgt-game/docs/workforce-ledger.md))
- **Reference File:** [competitive_command.rs:L94](file:///home/saehwan/repos/hs-mgt-game/src/model/competitive_command.rs#L94)
- **Description:** 
  The code location is listed as `competitive_command.rs:L94`. However, `L94` in `competitive_command.rs` is `impl ProjectKind {`, while the actual cost logic is implemented in `CompetitiveCommand::action_cost()` at lines 125-127.

### Finding 3: Inconsistent Workforce Trust Treatment in Competitive Bed Investment
- **Severity:** **MINOR**
- **Parameter/Formula:** Bed additions in competitive campaign (`InvestDomain::Beds`).
- **Description:** 
  In the stabilization campaign, adding staffed beds without hiring nurses penalizes workforce trust (`next.workforce_trust -= add_staffed_beds / 4`, citing Aiken 2002). However, in the competitive campaign, `InvestDomain::Beds` directly adds staffed beds without any trust penalty (see [transition_competitive.rs:L163-173](file:///home/saehwan/repos/hs-mgt-game/src/sim/transition_competitive.rs#L163-L173)), whereas `Recruit` (hiring nurses) does. This is conceptually backwards: adding beds without recruiting should penalize trust; recruiting nurses should not penalize trust (or at least less so than adding raw beds).

---

## Required Fixes

1. **Clarify or Fix `Pending Hire Trust Drop`:**
   - *Option A (Code Fix - Recommended):* To model a *temporary* trust drop during the recruitment delay, apply the trust penalty (`system.workforce_trust -= headcount`) in `apply_command` in `src/sim/transition_competitive.rs` when the recruitment is queued. Then, apply a corresponding trust recovery (`system.workforce_trust += headcount`) in `effects_competitive.rs` when the recruitment resolves.
   - *Option B (Documentation Fix):* If the penalty is meant to be permanent and occur at resolution, update the ledger's name, code location description, and design rationale to reflect the permanent drop.
2. **Update Line References:**
   - Change the codebase link for `Nurse Recruitment Cost` in `docs/workforce-ledger.md` from `competitive_command.rs:L94` to `src/model/competitive_command.rs#L125-127`.

---

## Residual Risks
- **Inactive Labor Actor in Competitive Campaign:** Currently, `workforce_trust` has no feedback loop in the competitive campaign (the labor actor is not invoked in `transition_competitive.rs`). Any changes to workforce trust are purely metric-level until the labor actor decision is integrated into the competitive campaign loop.

---

## Verification Evidence
- All 233 unit/integration tests passed successfully under `cargo test`.
- Verified file lines and codebase logic manually.
