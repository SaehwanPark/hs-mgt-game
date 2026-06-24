use crate::model::{
  ActorDecision, ActorDecisionRecord, LaborDecision, Observation, ResolvedInputs, Ruleset,
};

pub fn labor_decision(
  prior_workforce_trust: i32,
  retention_spend: i32,
  schedule_relief_commitment: i32,
  observation: &Observation,
  inputs: &ResolvedInputs,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let sick_call_pressure = inputs.labor_sick_call_delta <= -3;
  let strong_retention_threshold = ruleset.minimum_retention_spend * 2 + 2;
  let strong_schedule_threshold = ruleset.minimum_schedule_relief * 2;
  let strong_offer = retention_spend >= strong_retention_threshold
    && schedule_relief_commitment >= strong_schedule_threshold;
  let credible_offer = retention_spend >= ruleset.minimum_retention_spend
    && schedule_relief_commitment >= ruleset.minimum_schedule_relief;
  let labor_pressure = sick_call_pressure || prior_workforce_trust < 60;

  let (decision, rationale) = if strong_offer && labor_pressure {
    (
      LaborDecision::Cooperative,
      format!(
        "Retention spend {retention_spend} and schedule relief {schedule_relief_commitment} address labor pressure with workforce trust {prior_workforce_trust} and reported access {}.",
        observation.reported_access_index
      ),
    )
  } else if credible_offer {
    (
      LaborDecision::LimitedSupport,
      format!(
        "Retention spend {retention_spend} and schedule relief {schedule_relief_commitment} are credible but do not fully offset sick-call pressure {}.",
        inputs.labor_sick_call_delta
      ),
    )
  } else {
    (
      LaborDecision::WorkAction,
      format!(
        "Retention spend {retention_spend} and schedule relief {schedule_relief_commitment} fall below credible thresholds {} and {} under workforce trust {prior_workforce_trust}.",
        ruleset.minimum_retention_spend, ruleset.minimum_schedule_relief
      ),
    )
  };

  ActorDecisionRecord {
    actor: "nursing_workforce",
    decision: ActorDecision::Labor(decision),
    rationale,
  }
}
