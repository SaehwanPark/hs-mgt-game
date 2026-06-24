use hs_mgt_game::cli::{describe_cli_error, run};

fn main() {
  match run() {
    Ok(()) => {}
    Err(error) => {
      eprintln!("Unable to run demo: {}", describe_cli_error(&error));
      std::process::exit(1);
    }
  }
}

#[cfg(test)]
mod tests {
  use hs_mgt_game::artifact::*;
  use hs_mgt_game::cli::*;
  use hs_mgt_game::debrief::educational_debrief;
  use hs_mgt_game::inputs::resolve_inputs;
  use hs_mgt_game::model::*;
  use hs_mgt_game::replay::*;
  use hs_mgt_game::sim::*;

  use super::*;

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
  fn replay_reproduces_committed_final_state() {
    let ruleset = default_ruleset();
    let genesis = genesis_state();
    let first = transition(
      &genesis,
      PlayerCommand::StabilizeAccess {
        add_staffed_beds: 8,
        capital_spend: 18,
        requested_commercial_rate: 112,
      },
      ResolvedInputs {
        measurement_noise: -2,
        delayed_access_report: 67,
        labor_sick_call_delta: -3,
        policy_signal: 4,
        coalition_leverage_signal: 1,
        access_measurement_revision: 0,
      },
      &ruleset,
    )
    .unwrap();
    let history = History {
      genesis,
      transitions: vec![first.clone()],
    };

    assert_eq!(replay(&history, &ruleset).unwrap().final_state, first.next);
  }

  #[test]
  fn identical_state_records_produce_identical_hashes() {
    let ruleset = default_ruleset();
    let state = genesis_state();

    assert_eq!(hash_state(&state, &ruleset), hash_state(&state, &ruleset));
    assert_eq!(
      state_hash_record(&state, &ruleset),
      "state-hash-v1|ruleset=demo-ruleset-0.1.9|turn=0|cash=100|staffed_beds=120|access_index=70|quality_index=78|workforce_trust=62|community_trust=66|commercial_rate=100|policy_pressure=30"
    );
  }

  #[test]
  fn changed_state_field_changes_hash() {
    let ruleset = default_ruleset();
    let mut changed = genesis_state();
    changed.cash -= 1;

    assert_ne!(
      hash_state(&genesis_state(), &ruleset),
      hash_state(&changed, &ruleset)
    );
  }

  #[test]
  fn replay_detects_committed_state_hash_mismatch() {
    let ruleset = default_ruleset();
    let genesis = genesis_state();
    let mut first = transition(
      &genesis,
      PlayerCommand::StabilizeAccess {
        add_staffed_beds: 8,
        capital_spend: 18,
        requested_commercial_rate: 112,
      },
      ResolvedInputs {
        measurement_noise: -2,
        delayed_access_report: 67,
        labor_sick_call_delta: -3,
        policy_signal: 4,
        coalition_leverage_signal: 1,
        access_measurement_revision: 0,
      },
      &ruleset,
    )
    .unwrap();
    let actual = first.state_hash.clone();
    first.state_hash = "0000000000000000".to_string();
    first.next.turn = 99;
    let history = History {
      genesis,
      transitions: vec![first],
    };

    assert_eq!(
      replay(&history, &ruleset),
      Err(ReplayError::StateHashMismatch {
        turn: 1,
        expected: "0000000000000000".to_string(),
        actual,
      })
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
  fn replay_reproduces_two_transition_history() {
    let ruleset = default_ruleset();
    let genesis = genesis_state();
    let first = transition(
      &genesis,
      PlayerCommand::StabilizeAccess {
        add_staffed_beds: 8,
        capital_spend: 18,
        requested_commercial_rate: 112,
      },
      ResolvedInputs {
        measurement_noise: -2,
        delayed_access_report: 67,
        labor_sick_call_delta: -3,
        policy_signal: 4,
        coalition_leverage_signal: 1,
        access_measurement_revision: 0,
      },
      &ruleset,
    )
    .unwrap();
    let second = transition(
      &first.next,
      PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 10,
        access_commitment: 7,
      },
      ResolvedInputs {
        measurement_noise: 1,
        delayed_access_report: 69,
        labor_sick_call_delta: 0,
        policy_signal: 4,
        coalition_leverage_signal: 1,
        access_measurement_revision: 0,
      },
      &ruleset,
    )
    .unwrap();
    let history = History {
      genesis,
      transitions: vec![first, second.clone()],
    };

    assert_eq!(replay(&history, &ruleset).unwrap().final_state, second.next);
  }

  #[test]
  fn debrief_includes_actor_rationales() {
    let history = demo_history();
    let debrief = educational_debrief(&history).join("\n");

    assert!(debrief.contains("commercial_insurer:"));
    assert!(debrief.contains("state_policy_officials:"));
    assert!(debrief.contains("nursing_workforce:"));
    assert!(debrief.contains("regional_provider_coalition:"));
    assert!(debrief.contains("Reported access"));
    assert!(debrief.contains("Access commitment"));
    assert!(debrief.contains("coalition investment choice"));
  }

  #[test]
  fn debrief_includes_attributed_tradeoff() {
    let history = demo_history();
    let debrief = educational_debrief(&history).join("\n");

    assert!(debrief.contains("cash moved from 100 to 46"));
    assert!(debrief.contains("access from 70 to 83"));
    assert!(debrief.contains("capacity investment changed cash by -18"));
    assert!(debrief.contains("state policy response changed community_trust by 2"));
    assert!(debrief.contains("workforce response changed cash by"));
    assert!(debrief.contains("coalition response changed cash by"));
  }

  #[test]
  fn identical_histories_produce_identical_debriefs() {
    let first = demo_history();
    let second = demo_history();

    assert_eq!(educational_debrief(&first), educational_debrief(&second));
  }

  #[test]
  fn empty_play_mode_choice_defaults_to_interactive() {
    assert_eq!(parse_play_mode_choice("\n").unwrap(), PlayMode::Interactive);
  }

  #[test]
  fn interactive_play_mode_alias_is_parsed() {
    assert_eq!(
      parse_play_mode_choice("i\n").unwrap(),
      PlayMode::Interactive
    );
  }

  #[test]
  fn numbered_play_mode_choices_select_preset_paths() {
    assert_eq!(
      parse_play_mode_choice("1\n").unwrap(),
      PlayMode::Preset(StrategyPath::AccessStabilization)
    );
    assert_eq!(
      parse_play_mode_choice("2\n").unwrap(),
      PlayMode::Preset(StrategyPath::FiscalCaution)
    );
    assert_eq!(
      parse_play_mode_choice("3\n").unwrap(),
      PlayMode::Preset(StrategyPath::AggressiveBargaining)
    );
  }

  #[test]
  fn invalid_play_mode_choice_is_error() {
    assert_eq!(
      parse_play_mode_choice("9\n"),
      Err(CliError::InvalidPlayModeChoice("9".to_string()))
    );
  }

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
  fn turn_briefing_includes_prior_access_revision_when_present() {
    let observation = Observation {
      actor: "health_system_ceo",
      reported_access_index: 65,
      reported_quality_index: 78,
      prior_access_revision: -1,
      policy_briefing: "state officials are increasing scrutiny of access and affordability",
    };
    let briefing = turn_executive_briefing(&genesis_state(), &observation, 2).join("\n");

    assert!(briefing.contains("Prior access measurement revision: -1"));
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

  #[test]
  fn interactive_history_matches_access_stabilization_preset() {
    let ruleset = default_ruleset();
    let preset =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let interactive =
      build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();

    assert_eq!(interactive, preset);
  }

  #[test]
  fn interactive_history_replays_with_matching_state_hashes() {
    let ruleset = default_ruleset();
    let history =
      build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();

    assert_eq!(history.transitions.len(), 4);
    assert_eq!(
      replay(&history, &ruleset).unwrap().final_state,
      history.transitions.last().unwrap().next
    );
  }

  #[test]
  fn turn_briefing_uses_observation_not_future_actor_outcomes() {
    let ruleset = default_ruleset();
    let prior = genesis_state();
    let inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
    let observation = observe_for_player(&prior, &inputs);
    let briefing = turn_executive_briefing(&prior, &observation, 1).join("\n");

    assert!(briefing.contains("Reported access"));
    assert!(!briefing.contains("decision:"));
    assert!(!briefing.contains("Rejected"));
    assert!(!briefing.contains("Accepted"));
  }

  #[test]
  fn turn_resolution_summary_includes_actor_rationale_and_hash() {
    let ruleset = default_ruleset();
    let history =
      build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();
    let summary = turn_resolution_summary(&history.transitions[0]).join("\n");

    assert!(summary.contains("Turn 1 resolved:"));
    assert!(summary.contains("commercial_insurer"));
    assert!(summary.contains("State hash:"));
  }

  #[test]
  fn each_strategy_path_builds_replayable_history() {
    let ruleset = default_ruleset();

    for choice in [
      StrategyPath::AccessStabilization,
      StrategyPath::FiscalCaution,
      StrategyPath::AggressiveBargaining,
    ] {
      let history = build_history_for_strategy(choice, DEFAULT_SEED, &ruleset).unwrap();
      let final_state = history.transitions.last().unwrap().next.clone();

      assert_eq!(history.transitions.len(), 4);
      assert_eq!(replay(&history, &ruleset).unwrap().final_state, final_state);
    }
  }

  #[test]
  fn default_seed_resolves_identical_inputs_for_same_turn() {
    let ruleset = default_ruleset();
    let prior = genesis_state();

    let first = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
    let second = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);

    assert_eq!(first, second);
  }

  #[test]
  fn different_seeds_can_change_resolved_inputs() {
    let ruleset = default_ruleset();
    let prior = genesis_state();

    let default_inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
    let alternate_inputs = resolve_inputs(99, &prior, &ruleset);

    assert_ne!(default_inputs, alternate_inputs);
  }

  #[test]
  fn default_seed_reproduces_canonical_demo_trajectory() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();

    assert_eq!(
      history.transitions[0].resolved_inputs,
      ResolvedInputs {
        measurement_noise: 4,
        delayed_access_report: 67,
        labor_sick_call_delta: -3,
        policy_signal: 4,
        coalition_leverage_signal: 2,
        access_measurement_revision: 0,
      }
    );
    assert_eq!(
      history.transitions[1].resolved_inputs,
      ResolvedInputs {
        measurement_noise: -5,
        delayed_access_report: 70,
        labor_sick_call_delta: -2,
        policy_signal: 3,
        coalition_leverage_signal: 4,
        access_measurement_revision: -1,
      }
    );
    assert_eq!(
      history.transitions[0].actor_decision.decision,
      ActorDecision::Insurer(InsurerDecision::Reject)
    );
    assert_eq!(
      history.transitions[1].actor_decision.decision,
      ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility)
    );
    assert_eq!(
      history.transitions[2].resolved_inputs,
      ResolvedInputs {
        measurement_noise: -5,
        delayed_access_report: 69,
        labor_sick_call_delta: -5,
        policy_signal: 1,
        coalition_leverage_signal: 2,
        access_measurement_revision: 2,
      }
    );
    assert_eq!(
      history.transitions[2].actor_decision.decision,
      ActorDecision::Labor(LaborDecision::Cooperative)
    );
    assert_eq!(
      history.transitions[3].resolved_inputs,
      ResolvedInputs {
        measurement_noise: -2,
        delayed_access_report: 71,
        labor_sick_call_delta: -5,
        policy_signal: 5,
        coalition_leverage_signal: 3,
        access_measurement_revision: -1,
      }
    );
    assert_eq!(
      history.transitions[3].actor_decision.decision,
      ActorDecision::Coalition(CoalitionDecision::FullPartnership)
    );
    assert_eq!(
      history.transitions.last().unwrap().state_hash,
      "bce02dff9b4b4ac6"
    );
  }

  #[test]
  fn empty_seed_choice_defaults_to_default_seed() {
    assert_eq!(parse_seed_choice("\n").unwrap(), DEFAULT_SEED);
  }

  #[test]
  fn numeric_seed_choice_is_parsed() {
    assert_eq!(parse_seed_choice("99\n").unwrap(), 99);
  }

  #[test]
  fn invalid_seed_choice_is_error() {
    assert_eq!(
      parse_seed_choice("abc\n"),
      Err(CliError::InvalidSeed("abc".to_string()))
    );
  }

  #[test]
  fn executive_dashboard_reports_starting_state() {
    let dashboard = executive_dashboard(&genesis_state()).join("\n");

    assert!(dashboard.contains("Executive dashboard"));
    assert!(dashboard.contains("Cash 100"));
    assert!(dashboard.contains("staffed beds 120"));
    assert!(dashboard.contains("access 70"));
    assert!(dashboard.contains("policy pressure 30"));
  }

  #[test]
  fn strategy_previews_cover_all_compiled_paths() {
    let previews = strategy_previews();

    assert_eq!(previews.len(), 3);
    assert!(previews[0].contains("1. Access stabilization"));
    assert!(previews[0].contains("spends 54 total resource units"));
    assert!(previews[1].contains("2. Fiscal caution"));
    assert!(previews[1].contains("requests commercial rate 104"));
    assert!(previews[2].contains("3. Aggressive bargaining"));
    assert!(previews[2].contains("commits 9 access/workforce/coalition units"));
  }

  #[test]
  fn strategy_previews_do_not_describe_future_actor_outcomes() {
    let previews = strategy_previews().join("\n");

    assert!(!previews.contains("reject"));
    assert!(!previews.contains("grant flexibility"));
    assert!(!previews.contains("work action"));
    assert!(!previews.contains("full partnership"));
    assert!(!previews.contains("state hash"));
  }

  #[test]
  fn seed_zero_resolves_bounded_inputs() {
    let ruleset = default_ruleset();
    let inputs = resolve_inputs(0, &genesis_state(), &ruleset);

    assert!((-5..=5).contains(&inputs.measurement_noise));
    assert!((0..=100).contains(&inputs.delayed_access_report));
    assert!((-5..=0).contains(&inputs.labor_sick_call_delta));
    assert!((1..=6).contains(&inputs.policy_signal));
    assert!((1..=6).contains(&inputs.coalition_leverage_signal));
    assert!((-3..=3).contains(&inputs.access_measurement_revision));
  }

  #[test]
  fn fiscal_caution_accepts_rate_and_proceeds_with_mandate() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::FiscalCaution, DEFAULT_SEED, &ruleset).unwrap();

    assert_eq!(
      history.transitions[0].actor_decision.decision,
      ActorDecision::Insurer(InsurerDecision::Accept)
    );
    assert_eq!(
      history.transitions[1].actor_decision.decision,
      ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate)
    );
  }

  #[test]
  fn aggressive_bargaining_rejects_rate_and_escalates_oversight() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AggressiveBargaining, DEFAULT_SEED, &ruleset)
        .unwrap();

    assert_eq!(
      history.transitions[0].actor_decision.decision,
      ActorDecision::Insurer(InsurerDecision::Reject)
    );
    assert_eq!(
      history.transitions[1].actor_decision.decision,
      ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight)
    );
  }

  fn demo_history() -> History {
    let ruleset = default_ruleset();
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap()
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
  fn replay_reproduces_four_transition_history() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let final_state = history.transitions.last().unwrap().next.clone();

    assert_eq!(history.transitions.len(), 4);
    assert_eq!(replay(&history, &ruleset).unwrap().final_state, final_state);
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
    };

    let result = transition(&prior, command, inputs, &ruleset).unwrap();

    assert_eq!(
      result.actor_decision.decision,
      ActorDecision::Labor(LaborDecision::LimitedSupport)
    );
  }

  #[test]
  fn fiscal_caution_triggers_limited_support_on_workforce_turn() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::FiscalCaution, DEFAULT_SEED, &ruleset).unwrap();

    assert_eq!(
      history.transitions[2].actor_decision.decision,
      ActorDecision::Labor(LaborDecision::LimitedSupport)
    );
  }

  #[test]
  fn aggressive_bargaining_triggers_coalition_withdrawal_on_fourth_turn() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AggressiveBargaining, DEFAULT_SEED, &ruleset)
        .unwrap();

    assert_eq!(
      history.transitions[3].actor_decision.decision,
      ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal)
    );
  }

  #[test]
  fn fiscal_caution_triggers_limited_coalition_participation() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::FiscalCaution, DEFAULT_SEED, &ruleset).unwrap();

    assert_eq!(
      history.transitions[3].actor_decision.decision,
      ActorDecision::Coalition(CoalitionDecision::LimitedParticipation)
    );
  }

  #[test]
  fn aggressive_bargaining_triggers_work_action_on_workforce_turn() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AggressiveBargaining, DEFAULT_SEED, &ruleset)
        .unwrap();

    assert_eq!(
      history.transitions[2].actor_decision.decision,
      ActorDecision::Labor(LaborDecision::WorkAction)
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
    };

    assert_eq!(
      transition(&prior, command, inputs, &ruleset),
      Err(ValidationError::NonPositiveSharedAccessCommitment)
    );
  }

  #[test]
  fn genesis_turn_has_no_access_measurement_revision() {
    let ruleset = default_ruleset();
    let inputs = resolve_inputs(DEFAULT_SEED, &genesis_state(), &ruleset);

    assert_eq!(inputs.access_measurement_revision, 0);
  }

  #[test]
  fn later_turn_can_revise_prior_reported_access_in_observation() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();

    assert_eq!(history.transitions[1].observation.prior_access_revision, -1);
    assert_eq!(history.transitions[0].observation.prior_access_revision, 0);
  }

  #[test]
  fn debrief_notes_observation_revisions_without_rewriting_history() {
    let history = demo_history();
    let debrief = educational_debrief(&history).join("\n");

    assert!(debrief.contains("Observation revision note:"));
    assert!(debrief.contains("Prior committed observations remain unchanged"));
    assert_eq!(history.transitions[0].observation.prior_access_revision, 0);
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
  fn access_stabilization_triggers_full_coalition_partnership() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();

    assert_eq!(
      history.transitions[3].actor_decision.decision,
      ActorDecision::Coalition(CoalitionDecision::FullPartnership)
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

  fn sample_replay_artifact(play_mode: PlayMode, history: History) -> ReplayArtifact {
    ReplayArtifact {
      seed: DEFAULT_SEED,
      play_mode,
      ruleset_version: default_ruleset().version.to_string(),
      history,
    }
  }

  #[test]
  fn replay_artifact_round_trip_verifies_all_preset_paths() {
    let ruleset = default_ruleset();

    for (play_mode, choice) in [
      (
        PlayMode::Preset(StrategyPath::AccessStabilization),
        StrategyPath::AccessStabilization,
      ),
      (
        PlayMode::Preset(StrategyPath::FiscalCaution),
        StrategyPath::FiscalCaution,
      ),
      (
        PlayMode::Preset(StrategyPath::AggressiveBargaining),
        StrategyPath::AggressiveBargaining,
      ),
    ] {
      let history = build_history_for_strategy(choice, DEFAULT_SEED, &ruleset).unwrap();
      let artifact = sample_replay_artifact(play_mode, history.clone());
      let serialized = serialize_replay_artifact(&artifact);

      assert_eq!(
        deserialize_replay_artifact(&serialized).unwrap().history,
        history
      );
      assert_eq!(
        verify_replay_artifact(&serialized, &ruleset)
          .unwrap()
          .final_state,
        history.transitions.last().unwrap().next
      );
    }
  }

  #[test]
  fn replay_artifact_round_trip_verifies_preset_path_one() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let artifact = sample_replay_artifact(
      PlayMode::Preset(StrategyPath::AccessStabilization),
      history.clone(),
    );
    let serialized = serialize_replay_artifact(&artifact);
    let restored = deserialize_replay_artifact(&serialized).unwrap();

    assert_eq!(restored.seed, DEFAULT_SEED);
    assert_eq!(
      restored.play_mode,
      PlayMode::Preset(StrategyPath::AccessStabilization)
    );
    assert_eq!(restored.history, history);
    assert_eq!(
      verify_replay_artifact(&serialized, &ruleset)
        .unwrap()
        .final_state,
      history.transitions.last().unwrap().next
    );
  }

  #[test]
  fn replay_artifact_golden_header_is_stable() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let artifact =
      sample_replay_artifact(PlayMode::Preset(StrategyPath::AccessStabilization), history);
    let serialized = serialize_replay_artifact(&artifact);
    let mut lines = serialized.lines();

    assert_eq!(lines.next(), Some(REPLAY_ARTIFACT_VERSION));
    assert_eq!(lines.next(), Some("ruleset=demo-ruleset-0.1.9"));
    assert_eq!(lines.next(), Some("seed=42"));
    assert_eq!(lines.next(), Some("play_mode=preset:1"));
    assert_eq!(
      lines.next(),
      Some(
        "genesis=turn:0,cash:100,staffed_beds:120,access_index:70,quality_index:78,workforce_trust:62,community_trust:66,commercial_rate:100,policy_pressure:30"
      )
    );
    assert_eq!(lines.next(), Some("transition_count=4"));
  }

  #[test]
  fn corrupt_replay_artifact_hash_fails_verification() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let mut artifact =
      sample_replay_artifact(PlayMode::Preset(StrategyPath::AccessStabilization), history);
    artifact.history.transitions[0].state_hash = "0000000000000000".to_string();
    let serialized = serialize_replay_artifact(&artifact);

    assert!(matches!(
      verify_replay_artifact(&serialized, &ruleset),
      Err(ReplayArtifactError::ReplayFailed(_))
    ));
  }

  #[test]
  fn interactive_defaults_match_preset_replay_artifact_history() {
    let ruleset = default_ruleset();
    let preset_history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let interactive_history =
      build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();
    let preset_artifact = sample_replay_artifact(
      PlayMode::Preset(StrategyPath::AccessStabilization),
      preset_history.clone(),
    );
    let interactive_artifact = sample_replay_artifact(PlayMode::Interactive, interactive_history);

    assert_eq!(preset_history, interactive_artifact.history);
    assert_ne!(preset_artifact.play_mode, interactive_artifact.play_mode);
    assert_eq!(
      serialize_replay_artifact(&preset_artifact)
        .replace("play_mode=preset:1", "play_mode=interactive"),
      serialize_replay_artifact(&interactive_artifact)
    );
  }

  #[test]
  fn unsupported_replay_artifact_version_is_rejected() {
    let ruleset = default_ruleset();
    let history =
      build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset)
        .unwrap();
    let mut serialized = serialize_replay_artifact(&sample_replay_artifact(
      PlayMode::Preset(StrategyPath::AccessStabilization),
      history,
    ));
    serialized = serialized.replacen(REPLAY_ARTIFACT_VERSION, "replay-artifact-0.0.0", 1);

    assert_eq!(
      verify_replay_artifact(&serialized, &ruleset),
      Err(ReplayArtifactError::UnsupportedVersion {
        found: "replay-artifact-0.0.0".to_string(),
      })
    );
  }
}
