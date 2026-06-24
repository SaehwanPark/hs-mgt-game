use crate::cli::strategy::*;
use crate::model::*;
use crate::replay::replay;

#[test]
fn interactive_history_matches_access_stabilization_preset() {
  let ruleset = default_ruleset();
  let preset =
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
  let interactive =
    build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();

  assert_eq!(interactive, preset);
}
#[test]
fn interactive_history_replays_with_matching_state_hashes() {
  let ruleset = default_ruleset();
  let history =
    build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();

  assert_eq!(history.transitions.len(), 5);
  assert_eq!(
    replay(&history, &ruleset).unwrap().final_state,
    history.transitions.last().unwrap().next
  );
}
#[test]
fn each_strategy_path_builds_replayable_history() {
  let ruleset = default_ruleset();

  for choice in [
    StrategyPath::AccessStabilization,
    StrategyPath::FiscalCaution,
    StrategyPath::AggressiveBargaining,
  ] {
    let history = build_history_for_strategy(choice, DEFAULT_SEED, &ruleset).unwrap();
    let final_state = history.transitions.last().unwrap().next.clone();

    assert_eq!(history.transitions.len(), 5);
    assert_eq!(replay(&history, &ruleset).unwrap().final_state, final_state);
  }
}
#[test]
fn fiscal_caution_accepts_rate_and_proceeds_with_mandate() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::FiscalCaution, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[0].actor_decision.decision,
    ActorDecision::Insurer(InsurerDecision::Accept)
  );
  assert_eq!(
    history.transitions[1].actor_decision.decision,
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate)
  );
}
#[test]
fn aggressive_bargaining_rejects_rate_and_escalates_oversight() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AggressiveBargaining, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[0].actor_decision.decision,
    ActorDecision::Insurer(InsurerDecision::Reject)
  );
  assert_eq!(
    history.transitions[1].actor_decision.decision,
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight)
  );
}

#[test]
fn fiscal_caution_triggers_limited_support_on_workforce_turn() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::FiscalCaution, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[2].actor_decision.decision,
    ActorDecision::Labor(LaborDecision::LimitedSupport)
  );
}
#[test]
fn aggressive_bargaining_triggers_coalition_withdrawal_on_fourth_turn() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AggressiveBargaining, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[3].actor_decision.decision,
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal)
  );
}
#[test]
fn fiscal_caution_triggers_limited_coalition_participation() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::FiscalCaution, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[3].actor_decision.decision,
    ActorDecision::Coalition(CoalitionDecision::LimitedParticipation)
  );
}
#[test]
fn aggressive_bargaining_triggers_work_action_on_workforce_turn() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AggressiveBargaining, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[2].actor_decision.decision,
    ActorDecision::Labor(LaborDecision::WorkAction)
  );
}
#[test]
fn later_turn_can_revise_prior_reported_access_in_observation() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(history.transitions[1].observation.prior_access_revision, -1);
  assert_eq!(history.transitions[0].observation.prior_access_revision, 0);
}
#[test]
fn access_stabilization_triggers_full_coalition_partnership() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(
    history.transitions[3].actor_decision.decision,
    ActorDecision::Coalition(CoalitionDecision::FullPartnership)
  );
}
