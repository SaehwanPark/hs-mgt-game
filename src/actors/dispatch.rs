use crate::model::{
  ActorDecisionRecord, Observation, PlayerCommand, ResolvedInputs, Ruleset, WorldState,
};

use super::{
  coalition::coalition_decision, insurer::insurer_decision, labor::labor_decision,
  state_policy::state_policy_decision,
};

pub fn actor_decision(
  command: &PlayerCommand,
  prior: &WorldState,
  observation: &Observation,
  inputs: &ResolvedInputs,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  match command {
    PlayerCommand::StabilizeAccess {
      requested_commercial_rate,
      ..
    } => insurer_decision(*requested_commercial_rate, observation, ruleset),
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => state_policy_decision(
      *advocacy_spend,
      *access_commitment,
      observation,
      inputs,
      ruleset,
    ),
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => labor_decision(
      prior.workforce_trust,
      *retention_spend,
      *schedule_relief_commitment,
      observation,
      inputs,
      ruleset,
    ),
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => coalition_decision(
      prior.community_trust,
      *coalition_investment,
      *shared_access_commitment,
      observation,
      inputs,
      ruleset,
    ),
  }
}
