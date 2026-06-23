#[derive(Clone, Debug, PartialEq, Eq)]
struct WorldState {
  turn: u32,
  cash: i32,
  staffed_beds: i32,
  access_index: i32,
  quality_index: i32,
  workforce_trust: i32,
  community_trust: i32,
  commercial_rate: i32,
  policy_pressure: i32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Ruleset {
  version: &'static str,
  max_capital_spend: i32,
  target_commercial_rate: i32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct ResolvedInputs {
  measurement_noise: i32,
  delayed_access_report: i32,
  labor_sick_call_delta: i32,
  policy_signal: i32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum PlayerCommand {
  StabilizeAccess {
    add_staffed_beds: i32,
    capital_spend: i32,
    requested_commercial_rate: i32,
  },
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum ValidationError {
  NonPositiveCapacityChange,
  NegativeCapitalSpend {
    requested: i32,
  },
  CapitalSpendTooHigh {
    requested: i32,
    available_limit: i32,
  },
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum InsurerDecision {
  Accept,
  Counter { offered_rate: i32 },
  Reject,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct ActorDecisionRecord {
  actor: &'static str,
  decision: InsurerDecision,
  rationale: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Observation {
  actor: &'static str,
  reported_access_index: i32,
  reported_quality_index: i32,
  policy_briefing: &'static str,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Event {
  actor: &'static str,
  description: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct AttributedEffect {
  source: &'static str,
  metric: &'static str,
  delta: i32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Transition {
  prior: WorldState,
  command: PlayerCommand,
  resolved_inputs: ResolvedInputs,
  observation: Observation,
  actor_decision: ActorDecisionRecord,
  events: Vec<Event>,
  effects: Vec<AttributedEffect>,
  next: WorldState,
  state_fingerprint: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct History {
  genesis: WorldState,
  transitions: Vec<Transition>,
}

fn main() {
  let ruleset = default_ruleset();
  let genesis = genesis_state();
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
  };

  let transition =
    transition(&genesis, command, inputs, &ruleset).expect("scripted demo command should be valid");
  let history = History {
    genesis,
    transitions: vec![transition],
  };

  print_demo(&history, &ruleset);
}

fn default_ruleset() -> Ruleset {
  Ruleset {
    version: "demo-ruleset-0.1.2",
    max_capital_spend: 40,
    target_commercial_rate: 106,
  }
}

fn genesis_state() -> WorldState {
  WorldState {
    turn: 0,
    cash: 100,
    staffed_beds: 120,
    access_index: 70,
    quality_index: 78,
    workforce_trust: 62,
    community_trust: 66,
    commercial_rate: 100,
    policy_pressure: 30,
  }
}

fn transition(
  prior: &WorldState,
  command: PlayerCommand,
  resolved_inputs: ResolvedInputs,
  ruleset: &Ruleset,
) -> Result<Transition, ValidationError> {
  validate_command(&command, ruleset)?;

  let observation = observe_for_player(prior, &resolved_inputs);
  let actor_decision = insurer_decision(&command, &observation, ruleset);
  let requested_commercial_rate = requested_commercial_rate(&command);
  let mut next = prior.clone();
  let mut events = Vec::new();
  let mut effects = Vec::new();

  next.turn += 1;
  next.policy_pressure += resolved_inputs.policy_signal;

  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate: _,
    } => {
      next.cash -= capital_spend;
      next.staffed_beds += add_staffed_beds;
      push_effect(&mut effects, "capacity investment", "cash", -capital_spend);
      push_effect(
        &mut effects,
        "capacity investment",
        "staffed_beds",
        add_staffed_beds,
      );

      let net_access_delta = add_staffed_beds / 2 + resolved_inputs.labor_sick_call_delta;
      next.access_index += net_access_delta;
      next.workforce_trust -= add_staffed_beds / 4;
      push_effect(
        &mut effects,
        "staffing constraint",
        "access_index",
        net_access_delta,
      );
      push_effect(
        &mut effects,
        "staffing constraint",
        "workforce_trust",
        -(add_staffed_beds / 4),
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Opened {add_staffed_beds} staffed beds while absorbing {capital_spend} capital units."
        ),
      });
    }
  }

  match actor_decision.decision {
    InsurerDecision::Accept => {
      let delta = requested_commercial_rate - prior.commercial_rate;
      next.commercial_rate += delta;
      push_effect(&mut effects, "commercial insurer", "commercial_rate", delta);
      events.push(Event {
        actor: "commercial_insurer",
        description: "Accepted the requested rate path to preserve network access.".to_string(),
      });
    }
    InsurerDecision::Counter { offered_rate } => {
      let delta = offered_rate - prior.commercial_rate;
      next.commercial_rate += delta;
      next.community_trust -= 1;
      push_effect(&mut effects, "commercial insurer", "commercial_rate", delta);
      push_effect(
        &mut effects,
        "public bargaining friction",
        "community_trust",
        -1,
      );
      events.push(Event {
        actor: "commercial_insurer",
        description: format!("Countered with a rate of {offered_rate}."),
      });
    }
    InsurerDecision::Reject => {
      next.community_trust -= 3;
      push_effect(&mut effects, "failed negotiation", "community_trust", -3);
      events.push(Event {
        actor: "commercial_insurer",
        description: "Rejected the rate request and signaled a narrow-network threat.".to_string(),
      });
    }
  }

  next.quality_index = clamp_metric(next.quality_index);
  next.access_index = clamp_metric(next.access_index);
  next.workforce_trust = clamp_metric(next.workforce_trust);
  next.community_trust = clamp_metric(next.community_trust);
  next.policy_pressure = clamp_metric(next.policy_pressure);

  let state_fingerprint = fingerprint_state(&next, ruleset);

  Ok(Transition {
    prior: prior.clone(),
    command,
    resolved_inputs,
    observation,
    actor_decision,
    events,
    effects,
    next,
    state_fingerprint,
  })
}

fn validate_command(command: &PlayerCommand, ruleset: &Ruleset) -> Result<(), ValidationError> {
  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate: _,
    } => {
      if *add_staffed_beds <= 0 {
        return Err(ValidationError::NonPositiveCapacityChange);
      }

      if *capital_spend < 0 {
        return Err(ValidationError::NegativeCapitalSpend {
          requested: *capital_spend,
        });
      }

      if *capital_spend > ruleset.max_capital_spend {
        return Err(ValidationError::CapitalSpendTooHigh {
          requested: *capital_spend,
          available_limit: ruleset.max_capital_spend,
        });
      }
    }
  }

  Ok(())
}

fn requested_commercial_rate(command: &PlayerCommand) -> i32 {
  match command {
    PlayerCommand::StabilizeAccess {
      requested_commercial_rate,
      ..
    } => *requested_commercial_rate,
  }
}

fn observe_for_player(prior: &WorldState, inputs: &ResolvedInputs) -> Observation {
  let policy_briefing = if inputs.policy_signal >= 3 {
    "state officials are increasing scrutiny of access and affordability"
  } else {
    "state policy attention is stable"
  };

  Observation {
    actor: "health_system_ceo",
    reported_access_index: clamp_metric(inputs.delayed_access_report + inputs.measurement_noise),
    reported_quality_index: prior.quality_index,
    policy_briefing,
  }
}

fn insurer_decision(
  command: &PlayerCommand,
  observation: &Observation,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let PlayerCommand::StabilizeAccess {
    requested_commercial_rate,
    ..
  } = command;

  let (decision, rationale) = if *requested_commercial_rate <= ruleset.target_commercial_rate {
    (
      InsurerDecision::Accept,
      format!(
        "Requested rate {requested_commercial_rate} is within target and reported access is {}.",
        observation.reported_access_index
      ),
    )
  } else if observation.reported_access_index < 70 {
    (
      InsurerDecision::Counter {
        offered_rate: ruleset.target_commercial_rate,
      },
      format!(
        "Reported access {} gives the provider leverage, but requested rate {requested_commercial_rate} exceeds target {}.",
        observation.reported_access_index, ruleset.target_commercial_rate
      ),
    )
  } else {
    (
      InsurerDecision::Reject,
      format!(
        "Reported access {} is adequate, so the insurer resists requested rate {requested_commercial_rate}.",
        observation.reported_access_index
      ),
    )
  };

  ActorDecisionRecord {
    actor: "commercial_insurer",
    decision,
    rationale,
  }
}

fn replay(history: &History, ruleset: &Ruleset) -> Result<WorldState, ValidationError> {
  let mut state = history.genesis.clone();

  for committed in &history.transitions {
    let replayed = transition(
      &state,
      committed.command.clone(),
      committed.resolved_inputs.clone(),
      ruleset,
    )?;
    state = replayed.next;
  }

  Ok(state)
}

fn print_demo(history: &History, ruleset: &Ruleset) {
  let transition = history
    .transitions
    .last()
    .expect("demo history should include one transition");
  let replayed = replay(history, ruleset).expect("demo history should replay");

  println!("Health Policy Strategy Game deterministic demo");
  println!("Ruleset: {}", ruleset.version);
  println!(
    "Turn: {} -> {}",
    transition.prior.turn, transition.next.turn
  );
  println!(
    "CEO observation: access {}, quality {}, policy briefing: {}",
    transition.observation.reported_access_index,
    transition.observation.reported_quality_index,
    transition.observation.policy_briefing
  );
  println!(
    "Insurer decision: {:?} ({})",
    transition.actor_decision.decision, transition.actor_decision.rationale
  );
  println!("Events:");
  for event in &transition.events {
    println!("  - {}: {}", event.actor, event.description);
  }
  println!("Effects:");
  for effect in &transition.effects {
    println!(
      "  - {} changed {} by {}",
      effect.source, effect.metric, effect.delta
    );
  }
  println!("Next state fingerprint: {}", transition.state_fingerprint);
  println!(
    "Replay final state matches committed state: {}",
    replayed == transition.next
  );
}

fn push_effect(
  effects: &mut Vec<AttributedEffect>,
  source: &'static str,
  metric: &'static str,
  delta: i32,
) {
  effects.push(AttributedEffect {
    source,
    metric,
    delta,
  });
}

fn clamp_metric(value: i32) -> i32 {
  value.clamp(0, 100)
}

fn fingerprint_state(state: &WorldState, ruleset: &Ruleset) -> String {
  format!(
    "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}",
    ruleset.version,
    state.turn,
    state.cash,
    state.staffed_beds,
    state.access_index,
    state.quality_index,
    state.workforce_trust,
    state.community_trust,
    state.commercial_rate,
    state.policy_pressure
  )
}

#[cfg(test)]
mod tests {
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
    };

    let result = transition(&prior, command, inputs, &ruleset).unwrap();

    assert_eq!(result.actor_decision.decision, InsurerDecision::Accept);
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
    };

    let result = transition(&prior, command, inputs, &ruleset).unwrap();

    assert_eq!(result.actor_decision.decision, InsurerDecision::Reject);
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
      },
      &ruleset,
    )
    .unwrap();
    let history = History {
      genesis,
      transitions: vec![first.clone()],
    };

    assert_eq!(replay(&history, &ruleset).unwrap(), first.next);
  }
}
