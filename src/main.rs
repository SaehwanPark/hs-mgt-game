use std::io;

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
  max_advocacy_spend: i32,
  target_commercial_rate: i32,
  minimum_access_commitment: i32,
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
  RespondToStateAccessMandate {
    advocacy_spend: i32,
    access_commitment: i32,
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
  NegativeAdvocacySpend {
    requested: i32,
  },
  AdvocacySpendTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveAccessCommitment,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum InsurerDecision {
  Accept,
  Counter { offered_rate: i32 },
  Reject,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum StatePolicyDecision {
  GrantFlexibility,
  ProceedWithMandate,
  EscalateOversight,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum ActorDecision {
  Insurer(InsurerDecision),
  StatePolicy(StatePolicyDecision),
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct ActorDecisionRecord {
  actor: &'static str,
  decision: ActorDecision,
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

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum StrategyPath {
  AccessStabilization,
  FiscalCaution,
  AggressiveBargaining,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct StrategyPlan {
  name: &'static str,
  first_command: PlayerCommand,
  first_inputs: ResolvedInputs,
  second_command: PlayerCommand,
  second_inputs: ResolvedInputs,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum CliError {
  InvalidStrategyChoice(String),
  InvalidStrategyPlan(ValidationError),
  InputUnavailable,
}

fn main() {
  let ruleset = default_ruleset();

  match read_strategy_choice().and_then(|choice| run_selected_strategy(choice, &ruleset)) {
    Ok(()) => {}
    Err(error) => {
      eprintln!("Unable to run demo: {}", describe_cli_error(&error));
      std::process::exit(1);
    }
  }
}

fn default_ruleset() -> Ruleset {
  Ruleset {
    version: "demo-ruleset-0.1.5",
    max_capital_spend: 40,
    max_advocacy_spend: 20,
    target_commercial_rate: 106,
    minimum_access_commitment: 5,
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

fn read_strategy_choice() -> Result<StrategyPath, CliError> {
  println!("Choose a strategy path:");
  println!("  1. Access stabilization");
  println!("  2. Fiscal caution");
  println!("  3. Aggressive bargaining");
  println!("Press Enter for option 1.");

  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;
  parse_strategy_choice(&input)
}

fn run_selected_strategy(choice: StrategyPath, ruleset: &Ruleset) -> Result<(), CliError> {
  println!("Selected strategy: {}", strategy_plan(choice).name);
  let history =
    build_history_for_strategy(choice, ruleset).map_err(CliError::InvalidStrategyPlan)?;
  print_demo(&history, ruleset);
  Ok(())
}

fn parse_strategy_choice(input: &str) -> Result<StrategyPath, CliError> {
  let trimmed = input.trim();

  match trimmed {
    "" | "1" => Ok(StrategyPath::AccessStabilization),
    "2" => Ok(StrategyPath::FiscalCaution),
    "3" => Ok(StrategyPath::AggressiveBargaining),
    other => Err(CliError::InvalidStrategyChoice(other.to_string())),
  }
}

fn build_history_for_strategy(
  choice: StrategyPath,
  ruleset: &Ruleset,
) -> Result<History, ValidationError> {
  let plan = strategy_plan(choice);
  let genesis = genesis_state();
  let first = transition(
    &genesis,
    plan.first_command.clone(),
    plan.first_inputs.clone(),
    ruleset,
  )?;
  let second = transition(
    &first.next,
    plan.second_command.clone(),
    plan.second_inputs.clone(),
    ruleset,
  )?;

  Ok(History {
    genesis,
    transitions: vec![first, second],
  })
}

fn strategy_plan(choice: StrategyPath) -> StrategyPlan {
  match choice {
    StrategyPath::AccessStabilization => StrategyPlan {
      name: "Access stabilization",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 8,
        capital_spend: 18,
        requested_commercial_rate: 112,
      },
      first_inputs: ResolvedInputs {
        measurement_noise: -2,
        delayed_access_report: 67,
        labor_sick_call_delta: -3,
        policy_signal: 4,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 10,
        access_commitment: 7,
      },
      second_inputs: ResolvedInputs {
        measurement_noise: 1,
        delayed_access_report: 69,
        labor_sick_call_delta: 0,
        policy_signal: 4,
      },
    },
    StrategyPath::FiscalCaution => StrategyPlan {
      name: "Fiscal caution",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 4,
        capital_spend: 10,
        requested_commercial_rate: 104,
      },
      first_inputs: ResolvedInputs {
        measurement_noise: 0,
        delayed_access_report: 74,
        labor_sick_call_delta: 0,
        policy_signal: 1,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 4,
        access_commitment: 5,
      },
      second_inputs: ResolvedInputs {
        measurement_noise: 0,
        delayed_access_report: 75,
        labor_sick_call_delta: 0,
        policy_signal: 1,
      },
    },
    StrategyPath::AggressiveBargaining => StrategyPlan {
      name: "Aggressive bargaining",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 2,
        capital_spend: 5,
        requested_commercial_rate: 120,
      },
      first_inputs: ResolvedInputs {
        measurement_noise: 0,
        delayed_access_report: 80,
        labor_sick_call_delta: 0,
        policy_signal: 2,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 2,
        access_commitment: 3,
      },
      second_inputs: ResolvedInputs {
        measurement_noise: 0,
        delayed_access_report: 75,
        labor_sick_call_delta: 0,
        policy_signal: 2,
      },
    },
  }
}

fn describe_cli_error(error: &CliError) -> String {
  match error {
    CliError::InvalidStrategyChoice(choice) => {
      format!("strategy choice '{choice}' is not available; use 1, 2, or 3")
    }
    CliError::InvalidStrategyPlan(error) => {
      format!("selected strategy is internally invalid: {error:?}")
    }
    CliError::InputUnavailable => "could not read strategy choice from standard input".to_string(),
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
  let actor_decision = actor_decision(&command, &observation, &resolved_inputs, ruleset);
  let accepted_requested_commercial_rate = requested_commercial_rate(&command);
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
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => {
      next.cash -= advocacy_spend;
      next.access_index += access_commitment / 2;
      push_effect(&mut effects, "policy response", "cash", -advocacy_spend);
      push_effect(
        &mut effects,
        "policy response",
        "access_index",
        access_commitment / 2,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Committed {access_commitment} access units while spending {advocacy_spend} on state engagement."
        ),
      });
    }
  }

  match &actor_decision.decision {
    ActorDecision::Insurer(InsurerDecision::Accept) => {
      let requested_commercial_rate =
        accepted_requested_commercial_rate.expect("insurer decision requires rate command");
      let delta = requested_commercial_rate - prior.commercial_rate;
      next.commercial_rate += delta;
      push_effect(&mut effects, "commercial insurer", "commercial_rate", delta);
      events.push(Event {
        actor: "commercial_insurer",
        description: "Accepted the requested rate path to preserve network access.".to_string(),
      });
    }
    ActorDecision::Insurer(InsurerDecision::Counter { offered_rate }) => {
      let delta = *offered_rate - prior.commercial_rate;
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
    ActorDecision::Insurer(InsurerDecision::Reject) => {
      next.community_trust -= 3;
      push_effect(&mut effects, "failed negotiation", "community_trust", -3);
      events.push(Event {
        actor: "commercial_insurer",
        description: "Rejected the rate request and signaled a narrow-network threat.".to_string(),
      });
    }
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility) => {
      next.policy_pressure -= 5;
      next.community_trust += 2;
      push_effect(&mut effects, "state policy response", "policy_pressure", -5);
      push_effect(&mut effects, "state policy response", "community_trust", 2);
      events.push(Event {
        actor: "state_policy_officials",
        description: "Granted implementation flexibility after a credible access commitment."
          .to_string(),
      });
    }
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate) => {
      next.policy_pressure += 2;
      next.community_trust += 1;
      push_effect(&mut effects, "state policy response", "policy_pressure", 2);
      push_effect(&mut effects, "state policy response", "community_trust", 1);
      events.push(Event {
        actor: "state_policy_officials",
        description: "Kept the mandate on schedule while acknowledging the access plan."
          .to_string(),
      });
    }
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight) => {
      next.policy_pressure += 6;
      next.community_trust -= 2;
      push_effect(&mut effects, "state policy response", "policy_pressure", 6);
      push_effect(&mut effects, "state policy response", "community_trust", -2);
      events.push(Event {
        actor: "state_policy_officials",
        description: "Escalated oversight after judging the response insufficient.".to_string(),
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
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => {
      if *advocacy_spend < 0 {
        return Err(ValidationError::NegativeAdvocacySpend {
          requested: *advocacy_spend,
        });
      }

      if *advocacy_spend > ruleset.max_advocacy_spend {
        return Err(ValidationError::AdvocacySpendTooHigh {
          requested: *advocacy_spend,
          available_limit: ruleset.max_advocacy_spend,
        });
      }

      if *access_commitment <= 0 {
        return Err(ValidationError::NonPositiveAccessCommitment);
      }
    }
  }

  Ok(())
}

fn requested_commercial_rate(command: &PlayerCommand) -> Option<i32> {
  match command {
    PlayerCommand::StabilizeAccess {
      requested_commercial_rate,
      ..
    } => Some(*requested_commercial_rate),
    PlayerCommand::RespondToStateAccessMandate { .. } => None,
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

fn actor_decision(
  command: &PlayerCommand,
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
  }
}

fn insurer_decision(
  requested_commercial_rate: i32,
  observation: &Observation,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let (decision, rationale) = if requested_commercial_rate <= ruleset.target_commercial_rate {
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
    decision: ActorDecision::Insurer(decision),
    rationale,
  }
}

fn state_policy_decision(
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
  let replayed = replay(history, ruleset).expect("demo history should replay");

  println!("Health Policy Strategy Game deterministic demo");
  println!("Ruleset: {}", ruleset.version);
  for transition in &history.transitions {
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
      "{} decision: {} ({})",
      transition.actor_decision.actor,
      describe_actor_decision(&transition.actor_decision.decision),
      transition.actor_decision.rationale
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
  }
  println!(
    "Replay final state matches committed state: {}",
    history
      .transitions
      .last()
      .is_some_and(|transition| replayed == transition.next)
  );
  println!("Educational debrief:");
  for line in educational_debrief(history) {
    println!("  - {line}");
  }
}

fn educational_debrief(history: &History) -> Vec<String> {
  let Some(last_transition) = history.transitions.last() else {
    return vec!["No committed transitions are available for debriefing.".to_string()];
  };

  let initial = &history.genesis;
  let final_state = &last_transition.next;
  let actor_rationales = history
    .transitions
    .iter()
    .map(|transition| {
      format!(
        "{}: {}",
        transition.actor_decision.actor, transition.actor_decision.rationale
      )
    })
    .collect::<Vec<_>>()
    .join(" | ");

  let effect_summary = history
    .transitions
    .iter()
    .flat_map(|transition| transition.effects.iter())
    .map(|effect| {
      format!(
        "{} changed {} by {}",
        effect.source, effect.metric, effect.delta
      )
    })
    .collect::<Vec<_>>()
    .join("; ");

  vec![
    format!(
      "Run-level tradeoff: cash moved from {} to {}, access from {} to {}, workforce trust from {} to {}, community trust from {} to {}, policy pressure from {} to {}, and commercial rate from {} to {}.",
      initial.cash,
      final_state.cash,
      initial.access_index,
      final_state.access_index,
      initial.workforce_trust,
      final_state.workforce_trust,
      initial.community_trust,
      final_state.community_trust,
      initial.policy_pressure,
      final_state.policy_pressure,
      initial.commercial_rate,
      final_state.commercial_rate
    ),
    format!("Actor rationales at decision time: {actor_rationales}"),
    format!("Attributed mechanisms to inspect: {effect_summary}."),
    "Debrief prompt: Was the CEO's access strategy reasonable given the reported access values and the later policy response?".to_string(),
    "Decision quality and outcome quality are separate: replay preserves what each actor observed and why each modeled response occurred.".to_string(),
  ]
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

fn describe_actor_decision(decision: &ActorDecision) -> String {
  match decision {
    ActorDecision::Insurer(InsurerDecision::Accept) => "accept".to_string(),
    ActorDecision::Insurer(InsurerDecision::Counter { offered_rate }) => {
      format!("counter at {offered_rate}")
    }
    ActorDecision::Insurer(InsurerDecision::Reject) => "reject".to_string(),
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility) => {
      "grant flexibility".to_string()
    }
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate) => {
      "proceed with mandate".to_string()
    }
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight) => {
      "escalate oversight".to_string()
    }
  }
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
      },
      &ruleset,
    )
    .unwrap();
    let history = History {
      genesis,
      transitions: vec![first, second.clone()],
    };

    assert_eq!(replay(&history, &ruleset).unwrap(), second.next);
  }

  #[test]
  fn debrief_includes_actor_rationales() {
    let history = demo_history();
    let debrief = educational_debrief(&history).join("\n");

    assert!(debrief.contains("commercial_insurer:"));
    assert!(debrief.contains("state_policy_officials:"));
    assert!(debrief.contains("Reported access"));
    assert!(debrief.contains("Access commitment"));
  }

  #[test]
  fn debrief_includes_attributed_tradeoff() {
    let history = demo_history();
    let debrief = educational_debrief(&history).join("\n");

    assert!(debrief.contains("cash moved from 100 to 72"));
    assert!(debrief.contains("access from 70 to 74"));
    assert!(debrief.contains("capacity investment changed cash by -18"));
    assert!(debrief.contains("state policy response changed community_trust by 2"));
  }

  #[test]
  fn identical_histories_produce_identical_debriefs() {
    let first = demo_history();
    let second = demo_history();

    assert_eq!(educational_debrief(&first), educational_debrief(&second));
  }

  #[test]
  fn empty_cli_choice_defaults_to_access_stabilization() {
    assert_eq!(
      parse_strategy_choice("\n").unwrap(),
      StrategyPath::AccessStabilization
    );
  }

  #[test]
  fn numbered_cli_choices_select_expected_strategy_paths() {
    assert_eq!(
      parse_strategy_choice("1\n").unwrap(),
      StrategyPath::AccessStabilization
    );
    assert_eq!(
      parse_strategy_choice("2\n").unwrap(),
      StrategyPath::FiscalCaution
    );
    assert_eq!(
      parse_strategy_choice("3\n").unwrap(),
      StrategyPath::AggressiveBargaining
    );
  }

  #[test]
  fn invalid_cli_choice_is_error() {
    assert_eq!(
      parse_strategy_choice("9\n"),
      Err(CliError::InvalidStrategyChoice("9".to_string()))
    );
  }

  #[test]
  fn each_strategy_path_builds_replayable_history() {
    let ruleset = default_ruleset();

    for choice in [
      StrategyPath::AccessStabilization,
      StrategyPath::FiscalCaution,
      StrategyPath::AggressiveBargaining,
    ] {
      let history = build_history_for_strategy(choice, &ruleset).unwrap();
      let final_state = history.transitions.last().unwrap().next.clone();

      assert_eq!(history.transitions.len(), 2);
      assert_eq!(replay(&history, &ruleset).unwrap(), final_state);
    }
  }

  #[test]
  fn fiscal_caution_accepts_rate_and_proceeds_with_mandate() {
    let ruleset = default_ruleset();
    let history = build_history_for_strategy(StrategyPath::FiscalCaution, &ruleset).unwrap();

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
    let history = build_history_for_strategy(StrategyPath::AggressiveBargaining, &ruleset).unwrap();

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
    build_history_for_strategy(StrategyPath::AccessStabilization, &ruleset).unwrap()
  }
}
