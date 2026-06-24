use crate::cli::beginner::{beginner_options, parse_beginner_choice};
use crate::cli::strategy::{build_history_for_strategy, strategy_plan};
use crate::model::{StrategyPath, default_ruleset};

#[test]
fn beginner_options_have_metadata_for_each_turn() {
  for turn in 1..=5 {
    for option in beginner_options(turn) {
      assert!(!option.pros.is_empty());
      assert!(!option.cons.is_empty());
      assert!(!option.tradeoff.is_empty());
      assert!(!option.recommendability.is_empty());
    }
  }
}

#[test]
fn beginner_metadata_avoids_actor_outcome_spoilers() {
  for turn in 1..=5 {
    for option in beginner_options(turn) {
      let text = format!(
        "{} {} {} {}",
        option.pros, option.cons, option.tradeoff, option.recommendability
      );
      let lower = text.to_ascii_lowercase();
      assert!(!lower.contains("reject"));
      assert!(!lower.contains("work action"));
      assert!(!lower.contains("state hash"));
    }
  }
}

#[test]
fn beginner_choice_maps_to_preset_commands() {
  for turn in 1..=5 {
    for (index, path) in [
      StrategyPath::AccessStabilization,
      StrategyPath::FiscalCaution,
      StrategyPath::AggressiveBargaining,
    ]
    .iter()
    .enumerate()
    {
      let choice = parse_beginner_choice(&(index + 1).to_string(), turn).unwrap();
      let plan = strategy_plan(*path);
      let expected = match turn {
        1 => plan.first_command.clone(),
        2 => plan.second_command.clone(),
        3 => plan.third_command.clone(),
        4 => plan.fourth_command.clone(),
        5 => plan.fifth_command.clone(),
        _ => unreachable!(),
      };
      assert_eq!(choice, expected);
    }
  }
}

#[test]
fn beginner_all_ones_matches_access_stabilization_preset() {
  let ruleset = default_ruleset();
  let preset = build_history_for_strategy(StrategyPath::AccessStabilization, 42, &ruleset).unwrap();

  let commands = [
    parse_beginner_choice("1", 1).unwrap(),
    parse_beginner_choice("1", 2).unwrap(),
    parse_beginner_choice("1", 3).unwrap(),
    parse_beginner_choice("1", 4).unwrap(),
    parse_beginner_choice("1", 5).unwrap(),
  ];

  let interactive = crate::cli::build_history_interactive(42, &ruleset, commands).unwrap();
  assert_eq!(interactive, preset);
}
