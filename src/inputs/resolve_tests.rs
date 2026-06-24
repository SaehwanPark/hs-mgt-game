use crate::inputs::resolve_inputs;
use crate::model::{DEFAULT_SEED, default_ruleset, genesis_state};

#[test]
fn default_seed_resolves_identical_inputs_for_same_turn() {
  let ruleset = default_ruleset();
  let prior = genesis_state();

  let first = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
  let second = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);

  assert_eq!(first, second);
}
#[test]
fn different_seeds_can_change_resolved_inputs() {
  let ruleset = default_ruleset();
  let prior = genesis_state();

  let default_inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
  let alternate_inputs = resolve_inputs(99, &prior, &ruleset);

  assert_ne!(default_inputs, alternate_inputs);
}
#[test]
fn seed_zero_resolves_bounded_inputs() {
  let ruleset = default_ruleset();
  let inputs = resolve_inputs(0, &genesis_state(), &ruleset);

  assert!((-5..=5).contains(&inputs.measurement_noise));
  assert!((0..=100).contains(&inputs.delayed_access_report));
  assert!((-5..=0).contains(&inputs.labor_sick_call_delta));
  assert!((1..=6).contains(&inputs.policy_signal));
  assert!((1..=6).contains(&inputs.coalition_leverage_signal));
  assert!((-3..=3).contains(&inputs.access_measurement_revision));
}
#[test]
fn genesis_turn_has_no_access_measurement_revision() {
  let ruleset = default_ruleset();
  let inputs = resolve_inputs(DEFAULT_SEED, &genesis_state(), &ruleset);

  assert_eq!(inputs.access_measurement_revision, 0);
}

#[test]
fn competitor_market_signal_is_zero_before_fifth_turn() {
  let ruleset = default_ruleset();
  let mut prior = genesis_state();
  for turn in 0..4 {
    prior.turn = turn;
    let inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
    assert_eq!(inputs.competitor_market_signal, 0);
  }
}

#[test]
fn competitor_market_signal_resolves_on_fifth_turn() {
  let ruleset = default_ruleset();
  let mut prior = genesis_state();
  prior.turn = 4;
  let inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);

  assert_eq!(inputs.competitor_market_signal, 6);
}
