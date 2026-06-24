use crate::cli::build_history_for_strategy;
use crate::model::*;
use crate::replay::replay;
use crate::sim::transition;

#[test]
fn replay_reproduces_committed_final_state() {
  let ruleset = default_ruleset();
  let genesis = genesis_state();
  let first = transition(
    &genesis,
    PlayerCommand::StabilizeAccess {
      add_staffed_beds: 8,
      capital_spend: 18,
      requested_commercial_rate: 112,
    },
    ResolvedInputs {
      measurement_noise: -2,
      delayed_access_report: 67,
      labor_sick_call_delta: -3,
      policy_signal: 4,
      coalition_leverage_signal: 1,
      access_measurement_revision: 0,
      competitor_market_signal: 0,
    },
    &ruleset,
  )
  .unwrap();
  let history = History {
    genesis,
    transitions: vec![first.clone()],
  };

  assert_eq!(replay(&history, &ruleset).unwrap().final_state, first.next);
}
#[test]
fn replay_detects_committed_state_hash_mismatch() {
  let ruleset = default_ruleset();
  let genesis = genesis_state();
  let mut first = transition(
    &genesis,
    PlayerCommand::StabilizeAccess {
      add_staffed_beds: 8,
      capital_spend: 18,
      requested_commercial_rate: 112,
    },
    ResolvedInputs {
      measurement_noise: -2,
      delayed_access_report: 67,
      labor_sick_call_delta: -3,
      policy_signal: 4,
      coalition_leverage_signal: 1,
      access_measurement_revision: 0,
      competitor_market_signal: 0,
    },
    &ruleset,
  )
  .unwrap();
  let actual = first.state_hash.clone();
  first.state_hash = "0000000000000000".to_string();
  first.next.turn = 99;
  let history = History {
    genesis,
    transitions: vec![first],
  };

  assert_eq!(
    replay(&history, &ruleset),
    Err(ReplayError::StateHashMismatch {
      turn: 1,
      expected: "0000000000000000".to_string(),
      actual,
    })
  );
}
#[test]
fn replay_reproduces_two_transition_history() {
  let ruleset = default_ruleset();
  let genesis = genesis_state();
  let first = transition(
    &genesis,
    PlayerCommand::StabilizeAccess {
      add_staffed_beds: 8,
      capital_spend: 18,
      requested_commercial_rate: 112,
    },
    ResolvedInputs {
      measurement_noise: -2,
      delayed_access_report: 67,
      labor_sick_call_delta: -3,
      policy_signal: 4,
      coalition_leverage_signal: 1,
      access_measurement_revision: 0,
      competitor_market_signal: 0,
    },
    &ruleset,
  )
  .unwrap();
  let second = transition(
    &first.next,
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend: 10,
      access_commitment: 7,
    },
    ResolvedInputs {
      measurement_noise: 1,
      delayed_access_report: 69,
      labor_sick_call_delta: 0,
      policy_signal: 4,
      coalition_leverage_signal: 1,
      access_measurement_revision: 0,
      competitor_market_signal: 0,
    },
    &ruleset,
  )
  .unwrap();
  let history = History {
    genesis,
    transitions: vec![first, second.clone()],
  };

  assert_eq!(replay(&history, &ruleset).unwrap().final_state, second.next);
}
#[test]
fn replay_reproduces_four_transition_history() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
  let final_state = history.transitions.last().unwrap().next.clone();

  assert_eq!(history.transitions.len(), 5);
  assert_eq!(replay(&history, &ruleset).unwrap().final_state, final_state);
}
