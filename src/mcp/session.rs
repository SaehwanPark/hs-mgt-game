use std::collections::HashMap;

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::cli::{
  parse_coalition_command, parse_competitive_batch, parse_competitor_command, parse_policy_command,
  parse_stabilize_access_command, parse_workforce_command,
};
use crate::competitive::{genesis_competitive_world_with_ruleset, resolve_competitive_month};
use crate::debrief::educational_debrief;
use crate::inputs::resolve_inputs;
use crate::model::{
  AggregatedMonthlyActions, CampaignId, CompetitiveHistory, CompetitiveRuleset,
  CompetitiveTransition, CompetitiveWorldState, Difficulty, History, INTERACTIVE_TURN_COUNT,
  Observation, PlayerObservation, Ruleset, SystemMonthlyBatch, Transition,
  default_competitive_ruleset, default_ruleset,
};
use crate::scenario::{default_stabilization_scenario, validate_stabilization_scenario};
use crate::sim::{observe_for_human, observe_for_player, transition, validate_competitive_batch};

const COMPETITIVE_MONTH_LIMIT: u32 = 3;

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct StartSessionRequest {
  pub campaign: String,
  pub seed: Option<u64>,
  pub difficulty: Option<String>,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct GetObservationRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct SubmitTurnRequest {
  pub session_id: String,
  pub command_text: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct GetHistoryRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct EndSessionRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct SessionEnvelope {
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub difficulty: Option<String>,
  pub turn: u32,
  pub max_turns: u32,
  pub done: bool,
  pub observation: Vec<String>,
  pub legal_commands: Vec<String>,
  pub latest_transition: Option<TransitionSummary>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct HistoryEnvelope {
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub transition_count: usize,
  pub transitions: Vec<TransitionSummary>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct EndSessionEnvelope {
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub done: bool,
  pub debrief: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct TransitionSummary {
  pub turn: u32,
  pub command: String,
  pub events: Vec<String>,
  pub effects: Vec<String>,
  pub state_hash: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct McpErrorMessage {
  pub error: String,
}

#[derive(Debug)]
pub struct GameSessionStore {
  next_id: u64,
  sessions: HashMap<String, GameSession>,
}

#[derive(Debug)]
enum GameSession {
  Stabilization(StabilizationSession),
  Competitive(CompetitiveSession),
}

#[derive(Debug)]
struct StabilizationSession {
  seed: u64,
  ruleset: Ruleset,
  history: History,
  current: crate::model::WorldState,
  done: bool,
}

#[derive(Debug)]
struct CompetitiveSession {
  seed: u64,
  ruleset: CompetitiveRuleset,
  history: CompetitiveHistory,
  current: CompetitiveWorldState,
  prior_aggregated: Option<AggregatedMonthlyActions>,
  done: bool,
}

impl Default for GameSessionStore {
  fn default() -> Self {
    Self {
      next_id: 1,
      sessions: HashMap::new(),
    }
  }
}

impl GameSessionStore {
  pub fn start_session(
    &mut self,
    request: StartSessionRequest,
  ) -> Result<SessionEnvelope, McpErrorMessage> {
    let seed = request.seed.unwrap_or(crate::model::DEFAULT_SEED);
    let campaign = parse_campaign(&request.campaign)?;
    let session_id = self.allocate_session_id();

    let session = match campaign {
      CampaignId::StabilizationV1 => GameSession::Stabilization(start_stabilization(seed)?),
      CampaignId::CompetitiveRegionalV1 => {
        let difficulty = parse_difficulty(request.difficulty.as_deref())?;
        GameSession::Competitive(start_competitive(seed, difficulty))
      }
    };

    self.sessions.insert(session_id.clone(), session);
    self.envelope(&session_id)
  }

  pub fn get_observation(
    &self,
    request: GetObservationRequest,
  ) -> Result<SessionEnvelope, McpErrorMessage> {
    self.envelope(&request.session_id)
  }

  pub fn submit_turn(
    &mut self,
    request: SubmitTurnRequest,
  ) -> Result<SessionEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get_mut(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };

    if session.is_done() {
      return Err(error_message("session is already complete"));
    }

    let latest = match session {
      GameSession::Stabilization(session) => {
        let transition = advance_stabilization(session, &request.command_text)?;
        Some(summarize_stabilization_transition(&transition))
      }
      GameSession::Competitive(session) => {
        let transition = advance_competitive(session, &request.command_text)?;
        Some(summarize_competitive_transition(&transition))
      }
    };

    let mut envelope = self.envelope(&request.session_id)?;
    envelope.latest_transition = latest;
    Ok(envelope)
  }

  pub fn get_history(
    &self,
    request: GetHistoryRequest,
  ) -> Result<HistoryEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    Ok(match session {
      GameSession::Stabilization(session) => HistoryEnvelope {
        session_id: request.session_id,
        campaign: CampaignId::StabilizationV1.as_str().to_string(),
        seed: session.seed,
        transition_count: session.history.transitions.len(),
        transitions: session
          .history
          .transitions
          .iter()
          .map(summarize_stabilization_transition)
          .collect(),
      },
      GameSession::Competitive(session) => HistoryEnvelope {
        session_id: request.session_id,
        campaign: CampaignId::CompetitiveRegionalV1.as_str().to_string(),
        seed: session.seed,
        transition_count: session.history.transitions.len(),
        transitions: session
          .history
          .transitions
          .iter()
          .map(summarize_competitive_transition)
          .collect(),
      },
    })
  }

  pub fn end_session(
    &mut self,
    request: EndSessionRequest,
  ) -> Result<EndSessionEnvelope, McpErrorMessage> {
    let Some(mut session) = self.sessions.remove(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    session.mark_done();
    Ok(match session {
      GameSession::Stabilization(session) => EndSessionEnvelope {
        session_id: request.session_id,
        campaign: CampaignId::StabilizationV1.as_str().to_string(),
        seed: session.seed,
        done: session.done,
        debrief: educational_debrief(&session.history),
      },
      GameSession::Competitive(session) => EndSessionEnvelope {
        session_id: request.session_id,
        campaign: CampaignId::CompetitiveRegionalV1.as_str().to_string(),
        seed: session.seed,
        done: session.done,
        debrief: competitive_debrief(&session),
      },
    })
  }

  fn allocate_session_id(&mut self) -> String {
    let id = format!("session-{}", self.next_id);
    self.next_id += 1;
    id
  }

  fn envelope(&self, session_id: &str) -> Result<SessionEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(session_id) else {
      return Err(error_message(format!("unknown session '{session_id}'")));
    };
    Ok(match session {
      GameSession::Stabilization(session) => {
        if session.done {
          return Ok(SessionEnvelope {
            session_id: session_id.to_string(),
            campaign: CampaignId::StabilizationV1.as_str().to_string(),
            seed: session.seed,
            difficulty: None,
            turn: session.current.turn,
            max_turns: INTERACTIVE_TURN_COUNT,
            done: true,
            observation: vec![
              "Session complete.".to_string(),
              format!("Committed turns: {}", session.history.transitions.len()),
            ],
            legal_commands: Vec::new(),
            latest_transition: None,
          });
        }
        let inputs = resolve_inputs(session.seed, &session.current, &session.ruleset);
        let observation = observe_for_player(&session.current, &inputs);
        SessionEnvelope {
          session_id: session_id.to_string(),
          campaign: CampaignId::StabilizationV1.as_str().to_string(),
          seed: session.seed,
          difficulty: None,
          turn: session.current.turn + 1,
          max_turns: INTERACTIVE_TURN_COUNT,
          done: session.done,
          observation: format_stabilization_observation(&session.current, &observation),
          legal_commands: stabilization_legal_commands(session.current.turn + 1),
          latest_transition: None,
        }
      }
      GameSession::Competitive(session) => {
        if session.done {
          return Ok(SessionEnvelope {
            session_id: session_id.to_string(),
            campaign: CampaignId::CompetitiveRegionalV1.as_str().to_string(),
            seed: session.seed,
            difficulty: Some(session.current.difficulty.label().to_string()),
            turn: session.current.turn,
            max_turns: COMPETITIVE_MONTH_LIMIT,
            done: true,
            observation: vec![
              "Session complete.".to_string(),
              format!("Committed months: {}", session.history.transitions.len()),
            ],
            legal_commands: Vec::new(),
            latest_transition: None,
          });
        }
        let observation = observe_for_human(&session.current, session.prior_aggregated.as_ref());
        let human = session
          .current
          .human_system()
          .expect("competitive session must include human system");
        SessionEnvelope {
          session_id: session_id.to_string(),
          campaign: CampaignId::CompetitiveRegionalV1.as_str().to_string(),
          seed: session.seed,
          difficulty: Some(session.current.difficulty.label().to_string()),
          turn: session.current.turn + 1,
          max_turns: COMPETITIVE_MONTH_LIMIT,
          done: session.done,
          observation: format_competitive_observation(&session.current, &observation),
          legal_commands: competitive_legal_commands(
            human.resources.ap_budget,
            human.resources.cash,
            human.resources.political_capital,
          ),
          latest_transition: None,
        }
      }
    })
  }
}

impl GameSession {
  fn is_done(&self) -> bool {
    match self {
      GameSession::Stabilization(session) => session.done,
      GameSession::Competitive(session) => session.done,
    }
  }

  fn mark_done(&mut self) {
    match self {
      GameSession::Stabilization(session) => session.done = true,
      GameSession::Competitive(session) => session.done = true,
    }
  }
}

fn start_stabilization(seed: u64) -> Result<StabilizationSession, McpErrorMessage> {
  let ruleset = default_ruleset();
  let scenario = default_stabilization_scenario()
    .map_err(|error| error_message(format!("default stabilization scenario: {error}")))?;
  validate_stabilization_scenario(&scenario, &ruleset)
    .map_err(|error| error_message(format!("default stabilization scenario: {error}")))?;
  let genesis = scenario.initial_world_state();

  Ok(StabilizationSession {
    seed,
    ruleset,
    history: History {
      genesis: genesis.clone(),
      transitions: Vec::new(),
    },
    current: genesis,
    done: false,
  })
}

fn start_competitive(seed: u64, difficulty: Difficulty) -> CompetitiveSession {
  let ruleset = default_competitive_ruleset();
  let genesis = genesis_competitive_world_with_ruleset(difficulty, &ruleset);

  CompetitiveSession {
    seed,
    ruleset,
    history: CompetitiveHistory {
      genesis: genesis.clone(),
      transitions: Vec::new(),
    },
    current: genesis,
    prior_aggregated: None,
    done: false,
  }
}

fn advance_stabilization(
  session: &mut StabilizationSession,
  command_text: &str,
) -> Result<Transition, McpErrorMessage> {
  let turn_number = session.current.turn + 1;
  let parser = stabilization_parser(turn_number)?;
  let command =
    parser(command_text).map_err(|error| error_message(crate::cli::describe_cli_error(&error)))?;
  let inputs = resolve_inputs(session.seed, &session.current, &session.ruleset);
  let transition_record = transition(&session.current, command, inputs, &session.ruleset)
    .map_err(|error| error_message(format!("{error:?}")))?;

  session.current = transition_record.next.clone();
  session.history.transitions.push(transition_record.clone());
  session.done = session.current.turn >= INTERACTIVE_TURN_COUNT;

  Ok(transition_record)
}

fn advance_competitive(
  session: &mut CompetitiveSession,
  command_text: &str,
) -> Result<CompetitiveTransition, McpErrorMessage> {
  let commands = parse_competitive_batch(command_text)
    .map_err(|error| error_message(crate::cli::describe_cli_error(&error)))?;
  let human_resources = session
    .current
    .human_system()
    .ok_or_else(|| error_message("competitive session has no human system"))?
    .resources
    .clone();
  validate_competitive_batch(&commands, &human_resources, &session.ruleset)
    .map_err(|error| error_message(error.message()))?;
  let human_batch = SystemMonthlyBatch::new(0, commands);
  let transition = resolve_competitive_month(
    &session.current,
    &session.ruleset,
    session.seed,
    human_batch,
  )
  .map_err(|error| error_message(error.message()))?;

  session.prior_aggregated = Some(transition.aggregated.clone());
  session.current = transition.next.clone();
  session.history.transitions.push(transition.clone());
  session.done = session.current.turn >= COMPETITIVE_MONTH_LIMIT;

  Ok(transition)
}

fn stabilization_parser(
  turn_number: u32,
) -> Result<fn(&str) -> Result<crate::model::PlayerCommand, crate::model::CliError>, McpErrorMessage>
{
  match turn_number {
    1 => Ok(parse_stabilize_access_command),
    2 => Ok(parse_policy_command),
    3 => Ok(parse_workforce_command),
    4 => Ok(parse_coalition_command),
    5 => Ok(parse_competitor_command),
    _ => Err(error_message(
      "stabilization session has no remaining turns",
    )),
  }
}

fn parse_campaign(input: &str) -> Result<CampaignId, McpErrorMessage> {
  match input {
    "stabilization-v1" => Ok(CampaignId::StabilizationV1),
    "competitive-regional-v1" => Ok(CampaignId::CompetitiveRegionalV1),
    other => Err(error_message(format!("unsupported campaign '{other}'"))),
  }
}

fn parse_difficulty(input: Option<&str>) -> Result<Difficulty, McpErrorMessage> {
  match input.unwrap_or("normal").to_ascii_lowercase().as_str() {
    "easy" => Ok(Difficulty::Easy),
    "normal" => Ok(Difficulty::Normal),
    "hard" => Ok(Difficulty::Hard),
    "expert" => Ok(Difficulty::Expert),
    other => Err(error_message(format!("unsupported difficulty '{other}'"))),
  }
}

fn format_stabilization_observation(
  state: &crate::model::WorldState,
  obs: &Observation,
) -> Vec<String> {
  let mut lines = vec![
    format!("Turn {}", state.turn + 1),
    format!("Cash: {}", state.cash),
    format!("Staffed beds: {}", state.staffed_beds),
    format!("Reported access index: {}", obs.reported_access_index),
    format!("Reported quality index: {}", obs.reported_quality_index),
    format!("Policy briefing: {}", obs.policy_briefing),
  ];
  if obs.prior_access_revision != 0 {
    lines.push(format!(
      "Prior access revision: {}",
      obs.prior_access_revision
    ));
  }
  if !obs.market_competition_briefing.is_empty() {
    lines.push(format!(
      "Market competition briefing: {}",
      obs.market_competition_briefing
    ));
  }
  lines
}

fn format_competitive_observation(
  state: &CompetitiveWorldState,
  obs: &PlayerObservation,
) -> Vec<String> {
  let mut lines = vec![
    format!(
      "Year {}, Month {} ({})",
      state.policy_calendar.year,
      state.policy_calendar.month_in_year,
      state.policy_calendar.month_name()
    ),
    format!("Organization: {}", obs.org_name),
    format!("Reported access index: {}", obs.reported_access_index),
    format!("Reported quality index: {}", obs.reported_quality_index),
    format!("Workforce trust: {}", obs.workforce_trust_summary),
    format!("Community trust: {}", obs.community_trust_summary),
    format!("Cash runway: {}", obs.cash_runway_signal.label()),
    format!("In-flight projects: {}", obs.in_flight_projects),
  ];
  lines.extend(
    obs
      .market_bullets
      .iter()
      .map(|bullet| format!("Market: {bullet}")),
  );
  lines.extend(
    obs
      .policy_bullets
      .iter()
      .map(|bullet| format!("Policy: {bullet}")),
  );
  lines.extend(
    obs
      .intel_gaps
      .iter()
      .map(|bullet| format!("Intel gap: {bullet}")),
  );
  lines
}

fn stabilization_legal_commands(turn_number: u32) -> Vec<String> {
  match turn_number {
    1 => vec!["staffed_beds capital_spend requested_rate".to_string()],
    2 => vec!["advocacy_spend access_commitment".to_string()],
    3 => vec!["retention_spend schedule_relief".to_string()],
    4 => vec!["coalition_investment shared_access_commitment".to_string()],
    5 => vec!["defensive_capital access_posture".to_string()],
    _ => Vec::new(),
  }
}

fn competitive_legal_commands(ap: u32, cash: i32, political_capital: u32) -> Vec<String> {
  let mut commands = crate::cli::competitive_command_help_lines();
  commands.insert(
    0,
    format!("Available resources: AP {ap}, cash {cash}, political capital {political_capital}"),
  );
  commands
}

fn summarize_stabilization_transition(transition: &Transition) -> TransitionSummary {
  TransitionSummary {
    turn: transition.next.turn,
    command: format!("{:?}", transition.command),
    events: transition.events.iter().map(format_event).collect(),
    effects: transition.effects.iter().map(format_effect).collect(),
    state_hash: transition.state_hash.clone(),
  }
}

fn summarize_competitive_transition(transition: &CompetitiveTransition) -> TransitionSummary {
  let command = transition
    .aggregated
    .batch_for_system(0)
    .map(|batch| format!("{:?}", batch.commands))
    .unwrap_or_else(|| "[]".to_string());
  TransitionSummary {
    turn: transition.next.turn,
    command,
    events: transition.events.iter().map(format_event).collect(),
    effects: transition.effects.iter().map(format_effect).collect(),
    state_hash: transition.state_hash.clone(),
  }
}

fn format_event(event: &crate::model::Event) -> String {
  format!("{}: {}", event.actor, event.description)
}

fn format_effect(effect: &crate::model::AttributedEffect) -> String {
  format!(
    "{} changed {} by {}",
    effect.source, effect.metric, effect.delta
  )
}

fn format_command_debrief(cmd: &crate::model::CompetitiveCommand) -> String {
  match cmd {
    crate::model::CompetitiveCommand::Hold => "hold".to_string(),
    crate::model::CompetitiveCommand::Recruit { role, headcount } => {
      let r = match role {
        crate::model::RecruitRole::Nurse => "nurse",
        crate::model::RecruitRole::Physician => "physician",
        crate::model::RecruitRole::Admin => "admin",
      };
      format!("recruit role={} headcount={}", r, headcount)
    }
    crate::model::CompetitiveCommand::Invest { domain, amount } => {
      let d = match domain {
        crate::model::InvestDomain::Beds => "beds",
        crate::model::InvestDomain::Outpatient => "outpatient",
        crate::model::InvestDomain::Technology => "technology",
      };
      format!("invest domain={} amount={}", d, amount)
    }
    crate::model::CompetitiveCommand::Monitor { target, depth } => {
      let t = match target {
        crate::model::MonitorTarget::Northlake => "northlake",
        crate::model::MonitorTarget::Summit => "summit",
        crate::model::MonitorTarget::Valley => "valley",
        crate::model::MonitorTarget::Metro => "metro",
      };
      format!("monitor target={} depth={}", t, depth)
    }
    crate::model::CompetitiveCommand::Negotiate {
      payer,
      rate_posture,
    } => {
      let p = match payer {
        crate::model::PayerId::CarrierA => "carrier_a",
        crate::model::PayerId::CarrierB => "carrier_b",
      };
      let rp = match rate_posture {
        crate::model::RatePosture::Aggressive => "aggressive",
        crate::model::RatePosture::Neutral => "neutral",
        crate::model::RatePosture::Conservative => "conservative",
      };
      format!("negotiate payer={} rate_posture={}", p, rp)
    }
    crate::model::CompetitiveCommand::Commit { pledge_type, level } => {
      let pt = match pledge_type {
        crate::model::PledgeType::Access => "access",
        crate::model::PledgeType::Quality => "quality",
      };
      format!("commit pledge_type={} level={}", pt, level)
    }
    crate::model::CompetitiveCommand::Project { kind, budget } => {
      let k = match kind {
        crate::model::ProjectKind::EhrEpic => "ehr_epic",
        crate::model::ProjectKind::EhrCerner => "ehr_cerner",
        crate::model::ProjectKind::Tower => "tower",
        crate::model::ProjectKind::ClinicNetwork => "clinic_network",
      };
      format!("project kind={} budget={}", k, budget)
    }
  }
}

fn competitive_debrief(session: &CompetitiveSession) -> Vec<String> {
  let final_state = session.history.final_state();
  let mut lines = vec![
    format!(
      "Competitive preview completed {} committed month(s).",
      session.history.transitions.len()
    ),
    format!(
      "Final state hash: {}",
      session
        .history
        .transitions
        .last()
        .map(|transition| transition.state_hash.as_str())
        .unwrap_or("none")
    ),
    format!(
      "Final calendar: Year {}, Month {}.",
      final_state.policy_calendar.year, final_state.policy_calendar.month_in_year
    ),
  ];
  lines.extend(competitive_final_tradeoff_lines(
    &session.history.genesis,
    final_state,
  ));

  if !session.history.transitions.is_empty() {
    // Trace transitions
    for (idx, transition) in session.history.transitions.iter().enumerate() {
      let month_name = format!("Month {}", idx + 1);
      lines.push(format!("--- {} ---", month_name));

      if let Some(human_batch) = transition.aggregated.batch_for_system(0) {
        let cmds: Vec<String> = human_batch
          .commands
          .iter()
          .map(format_command_debrief)
          .collect();
        lines.push(format!("Player: {}", cmds.join("; ")));
      }

      let current_month_index = transition.prior.policy_calendar.month_index;
      let mut monitored_system_ids = std::collections::HashSet::new();
      for t_prev in &session.history.transitions {
        let m_prev = t_prev.prior.policy_calendar.month_index;
        if m_prev <= current_month_index {
          if let Some(human_batch) = t_prev.aggregated.batch_for_system(0) {
            for cmd in &human_batch.commands {
              if let crate::model::CompetitiveCommand::Monitor { target, depth } = cmd {
                if m_prev + *depth > current_month_index {
                  let system_id = match target {
                    crate::model::MonitorTarget::Northlake => 1,
                    crate::model::MonitorTarget::Summit => 2,
                    crate::model::MonitorTarget::Valley => 3,
                    crate::model::MonitorTarget::Metro => 4,
                  };
                  monitored_system_ids.insert(system_id);
                }
              }
            }
          }
        }
      }

      for system in &transition.prior.systems {
        if system.system_id == 0 {
          continue;
        }
        if let Some(rival_batch) = transition.aggregated.batch_for_system(system.system_id) {
          let mut cmd_strs = Vec::new();
          for cmd in &rival_batch.commands {
            let formatted = format_command_debrief(cmd);
            if crate::sim::is_public_command(cmd) {
              cmd_strs.push(format!("{} (publicly disclosed)", formatted));
            } else {
              let observed = monitored_system_ids.contains(&system.system_id);
              if observed {
                cmd_strs.push(format!("{} (observed via monitor)", formatted));
              } else {
                cmd_strs.push(format!("{} (unobserved by you)", formatted));
              }
            }
          }
          lines.push(format!("Rival {}: {}", system.name, cmd_strs.join("; ")));
          if let Some(rationale) = &rival_batch.rationale {
            lines.push(format!("Rival {} rationale: {}", system.name, rationale));
          }
        }
      }
    }

    // Summary of mechanisms and events
    let mut events = Vec::new();
    let mut effects = Vec::new();
    for transition in &session.history.transitions {
      for event in &transition.events {
        events.push(format_event(event));
      }
      for effect in &transition.effects {
        effects.push(format_effect(effect));
      }
    }
    let effect_summary = if effects.is_empty() {
      "none".to_string()
    } else {
      effects.join("; ")
    };
    let event_summary = if events.is_empty() {
      "none".to_string()
    } else {
      events.join("; ")
    };
    lines.push(format!(
      "Attributed mechanisms to inspect: {}.",
      effect_summary
    ));
    lines.push(format!("Resolved events: {}.", event_summary));
  }

  lines.extend([
    "Recruitment lesson: nurse, physician, and admin hiring spends cash immediately, resolves after role-specific delays, and can lower workforce trust while added capacity is pending.".to_string(),
    "Capital project lesson: EHR Epic/Cerner, Tower, and Clinic Network projects consume Action Points and cash immediately, draw cash monthly over their duration (9 to 12 months), and are limited to a maximum of 2 concurrent projects. They are long-term strategic investments that do not resolve within a short three-month preview but are critical in longer horizons.".to_string(),
    "Decision quality and outcome quality remain separate: the MCP surface reports actor-visible observations plus committed transition summaries.".to_string(),
  ]);
  lines
}

fn competitive_final_tradeoff_lines(
  genesis: &CompetitiveWorldState,
  final_state: &CompetitiveWorldState,
) -> Vec<String> {
  let Some(initial_human) = genesis.human_system() else {
    return vec![
      "Final player tradeoff metrics unavailable: no human system at genesis.".to_string(),
    ];
  };
  let Some(final_human) = final_state.human_system() else {
    return vec![
      "Final player tradeoff metrics unavailable: no human system in final state.".to_string(),
    ];
  };

  vec![
    format!(
      "Final player tradeoff: {} cash moved from {} to {}, access from {} to {}, quality from {} to {}, workforce trust from {} to {}, community trust from {} to {}, and market share from {} to {}.",
      final_human.name,
      initial_human.resources.cash,
      final_human.resources.cash,
      initial_human.access_index,
      final_human.access_index,
      initial_human.quality_index,
      final_human.quality_index,
      initial_human.workforce_trust,
      final_human.workforce_trust,
      initial_human.community_trust,
      final_human.community_trust,
      initial_human.market_share_index,
      final_human.market_share_index
    ),
    format!(
      "Final player resources: political capital {}, active projects {}, active project monthly draws {}, staffed beds {}.",
      final_human.resources.political_capital,
      final_human.resources.active_projects,
      final_human.resources.active_project_monthly_draws,
      final_human.staffed_beds
    ),
  ]
}

fn error_message(message: impl Into<String>) -> McpErrorMessage {
  McpErrorMessage {
    error: message.into(),
  }
}

#[cfg(test)]
mod tests {
  use super::*;

  fn start(store: &mut GameSessionStore, campaign: &str) -> SessionEnvelope {
    store
      .start_session(StartSessionRequest {
        campaign: campaign.to_string(),
        seed: Some(42),
        difficulty: Some("normal".to_string()),
      })
      .expect("session")
  }

  #[test]
  fn starts_stabilization_session_with_observation() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "stabilization-v1");

    assert_eq!(session.campaign, "stabilization-v1");
    assert_eq!(session.turn, 1);
    assert!(session.observation.iter().any(|line| line.contains("Cash")));
    assert_eq!(session.legal_commands.len(), 1);
  }

  #[test]
  fn starts_competitive_session_with_observation() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");

    assert_eq!(session.campaign, "competitive-regional-v1");
    assert_eq!(session.turn, 1);
    assert_eq!(session.difficulty, Some("Normal".to_string()));
    assert!(
      session
        .legal_commands
        .iter()
        .any(|line| line.contains("invest"))
    );
  }

  #[test]
  fn stabilization_advances_five_turns_then_done() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "stabilization-v1");
    let commands = ["12 20 106", "8 6", "10 4", "7 8", "12 5"];
    let mut current = session;

    for command_text in commands {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: command_text.to_string(),
        })
        .expect("advance");
    }

    assert!(current.done);
    assert_eq!(current.turn, 5);
    assert!(current.legal_commands.is_empty());
    let history = store
      .get_history(GetHistoryRequest {
        session_id: current.session_id,
      })
      .expect("history");
    assert_eq!(history.transition_count, 5);
  }

  #[test]
  fn competitive_advances_three_months_then_done() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let mut current = session;

    for _ in 0..3 {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("advance");
    }

    assert!(current.done);
    assert_eq!(current.turn, 3);
    assert!(current.legal_commands.is_empty());
    let history = store
      .get_history(GetHistoryRequest {
        session_id: current.session_id,
      })
      .expect("history");
    assert_eq!(history.transition_count, 3);
  }

  #[test]
  fn competitive_debrief_explains_recruitment_timing() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let ended = store
      .end_session(EndSessionRequest {
        session_id: session.session_id,
      })
      .expect("end session");
    let text = ended.debrief.join("\n");

    assert!(text.contains("Recruitment lesson"));
    assert!(text.contains("role-specific delays"));
    assert!(text.contains("workforce trust"));
  }

  #[test]
  fn completed_competitive_debrief_includes_final_player_tradeoff_metrics() {
    let mut store = GameSessionStore::default();
    let mut current = start(&mut store, "competitive-regional-v1");

    for command_text in [
      "monitor target=northlake depth=1; recruit role=nurse headcount=4",
      "invest domain=beds amount=15; commit pledge_type=access level=2",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
    ] {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: command_text.to_string(),
        })
        .expect("advance");
    }

    let ended = store
      .end_session(EndSessionRequest {
        session_id: current.session_id,
      })
      .expect("end session");
    let text = ended.debrief.join("\n");

    assert!(text.contains("Final player tradeoff:"));
    assert!(text.contains("cash moved from"));
    assert!(text.contains("access from"));
    assert!(text.contains("quality from"));
    assert!(text.contains("workforce trust from"));
    assert!(text.contains("community trust from"));
    assert!(text.contains("market share from"));
    assert!(text.contains("Final player resources: political capital"));
  }

  #[test]
  fn competitive_debrief_final_tradeoff_lines_do_not_name_rival_systems() {
    let mut store = GameSessionStore::default();
    let mut current = start(&mut store, "competitive-regional-v1");

    for _ in 0..3 {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("advance");
    }

    let ended = store
      .end_session(EndSessionRequest {
        session_id: current.session_id,
      })
      .expect("end session");

    // Tradeoff lines themselves should not contain rival names (they only name the player system)
    let tradeoff_text = ended.debrief[3..5].join("\n");
    assert!(!tradeoff_text.contains("Northlake"));
    assert!(!tradeoff_text.contains("Summit"));
    assert!(!tradeoff_text.contains("Valley"));
    assert!(!tradeoff_text.contains("Metro"));
  }

  #[test]
  fn competitive_debrief_contains_detailed_history_and_monitored_labels() {
    let mut store = GameSessionStore::default();
    let mut current = start(&mut store, "competitive-regional-v1");

    // In month 1, we monitor Northlake
    current = store
      .submit_turn(SubmitTurnRequest {
        session_id: current.session_id.clone(),
        command_text: "monitor target=northlake depth=1; recruit role=nurse headcount=2"
          .to_string(),
      })
      .expect("advance 1");

    // In month 2, we hold
    current = store
      .submit_turn(SubmitTurnRequest {
        session_id: current.session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("advance 2");

    let ended = store
      .end_session(EndSessionRequest {
        session_id: current.session_id,
      })
      .expect("end session");
    let text = ended.debrief.join("\n");

    // Verify player actions are tracked
    assert!(
      text.contains("Player: monitor target=northlake depth=1; recruit role=nurse headcount=2")
    );

    // Verify rival names and unobserved / observed labels exist
    assert!(text.contains("Rival Northlake Health:"));
    assert!(text.contains("Rival Summit Care:"));

    // Verify observed / unobserved / public labels
    assert!(
      text.contains("observed via monitor")
        || text.contains("unobserved by you")
        || text.contains("publicly disclosed")
    );

    // Attributed mechanisms should be outputted
    assert!(text.contains("Attributed mechanisms to inspect:"));
    assert!(text.contains("Resolved events:"));
  }

  #[test]
  fn invalid_stabilization_command_does_not_advance() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "stabilization-v1");

    assert!(
      store
        .submit_turn(SubmitTurnRequest {
          session_id: session.session_id.clone(),
          command_text: "-1 20 106".to_string(),
        })
        .is_err()
    );

    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");
    assert_eq!(current.turn, 1);
  }

  #[test]
  fn invalid_competitive_command_does_not_advance() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");

    assert!(
      store
        .submit_turn(SubmitTurnRequest {
          session_id: session.session_id.clone(),
          command_text: "invest domain=beds amount=-1".to_string(),
        })
        .is_err()
    );

    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");
    assert_eq!(current.turn, 1);
  }

  #[test]
  fn identical_seed_and_commands_produce_same_hashes() {
    let mut first = GameSessionStore::default();
    let mut second = GameSessionStore::default();
    let first_session = start(&mut first, "competitive-regional-v1");
    let second_session = start(&mut second, "competitive-regional-v1");

    let first_after = first
      .submit_turn(SubmitTurnRequest {
        session_id: first_session.session_id,
        command_text: "hold".to_string(),
      })
      .expect("first");
    let second_after = second
      .submit_turn(SubmitTurnRequest {
        session_id: second_session.session_id,
        command_text: "hold".to_string(),
      })
      .expect("second");

    assert_eq!(
      first_after
        .latest_transition
        .expect("first transition")
        .state_hash,
      second_after
        .latest_transition
        .expect("second transition")
        .state_hash
    );
  }
}
