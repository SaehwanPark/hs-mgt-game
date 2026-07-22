use std::collections::HashMap;

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::cli::{
  parse_affiliation_command, parse_coalition_command, parse_competitive_batch,
  parse_competitor_command, parse_policy_command, parse_stabilize_access_command,
  parse_workforce_command,
};
use crate::competitive::{genesis_competitive_world_with_ruleset, resolve_competitive_month};
use crate::debrief::{affiliation_debrief, competitive_debrief, educational_debrief};
use crate::inputs::resolve_inputs;
use crate::model::{
  AffiliationHistory, AffiliationRuleset, AffiliationTransition, AffiliationWorldState,
  AggregatedMonthlyActions, CampaignId, CompetitiveHistory, CompetitiveRuleset,
  CompetitiveTransition, CompetitiveWorldState, Difficulty, History, INTERACTIVE_TURN_COUNT,
  Observation, PlayerObservation, Ruleset, SystemMonthlyBatch, Transition,
  default_affiliation_ruleset, default_competitive_ruleset, default_ruleset,
};
use crate::scenario::{
  Scenario, default_stabilization_scenario, validate_competitive_scenario,
  validate_stabilization_scenario,
};
use crate::sim::{observe_for_human, observe_for_player, transition, validate_competitive_batch};

pub(crate) const COMPETITIVE_MONTH_LIMIT: u32 = 24;

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct StartSessionRequest {
  pub campaign: String,
  pub seed: Option<u64>,
  pub difficulty: Option<String>,
  pub scenario_path: Option<String>,
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
pub struct GetPresentationRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct GetResolutionRequest {
  pub session_id: String,
  pub turn: Option<u32>,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct GetRegionalWorldRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct GetCampaignCoverageRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct GetActionCatalogRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct ValidateTurnRequest {
  pub session_id: String,
  pub command_text: String,
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
  pub consultant_options: Vec<crate::model::ConsultantOption>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct McpErrorMessage {
  pub error: String,
  #[serde(skip_serializing_if = "Option::is_none")]
  pub code: Option<String>,
  #[serde(skip_serializing_if = "Option::is_none")]
  pub resource_limit: Option<ResourceLimitError>,
  #[serde(skip_serializing_if = "Option::is_none")]
  pub hint: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct ResourceLimitError {
  pub resource: String,
  pub required: i64,
  pub available: i64,
}

#[derive(Debug)]
pub struct GameSessionStore {
  next_id: u64,
  sessions: HashMap<String, GameSession>,
}

#[derive(Debug)]
#[allow(clippy::large_enum_variant)]
enum GameSession {
  Stabilization(StabilizationSession),
  Competitive(CompetitiveSession),
  Affiliation(AffiliationSession),
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

#[derive(Debug)]
struct AffiliationSession {
  seed: u64,
  ruleset: AffiliationRuleset,
  history: AffiliationHistory,
  current: AffiliationWorldState,
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

    let custom_scenario = if let Some(ref path_str) = request.scenario_path {
      let path = std::path::Path::new(path_str);
      let scenario = crate::scenario::load_scenario_file(path)
        .map_err(|error| error_message(format!("could not load scenario file: {error}")))?;
      if scenario.campaign_id != request.campaign {
        return Err(error_message(format!(
          "scenario campaign '{}' does not match request campaign '{}'",
          scenario.campaign_id, request.campaign
        )));
      }
      Some(scenario)
    } else {
      None
    };

    let session = match campaign {
      CampaignId::StabilizationV1 => {
        GameSession::Stabilization(start_stabilization(seed, custom_scenario)?)
      }
      CampaignId::CompetitiveRegionalV1 => {
        let difficulty = match request.difficulty.as_deref() {
          Some(diff_str) => {
            let difficulty = parse_difficulty(Some(diff_str))?;
            if let Some(systems) = custom_scenario
              .as_ref()
              .and_then(|s| s.systems.as_ref())
              .filter(|systems| systems.len() as u32 != difficulty.k_rivals() + 1)
            {
              return Err(error_message(format!(
                "difficulty '{}' expects {} systems (1 human + {} rivals), but scenario has {}",
                difficulty.label(),
                difficulty.k_rivals() + 1,
                difficulty.k_rivals(),
                systems.len()
              )));
            }
            difficulty
          }
          None => {
            if let Some(ref scenario) = custom_scenario {
              let systems_len = scenario.systems.as_ref().map(|s| s.len()).unwrap_or(0);
              match systems_len {
                2 => Difficulty::Easy,
                3 => Difficulty::Normal,
                4 => Difficulty::Hard,
                5 => Difficulty::Expert,
                other => {
                  return Err(error_message(format!(
                    "custom competitive scenario must have between 2 and 5 systems, got {}",
                    other
                  )));
                }
              }
            } else {
              Difficulty::Normal
            }
          }
        };
        GameSession::Competitive(start_competitive(seed, difficulty, custom_scenario)?)
      }
      CampaignId::RegionalAffiliationV1 => {
        GameSession::Affiliation(start_affiliation(seed, custom_scenario)?)
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
      GameSession::Affiliation(session) => {
        let transition = advance_affiliation(session, &request.command_text)?;
        Some(summarize_affiliation_transition(&transition))
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
      GameSession::Affiliation(session) => HistoryEnvelope {
        session_id: request.session_id,
        campaign: CampaignId::RegionalAffiliationV1.as_str().to_string(),
        seed: session.seed,
        transition_count: session.history.transitions.len(),
        transitions: session
          .history
          .transitions
          .iter()
          .map(summarize_affiliation_transition)
          .collect(),
      },
    })
  }

  pub fn get_presentation(
    &self,
    request: GetPresentationRequest,
  ) -> Result<crate::mcp::presentation::ReadOnlyPresentationEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    let GameSession::Competitive(session) = session else {
      return Err(error_message(
        "typed read-only presentation currently supports competitive-regional-v1 only",
      ));
    };
    let observation = observe_for_human(&session.current, session.prior_aggregated.as_ref());
    let player = session
      .current
      .human_system()
      .expect("competitive session must include human system");
    let history = session
      .history
      .transitions
      .iter()
      .map(summarize_competitive_transition)
      .collect::<Vec<_>>();
    Ok(crate::mcp::presentation::from_competitive_observation(
      crate::mcp::presentation::ReadOnlySession {
        session_id: request.session_id,
        campaign: CampaignId::CompetitiveRegionalV1.as_str().to_string(),
        seed: session.seed,
        difficulty: Some(session.current.difficulty.label().to_string()),
        year: session.current.policy_calendar.year,
        month: session.current.policy_calendar.month_in_year,
        month_name: session.current.policy_calendar.month_name().to_string(),
        turn: if session.done {
          session.current.turn
        } else {
          session.current.turn + 1
        },
        max_turns: COMPETITIVE_MONTH_LIMIT,
        done: session.done,
      },
      player,
      &observation,
      &history,
    ))
  }

  pub fn get_action_catalog(
    &self,
    request: GetActionCatalogRequest,
  ) -> Result<crate::mcp::action::ActionCatalogEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    let GameSession::Competitive(session) = session else {
      return Err(error_message(
        "typed action catalog currently supports competitive-regional-v1 only",
      ));
    };
    if session.done {
      return Err(error_message("session is already complete"));
    }
    let player = session
      .current
      .human_system()
      .expect("competitive session must include human system");
    Ok(crate::mcp::action::competitive_action_catalog(
      request.session_id,
      session.current.turn + 1,
      crate::mcp::presentation::ReadOnlyResources {
        cash: player.resources.cash,
        action_points: player.resources.ap_budget,
        political_capital: player.resources.political_capital,
      },
    ))
  }

  pub fn get_resolution(
    &self,
    request: GetResolutionRequest,
  ) -> Result<crate::mcp::resolution::ResolutionEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    let GameSession::Competitive(session) = session else {
      return Err(error_message(
        "typed resolution currently supports competitive-regional-v1 only",
      ));
    };
    let Some(latest_index) = session.history.transitions.len().checked_sub(1) else {
      return Err(error_message(
        "no committed competitive transition is available",
      ));
    };
    let index = match request.turn {
      Some(turn) => session
        .history
        .transitions
        .iter()
        .position(|transition| transition.next.turn == turn)
        .ok_or_else(|| error_message(format!("no committed transition for turn {turn}")))?,
      None => latest_index,
    };
    let transition = &session.history.transitions[index];
    let prior_aggregated = index
      .checked_sub(1)
      .and_then(|prior_index| session.history.transitions.get(prior_index))
      .map(|prior| &prior.aggregated);
    Ok(crate::mcp::resolution::from_competitive_transition(
      request.session_id,
      session.seed,
      session.current.difficulty,
      transition,
      prior_aggregated,
      session.history.transitions.len(),
      summarize_competitive_transition(transition),
    ))
  }

  pub fn get_regional_world(
    &self,
    request: GetRegionalWorldRequest,
  ) -> Result<crate::mcp::regional_world::RegionalWorldEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    let GameSession::Competitive(session) = session else {
      return Err(error_message(
        "regional world currently supports competitive-regional-v1 only",
      ));
    };
    let state_hash = session
      .history
      .transitions
      .last()
      .map(|transition| transition.state_hash.clone());
    Ok(crate::mcp::regional_world::from_competitive_world(
      request.session_id,
      session.seed,
      session.done,
      &session.current,
      session.prior_aggregated.as_ref(),
      session.history.transitions.len(),
      state_hash,
    ))
  }

  pub fn get_campaign_coverage(
    &self,
    request: GetCampaignCoverageRequest,
  ) -> Result<crate::mcp::campaign_coverage::CampaignCoverageEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    match session {
      GameSession::Stabilization(session) => {
        let history = session
          .history
          .transitions
          .iter()
          .map(summarize_stabilization_transition)
          .collect::<Vec<_>>();
        Ok(crate::mcp::campaign_coverage::from_stabilization(
          request.session_id,
          session.seed,
          session.done,
          &session.current,
          &session.ruleset,
          &history,
          &session.history,
        ))
      }
      GameSession::Affiliation(session) => {
        let history = session
          .history
          .transitions
          .iter()
          .map(summarize_affiliation_transition)
          .collect::<Vec<_>>();
        Ok(crate::mcp::campaign_coverage::from_affiliation(
          request.session_id,
          session.seed,
          session.done,
          &session.current,
          &session.ruleset,
          &history,
          &session.history,
        ))
      }
      GameSession::Competitive(_) => Err(error_message(
        "campaign coverage currently supports stabilization-v1 and regional-affiliation-v1 only",
      )),
    }
  }

  pub fn validate_turn(
    &self,
    request: ValidateTurnRequest,
  ) -> Result<crate::mcp::action::ValidateTurnEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    let GameSession::Competitive(session) = session else {
      return Err(error_message(
        "typed action validation currently supports competitive-regional-v1 only",
      ));
    };
    if session.done {
      return Ok(crate::mcp::action::validation_envelope(
        request.session_id,
        &request.command_text,
        &[],
        false,
        vec!["session is already complete".to_string()],
      ));
    }
    let commands = match parse_competitive_batch(&request.command_text) {
      Ok(commands) => commands,
      Err(error) => {
        return Ok(crate::mcp::action::validation_envelope(
          request.session_id,
          &request.command_text,
          &[],
          false,
          vec![crate::cli::describe_cli_error(&error)],
        ));
      }
    };
    let player = session
      .current
      .human_system()
      .expect("competitive session must include human system");
    let result = validate_competitive_batch(&commands, &player.resources, &session.ruleset);
    let (valid, errors) = match result {
      Ok(()) => (true, Vec::new()),
      Err(error) => {
        let message = competitive_validation_error_message(error);
        (false, vec![message.error])
      }
    };
    Ok(crate::mcp::action::validation_envelope(
      request.session_id,
      &request.command_text,
      &commands,
      valid,
      errors,
    ))
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
        debrief: competitive_debrief(&session.history),
      },
      GameSession::Affiliation(session) => EndSessionEnvelope {
        session_id: request.session_id,
        campaign: CampaignId::RegionalAffiliationV1.as_str().to_string(),
        seed: session.seed,
        done: session.done,
        debrief: affiliation_debrief(&session.history),
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
      GameSession::Affiliation(session) => {
        if session.done {
          return Ok(SessionEnvelope {
            session_id: session_id.to_string(),
            campaign: CampaignId::RegionalAffiliationV1.as_str().to_string(),
            seed: session.seed,
            difficulty: None,
            turn: session.current.turn,
            max_turns: crate::model::AFFILIATION_TURN_COUNT,
            done: true,
            observation: vec![
              "Session complete.".to_string(),
              format!("Committed stages: {}", session.history.transitions.len()),
            ],
            legal_commands: Vec::new(),
            latest_transition: None,
          });
        }
        let observation = crate::affiliation::observe_affiliation(&session.current);
        SessionEnvelope {
          session_id: session_id.to_string(),
          campaign: CampaignId::RegionalAffiliationV1.as_str().to_string(),
          seed: session.seed,
          difficulty: None,
          turn: session.current.turn + 1,
          max_turns: crate::model::AFFILIATION_TURN_COUNT,
          done: session.done,
          observation: format_affiliation_observation(&observation),
          legal_commands: affiliation_legal_commands(&session.current),
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
      GameSession::Affiliation(session) => session.done,
    }
  }

  fn mark_done(&mut self) {
    match self {
      GameSession::Stabilization(session) => session.done = true,
      GameSession::Competitive(session) => session.done = true,
      GameSession::Affiliation(session) => session.done = true,
    }
  }
}

fn start_stabilization(
  seed: u64,
  custom_scenario: Option<Scenario>,
) -> Result<StabilizationSession, McpErrorMessage> {
  let ruleset = default_ruleset();
  let scenario = match custom_scenario {
    Some(s) => s,
    None => default_stabilization_scenario()
      .map_err(|error| error_message(format!("default stabilization scenario: {error}")))?,
  };
  validate_stabilization_scenario(&scenario, &ruleset)
    .map_err(|error| error_message(format!("invalid stabilization scenario: {error}")))?;
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

fn start_competitive(
  seed: u64,
  difficulty: Difficulty,
  custom_scenario: Option<Scenario>,
) -> Result<CompetitiveSession, McpErrorMessage> {
  let ruleset = default_competitive_ruleset();
  let genesis = match custom_scenario {
    Some(scenario) => {
      validate_competitive_scenario(&scenario, &ruleset)
        .map_err(|error| error_message(format!("invalid competitive scenario: {error}")))?;
      scenario
        .initial_competitive_world_state(difficulty, &ruleset)
        .map_err(|error| {
          error_message(format!(
            "failed to initialize competitive world state: {error}"
          ))
        })?
    }
    None => genesis_competitive_world_with_ruleset(difficulty, &ruleset),
  };

  Ok(CompetitiveSession {
    seed,
    ruleset,
    history: CompetitiveHistory {
      genesis: genesis.clone(),
      transitions: Vec::new(),
    },
    current: genesis,
    prior_aggregated: None,
    done: false,
  })
}

fn start_affiliation(
  seed: u64,
  custom_scenario: Option<Scenario>,
) -> Result<AffiliationSession, McpErrorMessage> {
  let ruleset = default_affiliation_ruleset();
  let scenario = match custom_scenario {
    Some(scenario) => scenario,
    None => crate::scenario::default_regional_affiliation_scenario()
      .map_err(|error| error_message(format!("default affiliation scenario: {error}")))?,
  };
  crate::scenario::validate_regional_affiliation_scenario(&scenario, &ruleset)
    .map_err(|error| error_message(format!("invalid affiliation scenario: {error}")))?;
  let genesis = scenario
    .initial_affiliation_world_state()
    .map_err(|error| error_message(format!("failed to initialize affiliation state: {error}")))?;
  Ok(AffiliationSession {
    seed,
    ruleset,
    history: AffiliationHistory {
      genesis: genesis.clone(),
      transitions: Vec::new(),
    },
    current: genesis,
    done: false,
  })
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
    .map_err(competitive_validation_error_message)?;
  let human_batch = SystemMonthlyBatch::new(0, commands);
  let transition = resolve_competitive_month(
    &session.current,
    &session.ruleset,
    session.seed,
    human_batch,
    session.prior_aggregated.as_ref(),
  )
  .map_err(|error| error_message(error.message()))?;

  session.prior_aggregated = Some(transition.aggregated.clone());
  session.current = transition.next.clone();
  session.history.transitions.push(transition.clone());
  session.done = session.current.turn >= COMPETITIVE_MONTH_LIMIT;

  Ok(transition)
}

fn advance_affiliation(
  session: &mut AffiliationSession,
  command_text: &str,
) -> Result<AffiliationTransition, McpErrorMessage> {
  let command = parse_affiliation_command(command_text).map_err(error_message)?;
  let transition = crate::affiliation::resolve_affiliation_turn(
    &session.current,
    command,
    session.seed,
    &session.ruleset,
  )
  .map_err(|error| error_message(error.message()))?;
  session.current = transition.next.clone();
  session.history.transitions.push(transition.clone());
  session.done = session.current.turn >= crate::model::AFFILIATION_TURN_COUNT;
  Ok(transition)
}

type CommandParser = fn(&str) -> Result<crate::model::PlayerCommand, crate::model::CliError>;

fn stabilization_parser(turn_number: u32) -> Result<CommandParser, McpErrorMessage> {
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
    "regional-affiliation-v1" => Ok(CampaignId::RegionalAffiliationV1),
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
    format!(
      "Staffing: nurses {}, physicians {}, admins {}",
      obs.nurses, obs.physicians, obs.admins
    ),
    format!(
      "Physical capacity: staffed beds {}, outpatient {}, emergency {}, ICU {}, obstetrics {}, psychiatric {}, cardiology {}, oncology {}, infusion {}, neurology {}, ASC {}",
      obs.staffed_beds,
      obs.outpatient_capacity,
      obs.emergency_capacity,
      obs.icu_capacity,
      obs.obstetrics_capacity,
      obs.psychiatric_capacity,
      obs.cardiology_capacity,
      obs.oncology_capacity,
      obs.infusion_capacity,
      obs.neurology_capacity,
      obs.asc_capacity
    ),
    format!("Community trust: {}", obs.community_trust_summary),
    format!("Cash runway: {}", obs.cash_runway_signal.label()),
    format!(
      "Prior-month operations: treated {}/{} demand units ({} unmet); revenue {}, cost {}, margin {:+}",
      obs.monthly_treated_volume,
      obs.monthly_demand,
      obs.monthly_unmet_demand,
      obs.monthly_operating_revenue,
      obs.monthly_operating_cost,
      obs.monthly_operating_margin
    ),
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
  lines.push("STRATEGY CONSULTANT NOTES — Advisory, not binding".to_string());
  for option in &obs.consultant_options {
    lines.push(format!("Option {} — {}", option.label, option.title));
    lines.extend(
      option
        .tradeoff_bullets
        .iter()
        .map(|bullet| format!("  Tradeoff: {bullet}")),
    );
  }
  lines.extend(
    obs
      .intel_gaps
      .iter()
      .map(|bullet| format!("Intel gap: {bullet}")),
  );
  lines
}

pub(crate) fn stabilization_legal_commands(turn_number: u32) -> Vec<String> {
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

pub(crate) fn summarize_stabilization_transition(transition: &Transition) -> TransitionSummary {
  TransitionSummary {
    turn: transition.next.turn,
    command: format!("{:?}", transition.command),
    events: transition.events.iter().map(format_event).collect(),
    effects: transition.effects.iter().map(format_effect).collect(),
    state_hash: transition.state_hash.clone(),
    consultant_options: Vec::new(),
  }
}

pub(crate) fn summarize_competitive_transition(
  transition: &CompetitiveTransition,
) -> TransitionSummary {
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
    consultant_options: transition.consultant_options.clone(),
  }
}

pub(crate) fn summarize_affiliation_transition(
  transition: &AffiliationTransition,
) -> TransitionSummary {
  TransitionSummary {
    turn: transition.next.turn,
    command: format!("{:?}", transition.command),
    events: transition.events.iter().map(format_event).collect(),
    effects: transition.effects.iter().map(format_effect).collect(),
    state_hash: transition.state_hash.clone(),
    consultant_options: Vec::new(),
  }
}

fn format_affiliation_observation(
  observation: &crate::model::AffiliationObservation,
) -> Vec<String> {
  let mut lines = vec![
    format!("Stage {}: {:?}", observation.turn, observation.stage),
    format!("Riverside cash: {}", observation.cash),
    format!(
      "Access {}, quality {}, workforce trust {}, community trust {}",
      observation.access_index,
      observation.quality_index,
      observation.workforce_trust,
      observation.community_trust
    ),
    format!("Partner: {}", observation.partner_name),
    format!("Status: {:?}", observation.status),
    observation
      .reported_condition
      .map(|condition| format!("Reported partner condition: {condition:?}"))
      .unwrap_or_else(|| "Reported partner condition: not yet assessed".to_string()),
    format!(
      "Commitments: community {}, workforce {}, continuity {}, total {}",
      observation.commitments.community,
      observation.commitments.workforce,
      observation.commitments.continuity,
      observation.commitments.total()
    ),
  ];
  lines.extend(
    observation
      .alternatives
      .iter()
      .map(|alternative| format!("Alternative: {alternative}")),
  );
  lines.extend(
    observation
      .assumptions
      .iter()
      .map(|assumption| format!("Assumption: {assumption}")),
  );
  lines
}

pub(crate) fn affiliation_legal_commands(state: &AffiliationWorldState) -> Vec<String> {
  match state.stage {
    crate::model::AffiliationStage::AssessPartner => vec!["assess".to_string()],
    crate::model::AffiliationStage::ChoosePosture => {
      vec!["posture choice=independent|defer|pursue".to_string()]
    }
    crate::model::AffiliationStage::NegotiateCommitments => {
      if state.status == crate::model::AffiliationStatus::Pursuing {
        vec!["commit community=1..8 workforce=1..8 continuity=1..8".to_string()]
      } else {
        vec!["hold".to_string()]
      }
    }
    crate::model::AffiliationStage::SubmitReview => {
      if matches!(
        state.status,
        crate::model::AffiliationStatus::PartnerAccepted
          | crate::model::AffiliationStatus::PartnerConditioned
      ) {
        vec!["submit_review".to_string()]
      } else {
        vec!["hold".to_string()]
      }
    }
    crate::model::AffiliationStage::ResolveReview => {
      if state.status == crate::model::AffiliationStatus::ReviewPending {
        vec!["await_review".to_string()]
      } else {
        vec!["hold".to_string()]
      }
    }
    crate::model::AffiliationStage::IntegrateOrDecline => {
      if matches!(
        state.status,
        crate::model::AffiliationStatus::Approved
          | crate::model::AffiliationStatus::ConditionallyApproved
      ) {
        vec!["integrate decision=begin|decline".to_string()]
      } else {
        vec!["hold".to_string()]
      }
    }
    crate::model::AffiliationStage::Complete => Vec::new(),
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

fn error_message(message: impl Into<String>) -> McpErrorMessage {
  McpErrorMessage {
    error: message.into(),
    code: None,
    resource_limit: None,
    hint: None,
  }
}

fn competitive_validation_error_message(
  error: crate::model::CompetitiveValidationError,
) -> McpErrorMessage {
  let message = error.message();
  let code = competitive_validation_error_code(&error);
  let (resource_limit, hint) = match error {
    crate::model::CompetitiveValidationError::InsufficientCash {
      required,
      available,
    } => (
      Some(ResourceLimitError {
        resource: "cash".to_string(),
        required: required.into(),
        available: available.into(),
      }),
      Some(
        "Reduce cash spending, choose hold or monitor, or wait for resources before resubmitting."
          .to_string(),
      ),
    ),
    crate::model::CompetitiveValidationError::ApBudgetExceeded { requested, budget } => (
      Some(ResourceLimitError {
        resource: "action_points".to_string(),
        required: requested.into(),
        available: budget.into(),
      }),
      Some("Reduce the number or AP cost of commands in this monthly batch.".to_string()),
    ),
    crate::model::CompetitiveValidationError::InsufficientPoliticalCapital {
      required,
      available,
    } => (
      Some(ResourceLimitError {
        resource: "political_capital".to_string(),
        required: required.into(),
        available: available.into(),
      }),
      Some("Choose fewer political actions or wait for political capital to refresh.".to_string()),
    ),
    _ => (None, None),
  };
  McpErrorMessage {
    error: message,
    code: Some(code.to_string()),
    resource_limit,
    hint,
  }
}

fn competitive_validation_error_code(
  error: &crate::model::CompetitiveValidationError,
) -> &'static str {
  match error {
    crate::model::CompetitiveValidationError::ApBudgetExceeded { .. } => "ap_budget_exceeded",
    crate::model::CompetitiveValidationError::InsufficientCash { .. } => "insufficient_cash",
    crate::model::CompetitiveValidationError::InsufficientPoliticalCapital { .. } => {
      "insufficient_political_capital"
    }
    crate::model::CompetitiveValidationError::TooManyConcurrentProjects { .. } => {
      "too_many_concurrent_projects"
    }
    crate::model::CompetitiveValidationError::InvalidRecruitHeadcount { .. } => {
      "invalid_recruit_headcount"
    }
    crate::model::CompetitiveValidationError::InvestAmountNonPositive => {
      "invest_amount_non_positive"
    }
    crate::model::CompetitiveValidationError::InvestAmountTooHigh { .. } => {
      "invest_amount_too_high"
    }
    crate::model::CompetitiveValidationError::MonitorDepthOutOfRange { .. } => {
      "monitor_depth_out_of_range"
    }
    crate::model::CompetitiveValidationError::CommitLevelOutOfRange { .. } => {
      "commit_level_out_of_range"
    }
    crate::model::CompetitiveValidationError::ProjectBudgetNonPositive => {
      "project_budget_non_positive"
    }
    crate::model::CompetitiveValidationError::ProjectBudgetBelowDuration { .. } => {
      "project_budget_below_duration"
    }
    crate::model::CompetitiveValidationError::ProjectBudgetNotDivisible { .. } => {
      "project_budget_not_divisible"
    }
    crate::model::CompetitiveValidationError::ProjectMonthlyDrawInfeasible { .. } => {
      "project_monthly_draw_infeasible"
    }
    crate::model::CompetitiveValidationError::UnknownSystemId { .. } => "unknown_system_id",
    crate::model::CompetitiveValidationError::BatchCountMismatch { .. } => "batch_count_mismatch",
    crate::model::CompetitiveValidationError::MonthIndexMismatch { .. } => "month_index_mismatch",
    crate::model::CompetitiveValidationError::InvalidMedicaidPosture => "invalid_medicaid_posture",
    crate::model::CompetitiveValidationError::InvalidMedicarePosture => "invalid_medicare_posture",
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
        scenario_path: None,
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
        .observation
        .iter()
        .any(|line| line.contains("STRATEGY CONSULTANT NOTES"))
    );
    assert!(
      session
        .legal_commands
        .iter()
        .any(|line| line.contains("invest"))
    );
  }

  #[test]
  fn competitive_observation_includes_staffing_and_physical_capacity_context() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");

    assert!(
      session
        .observation
        .iter()
        .any(|line| { line == "Staffing: nurses 24, physicians 10, admins 11" })
    );
    assert!(session.observation.iter().any(|line| {
      line == "Physical capacity: staffed beds 118, outpatient 100, emergency 0, ICU 0, obstetrics 0, psychiatric 0, cardiology 0, oncology 0, infusion 0, neurology 0, ASC 0"
    }));
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
  fn competitive_advances_twenty_four_months_then_done() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let mut current = session;

    for _ in 0..24 {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("advance");
    }

    assert!(current.done);
    assert_eq!(current.turn, 24);
    assert!(current.legal_commands.is_empty());
    let history = store
      .get_history(GetHistoryRequest {
        session_id: current.session_id,
      })
      .expect("history");
    assert_eq!(history.transition_count, 24);
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
  fn competitive_history_and_debrief_retain_consultant_options() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let ended = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("advance");
    let history = store
      .get_history(GetHistoryRequest {
        session_id: session.session_id.clone(),
      })
      .expect("history");

    assert_eq!(history.transition_count, 1);
    assert_eq!(history.transitions[0].consultant_options.len(), 4);
    assert_eq!(
      ended
        .latest_transition
        .as_ref()
        .expect("latest transition")
        .consultant_options
        .len(),
      4
    );
    assert!(
      ended
        .observation
        .iter()
        .any(|line| line.contains("STRATEGY CONSULTANT NOTES"))
    );

    let ended = store
      .end_session(EndSessionRequest {
        session_id: session.session_id,
      })
      .expect("end session");
    assert!(
      ended
        .debrief
        .iter()
        .any(|line| line.contains("Consultant options shown"))
    );
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
  fn competitive_debrief_includes_monthly_operating_result() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let session = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id,
        command_text: "hold".to_string(),
      })
      .expect("advance one month");
    let ended = store
      .end_session(EndSessionRequest {
        session_id: session.session_id,
      })
      .expect("end session");
    let text = ended.debrief.join("\n");

    assert!(text.contains("Operating result: treated "));
    assert!(text.contains("operating revenue "));
    assert!(text.contains("operating cost "));
    assert!(text.contains("operating margin "));
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
  fn competitive_cash_validation_error_is_structured_and_does_not_advance() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");

    let err = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "invest domain=beds amount=40; recruit role=nurse headcount=5".to_string(),
      })
      .expect_err("batch should exceed starting cash");

    assert_eq!(err.error, "cash required 65 exceeds available 60");
    assert_eq!(err.code.as_deref(), Some("insufficient_cash"));
    assert_eq!(
      err.resource_limit,
      Some(ResourceLimitError {
        resource: "cash".to_string(),
        required: 65,
        available: 60,
      })
    );
    assert!(
      err
        .hint
        .as_deref()
        .is_some_and(|hint| hint.contains("Reduce cash spending"))
    );

    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");
    assert_eq!(current.turn, 1);
  }

  #[test]
  fn competitive_non_resource_validation_error_has_code_only() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");

    let err = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "commit pledge_type=access level=6".to_string(),
      })
      .expect_err("level should be out of range");

    assert_eq!(err.code.as_deref(), Some("commit_level_out_of_range"));
    assert!(err.error.contains("commit level 6"));
    assert_eq!(err.resource_limit, None);
    assert_eq!(err.hint, None);

    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");
    assert_eq!(current.turn, 1);
  }

  #[test]
  fn competitive_parser_error_remains_plain_and_does_not_advance() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");

    let err = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "bogus".to_string(),
      })
      .expect_err("unknown command should fail parsing");

    assert!(err.error.contains("unknown competitive verb"));
    assert_eq!(err.code, None);
    assert_eq!(err.resource_limit, None);
    assert_eq!(err.hint, None);

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

  #[test]
  fn starts_session_with_custom_scenario_path() {
    let mut store = GameSessionStore::default();
    let session = store
      .start_session(StartSessionRequest {
        campaign: "stabilization-v1".to_string(),
        seed: Some(42),
        difficulty: None,
        scenario_path: Some("scenarios/stabilization-v1.toml".to_string()),
      })
      .expect("session with custom scenario");

    assert_eq!(session.campaign, "stabilization-v1");
    assert_eq!(session.turn, 1);
    assert!(session.observation.iter().any(|line| line.contains("Cash")));
  }

  #[test]
  fn start_session_fails_on_campaign_mismatch() {
    let mut store = GameSessionStore::default();
    let result = store.start_session(StartSessionRequest {
      campaign: "stabilization-v1".to_string(),
      seed: Some(42),
      difficulty: None,
      scenario_path: Some("scenarios/competitive-v1-template.toml".to_string()),
    });

    assert!(result.is_err());
    let err = result.unwrap_err();
    assert!(err.error.contains("does not match request campaign"));
  }

  #[test]
  fn starts_competitive_session_with_custom_scenario_path() {
    let mut store = GameSessionStore::default();
    let session = store
      .start_session(StartSessionRequest {
        campaign: "competitive-regional-v1".to_string(),
        seed: Some(42),
        difficulty: None,
        scenario_path: Some("scenarios/competitive-v1-template.toml".to_string()),
      })
      .expect("session with custom competitive scenario");

    assert_eq!(session.campaign, "competitive-regional-v1");
    assert_eq!(session.turn, 1);
    assert_eq!(session.difficulty, Some("Normal".to_string())); // Derived from 3 systems
    assert!(
      session
        .observation
        .iter()
        .any(|line| line.contains("Riverside"))
    );
  }

  #[test]
  fn starts_competitive_session_fails_on_difficulty_mismatch() {
    let mut store = GameSessionStore::default();
    let result = store.start_session(StartSessionRequest {
      campaign: "competitive-regional-v1".to_string(),
      seed: Some(42),
      difficulty: Some("easy".to_string()), // expects 2 systems, template has 3
      scenario_path: Some("scenarios/competitive-v1-template.toml".to_string()),
    });

    assert!(result.is_err());
    let err = result.unwrap_err();
    assert!(err.error.contains("expects 2 systems"));
  }

  #[test]
  fn affiliation_session_completes_six_stages_and_debriefs() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "regional-affiliation-v1");
    let commands = [
      "assess",
      "posture choice=independent",
      "hold",
      "hold",
      "hold",
      "hold",
    ];
    let mut current = session;
    for command in commands {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id,
          command_text: command.to_string(),
        })
        .expect("affiliation stage");
    }
    assert!(current.done);
    let ended = store
      .end_session(EndSessionRequest {
        session_id: current.session_id,
      })
      .expect("debrief");
    assert!(
      ended
        .debrief
        .iter()
        .any(|line| line.contains("Regional affiliation debrief"))
    );
  }

  #[test]
  fn affiliation_observation_includes_context() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "regional-affiliation-v1");
    assert!(
      session
        .observation
        .iter()
        .any(|line| line == "Commitments: community 0, workforce 0, continuity 0, total 0")
    );
    assert_eq!(
      session
        .observation
        .iter()
        .filter(|line| line.starts_with("Alternative:"))
        .count(),
      2
    );
    assert_eq!(
      session
        .observation
        .iter()
        .filter(|line| line.starts_with("Assumption:"))
        .count(),
      2
    );

    let assessed = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "assess".to_string(),
      })
      .expect("assessment");
    assert_eq!(
      assessed
        .observation
        .iter()
        .filter(|line| line.starts_with("Alternative:"))
        .count(),
      3
    );

    let pursuing = store
      .submit_turn(SubmitTurnRequest {
        session_id: assessed.session_id.clone(),
        command_text: "posture choice=pursue".to_string(),
      })
      .expect("posture");
    let committed = store
      .submit_turn(SubmitTurnRequest {
        session_id: pursuing.session_id,
        command_text: "commit community=6 workforce=6 continuity=6".to_string(),
      })
      .expect("commitments");
    assert!(
      committed
        .observation
        .iter()
        .any(|line| line == "Commitments: community 6, workforce 6, continuity 6, total 18")
    );
  }

  #[test]
  fn campaign_coverage_preserves_campaign_specific_observations() {
    let mut store = GameSessionStore::default();
    let stabilization = start(&mut store, "stabilization-v1");
    let stabilization_before = store
      .get_observation(GetObservationRequest {
        session_id: stabilization.session_id.clone(),
      })
      .expect("stabilization before coverage");
    let stabilization_coverage = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: stabilization.session_id.clone(),
      })
      .expect("stabilization coverage");
    let stabilization_after = store
      .get_observation(GetObservationRequest {
        session_id: stabilization.session_id,
      })
      .expect("stabilization after coverage");
    let stabilization_json =
      serde_json::to_string(&stabilization_coverage).expect("stabilization coverage json");
    assert_eq!(
      stabilization_coverage.schema_version,
      "campaign-coverage-v1"
    );
    assert_eq!(
      stabilization_coverage.campaign_role,
      "tutorial-oriented stabilization"
    );
    assert_eq!(stabilization_coverage.stage.id, "turn-1");
    assert_eq!(stabilization_coverage.decisions.len(), 1);
    assert_eq!(stabilization_coverage.decisions[0].parameters.len(), 3);
    assert_eq!(stabilization_before, stabilization_after);

    let affiliation = start(&mut store, "regional-affiliation-v1");
    let affiliation_coverage = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: affiliation.session_id,
      })
      .expect("affiliation coverage");
    let affiliation_json =
      serde_json::to_string(&affiliation_coverage).expect("affiliation coverage json");
    assert_eq!(
      affiliation_coverage.campaign_role,
      "institutional fit and obligation process"
    );
    assert_eq!(affiliation_coverage.stage.id, "assesspartner");
    assert!(
      affiliation_coverage
        .actors
        .iter()
        .any(|actor| actor.role == "Potential partner")
    );
    assert!(
      affiliation_coverage
        .metrics
        .iter()
        .any(|metric| metric.label == "Continuity commitment")
    );
    for json in [stabilization_json, affiliation_json] {
      for forbidden in [
        "WorldState",
        "AffiliationWorldState",
        "ResolvedInputs",
        "resolved_inputs",
        "effect_queue",
        "integration_drag",
        "condition_index",
      ] {
        assert!(!json.contains(forbidden), "found {forbidden}");
      }
    }

    let competitive = start(&mut store, "competitive-regional-v1");
    let competitive_before = store
      .get_observation(GetObservationRequest {
        session_id: competitive.session_id.clone(),
      })
      .expect("competitive before unsupported coverage");
    let error = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: competitive.session_id.clone(),
      })
      .expect_err("competitive coverage is intentionally unsupported");
    assert!(error.error.contains("stabilization-v1"));
    let competitive_after = store
      .get_observation(GetObservationRequest {
        session_id: competitive.session_id,
      })
      .expect("competitive after unsupported coverage");
    assert_eq!(competitive_before, competitive_after);
  }

  #[test]
  fn campaign_coverage_terminal_affiliation_includes_debrief() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "regional-affiliation-v1");
    let commands = [
      "assess",
      "posture choice=independent",
      "hold",
      "hold",
      "hold",
      "hold",
    ];
    let mut current = session;
    for command in commands {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id,
          command_text: command.to_string(),
        })
        .expect("affiliation stage");
    }
    let coverage = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: current.session_id,
      })
      .expect("terminal affiliation coverage");
    assert!(coverage.session.done);
    assert!(
      coverage
        .debrief
        .iter()
        .any(|line| line.contains("Regional affiliation debrief"))
    );
  }

  #[test]
  fn affiliation_invalid_command_does_not_advance() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "regional-affiliation-v1");
    let error = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect_err("hold is invalid before assessment");
    assert!(error.error.contains("not valid"));
    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");
    assert_eq!(current.turn, 1);
  }

  #[test]
  fn presentation_is_typed_read_only_and_excludes_hidden_fields() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let before = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("observation before presentation");
    let presentation = store
      .get_presentation(GetPresentationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("presentation");
    let after = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("observation after presentation");
    let json = serde_json::to_value(&presentation).expect("presentation JSON");

    assert_eq!(presentation.schema_version, "competitive-read-only-v1");
    assert_eq!(presentation.session.turn, before.turn);
    assert_eq!(presentation.replay.transition_count, 0);
    assert_eq!(presentation.institutions.len(), 1);
    assert_eq!(
      presentation.institutions[0].name,
      "Riverside Community Health"
    );
    assert_eq!(before, after);
    for forbidden in [
      "legal_commands",
      "CompetitiveWorldState",
      "resolved_inputs",
      "effect_queue",
      "event_metadata",
      "rna_strike_active",
    ] {
      assert!(!json.to_string().contains(forbidden), "found {forbidden}");
    }
  }

  #[test]
  fn presentation_carries_committed_history_and_hash() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let advanced = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("competitive month");
    let presentation = store
      .get_presentation(GetPresentationRequest {
        session_id: session.session_id,
      })
      .expect("presentation");

    let transition = advanced.latest_transition.expect("latest transition");
    assert_eq!(presentation.history.len(), 1);
    assert_eq!(presentation.replay.transition_count, 1);
    assert_eq!(
      presentation.replay.latest_state_hash,
      Some(transition.state_hash.clone())
    );
    assert_eq!(presentation.latest_transition, Some(transition));
  }

  #[test]
  fn presentation_rejects_other_campaigns_without_mutation() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "stabilization-v1");
    let result = store.get_presentation(GetPresentationRequest {
      session_id: session.session_id.clone(),
    });
    assert!(result.is_err());
    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");
    assert_eq!(current.turn, 1);
  }

  #[test]
  fn resolution_returns_eight_host_sourced_steps_without_advancing() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let advanced = store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("competitive month");
    let before = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("observation before resolution read");
    let resolution = store
      .get_resolution(GetResolutionRequest {
        session_id: session.session_id,
        turn: None,
      })
      .expect("resolution");
    let after = store
      .get_observation(GetObservationRequest {
        session_id: advanced.session_id.clone(),
      })
      .expect("observation after resolution read");
    let ids = resolution
      .steps
      .iter()
      .map(|step| step.id.as_str())
      .collect::<Vec<_>>();
    let json = serde_json::to_string(&resolution).expect("resolution json");

    assert_eq!(resolution.schema_version, "competitive-resolution-v1");
    assert_eq!(resolution.turn, 1);
    assert_eq!(
      ids,
      [
        "submitted",
        "responses",
        "processes",
        "operations",
        "resources",
        "effects",
        "information",
        "pending"
      ]
    );
    assert_eq!(
      resolution.replay.state_hash,
      advanced
        .latest_transition
        .as_ref()
        .expect("latest transition")
        .state_hash
    );
    assert_eq!(before, after);
    for forbidden in [
      "CompetitiveWorldState",
      "resolved_inputs",
      "effect_queue",
      "event_metadata",
      "rna_strike_active",
    ] {
      assert!(!json.contains(forbidden), "found {forbidden}");
    }
  }

  #[test]
  fn resolution_historical_lookup_is_hash_stable_and_recoverable() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let mut current = session;
    for _ in 0..2 {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("competitive month");
    }
    let history = store
      .get_history(GetHistoryRequest {
        session_id: current.session_id.clone(),
      })
      .expect("history");
    let resolution = store
      .get_resolution(GetResolutionRequest {
        session_id: current.session_id.clone(),
        turn: Some(1),
      })
      .expect("historical resolution");
    let after = store
      .get_observation(GetObservationRequest {
        session_id: current.session_id.clone(),
      })
      .expect("current observation");

    assert_eq!(resolution.turn, 1);
    assert_eq!(
      resolution.replay.state_hash,
      history.transitions[0].state_hash
    );
    assert_eq!(resolution.replay.transition_count, 2);
    assert_eq!(after.turn, 3);
    assert!(
      store
        .get_resolution(GetResolutionRequest {
          session_id: current.session_id,
          turn: Some(99),
        })
        .is_err()
    );
  }

  #[test]
  fn resolution_rejects_unsupported_campaign_and_empty_history() {
    let mut store = GameSessionStore::default();
    let stabilization = start(&mut store, "stabilization-v1");
    assert!(
      store
        .get_resolution(GetResolutionRequest {
          session_id: stabilization.session_id,
          turn: None,
        })
        .is_err()
    );

    let competitive = start(&mut store, "competitive-regional-v1");
    let result = store.get_resolution(GetResolutionRequest {
      session_id: competitive.session_id,
      turn: None,
    });
    assert!(result.is_err());
  }

  #[test]
  fn regional_world_projection_is_actor_visible_and_non_mutating() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let before = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("observation before regional world");
    let world = store
      .get_regional_world(GetRegionalWorldRequest {
        session_id: session.session_id.clone(),
      })
      .expect("regional world");
    let after = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation after regional world");
    let json = serde_json::to_string(&world).expect("regional world json");

    assert_eq!(world.schema_version, "competitive-regional-world-v1");
    assert!(
      world
        .entities
        .iter()
        .any(|entity| entity.visibility == "owned")
    );
    assert!(
      world
        .entities
        .iter()
        .any(|entity| entity.visibility == "public identity")
    );
    let owned_facilities = world
      .entities
      .iter()
      .find(|entity| entity.visibility == "owned")
      .expect("owned regional-world entity")
      .facilities
      .iter()
      .map(|facility| facility.component_id.as_str())
      .collect::<Vec<_>>();
    assert_eq!(
      owned_facilities,
      vec![
        "general-hospital-base",
        "ambulatory-center",
        "emergency-department",
        "specialty-center",
      ]
    );
    assert!(world.overlays.iter().any(|overlay| overlay.id == "demand"));
    assert!(
      world
        .missing
        .iter()
        .any(|missing| missing.id.ends_with("private-detail"))
    );
    assert!(
      world
        .missing
        .iter()
        .any(|missing| missing.id.ends_with("-process"))
    );
    assert_eq!(before, after);
    for forbidden in [
      "CompetitiveWorldState",
      "HealthSystemState",
      "effect_queue",
      "event_metadata",
      "resolved_inputs",
      "monthly_operating_margin",
    ] {
      assert!(!json.contains(forbidden), "found {forbidden}");
    }
  }

  #[test]
  fn regional_world_public_signals_respect_observation_lag() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let mut current = session;
    for _ in 0..2 {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("competitive month");
    }
    let world = store
      .get_regional_world(GetRegionalWorldRequest {
        session_id: current.session_id,
      })
      .expect("regional world");

    let session_turn = world.session.turn;
    for entity in world.entities {
      for signal in entity.signals {
        assert!(signal.observed_month < session_turn);
        assert!(signal.source.contains("one-month observation lag"));
      }
    }
  }

  #[test]
  fn regional_world_rejects_unsupported_campaign() {
    let mut store = GameSessionStore::default();
    let stabilization = start(&mut store, "stabilization-v1");
    assert!(
      store
        .get_regional_world(GetRegionalWorldRequest {
          session_id: stabilization.session_id,
        })
        .is_err()
    );
  }

  #[test]
  fn action_catalog_covers_existing_competitive_command_families() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let catalog = store
      .get_action_catalog(GetActionCatalogRequest {
        session_id: session.session_id,
      })
      .expect("action catalog");
    let ids = catalog
      .actions
      .iter()
      .map(|action| action.id.as_str())
      .collect::<Vec<_>>();

    assert_eq!(catalog.schema_version, "competitive-actions-v1");
    assert_eq!(
      ids,
      [
        "hold",
        "invest",
        "recruit",
        "monitor",
        "negotiate",
        "commit",
        "project"
      ]
    );
    assert_eq!(
      catalog
        .actions
        .iter()
        .map(|action| action.command_template.as_str())
        .collect::<Vec<_>>(),
      [
        "hold",
        "invest domain={{domain}} amount={{amount}}",
        "recruit role={{role}} headcount={{headcount}}",
        "monitor target={{target}} depth={{depth}}",
        "negotiate payer={{payer}} rate_posture={{rate_posture}}",
        "commit pledge_type={{pledge_type}} level={{level}}",
        "project kind={{kind}} budget={{budget}}",
      ]
    );
    assert!(
      catalog
        .actions
        .iter()
        .all(|action| { action.command_template == "hold" || !action.parameters.is_empty() })
    );
  }

  #[test]
  fn action_validation_returns_host_costs_without_advancing() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let before = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("observation before validation");
    let validation = store
      .validate_turn(ValidateTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "recruit role=nurse headcount=2; invest domain=beds amount=10".to_string(),
      })
      .expect("validation");
    let after = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation after validation");
    let cost = validation.cost.expect("host cost");

    assert_eq!(validation.schema_version, "competitive-validation-v1");
    assert!(validation.valid);
    assert_eq!(
      validation.canonical_command_text,
      "recruit role=nurse headcount=2; invest domain=beds amount=10"
    );
    assert_eq!(cost.action_points, 2);
    assert_eq!(cost.cash_cost, 20);
    assert_eq!(validation.previews.len(), 2);
    assert_eq!(
      validation.previews[0].canonical_command,
      "recruit role=nurse headcount=2"
    );
    assert_eq!(before, after);
  }

  #[test]
  fn invalid_action_validation_is_recoverable_and_non_mutating() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let before = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id.clone(),
      })
      .expect("observation before validation");
    let validation = store
      .validate_turn(ValidateTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "recruit role=nurse headcount=99".to_string(),
      })
      .expect("validation response");
    let current = store
      .get_observation(GetObservationRequest {
        session_id: session.session_id,
      })
      .expect("observation");

    assert!(!validation.valid);
    assert!(
      validation
        .errors
        .iter()
        .any(|error| error.contains("outside range"))
    );
    assert_eq!(current, before);
  }
}
