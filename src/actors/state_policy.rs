use crate::model::{
  ActorDecision, ActorDecisionRecord, Observation, ResolvedInputs, Ruleset, StatePolicyDecision,
};

pub fn state_policy_decision(
  advocacy_spend: i32,
  access_commitment: i32,
  observation: &Observation,
  inputs: &ResolvedInputs,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let credible_commitment = access_commitment >= ruleset.minimum_access_commitment;
  let high_pressure = inputs.policy_signal >= 4 || observation.reported_access_index < 70;

  let (decision, rationale) = if credible_commitment && advocacy_spend >= 8 && high_pressure {
    (
      StatePolicyDecision::GrantFlexibility,
      format!(
        "Access commitment {access_commitment} and advocacy spend {advocacy_spend} give officials a defensible implementation path under reported access {}.",
        observation.reported_access_index
      ),
    )
  } else if credible_commitment {
    (
      StatePolicyDecision::ProceedWithMandate,
      format!(
        "Access commitment {access_commitment} is credible, but advocacy spend {advocacy_spend} does not justify delaying the mandate."
      ),
    )
  } else {
    (
      StatePolicyDecision::EscalateOversight,
      format!(
        "Access commitment {access_commitment} falls below the minimum credible commitment {}.",
        ruleset.minimum_access_commitment
      ),
    )
  };

  ActorDecisionRecord {
    actor: "state_policy_officials",
    decision: ActorDecision::StatePolicy(decision),
    rationale,
  }
}
