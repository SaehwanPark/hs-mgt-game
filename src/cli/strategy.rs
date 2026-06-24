use crate::inputs::resolve_inputs;
use crate::model::{
  History, PlayerCommand, Ruleset, StrategyPath, StrategyPlan, ValidationError, genesis_state,
};
use crate::sim::transition;

pub fn build_history_for_strategy(
  choice: StrategyPath,
  seed: u64,
  ruleset: &Ruleset,
) -> Result<History, ValidationError> {
  let plan = strategy_plan(choice);
  let genesis = genesis_state();
  let first_inputs = resolve_inputs(seed, &genesis, ruleset);
  let first = transition(&genesis, plan.first_command.clone(), first_inputs, ruleset)?;
  let second_inputs = resolve_inputs(seed, &first.next, ruleset);
  let second = transition(
    &first.next,
    plan.second_command.clone(),
    second_inputs,
    ruleset,
  )?;
  let third_inputs = resolve_inputs(seed, &second.next, ruleset);
  let third = transition(
    &second.next,
    plan.third_command.clone(),
    third_inputs,
    ruleset,
  )?;
  let fourth_inputs = resolve_inputs(seed, &third.next, ruleset);
  let fourth = transition(
    &third.next,
    plan.fourth_command.clone(),
    fourth_inputs,
    ruleset,
  )?;
  let fifth_inputs = resolve_inputs(seed, &fourth.next, ruleset);
  let fifth = transition(
    &fourth.next,
    plan.fifth_command.clone(),
    fifth_inputs,
    ruleset,
  )?;

  Ok(History {
    genesis,
    transitions: vec![first, second, third, fourth, fifth],
  })
}

pub fn build_history_interactive(
  seed: u64,
  ruleset: &Ruleset,
  commands: [PlayerCommand; 5],
) -> Result<History, ValidationError> {
  let genesis = genesis_state();
  let first_inputs = resolve_inputs(seed, &genesis, ruleset);
  let first = transition(&genesis, commands[0].clone(), first_inputs, ruleset)?;
  let second_inputs = resolve_inputs(seed, &first.next, ruleset);
  let second = transition(&first.next, commands[1].clone(), second_inputs, ruleset)?;
  let third_inputs = resolve_inputs(seed, &second.next, ruleset);
  let third = transition(&second.next, commands[2].clone(), third_inputs, ruleset)?;
  let fourth_inputs = resolve_inputs(seed, &third.next, ruleset);
  let fourth = transition(&third.next, commands[3].clone(), fourth_inputs, ruleset)?;
  let fifth_inputs = resolve_inputs(seed, &fourth.next, ruleset);
  let fifth = transition(&fourth.next, commands[4].clone(), fifth_inputs, ruleset)?;

  Ok(History {
    genesis,
    transitions: vec![first, second, third, fourth, fifth],
  })
}

pub fn default_interactive_commands() -> [PlayerCommand; 5] {
  let plan = strategy_plan(StrategyPath::AccessStabilization);
  [
    plan.first_command,
    plan.second_command,
    plan.third_command,
    plan.fourth_command,
    plan.fifth_command,
  ]
}
pub fn strategy_plan(choice: StrategyPath) -> StrategyPlan {
  match choice {
    StrategyPath::AccessStabilization => StrategyPlan {
      name: "Access stabilization",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 8,
        capital_spend: 18,
        requested_commercial_rate: 112,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 10,
        access_commitment: 7,
      },
      third_command: PlayerCommand::RespondToWorkforcePressure {
        retention_spend: 14,
        schedule_relief_commitment: 8,
      },
      fourth_command: PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment: 12,
        shared_access_commitment: 8,
      },
      fifth_command: PlayerCommand::RespondToCompetitorCapacityMove {
        defensive_capital_commitment: 14,
        access_posture: 8,
      },
    },
    StrategyPath::FiscalCaution => StrategyPlan {
      name: "Fiscal caution",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 4,
        capital_spend: 10,
        requested_commercial_rate: 104,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 4,
        access_commitment: 5,
      },
      third_command: PlayerCommand::RespondToWorkforcePressure {
        retention_spend: 8,
        schedule_relief_commitment: 5,
      },
      fourth_command: PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment: 6,
        shared_access_commitment: 5,
      },
      fifth_command: PlayerCommand::RespondToCompetitorCapacityMove {
        defensive_capital_commitment: 8,
        access_posture: 5,
      },
    },
    StrategyPath::AggressiveBargaining => StrategyPlan {
      name: "Aggressive bargaining",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 2,
        capital_spend: 5,
        requested_commercial_rate: 120,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 2,
        access_commitment: 3,
      },
      third_command: PlayerCommand::RespondToWorkforcePressure {
        retention_spend: 2,
        schedule_relief_commitment: 2,
      },
      fourth_command: PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment: 4,
        shared_access_commitment: 4,
      },
      fifth_command: PlayerCommand::RespondToCompetitorCapacityMove {
        defensive_capital_commitment: 4,
        access_posture: 4,
      },
    },
  }
}
