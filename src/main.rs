use std::io;

const DEFAULT_SEED: u64 = 42;

const STREAM_MEASUREMENT: u32 = 0;
const STREAM_ACCESS_DELAY: u32 = 1;
const STREAM_ACCESS_NOISE: u32 = 2;
const STREAM_LABOR: u32 = 3;
const STREAM_POLICY: u32 = 4;
const STREAM_COALITION: u32 = 5;
const STREAM_REVISION: u32 = 6;

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
  max_retention_spend: i32,
  max_schedule_relief_commitment: i32,
  max_coalition_investment: i32,
  target_commercial_rate: i32,
  minimum_access_commitment: i32,
  minimum_retention_spend: i32,
  minimum_schedule_relief: i32,
  minimum_coalition_investment: i32,
  minimum_shared_access_commitment: i32,
  max_shared_access_commitment: i32,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct ResolvedInputs {
  measurement_noise: i32,
  delayed_access_report: i32,
  labor_sick_call_delta: i32,
  policy_signal: i32,
  coalition_leverage_signal: i32,
  access_measurement_revision: i32,
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
  RespondToWorkforcePressure {
    retention_spend: i32,
    schedule_relief_commitment: i32,
  },
  JoinRegionalAccessCoalition {
    coalition_investment: i32,
    shared_access_commitment: i32,
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
  NegativeRetentionSpend {
    requested: i32,
  },
  RetentionSpendTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveScheduleRelief,
  ScheduleReliefTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NegativeCoalitionInvestment {
    requested: i32,
  },
  CoalitionInvestmentTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveSharedAccessCommitment,
  SharedAccessCommitmentTooHigh {
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
enum StatePolicyDecision {
  GrantFlexibility,
  ProceedWithMandate,
  EscalateOversight,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum LaborDecision {
  Cooperative,
  LimitedSupport,
  WorkAction,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum CoalitionDecision {
  FullPartnership,
  LimitedParticipation,
  CoalitionWithdrawal,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum ActorDecision {
  Insurer(InsurerDecision),
  StatePolicy(StatePolicyDecision),
  Labor(LaborDecision),
  Coalition(CoalitionDecision),
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
  prior_access_revision: i32,
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
  second_command: PlayerCommand,
  third_command: PlayerCommand,
  fourth_command: PlayerCommand,
}

#[derive(Clone, Debug, PartialEq, Eq)]
enum CliError {
  InvalidStrategyChoice(String),
  InvalidSeed(String),
  InvalidStrategyPlan(ValidationError),
  InputUnavailable,
}

fn main() {
  let ruleset = default_ruleset();

  match read_run_config().and_then(|config| run_selected_strategy(config, &ruleset)) {
    Ok(()) => {}
    Err(error) => {
      eprintln!("Unable to run demo: {}", describe_cli_error(&error));
      std::process::exit(1);
    }
  }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct RunConfig {
  seed: u64,
  strategy: StrategyPath,
}

fn default_ruleset() -> Ruleset {
  Ruleset {
    version: "demo-ruleset-0.1.9",
    max_capital_spend: 40,
    max_advocacy_spend: 20,
    max_retention_spend: 25,
    max_schedule_relief_commitment: 20,
    max_coalition_investment: 20,
    target_commercial_rate: 106,
    minimum_access_commitment: 5,
    minimum_retention_spend: 5,
    minimum_schedule_relief: 3,
    minimum_coalition_investment: 4,
    minimum_shared_access_commitment: 4,
    max_shared_access_commitment: 20,
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

fn read_run_config() -> Result<RunConfig, CliError> {
  let strategy = read_strategy_choice()?;
  let seed = read_seed_choice()?;
  Ok(RunConfig { seed, strategy })
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

fn read_seed_choice() -> Result<u64, CliError> {
  println!("Seed (Enter for default {DEFAULT_SEED}):");

  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;
  parse_seed_choice(&input)
}

fn parse_seed_choice(input: &str) -> Result<u64, CliError> {
  let trimmed = input.trim();

  if trimmed.is_empty() {
    return Ok(DEFAULT_SEED);
  }

  trimmed
    .parse::<u64>()
    .map_err(|_| CliError::InvalidSeed(trimmed.to_string()))
}

fn run_selected_strategy(config: RunConfig, ruleset: &Ruleset) -> Result<(), CliError> {
  println!("Selected strategy: {}", strategy_plan(config.strategy).name);
  let history = build_history_for_strategy(config.strategy, config.seed, ruleset)
    .map_err(CliError::InvalidStrategyPlan)?;
  print_demo(config.seed, &history, ruleset);
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
  seed: u64,
  ruleset: &Ruleset,
) -> Result<History, ValidationError> {
  let plan = strategy_plan(choice);
  let genesis = genesis_state();
  let first_inputs = resolve_inputs(seed, &genesis, ruleset);
  let first = transition(&genesis, plan.first_command.clone(), first_inputs, ruleset)?;
  let second_inputs = resolve_inputs(seed, &first.next, ruleset);
  let second = transition(
    &first.next,
    plan.second_command.clone(),
    second_inputs,
    ruleset,
  )?;
  let third_inputs = resolve_inputs(seed, &second.next, ruleset);
  let third = transition(
    &second.next,
    plan.third_command.clone(),
    third_inputs,
    ruleset,
  )?;
  let fourth_inputs = resolve_inputs(seed, &third.next, ruleset);
  let fourth = transition(
    &third.next,
    plan.fourth_command.clone(),
    fourth_inputs,
    ruleset,
  )?;

  Ok(History {
    genesis,
    transitions: vec![first, second, third, fourth],
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
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 10,
        access_commitment: 7,
      },
      third_command: PlayerCommand::RespondToWorkforcePressure {
        retention_spend: 14,
        schedule_relief_commitment: 8,
      },
      fourth_command: PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment: 12,
        shared_access_commitment: 8,
      },
    },
    StrategyPath::FiscalCaution => StrategyPlan {
      name: "Fiscal caution",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 4,
        capital_spend: 10,
        requested_commercial_rate: 104,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 4,
        access_commitment: 5,
      },
      third_command: PlayerCommand::RespondToWorkforcePressure {
        retention_spend: 8,
        schedule_relief_commitment: 5,
      },
      fourth_command: PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment: 6,
        shared_access_commitment: 5,
      },
    },
    StrategyPath::AggressiveBargaining => StrategyPlan {
      name: "Aggressive bargaining",
      first_command: PlayerCommand::StabilizeAccess {
        add_staffed_beds: 2,
        capital_spend: 5,
        requested_commercial_rate: 120,
      },
      second_command: PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend: 2,
        access_commitment: 3,
      },
      third_command: PlayerCommand::RespondToWorkforcePressure {
        retention_spend: 2,
        schedule_relief_commitment: 2,
      },
      fourth_command: PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment: 4,
        shared_access_commitment: 4,
      },
    },
  }
}

fn describe_cli_error(error: &CliError) -> String {
  match error {
    CliError::InvalidStrategyChoice(choice) => {
      format!("strategy choice '{choice}' is not available; use 1, 2, or 3")
    }
    CliError::InvalidSeed(seed) => {
      format!("seed '{seed}' is not a valid unsigned integer")
    }
    CliError::InvalidStrategyPlan(error) => {
      format!("selected strategy is internally invalid: {error:?}")
    }
    CliError::InputUnavailable => "could not read input from standard input".to_string(),
  }
}

fn resolve_inputs(seed: u64, prior: &WorldState, _ruleset: &Ruleset) -> ResolvedInputs {
  // `_ruleset` is reserved for future ruleset-gated stream bounds.
  let turn = prior.turn;

  let measurement_noise = bounded_i32(stream_rng(seed, turn, STREAM_MEASUREMENT), -5, 5);
  let access_delay = bounded_u32(stream_rng(seed, turn, STREAM_ACCESS_DELAY), 2, 8);
  let access_noise = bounded_i32(stream_rng(seed, turn, STREAM_ACCESS_NOISE), -2, 2);
  let delayed_access_report = clamp_metric(prior.access_index - access_delay as i32 + access_noise);
  let labor_sick_call_delta = bounded_i32(stream_rng(seed, turn, STREAM_LABOR), -5, 0);
  let policy_signal = bounded_i32(stream_rng(seed, turn, STREAM_POLICY), 1, 6);
  let coalition_leverage_signal = bounded_i32(stream_rng(seed, turn, STREAM_COALITION), 1, 6);
  let access_measurement_revision = if turn > 0 {
    bounded_i32(stream_rng(seed, turn, STREAM_REVISION), -3, 3)
  } else {
    0
  };

  ResolvedInputs {
    measurement_noise,
    delayed_access_report,
    labor_sick_call_delta,
    policy_signal,
    coalition_leverage_signal,
    access_measurement_revision,
  }
}

fn stream_rng(seed: u64, turn: u32, stream_id: u32) -> u64 {
  let state = seed
    .wrapping_add((turn as u64).wrapping_mul(0x517c_c1b7_2722_0a95))
    .wrapping_add((stream_id as u64).wrapping_mul(0x6c62_272e_07bb_0142));
  splitmix64(state)
}

fn splitmix64(mut z: u64) -> u64 {
  z = z.wrapping_add(0x9e37_79b9_7f4a_7c15);
  z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
  z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
  z ^ (z >> 31)
}

fn bounded_u32(value: u64, lo: u32, hi: u32) -> u32 {
  debug_assert!(lo <= hi, "bounded_u32: hi must be >= lo");
  let span = (hi - lo + 1) as u64;
  lo + (value % span) as u32
}

fn bounded_i32(value: u64, lo: i32, hi: i32) -> i32 {
  debug_assert!(lo <= hi, "bounded_i32: hi must be >= lo");
  let span = (hi - lo + 1) as u64;
  lo + (value % span) as i32
}

fn transition(
  prior: &WorldState,
  command: PlayerCommand,
  resolved_inputs: ResolvedInputs,
  ruleset: &Ruleset,
) -> Result<Transition, ValidationError> {
  validate_command(&command, ruleset)?;

  let observation = observe_for_player(prior, &resolved_inputs);
  let actor_decision = actor_decision(&command, prior, &observation, &resolved_inputs, ruleset);
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
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => {
      next.cash -= retention_spend;
      next.workforce_trust += schedule_relief_commitment / 2;
      next.access_index += schedule_relief_commitment / 4;
      push_effect(&mut effects, "workforce response", "cash", -retention_spend);
      push_effect(
        &mut effects,
        "workforce response",
        "workforce_trust",
        schedule_relief_commitment / 2,
      );
      push_effect(
        &mut effects,
        "schedule relief",
        "access_index",
        schedule_relief_commitment / 4,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Offered {retention_spend} retention units and {schedule_relief_commitment} schedule-relief commitment to address labor pressure."
        ),
      });
    }
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => {
      next.cash -= coalition_investment;
      next.access_index += shared_access_commitment / 2;
      next.community_trust += shared_access_commitment / 4;
      push_effect(
        &mut effects,
        "coalition response",
        "cash",
        -coalition_investment,
      );
      push_effect(
        &mut effects,
        "coalition response",
        "access_index",
        shared_access_commitment / 2,
      );
      push_effect(
        &mut effects,
        "coalition response",
        "community_trust",
        shared_access_commitment / 4,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Committed {shared_access_commitment} shared access units and {coalition_investment} coalition investment to join the regional access coalition."
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
    ActorDecision::Labor(LaborDecision::Cooperative) => {
      next.workforce_trust += 4;
      next.quality_index += 2;
      next.access_index += 1;
      push_effect(&mut effects, "nursing workforce", "workforce_trust", 4);
      push_effect(&mut effects, "nursing workforce", "quality_index", 2);
      push_effect(&mut effects, "nursing workforce", "access_index", 1);
      events.push(Event {
        actor: "nursing_workforce",
        description: "Accepted the retention package and schedule relief plan.".to_string(),
      });
    }
    ActorDecision::Labor(LaborDecision::LimitedSupport) => {
      next.workforce_trust += 1;
      push_effect(&mut effects, "nursing workforce", "workforce_trust", 1);
      events.push(Event {
        actor: "nursing_workforce",
        description: "Offered limited support while monitoring staffing conditions.".to_string(),
      });
    }
    ActorDecision::Labor(LaborDecision::WorkAction) => {
      next.access_index -= 4;
      next.quality_index -= 2;
      next.community_trust -= 2;
      next.workforce_trust -= 2;
      push_effect(&mut effects, "work action signal", "access_index", -4);
      push_effect(&mut effects, "work action signal", "quality_index", -2);
      push_effect(&mut effects, "work action signal", "community_trust", -2);
      push_effect(&mut effects, "work action signal", "workforce_trust", -2);
      events.push(Event {
        actor: "nursing_workforce",
        description: "Signaled a work action after judging the retention offer insufficient."
          .to_string(),
      });
    }
    ActorDecision::Coalition(CoalitionDecision::FullPartnership) => {
      next.community_trust += 4;
      next.policy_pressure -= 3;
      next.access_index += 2;
      push_effect(
        &mut effects,
        "regional provider coalition",
        "community_trust",
        4,
      );
      push_effect(
        &mut effects,
        "regional provider coalition",
        "policy_pressure",
        -3,
      );
      push_effect(
        &mut effects,
        "regional provider coalition",
        "access_index",
        2,
      );
      events.push(Event {
        actor: "regional_provider_coalition",
        description:
          "Accepted full partnership after a credible coalition investment and access commitment."
            .to_string(),
      });
    }
    ActorDecision::Coalition(CoalitionDecision::LimitedParticipation) => {
      next.community_trust += 1;
      push_effect(
        &mut effects,
        "regional provider coalition",
        "community_trust",
        1,
      );
      events.push(Event {
        actor: "regional_provider_coalition",
        description: "Offered limited participation while monitoring coalition conditions."
          .to_string(),
      });
    }
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal) => {
      next.community_trust -= 3;
      next.policy_pressure += 4;
      push_effect(&mut effects, "coalition withdrawal", "community_trust", -3);
      push_effect(&mut effects, "coalition withdrawal", "policy_pressure", 4);
      events.push(Event {
        actor: "regional_provider_coalition",
        description: "Withdrew from the coalition after judging the investment and access commitment insufficient.".to_string(),
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
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => {
      if *retention_spend < 0 {
        return Err(ValidationError::NegativeRetentionSpend {
          requested: *retention_spend,
        });
      }

      if *retention_spend > ruleset.max_retention_spend {
        return Err(ValidationError::RetentionSpendTooHigh {
          requested: *retention_spend,
          available_limit: ruleset.max_retention_spend,
        });
      }

      if *schedule_relief_commitment <= 0 {
        return Err(ValidationError::NonPositiveScheduleRelief);
      }

      if *schedule_relief_commitment > ruleset.max_schedule_relief_commitment {
        return Err(ValidationError::ScheduleReliefTooHigh {
          requested: *schedule_relief_commitment,
          available_limit: ruleset.max_schedule_relief_commitment,
        });
      }
    }
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => {
      if *coalition_investment < 0 {
        return Err(ValidationError::NegativeCoalitionInvestment {
          requested: *coalition_investment,
        });
      }

      if *coalition_investment > ruleset.max_coalition_investment {
        return Err(ValidationError::CoalitionInvestmentTooHigh {
          requested: *coalition_investment,
          available_limit: ruleset.max_coalition_investment,
        });
      }

      if *shared_access_commitment <= 0 {
        return Err(ValidationError::NonPositiveSharedAccessCommitment);
      }

      if *shared_access_commitment > ruleset.max_shared_access_commitment {
        return Err(ValidationError::SharedAccessCommitmentTooHigh {
          requested: *shared_access_commitment,
          available_limit: ruleset.max_shared_access_commitment,
        });
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
    PlayerCommand::RespondToWorkforcePressure { .. } => None,
    PlayerCommand::JoinRegionalAccessCoalition { .. } => None,
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
    prior_access_revision: inputs.access_measurement_revision,
    policy_briefing,
  }
}

fn actor_decision(
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

fn labor_decision(
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

fn coalition_decision(
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

fn print_demo(seed: u64, history: &History, ruleset: &Ruleset) {
  let replayed = replay(history, ruleset).expect("demo history should replay");

  println!("Health Policy Strategy Game deterministic demo");
  println!("Ruleset: {}", ruleset.version);
  println!("Run seed: {seed}");
  for transition in &history.transitions {
    println!(
      "Turn: {} -> {}",
      transition.prior.turn, transition.next.turn
    );
    println!(
      "Resolved inputs: measurement_noise {}, delayed_access_report {}, labor_sick_call_delta {}, policy_signal {}, coalition_leverage_signal {}, access_measurement_revision {}",
      transition.resolved_inputs.measurement_noise,
      transition.resolved_inputs.delayed_access_report,
      transition.resolved_inputs.labor_sick_call_delta,
      transition.resolved_inputs.policy_signal,
      transition.resolved_inputs.coalition_leverage_signal,
      transition.resolved_inputs.access_measurement_revision
    );
    println!(
      "CEO observation: access {}, quality {}, prior access revision {}, policy briefing: {}",
      transition.observation.reported_access_index,
      transition.observation.reported_quality_index,
      transition.observation.prior_access_revision,
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

  let revision_notes = history
    .transitions
    .iter()
    .filter(|transition| transition.observation.prior_access_revision != 0)
    .map(|transition| {
      format!(
        "turn {} revised the prior reported access estimate by {}",
        transition.prior.turn + 1,
        transition.observation.prior_access_revision
      )
    })
    .collect::<Vec<_>>()
    .join("; ");

  let mut lines = vec![
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
    "Debrief prompt: Was the CEO's access strategy reasonable given the reported access values, the later policy response, the workforce retention tradeoff, and the coalition investment choice?".to_string(),
    "Decision quality and outcome quality are separate: replay preserves what each actor observed and why each modeled response occurred.".to_string(),
  ];

  if !revision_notes.is_empty() {
    lines.push(format!(
      "Observation revision note: {revision_notes}. Prior committed observations remain unchanged in history; revisions affect only the current briefing."
    ));
  }

  lines
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
    ActorDecision::Labor(LaborDecision::Cooperative) => "cooperative".to_string(),
    ActorDecision::Labor(LaborDecision::LimitedSupport) => "limited support".to_string(),
    ActorDecision::Labor(LaborDecision::WorkAction) => "work action".to_string(),
    ActorDecision::Coalition(CoalitionDecision::FullPartnership) => "full partnership".to_string(),
    ActorDecision::Coalition(CoalitionDecision::LimitedParticipation) => {
      "limited participation".to_string()
    }
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal) => {
      "coalition withdrawal".to_string()
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

    assert_eq!(replay(&history, &ruleset).unwrap(), second.next);
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
      let history = build_history_for_strategy(choice, DEFAULT_SEED, &ruleset).unwrap();
      let final_state = history.transitions.last().unwrap().next.clone();

      assert_eq!(history.transitions.len(), 4);
      assert_eq!(replay(&history, &ruleset).unwrap(), final_state);
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
      history.transitions.last().unwrap().state_fingerprint,
      "demo-ruleset-0.1.9:4:46:128:83:80:68:71:100:35"
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
    assert_eq!(replay(&history, &ruleset).unwrap(), final_state);
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
}
