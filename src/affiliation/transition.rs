use crate::inputs::resolve_affiliation_inputs;
use crate::model::{
  AffiliationActorDecision, AffiliationCommand, AffiliationHistory, AffiliationPosture,
  AffiliationResolvedInputs, AffiliationRuleset, AffiliationStage, AffiliationStatus,
  AffiliationTransition, AffiliationValidationError, AffiliationWorldState, CommunityResponse,
  IntegrationDecision, LaborResponse, PartnerResponse, PayerResponse, ReviewResponse,
  hash_affiliation_state,
};

use super::observe::observe_affiliation;

pub fn validate_affiliation_command(
  prior: &AffiliationWorldState,
  command: &AffiliationCommand,
  ruleset: &AffiliationRuleset,
) -> Result<(), AffiliationValidationError> {
  if prior.stage == AffiliationStage::Complete || prior.turn >= crate::model::AFFILIATION_TURN_COUNT
  {
    return Err(AffiliationValidationError::TerminalState);
  }

  let expected = match prior.stage {
    AffiliationStage::AssessPartner => matches!(command, AffiliationCommand::AssessPartner),
    AffiliationStage::ChoosePosture => matches!(command, AffiliationCommand::ChoosePosture { .. }),
    AffiliationStage::NegotiateCommitments => match prior.status {
      AffiliationStatus::Pursuing => matches!(command, AffiliationCommand::SetCommitments { .. }),
      _ => matches!(command, AffiliationCommand::Hold),
    },
    AffiliationStage::SubmitReview => match prior.status {
      AffiliationStatus::PartnerAccepted | AffiliationStatus::PartnerConditioned => {
        matches!(command, AffiliationCommand::SubmitReview)
      }
      _ => matches!(command, AffiliationCommand::Hold),
    },
    AffiliationStage::ResolveReview => match prior.status {
      AffiliationStatus::ReviewPending => matches!(command, AffiliationCommand::AwaitReview),
      _ => matches!(command, AffiliationCommand::Hold),
    },
    AffiliationStage::IntegrateOrDecline => match prior.status {
      AffiliationStatus::Approved | AffiliationStatus::ConditionallyApproved => {
        matches!(command, AffiliationCommand::ChooseIntegration { .. })
      }
      _ => matches!(command, AffiliationCommand::Hold),
    },
    AffiliationStage::Complete => false,
  };
  if !expected {
    return Err(AffiliationValidationError::InvalidCommandForStatus);
  }

  if let AffiliationCommand::SetCommitments {
    community,
    workforce,
    continuity,
  } = command
  {
    for value in [*community, *workforce, *continuity] {
      if !(ruleset.min_commitment..=ruleset.max_commitment).contains(&value) {
        return Err(AffiliationValidationError::CommitmentOutOfRange {
          value,
          min: ruleset.min_commitment,
          max: ruleset.max_commitment,
        });
      }
    }
    let total = community + workforce + continuity;
    if total > ruleset.max_total_commitment {
      return Err(AffiliationValidationError::TotalCommitmentExceeded {
        total,
        max: ruleset.max_total_commitment,
      });
    }
    if prior.riverside.cash < total {
      return Err(AffiliationValidationError::InsufficientCash {
        required: total,
        available: prior.riverside.cash,
      });
    }
  }

  if matches!(command, AffiliationCommand::AssessPartner)
    && prior.riverside.cash < ruleset.assessment_cash_cost
  {
    return Err(AffiliationValidationError::InsufficientCash {
      required: ruleset.assessment_cash_cost,
      available: prior.riverside.cash,
    });
  }
  if matches!(command, AffiliationCommand::SubmitReview)
    && prior.riverside.cash < ruleset.review_submission_cash_cost
  {
    return Err(AffiliationValidationError::InsufficientCash {
      required: ruleset.review_submission_cash_cost,
      available: prior.riverside.cash,
    });
  }
  if matches!(
    command,
    AffiliationCommand::ChooseIntegration {
      decision: IntegrationDecision::Begin
    }
  ) && prior.riverside.cash < ruleset.integration_start_cash_cost
  {
    return Err(AffiliationValidationError::InsufficientCash {
      required: ruleset.integration_start_cash_cost,
      available: prior.riverside.cash,
    });
  }
  Ok(())
}

pub fn transition_affiliation(
  prior: &AffiliationWorldState,
  command: AffiliationCommand,
  observation: crate::model::AffiliationObservation,
  resolved_inputs: AffiliationResolvedInputs,
  ruleset: &AffiliationRuleset,
) -> Result<AffiliationTransition, AffiliationValidationError> {
  validate_affiliation_command(prior, &command, ruleset)?;
  if matches!(
    command,
    AffiliationCommand::ChooseIntegration {
      decision: IntegrationDecision::Begin
    }
  ) {
    let required = ruleset.integration_start_cash_cost + resolved_inputs.integration_drag;
    if prior.riverside.cash < required {
      return Err(AffiliationValidationError::InsufficientCash {
        required,
        available: prior.riverside.cash,
      });
    }
  }
  let mut next = prior.clone();
  let mut events = Vec::new();
  let mut effects = Vec::new();
  let mut decisions = Vec::new();

  match command {
    AffiliationCommand::AssessPartner => {
      next.riverside.cash = next
        .riverside
        .cash
        .saturating_sub(ruleset.assessment_cash_cost);
      let reported =
        (next.partner.condition_index + resolved_inputs.partner_report_noise).clamp(0, 100);
      next.partner.reported_condition = Some(if reported < 40 {
        crate::model::PartnerConditionBand::Fragile
      } else if reported < 70 {
        crate::model::PartnerConditionBand::Stable
      } else {
        crate::model::PartnerConditionBand::Strong
      });
      next.status = AffiliationStatus::Unassessed;
      events.push(event(
        "partner",
        "Riverside received a bounded partner condition report",
      ));
      effect(
        &mut effects,
        "partner assessment",
        "cash",
        -ruleset.assessment_cash_cost,
      );
    }
    AffiliationCommand::ChoosePosture { posture } => {
      next.status = match posture {
        AffiliationPosture::Independent => AffiliationStatus::Independent,
        AffiliationPosture::Deferred => AffiliationStatus::Deferred,
        AffiliationPosture::Pursue => AffiliationStatus::Pursuing,
      };
      events.push(event(
        "riverside",
        &format!("Riverside chose the {posture:?} posture"),
      ));
    }
    AffiliationCommand::SetCommitments {
      community,
      workforce,
      continuity,
    } => {
      next.commitments = crate::model::AffiliationCommitments {
        community,
        workforce,
        continuity,
      };
      let total = next.commitments.total();
      next.riverside.cash = next.riverside.cash.saturating_sub(total);
      next.riverside.workforce_trust = adjust(next.riverside.workforce_trust, workforce / 2);
      next.riverside.community_trust = adjust(next.riverside.community_trust, community / 2);
      next.riverside.access_index = adjust(next.riverside.access_index, continuity / 2);
      next.partner_response = resolved_inputs.partner_response;
      match resolved_inputs.partner_response {
        PartnerResponse::Accepted => {
          next.status = AffiliationStatus::PartnerAccepted;
          decisions.push(decision(
            "partner",
            "accepted",
            "The package met the partner's fit and continuity threshold.",
          ));
        }
        PartnerResponse::Conditioned => {
          next.status = AffiliationStatus::PartnerConditioned;
          next.review.conditions = 1;
          decisions.push(decision(
            "partner",
            "conditioned",
            "The partner accepted the relationship with an explicit continuity condition.",
          ));
        }
        PartnerResponse::Rejected => {
          next.status = AffiliationStatus::PartnerRejected;
          decisions.push(decision(
            "partner",
            "rejected",
            "The partner's fit and continuity concerns outweighed the package strength.",
          ));
        }
        PartnerResponse::NotEngaged => {}
      }
      events.push(event(
        "riverside",
        &format!("Riverside proposed {total} commitment points"),
      ));
      effect(&mut effects, "affiliation commitments", "cash", -total);
      effect(
        &mut effects,
        "affiliation commitments",
        "workforce_trust",
        workforce / 2,
      );
      effect(
        &mut effects,
        "affiliation commitments",
        "community_trust",
        community / 2,
      );
      effect(
        &mut effects,
        "affiliation commitments",
        "access_index",
        continuity / 2,
      );
    }
    AffiliationCommand::SubmitReview => {
      next.riverside.cash = next
        .riverside
        .cash
        .saturating_sub(ruleset.review_submission_cash_cost);
      next.status = AffiliationStatus::ReviewPending;
      events.push(event(
        "review",
        "Riverside submitted the affiliation package for institutional review",
      ));
      effect(
        &mut effects,
        "institutional review submission",
        "cash",
        -ruleset.review_submission_cash_cost,
      );
    }
    AffiliationCommand::AwaitReview => {
      next.review.response = Some(resolved_inputs.review_response);
      next.labor_response = resolved_inputs.labor_response;
      next.payer_response = resolved_inputs.payer_response;
      next.community_response = resolved_inputs.community_response;
      next.status = match resolved_inputs.review_response {
        ReviewResponse::Approved => AffiliationStatus::Approved,
        ReviewResponse::Conditional => AffiliationStatus::ConditionallyApproved,
        ReviewResponse::Delayed => AffiliationStatus::ReviewDelayed,
        ReviewResponse::Rejected => AffiliationStatus::ReviewRejected,
        ReviewResponse::NotEngaged => AffiliationStatus::ReviewPending,
      };
      apply_responses(&mut next, &mut effects);
      decisions.push(decision(
        "review",
        &format!("{:?}", resolved_inputs.review_response),
        "Review response is a stylized institutional outcome, not a legal prediction.",
      ));
      decisions.push(decision(
        "labor",
        &format!("{:?}", resolved_inputs.labor_response),
        "Labor response reflects workforce commitment and perceived disruption risk.",
      ));
      decisions.push(decision(
        "payer",
        &format!("{:?}", resolved_inputs.payer_response),
        "Payer response reflects continuity commitments and concentration concerns.",
      ));
      decisions.push(decision(
        "community",
        &format!("{:?}", resolved_inputs.community_response),
        "Community response reflects continuity and public-benefit commitments.",
      ));
      events.push(event(
        "review",
        &format!(
          "Institutional review resolved as {:?}",
          resolved_inputs.review_response
        ),
      ));
    }
    AffiliationCommand::ChooseIntegration {
      decision: integration_decision,
    } => {
      if integration_decision == IntegrationDecision::Begin {
        next.riverside.cash = next
          .riverside
          .cash
          .saturating_sub(ruleset.integration_start_cash_cost + resolved_inputs.integration_drag);
        next.riverside.access_index = adjust(
          next.riverside.access_index,
          -resolved_inputs.continuity_shock,
        );
        next.riverside.quality_index = adjust(
          next.riverside.quality_index,
          -(resolved_inputs.integration_drag / 2),
        );
        next.riverside.workforce_trust = adjust(next.riverside.workforce_trust, -1);
        next.riverside.market_share_index = adjust(next.riverside.market_share_index, 3);
        next.integration.progress = 1;
        next.integration.drag_applied = resolved_inputs.integration_drag;
        next.integration.continuity_shock_applied = resolved_inputs.continuity_shock;
        next.status = AffiliationStatus::Integrated;
        events.push(event(
          "integration",
          "Riverside began early integration with initial drag and continuity effects",
        ));
        effect(
          &mut effects,
          "integration start",
          "cash",
          -(ruleset.integration_start_cash_cost + resolved_inputs.integration_drag),
        );
        effect(
          &mut effects,
          "integration drag",
          "quality_index",
          -(resolved_inputs.integration_drag / 2),
        );
        effect(
          &mut effects,
          "continuity shock",
          "access_index",
          -resolved_inputs.continuity_shock,
        );
      } else {
        next.status = AffiliationStatus::IntegrationDeclined;
        events.push(event(
          "riverside",
          "Riverside declined early integration after approval",
        ));
      }
    }
    AffiliationCommand::Hold => {
      events.push(event(
        "riverside",
        "Riverside held its current affiliation posture",
      ));
    }
  }

  next.turn = prior.turn + 1;
  next.stage = next.stage.next();
  if next.turn >= crate::model::AFFILIATION_TURN_COUNT {
    next.stage = AffiliationStage::Complete;
  }
  let state_hash = hash_affiliation_state(&next, ruleset);
  Ok(AffiliationTransition {
    prior: prior.clone(),
    command,
    observation,
    resolved_inputs,
    actor_decisions: decisions,
    events,
    effects,
    next,
    state_hash,
  })
}

pub fn resolve_affiliation_turn(
  prior: &AffiliationWorldState,
  command: AffiliationCommand,
  seed: u64,
  ruleset: &AffiliationRuleset,
) -> Result<AffiliationTransition, AffiliationValidationError> {
  validate_affiliation_command(prior, &command, ruleset)?;
  let observation = observe_affiliation(prior);
  let inputs = resolve_affiliation_inputs(seed, prior, &command);
  transition_affiliation(prior, command, observation, inputs, ruleset)
}

pub fn replay_affiliation(
  history: &AffiliationHistory,
  ruleset: &AffiliationRuleset,
) -> Result<AffiliationWorldState, AffiliationValidationError> {
  let mut current = history.genesis.clone();
  for transition in &history.transitions {
    if transition.prior != current {
      return Err(AffiliationValidationError::ReplayStateMismatch);
    }
    if transition.observation != observe_affiliation(&current) {
      return Err(AffiliationValidationError::ObservationMismatch);
    }
    let replayed = transition_affiliation(
      &current,
      transition.command,
      transition.observation.clone(),
      transition.resolved_inputs.clone(),
      ruleset,
    )?;
    if replayed.state_hash != transition.state_hash {
      return Err(AffiliationValidationError::StateHashMismatch {
        turn: replayed.next.turn,
        expected: transition.state_hash.clone(),
        actual: replayed.state_hash,
      });
    }
    current = replayed.next;
  }
  Ok(current)
}

fn apply_responses(
  state: &mut AffiliationWorldState,
  effects: &mut Vec<crate::model::AttributedEffect>,
) {
  match state.labor_response {
    LaborResponse::Support => adjust_effect(state, effects, "workforce_trust", 2),
    LaborResponse::Concern => adjust_effect(state, effects, "workforce_trust", -1),
    LaborResponse::Opposition => adjust_effect(state, effects, "workforce_trust", -3),
    LaborResponse::Disruption => {
      adjust_effect(state, effects, "workforce_trust", -6);
      adjust_effect(state, effects, "access_index", -2);
      adjust_effect(state, effects, "quality_index", -2);
    }
    LaborResponse::NotEngaged => {}
  }
  match state.payer_response {
    PayerResponse::Support => adjust_effect(state, effects, "cash", 4),
    PayerResponse::Neutral => {}
    PayerResponse::Leverage => adjust_effect(state, effects, "cash", -3),
    PayerResponse::Retrenchment => {
      adjust_effect(state, effects, "cash", -8);
      adjust_effect(state, effects, "access_index", -2);
    }
    PayerResponse::NotEngaged => {}
  }
  match state.community_response {
    CommunityResponse::Support => adjust_effect(state, effects, "community_trust", 3),
    CommunityResponse::Conditional => adjust_effect(state, effects, "community_trust", 1),
    CommunityResponse::Opposition => adjust_effect(state, effects, "community_trust", -4),
    CommunityResponse::NotEngaged => {}
  }
}

fn adjust_effect(
  state: &mut AffiliationWorldState,
  effects: &mut Vec<crate::model::AttributedEffect>,
  metric: &'static str,
  delta: i32,
) {
  match metric {
    "cash" => state.riverside.cash = (state.riverside.cash + delta).max(0),
    "access_index" => state.riverside.access_index = adjust(state.riverside.access_index, delta),
    "quality_index" => state.riverside.quality_index = adjust(state.riverside.quality_index, delta),
    "workforce_trust" => {
      state.riverside.workforce_trust = adjust(state.riverside.workforce_trust, delta)
    }
    "community_trust" => {
      state.riverside.community_trust = adjust(state.riverside.community_trust, delta)
    }
    _ => {}
  }
  effect(effects, "external response", metric, delta);
}

fn adjust(value: i32, delta: i32) -> i32 {
  value.saturating_add(delta).clamp(0, 100)
}

fn effect(
  effects: &mut Vec<crate::model::AttributedEffect>,
  source: &'static str,
  metric: &'static str,
  delta: i32,
) {
  effects.push(crate::model::AttributedEffect {
    source,
    metric,
    delta,
  });
}

fn event(actor: &'static str, description: &str) -> crate::model::Event {
  crate::model::Event {
    actor,
    description: description.to_string(),
  }
}

fn decision(actor: &str, outcome: &str, rationale: &str) -> AffiliationActorDecision {
  AffiliationActorDecision {
    actor: actor.to_string(),
    outcome: outcome.to_string(),
    rationale: rationale.to_string(),
  }
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{AffiliationCommand, AffiliationPosture, default_affiliation_ruleset};
  use crate::scenario::default_regional_affiliation_scenario;

  fn state() -> AffiliationWorldState {
    default_regional_affiliation_scenario()
      .unwrap()
      .initial_affiliation_world_state()
      .unwrap()
  }

  #[test]
  fn independent_path_completes_six_stages() {
    let ruleset = default_affiliation_ruleset();
    let mut current = state();
    let commands = [
      AffiliationCommand::AssessPartner,
      AffiliationCommand::ChoosePosture {
        posture: AffiliationPosture::Independent,
      },
      AffiliationCommand::Hold,
      AffiliationCommand::Hold,
      AffiliationCommand::Hold,
      AffiliationCommand::Hold,
    ];
    for command in commands {
      current = resolve_affiliation_turn(&current, command, 42, &ruleset)
        .unwrap()
        .next;
    }
    assert_eq!(current.stage, AffiliationStage::Complete);
    assert_eq!(current.status, AffiliationStatus::Independent);
  }

  #[test]
  fn invalid_stage_command_does_not_transition() {
    let ruleset = default_affiliation_ruleset();
    let current = state();
    assert!(matches!(
      validate_affiliation_command(&current, &AffiliationCommand::Hold, &ruleset),
      Err(AffiliationValidationError::InvalidCommandForStatus)
    ));
  }

  #[test]
  fn integration_drag_is_included_in_cash_validation() {
    let ruleset = default_affiliation_ruleset();
    let mut current = state();
    current.stage = AffiliationStage::IntegrateOrDecline;
    current.status = AffiliationStatus::Approved;
    current.riverside.cash = ruleset.integration_start_cash_cost;
    let inputs = AffiliationResolvedInputs {
      partner_report_noise: 0,
      partner_response: PartnerResponse::NotEngaged,
      review_response: ReviewResponse::NotEngaged,
      labor_response: LaborResponse::NotEngaged,
      payer_response: PayerResponse::NotEngaged,
      community_response: CommunityResponse::NotEngaged,
      integration_drag: 1,
      continuity_shock: 0,
    };
    let result = transition_affiliation(
      &current,
      AffiliationCommand::ChooseIntegration {
        decision: IntegrationDecision::Begin,
      },
      observe_affiliation(&current),
      inputs,
      &ruleset,
    );
    assert!(matches!(
      result,
      Err(AffiliationValidationError::InsufficientCash { .. })
    ));
  }
}
