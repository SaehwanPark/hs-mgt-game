use crate::cli::build_history_for_strategy;
use crate::debrief::counterfactual_difference_lines;
use crate::model::{PlayerCommand, StrategyPath, default_ruleset};

fn sample_history() -> crate::model::History {
  build_history_for_strategy(StrategyPath::AccessStabilization, 42, &default_ruleset()).unwrap()
}

#[test]
fn comparison_is_deterministic_and_reports_unchanged_runs() {
  let history = sample_history();
  let lines = counterfactual_difference_lines(&history, &history).join("\n");

  assert!(lines.contains("Genesis parity: same starting state."));
  assert!(lines.contains("Resolved-input parity: same recorded inputs."));
  assert!(lines.contains("Committed state difference: none."));
  assert!(lines.contains("Attributed effect difference: none."));
  assert!(lines.contains("no option is marked correct"));
}

#[test]
fn comparison_shows_command_state_and_effect_differences() {
  let baseline = sample_history();
  let mut alternative = baseline.clone();
  alternative.transitions[0].command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 0,
    capital_spend: 0,
    requested_commercial_rate: 0,
  };
  alternative.transitions[0].next.access_index += 3;
  alternative.transitions[0].effects[0].delta += 2;

  let lines = counterfactual_difference_lines(&baseline, &alternative).join("\n");

  assert!(lines.contains("Baseline command:"));
  assert!(lines.contains("Alternative command:"));
  assert!(lines.contains("Committed state difference: access_index"));
  assert!(lines.contains("Attributed effect difference:"));
}

#[test]
fn comparison_uses_written_fallback_for_incompatible_or_stochastic_runs() {
  let baseline = sample_history();
  let mut mismatched_genesis = baseline.clone();
  mismatched_genesis.genesis.cash += 1;
  assert!(
    counterfactual_difference_lines(&baseline, &mismatched_genesis)
      .join("\n")
      .contains("Written fallback")
  );

  let mut different_inputs = baseline.clone();
  different_inputs.transitions[0]
    .resolved_inputs
    .policy_signal += 1;
  let lines = counterfactual_difference_lines(&baseline, &different_inputs).join("\n");
  assert!(lines.contains("different recorded inputs"));

  let mut extra_turn = baseline.clone();
  extra_turn.transitions.push(baseline.transitions[0].clone());
  let lines = counterfactual_difference_lines(&baseline, &extra_turn).join("\n");
  assert!(lines.contains("different recorded inputs"));
}
