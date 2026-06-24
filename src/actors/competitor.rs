use crate::model::{
  ActorDecision, ActorDecisionRecord, CompetitorDecision, Observation, ResolvedInputs, Ruleset,
};

pub fn competitor_decision(
  defensive_capital_commitment: i32,
  access_posture: i32,
  observation: &Observation,
  inputs: &ResolvedInputs,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let strong_capital_threshold = ruleset.minimum_defensive_capital_commitment * 2 + 2;
  let strong_posture_threshold = ruleset.minimum_access_posture * 2;
  let strong_response = defensive_capital_commitment >= strong_capital_threshold
    && access_posture >= strong_posture_threshold;
  let credible_response = defensive_capital_commitment
    >= ruleset.minimum_defensive_capital_commitment
    && access_posture >= ruleset.minimum_access_posture;

  let (decision, rationale) = if strong_response {
    (
      CompetitorDecision::PartialRetreat,
      format!(
        "Defensive capital {defensive_capital_commitment} and access posture {access_posture} credibly defend share under reported access {} and market signal {}.",
        observation.reported_access_index, inputs.competitor_market_signal
      ),
    )
  } else if credible_response
    && defensive_capital_commitment <= ruleset.minimum_defensive_capital_commitment + 1
    && access_posture <= ruleset.minimum_access_posture + 1
    && inputs.competitor_market_signal >= 4
  {
    (
      CompetitorDecision::AccelerateExpansion,
      format!(
        "Defensive capital {defensive_capital_commitment} and access posture {access_posture} look too weak to deter expansion under market signal {}.",
        inputs.competitor_market_signal
      ),
    )
  } else if credible_response {
    (
      CompetitorDecision::HoldPosition,
      format!(
        "Defensive capital {defensive_capital_commitment} and access posture {access_posture} are credible but not strong enough to force retreat under market signal {}.",
        inputs.competitor_market_signal
      ),
    )
  } else {
    (
      CompetitorDecision::AccelerateExpansion,
      format!(
        "Defensive capital {defensive_capital_commitment} and access posture {access_posture} fall below credible thresholds {} and {} under market signal {}.",
        ruleset.minimum_defensive_capital_commitment,
        ruleset.minimum_access_posture,
        inputs.competitor_market_signal
      ),
    )
  };

  ActorDecisionRecord {
    actor: "competitor_health_system",
    decision: ActorDecision::Competitor(decision),
    rationale,
  }
}
