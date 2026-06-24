use crate::model::{PlayerCommand, StrategyCommitments, StrategyPath, StrategyPlan, WorldState};

use super::super::strategy::strategy_plan;

pub fn print_pre_run_briefing(state: &WorldState) {
  for line in executive_dashboard(state) {
    println!("{line}");
  }
  for line in strategy_previews() {
    println!("{line}");
  }
}

pub fn executive_dashboard(state: &WorldState) -> Vec<String> {
  vec![
    "Executive dashboard".to_string(),
    format!(
      "  Cash {cash}, staffed beds {staffed_beds}, access {access}, quality {quality}",
      cash = state.cash,
      staffed_beds = state.staffed_beds,
      access = state.access_index,
      quality = state.quality_index
    ),
    format!(
      "  Workforce trust {workforce}, community trust {community}, commercial rate {rate}, policy pressure {policy}",
      workforce = state.workforce_trust,
      community = state.community_trust,
      rate = state.commercial_rate,
      policy = state.policy_pressure
    ),
  ]
}

pub fn strategy_previews() -> Vec<String> {
  [
    StrategyPath::AccessStabilization,
    StrategyPath::FiscalCaution,
    StrategyPath::AggressiveBargaining,
  ]
  .iter()
  .enumerate()
  .map(|(index, choice)| {
    let plan = strategy_plan(*choice);
    format!(
      "  {}. {}: {}",
      index + 1,
      plan.name,
      describe_strategy_commitments(&plan)
    )
  })
  .collect()
}

pub fn describe_strategy_commitments(plan: &StrategyPlan) -> String {
  let commitments = strategy_commitments(plan);

  format!(
    "adds {staffed_beds} staffed beds, requests commercial rate {requested_commercial_rate}, spends {total_spend} total resource units, and commits {total_commitment} access/workforce/coalition units",
    staffed_beds = commitments.staffed_beds,
    requested_commercial_rate = commitments.requested_commercial_rate,
    total_spend = commitments.capital_spend
      + commitments.advocacy_spend
      + commitments.retention_spend
      + commitments.coalition_investment
      + commitments.defensive_capital_commitment,
    total_commitment = commitments.access_commitment
      + commitments.schedule_relief_commitment
      + commitments.shared_access_commitment
      + commitments.access_posture
  )
}

pub fn strategy_commitments(plan: &StrategyPlan) -> StrategyCommitments {
  let &PlayerCommand::StabilizeAccess {
    add_staffed_beds,
    capital_spend,
    requested_commercial_rate,
  } = &plan.first_command
  else {
    panic!("strategy preview expects a capacity command first");
  };

  let &PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend,
    access_commitment,
  } = &plan.second_command
  else {
    panic!("strategy preview expects a policy response command second");
  };

  let &PlayerCommand::RespondToWorkforcePressure {
    retention_spend,
    schedule_relief_commitment,
  } = &plan.third_command
  else {
    panic!("strategy preview expects a workforce response command third");
  };

  let &PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment,
    shared_access_commitment,
  } = &plan.fourth_command
  else {
    panic!("strategy preview expects a coalition command fourth");
  };

  let &PlayerCommand::RespondToCompetitorCapacityMove {
    defensive_capital_commitment,
    access_posture,
  } = &plan.fifth_command
  else {
    panic!("strategy preview expects a competitor response command fifth");
  };

  StrategyCommitments {
    staffed_beds: add_staffed_beds,
    capital_spend,
    requested_commercial_rate,
    advocacy_spend,
    access_commitment,
    retention_spend,
    schedule_relief_commitment,
    coalition_investment,
    shared_access_commitment,
    defensive_capital_commitment,
    access_posture,
  }
}
