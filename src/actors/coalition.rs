use crate::model::{
  ActorDecision, ActorDecisionRecord, CoalitionDecision, Observation, ResolvedInputs, Ruleset,
};

pub fn coalition_decision(
  prior_community_trust: i32,
  coalition_investment: i32,
  shared_access_commitment: i32,
  observation: &Observation,
  inputs: &ResolvedInputs,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let strong_investment_threshold = ruleset.minimum_coalition_investment * 2 + 2;
  let strong_commitment_threshold = ruleset.minimum_shared_access_commitment * 2;
  let strong_offer = coalition_investment >= strong_investment_threshold
    && shared_access_commitment >= strong_commitment_threshold;
  let credible_offer = coalition_investment >= ruleset.minimum_coalition_investment
    && shared_access_commitment >= ruleset.minimum_shared_access_commitment;

  let (decision, rationale) = if strong_offer {
    (
      CoalitionDecision::FullPartnership,
      format!(
        "Coalition investment {coalition_investment} and shared access commitment {shared_access_commitment} give the coalition a defensible partnership path under reported access {} and leverage {}.",
        observation.reported_access_index, inputs.coalition_leverage_signal
      ),
    )
  } else if credible_offer
    && coalition_investment <= ruleset.minimum_coalition_investment + 1
    && shared_access_commitment <= ruleset.minimum_shared_access_commitment + 1
    && (inputs.coalition_leverage_signal >= 4 || prior_community_trust < 62)
  {
    (
      CoalitionDecision::CoalitionWithdrawal,
      format!(
        "Coalition investment {coalition_investment} and shared access commitment {shared_access_commitment} are too weak after community trust fell to {prior_community_trust} under leverage {}.",
        inputs.coalition_leverage_signal
      ),
    )
  } else if credible_offer {
    (
      CoalitionDecision::LimitedParticipation,
      format!(
        "Coalition investment {coalition_investment} and shared access commitment {shared_access_commitment} are credible but do not justify full partnership under community trust {prior_community_trust}."
      ),
    )
  } else {
    (
      CoalitionDecision::CoalitionWithdrawal,
      format!(
        "Coalition investment {coalition_investment} and shared access commitment {shared_access_commitment} fall below credible thresholds {} and {} under leverage {}.",
        ruleset.minimum_coalition_investment,
        ruleset.minimum_shared_access_commitment,
        inputs.coalition_leverage_signal
      ),
    )
  };

  ActorDecisionRecord {
    actor: "regional_provider_coalition",
    decision: ActorDecision::Coalition(decision),
    rationale,
  }
}
