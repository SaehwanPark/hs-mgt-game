use crate::cli::parse::*;
use crate::cli::strategy::{default_interactive_commands, strategy_plan};
use crate::inputs::resolve_inputs;
use crate::model::*;
use crate::sim::transition;

#[test]
fn parse_stabilize_access_command_accepts_valid_input() {
  let command = parse_stabilize_access_command("8 18 112\n").unwrap();

  assert_eq!(
    command,
    PlayerCommand::StabilizeAccess {
      add_staffed_beds: 8,
      capital_spend: 18,
      requested_commercial_rate: 112,
    }
  );
}
#[test]
fn parse_stabilize_access_command_defaults_on_empty_input() {
  assert_eq!(
    parse_stabilize_access_command("\n").unwrap(),
    default_interactive_commands()[0]
  );
}
#[test]
fn parse_stabilize_access_command_rejects_malformed_input() {
  assert!(parse_stabilize_access_command("8 18\n").is_err());
}
#[test]
fn parse_policy_command_defaults_on_empty_input() {
  assert_eq!(
    parse_policy_command("\n").unwrap(),
    default_interactive_commands()[1]
  );
}
#[test]
fn parse_workforce_command_defaults_on_empty_input() {
  assert_eq!(
    parse_workforce_command("\n").unwrap(),
    default_interactive_commands()[2]
  );
}
#[test]
fn parse_coalition_command_defaults_on_empty_input() {
  assert_eq!(
    parse_coalition_command("\n").unwrap(),
    default_interactive_commands()[3]
  );
}
#[test]
fn describe_command_defaults_matches_access_stabilization_plan() {
  let plan = strategy_plan(StrategyPath::AccessStabilization);
  let defaults = default_interactive_commands();

  assert_eq!(
    describe_command_defaults(&defaults[0]),
    "Enter for defaults: 8 18 112"
  );
  assert_eq!(
    describe_command_defaults(&plan.first_command),
    describe_command_defaults(&defaults[0])
  );
}
#[test]
fn parse_policy_command_rejects_out_of_bounds_values_at_transition() {
  let ruleset = default_ruleset();
  let command = parse_policy_command("25 5\n").unwrap();

  assert_eq!(
    transition(
      &genesis_state(),
      command,
      resolve_inputs(DEFAULT_SEED, &genesis_state(), &ruleset),
      &ruleset
    ),
    Err(ValidationError::AdvocacySpendTooHigh {
      requested: 25,
      available_limit: 20
    })
  );
}
