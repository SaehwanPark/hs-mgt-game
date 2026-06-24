use crate::model::*;
use crate::sim::transition;

#[test]
fn identical_inputs_produce_identical_transition() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 8,
    capital_spend: 18,
    requested_commercial_rate: 112,
  };
  let inputs = ResolvedInputs {
    measurement_noise: -2,
    delayed_access_report: 67,
    labor_sick_call_delta: -3,
    policy_signal: 4,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let first = transition(&prior, command.clone(), inputs.clone(), &ruleset).unwrap();
  let second = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(first, second);
}
#[test]
fn true_state_and_observed_state_can_differ() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 4,
    capital_spend: 10,
    requested_commercial_rate: 104,
  };
  let inputs = ResolvedInputs {
    measurement_noise: -5,
    delayed_access_report: 60,
    labor_sick_call_delta: 0,
    policy_signal: 1,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_ne!(
    result.observation.reported_access_index,
    result.prior.access_index
  );
  assert_ne!(
    result.observation.reported_access_index,
    result.next.access_index
  );
}
#[test]
fn invalid_command_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 8,
    capital_spend: 80,
    requested_commercial_rate: 110,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::CapitalSpendTooHigh {
      requested: 80,
      available_limit: 40
    })
  );
}
#[test]
fn negative_capital_spend_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 8,
    capital_spend: -1,
    requested_commercial_rate: 104,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NegativeCapitalSpend { requested: -1 })
  );
}
#[test]
fn accepted_negotiation_applies_requested_rate() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 4,
    capital_spend: 10,
    requested_commercial_rate: 104,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 75,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::Insurer(InsurerDecision::Accept)
  );
  assert_eq!(result.next.commercial_rate, 104);
}
#[test]
fn unfavorable_valid_outcome_is_not_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::StabilizeAccess {
    add_staffed_beds: 2,
    capital_spend: 5,
    requested_commercial_rate: 120,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 80,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::Insurer(InsurerDecision::Reject)
  );
  assert!(
    result
      .events
      .iter()
      .any(|event| event.description.contains("Rejected"))
  );
}
#[test]
fn policy_response_is_deterministic() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend: 10,
    access_commitment: 7,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 1,
    delayed_access_report: 69,
    labor_sick_call_delta: 0,
    policy_signal: 4,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let first = transition(&prior, command.clone(), inputs.clone(), &ruleset).unwrap();
  let second = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(first, second);
  assert_eq!(
    first.actor_decision.decision,
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility)
  );
}
#[test]
fn negative_advocacy_spend_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend: -1,
    access_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NegativeAdvocacySpend { requested: -1 })
  );
}
#[test]
fn excessive_advocacy_spend_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend: 25,
    access_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::AdvocacySpendTooHigh {
      requested: 25,
      available_limit: 20
    })
  );
}
#[test]
fn non_positive_access_commitment_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend: 4,
    access_commitment: 0,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NonPositiveAccessCommitment)
  );
}
#[test]
fn credible_policy_response_can_proceed_with_mandate() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend: 4,
    access_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 75,
    labor_sick_call_delta: 0,
    policy_signal: 1,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate)
  );
  assert_eq!(result.next.policy_pressure, 33);
}
#[test]
fn unfavorable_policy_outcome_is_not_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend: 2,
    access_commitment: 3,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 75,
    labor_sick_call_delta: 0,
    policy_signal: 2,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight)
  );
  assert!(
    result
      .events
      .iter()
      .any(|event| event.description.contains("Escalated oversight"))
  );
}
#[test]
fn workforce_response_is_deterministic() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: 14,
    schedule_relief_commitment: 8,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: -4,
    policy_signal: 2,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let first = transition(&prior, command.clone(), inputs.clone(), &ruleset).unwrap();
  let second = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(first, second);
  assert_eq!(
    first.actor_decision.decision,
    ActorDecision::Labor(LaborDecision::Cooperative)
  );
}
#[test]
fn negative_retention_spend_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: -1,
    schedule_relief_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NegativeRetentionSpend { requested: -1 })
  );
}
#[test]
fn excessive_retention_spend_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: 30,
    schedule_relief_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::RetentionSpendTooHigh {
      requested: 30,
      available_limit: 25
    })
  );
}
#[test]
fn non_positive_schedule_relief_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: 8,
    schedule_relief_commitment: 0,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NonPositiveScheduleRelief)
  );
}
#[test]
fn unfavorable_labor_outcome_is_not_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: 2,
    schedule_relief_commitment: 2,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: -4,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::Labor(LaborDecision::WorkAction)
  );
  assert!(
    result
      .events
      .iter()
      .any(|event| event.description.contains("work action"))
  );
}
#[test]
fn excessive_schedule_relief_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: 8,
    schedule_relief_commitment: 25,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::ScheduleReliefTooHigh {
      requested: 25,
      available_limit: 20
    })
  );
}
#[test]
fn credible_workforce_offer_triggers_limited_support() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToWorkforcePressure {
    retention_spend: 8,
    schedule_relief_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::Labor(LaborDecision::LimitedSupport)
  );
}
#[test]
fn coalition_response_is_deterministic() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment: 12,
    shared_access_commitment: 8,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 2,
    coalition_leverage_signal: 5,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let first = transition(&prior, command.clone(), inputs.clone(), &ruleset).unwrap();
  let second = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(first, second);
  assert_eq!(
    first.actor_decision.decision,
    ActorDecision::Coalition(CoalitionDecision::FullPartnership)
  );
}
#[test]
fn negative_coalition_investment_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment: -1,
    shared_access_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NegativeCoalitionInvestment { requested: -1 })
  );
}
#[test]
fn excessive_coalition_investment_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment: 25,
    shared_access_commitment: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::CoalitionInvestmentTooHigh {
      requested: 25,
      available_limit: 20
    })
  );
}
#[test]
fn non_positive_shared_access_commitment_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment: 8,
    shared_access_commitment: 0,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NonPositiveSharedAccessCommitment)
  );
}
#[test]
fn excessive_shared_access_commitment_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment: 8,
    shared_access_commitment: 25,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 1,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::SharedAccessCommitmentTooHigh {
      requested: 25,
      available_limit: 20
    })
  );
}
#[test]
fn unfavorable_coalition_outcome_is_not_validation_failure() {
  let ruleset = default_ruleset();
  let mut prior = genesis_state();
  prior.community_trust = 55;
  let command = PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment: 4,
    shared_access_commitment: 4,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 3,
    access_measurement_revision: 0,
    competitor_market_signal: 0,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal)
  );
  assert!(
    result
      .events
      .iter()
      .any(|event| event.description.contains("Withdrew"))
  );
}

#[test]
fn negative_defensive_capital_is_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToCompetitorCapacityMove {
    defensive_capital_commitment: -1,
    access_posture: 5,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 0,
    access_measurement_revision: 0,
    competitor_market_signal: 4,
  };

  assert_eq!(
    transition(&prior, command, inputs, &ruleset),
    Err(ValidationError::NegativeDefensiveCapitalCommitment { requested: -1 })
  );
}

#[test]
fn unfavorable_competitor_outcome_is_not_validation_failure() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let command = PlayerCommand::RespondToCompetitorCapacityMove {
    defensive_capital_commitment: 4,
    access_posture: 4,
  };
  let inputs = ResolvedInputs {
    measurement_noise: 0,
    delayed_access_report: 70,
    labor_sick_call_delta: 0,
    policy_signal: 0,
    coalition_leverage_signal: 0,
    access_measurement_revision: 0,
    competitor_market_signal: 6,
  };

  let result = transition(&prior, command, inputs, &ruleset).unwrap();

  assert_eq!(
    result.actor_decision.decision,
    ActorDecision::Competitor(CompetitorDecision::AccelerateExpansion)
  );
}

#[test]
fn five_transition_history_replays_from_genesis() {
  let ruleset = default_ruleset();
  let history = crate::test_support::demo_history();

  assert_eq!(history.transitions.len(), 5);
  assert_eq!(
    crate::replay::replay(&history, &ruleset)
      .unwrap()
      .final_state,
    history.transitions.last().unwrap().next
  );
}
