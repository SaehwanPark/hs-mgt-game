use std::collections::HashMap;
use std::path::PathBuf;

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
  AFFILIATION_TURN_COUNT, AffiliationHistory, AffiliationRuleset, AffiliationTransition,
  AffiliationWorldState, AggregatedMonthlyActions, CampaignId, CompetitiveHistory,
  CompetitiveRuleset, CompetitiveTransition, CompetitiveWorldState, Difficulty, History,
  INTERACTIVE_TURN_COUNT, Observation, PlayerObservation, Ruleset, SystemMonthlyBatch, Transition,
  default_affiliation_ruleset, default_competitive_ruleset, default_ruleset,
};
use crate::scenario::{
  Scenario, default_stabilization_scenario, validate_competitive_scenario,
  validate_stabilization_scenario,
};
use crate::sim::{observe_for_human, observe_for_player, transition, validate_competitive_batch};

use super::persistence::{
  GuiSessionSave, load_gui_session_save, remove_gui_session_save, write_affiliation_session_save,
  write_competitive_session_save, write_stabilization_session_save,
};

pub(crate) const COMPETITIVE_MONTH_LIMIT: u32 = 24;
pub const HISTORY_SCHEMA_VERSION: &str = "competitive-history-v1";
pub const REPLAY_SCHEMA_VERSION: &str = "competitive-replay-v1";
pub const SAVE_SCHEMA_VERSION: &str = "competitive-save-v1";
pub const END_SESSION_SCHEMA_VERSION: &str = "competitive-end-session-v1";

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
pub struct GetReplayRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct SaveSessionRequest {
  pub session_id: String,
}

#[derive(Clone, Debug, Deserialize, JsonSchema, Serialize)]
pub struct LoadSessionRequest {
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
  pub schema_version: String,
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub transition_count: usize,
  pub transitions: Vec<TransitionSummary>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct ReplayEnvelope {
  pub schema_version: String,
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub transition_count: usize,
  pub latest_state_hash: Option<String>,
  pub transitions: Vec<TransitionSummary>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct SaveEnvelope {
  pub schema_version: String,
  pub operation: String,
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub transition_count: usize,
  pub latest_state_hash: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct EndSessionEnvelope {
  pub schema_version: String,
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub turn: u32,
  pub max_turns: u32,
  pub done: bool,
  pub history: Vec<TransitionSummary>,
  pub debrief: Vec<String>,
  pub replay: EndSessionReplayMetadata,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, JsonSchema)]
pub struct EndSessionReplayMetadata {
  pub seed: u64,
  pub transition_count: usize,
  pub latest_state_hash: Option<String>,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Eq, Serialize, JsonSchema)]
pub struct TransitionSummary {
  pub turn: u32,
  pub command: String,
  #[serde(default, skip_serializing_if = "Option::is_none")]
  pub observation: Option<Vec<String>>,
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
  checkpoints: HashMap<String, GameSession>,
  durable_gui_save_path: Option<PathBuf>,
}

#[derive(Clone, Debug)]
#[allow(clippy::large_enum_variant)]
enum GameSession {
  Stabilization(StabilizationSession),
  Competitive(CompetitiveSession),
  Affiliation(AffiliationSession),
}

#[derive(Clone, Debug)]
struct StabilizationSession {
  seed: u64,
  ruleset: Ruleset,
  history: History,
  current: crate::model::WorldState,
  done: bool,
}

#[derive(Clone, Debug)]
struct CompetitiveSession {
  seed: u64,
  ruleset: CompetitiveRuleset,
  history: CompetitiveHistory,
  current: CompetitiveWorldState,
  prior_aggregated: Option<AggregatedMonthlyActions>,
  done: bool,
}

#[derive(Clone, Debug)]
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
      checkpoints: HashMap::new(),
      durable_gui_save_path: None,
    }
  }
}

impl GameSessionStore {
  pub fn with_competitive_persistence(path: PathBuf) -> Self {
    Self::with_gui_persistence(path)
  }

  pub fn with_gui_persistence(path: PathBuf) -> Self {
    Self {
      durable_gui_save_path: Some(path),
      ..Self::default()
    }
  }

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
        schema_version: HISTORY_SCHEMA_VERSION.to_string(),
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
        schema_version: HISTORY_SCHEMA_VERSION.to_string(),
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
        schema_version: HISTORY_SCHEMA_VERSION.to_string(),
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

  pub fn get_replay(&self, request: GetReplayRequest) -> Result<ReplayEnvelope, McpErrorMessage> {
    if let Some(GameSession::Competitive(session)) = self.sessions.get(&request.session_id) {
      crate::competitive::regenerate_competitive_history(
        &session.history,
        &session.ruleset,
        session.seed,
      )
      .map_err(|error| McpErrorMessage {
        error: format!("replay verification failed: {}", error.message()),
        code: Some("replay_verification_failed".to_string()),
        resource_limit: None,
        hint: None,
      })?;
    }
    let history = self.get_history(GetHistoryRequest {
      session_id: request.session_id,
    })?;
    let latest_state_hash = history
      .transitions
      .last()
      .map(|transition| transition.state_hash.clone());
    Ok(ReplayEnvelope {
      schema_version: REPLAY_SCHEMA_VERSION.to_string(),
      session_id: history.session_id,
      campaign: history.campaign,
      seed: history.seed,
      transition_count: history.transition_count,
      latest_state_hash,
      transitions: history.transitions,
    })
  }

  pub fn save_session(
    &mut self,
    request: SaveSessionRequest,
  ) -> Result<SaveEnvelope, McpErrorMessage> {
    let Some(session) = self.sessions.get(&request.session_id).cloned() else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    if let Some(path) = &self.durable_gui_save_path {
      match &session {
        GameSession::Competitive(competitive) => write_competitive_session_save(
          path,
          &request.session_id,
          &competitive_session_save(competitive),
        )
        .map_err(checkpoint_persistence_error)?,
        GameSession::Stabilization(stabilization) => write_stabilization_session_save(
          path,
          &request.session_id,
          &stabilization_session_save(stabilization),
        )
        .map_err(checkpoint_persistence_error)?,
        GameSession::Affiliation(affiliation) => write_affiliation_session_save(
          path,
          &request.session_id,
          &affiliation_session_save(affiliation),
        )
        .map_err(checkpoint_persistence_error)?,
      }
    }
    self.checkpoints.insert(request.session_id.clone(), session);
    self.save_envelope(&request.session_id, "saved")
  }

  pub fn load_session(
    &mut self,
    request: LoadSessionRequest,
  ) -> Result<SaveEnvelope, McpErrorMessage> {
    if !self.sessions.contains_key(&request.session_id)
      && !self.hydrate_durable_session(&request.session_id)?
    {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    }
    let snapshot = match self.checkpoints.get(&request.session_id).cloned() {
      Some(snapshot) => snapshot,
      None => {
        if !self.hydrate_durable_session(&request.session_id)? {
          return Err(McpErrorMessage {
            error: format!("no checkpoint saved for session '{}'", request.session_id),
            code: Some("checkpoint_missing".to_string()),
            resource_limit: None,
            hint: Some("Save a host checkpoint before restoring it.".to_string()),
          });
        }
        self
          .checkpoints
          .get(&request.session_id)
          .cloned()
          .expect("durable hydration stores a checkpoint")
      }
    };
    if let Some(session) = self.sessions.get_mut(&request.session_id) {
      *session = snapshot;
    }
    self.save_envelope(&request.session_id, "loaded")
  }

  fn save_envelope(
    &self,
    session_id: &str,
    operation: &str,
  ) -> Result<SaveEnvelope, McpErrorMessage> {
    let replay = self.get_replay(GetReplayRequest {
      session_id: session_id.to_string(),
    })?;
    Ok(SaveEnvelope {
      schema_version: SAVE_SCHEMA_VERSION.to_string(),
      operation: operation.to_string(),
      session_id: replay.session_id,
      campaign: replay.campaign,
      seed: replay.seed,
      transition_count: replay.transition_count,
      latest_state_hash: replay.latest_state_hash,
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
      GameSession::Competitive(session) => {
        let history = session
          .history
          .transitions
          .iter()
          .map(summarize_competitive_campaign_coverage_transition)
          .collect::<Vec<_>>();
        Ok(crate::mcp::campaign_coverage::from_competitive(
          request.session_id,
          session.seed,
          session.done,
          &session.current,
          session.prior_aggregated.as_ref(),
          &history,
          &session.history,
        ))
      }
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
    let durable_gui_checkpoint = self
      .sessions
      .get(&request.session_id)
      .is_some_and(|session| {
        matches!(
          session,
          GameSession::Competitive(_) | GameSession::Stabilization(_) | GameSession::Affiliation(_)
        ) && self.checkpoints.contains_key(&request.session_id)
      });
    if durable_gui_checkpoint && let Some(path) = &self.durable_gui_save_path {
      remove_gui_session_save(path, &request.session_id).map_err(checkpoint_persistence_error)?;
    }
    let Some(mut session) = self.sessions.remove(&request.session_id) else {
      return Err(error_message(format!(
        "unknown session '{}'",
        request.session_id
      )));
    };
    self.checkpoints.remove(&request.session_id);
    session.mark_done();
    Ok(match session {
      GameSession::Stabilization(session) => {
        let history: Vec<_> = session
          .history
          .transitions
          .iter()
          .map(summarize_stabilization_transition)
          .collect();
        EndSessionEnvelope {
          schema_version: END_SESSION_SCHEMA_VERSION.to_string(),
          session_id: request.session_id,
          campaign: CampaignId::StabilizationV1.as_str().to_string(),
          seed: session.seed,
          turn: session.current.turn,
          max_turns: INTERACTIVE_TURN_COUNT,
          done: session.done,
          history: history.clone(),
          debrief: educational_debrief(&session.history),
          replay: end_session_replay(session.seed, &history),
        }
      }
      GameSession::Competitive(session) => {
        let history: Vec<_> = session
          .history
          .transitions
          .iter()
          .map(summarize_competitive_transition)
          .collect();
        EndSessionEnvelope {
          schema_version: END_SESSION_SCHEMA_VERSION.to_string(),
          session_id: request.session_id,
          campaign: CampaignId::CompetitiveRegionalV1.as_str().to_string(),
          seed: session.seed,
          turn: session.current.turn,
          max_turns: COMPETITIVE_MONTH_LIMIT,
          done: session.done,
          history: history.clone(),
          debrief: competitive_debrief(&session.history),
          replay: end_session_replay(session.seed, &history),
        }
      }
      GameSession::Affiliation(session) => {
        let history: Vec<_> = session
          .history
          .transitions
          .iter()
          .map(summarize_affiliation_transition)
          .collect();
        EndSessionEnvelope {
          schema_version: END_SESSION_SCHEMA_VERSION.to_string(),
          session_id: request.session_id,
          campaign: CampaignId::RegionalAffiliationV1.as_str().to_string(),
          seed: session.seed,
          turn: session.current.turn,
          max_turns: AFFILIATION_TURN_COUNT,
          done: session.done,
          history: history.clone(),
          debrief: affiliation_debrief(&session.history),
          replay: end_session_replay(session.seed, &history),
        }
      }
    })
  }

  fn allocate_session_id(&mut self) -> String {
    loop {
      let id = format!("session-{}", self.next_id);
      self.next_id += 1;
      if !self.sessions.contains_key(&id) {
        return id;
      }
    }
  }

  fn hydrate_durable_session(&mut self, session_id: &str) -> Result<bool, McpErrorMessage> {
    if self.sessions.contains_key(session_id) {
      return Ok(false);
    }
    let Some(path) = &self.durable_gui_save_path else {
      return Ok(false);
    };
    let Some(save) = load_gui_session_save(
      path,
      session_id,
      &default_competitive_ruleset(),
      &default_ruleset(),
      &default_affiliation_ruleset(),
    )
    .map_err(checkpoint_persistence_error)?
    else {
      return Ok(false);
    };
    let session = match save {
      GuiSessionSave::Competitive(save) => competitive_session_from_save(save),
      GuiSessionSave::Stabilization(save) => stabilization_session_from_save(save),
      GuiSessionSave::Affiliation(save) => affiliation_session_from_save(save),
    };
    self
      .checkpoints
      .insert(session_id.to_string(), session.clone());
    self.sessions.insert(session_id.to_string(), session);
    self.reserve_loaded_session_id(session_id);
    Ok(true)
  }

  fn reserve_loaded_session_id(&mut self, session_id: &str) {
    let Some(id) = session_id.strip_prefix("session-") else {
      return;
    };
    let Ok(id) = id.parse::<u64>() else {
      return;
    };
    self.next_id = self.next_id.max(id.saturating_add(1));
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

fn competitive_session_save(session: &CompetitiveSession) -> crate::model::CompetitiveSessionSave {
  crate::model::CompetitiveSessionSave {
    ruleset_version: session.ruleset.version.to_string(),
    seed: session.seed,
    difficulty: session.current.difficulty,
    history: session.history.clone(),
    next_month: session.current.policy_calendar.month_index,
  }
}

fn stabilization_session_save(session: &StabilizationSession) -> crate::model::SessionSave {
  crate::model::SessionSave {
    ruleset_version: session.ruleset.version.to_string(),
    seed: session.seed,
    experience_mode: crate::model::ExperienceMode::Standard,
    history: session.history.clone(),
    next_turn: session.current.turn + 1,
  }
}

fn affiliation_session_save(
  session: &AffiliationSession,
) -> crate::model::AffiliationReplayArtifact {
  crate::model::AffiliationReplayArtifact {
    artifact_version: crate::model::AFFILIATION_REPLAY_ARTIFACT_VERSION.to_string(),
    seed: session.seed,
    ruleset_version: session.ruleset.version.to_string(),
    history: session.history.clone(),
  }
}

fn competitive_session_from_save(save: crate::model::CompetitiveSessionSave) -> GameSession {
  let current = save.history.final_state().clone();
  let prior_aggregated = save
    .history
    .transitions
    .last()
    .map(|transition| transition.aggregated.clone());
  let done = current.turn >= COMPETITIVE_MONTH_LIMIT;
  GameSession::Competitive(CompetitiveSession {
    seed: save.seed,
    ruleset: default_competitive_ruleset(),
    history: save.history,
    current,
    prior_aggregated,
    done,
  })
}

fn stabilization_session_from_save(save: crate::model::SessionSave) -> GameSession {
  let current = save
    .history
    .transitions
    .last()
    .map(|transition| transition.next.clone())
    .unwrap_or_else(|| save.history.genesis.clone());
  let done = current.turn >= INTERACTIVE_TURN_COUNT;
  GameSession::Stabilization(StabilizationSession {
    seed: save.seed,
    ruleset: default_ruleset(),
    history: save.history,
    current,
    done,
  })
}

fn affiliation_session_from_save(save: crate::model::AffiliationReplayArtifact) -> GameSession {
  let current = save.history.final_state().clone();
  let done = current.turn >= AFFILIATION_TURN_COUNT;
  GameSession::Affiliation(AffiliationSession {
    seed: save.seed,
    ruleset: default_affiliation_ruleset(),
    history: save.history,
    current,
    done,
  })
}

fn checkpoint_persistence_error(error: String) -> McpErrorMessage {
  McpErrorMessage {
    error,
    code: Some("checkpoint_persistence".to_string()),
    resource_limit: None,
    hint: Some(
      "The current host session remains available; retry the checkpoint operation.".to_string(),
    ),
  }
}

fn end_session_replay(seed: u64, history: &[TransitionSummary]) -> EndSessionReplayMetadata {
  EndSessionReplayMetadata {
    seed,
    transition_count: history.len(),
    latest_state_hash: history.last().map(|entry| entry.state_hash.clone()),
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
    observation: Some(format_stabilization_observation(
      &transition.prior,
      &transition.observation,
    )),
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
    observation: None,
    events: transition.events.iter().map(format_event).collect(),
    effects: transition.effects.iter().map(format_effect).collect(),
    state_hash: transition.state_hash.clone(),
    consultant_options: transition.consultant_options.clone(),
  }
}

pub(crate) fn summarize_competitive_campaign_coverage_transition(
  transition: &CompetitiveTransition,
) -> TransitionSummary {
  let command = transition
    .aggregated
    .batch_for_system(0)
    .map(|batch| format!("{:?}", batch.commands))
    .unwrap_or_else(|| "[]".to_string());
  let current_month = transition.prior.policy_calendar.month_index;
  let events = transition
    .next
    .public_action_log
    .iter()
    .filter(|entry| entry.month_index == current_month)
    .map(|entry| format!("Public action: {}", entry.summary))
    .collect();

  TransitionSummary {
    turn: transition.next.turn,
    command,
    observation: None,
    events,
    effects: Vec::new(),
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
    observation: Some(format_affiliation_observation(&transition.observation)),
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
  use crate::model::CompetitiveCommand;

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
    assert_eq!(history.schema_version, HISTORY_SCHEMA_VERSION);
    assert_eq!(history.transition_count, 5);
  }

  #[test]
  fn competitive_replay_projection_aligns_with_immutable_history() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let replay = store
      .get_replay(GetReplayRequest {
        session_id: session.session_id.clone(),
      })
      .expect("empty replay");
    assert_eq!(replay.schema_version, REPLAY_SCHEMA_VERSION);
    assert_eq!(replay.transition_count, 0);
    assert!(replay.latest_state_hash.is_none());

    store
      .submit_turn(SubmitTurnRequest {
        session_id: session.session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("advance one month");
    let replay = store
      .get_replay(GetReplayRequest {
        session_id: session.session_id.clone(),
      })
      .expect("committed replay");
    let history = store
      .get_history(GetHistoryRequest {
        session_id: session.session_id,
      })
      .expect("history");
    assert_eq!(replay.transition_count, 1);
    assert_eq!(replay.transitions, history.transitions);
    assert_eq!(
      replay.latest_state_hash,
      history
        .transitions
        .last()
        .map(|transition| transition.state_hash.clone())
    );
  }

  #[test]
  fn competitive_replay_rejects_tampered_history_before_projection() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let session_id = session.session_id.clone();
    store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("advance one month");

    let GameSession::Competitive(session) = store.sessions.get_mut(&session_id).expect("session")
    else {
      panic!("expected competitive session");
    };
    session.history.transitions[0].effects[0].delta += 1;

    let error = store
      .get_replay(GetReplayRequest { session_id })
      .expect_err("tampered replay");
    assert_eq!(error.code.as_deref(), Some("replay_verification_failed"));
  }

  #[test]
  fn competitive_checkpoint_restore_rewinds_visible_history_and_hashes() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let session_id = session.session_id.clone();
    store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("first month");
    let saved = store
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("save checkpoint");
    assert_eq!(saved.schema_version, SAVE_SCHEMA_VERSION);
    assert_eq!(saved.operation, "saved");
    assert_eq!(saved.transition_count, 1);
    let second = store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("second month");
    let restored = store
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("restore checkpoint");
    assert_eq!(restored.operation, "loaded");
    assert_eq!(restored.transition_count, 1);
    let current = store
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("restored replay");
    assert_eq!(current.transition_count, 1);
    assert_eq!(current.latest_state_hash, restored.latest_state_hash);
    let replayed = store
      .submit_turn(SubmitTurnRequest {
        session_id,
        command_text: "hold".to_string(),
      })
      .expect("replayed month");
    assert_eq!(
      replayed
        .latest_transition
        .map(|transition| transition.state_hash),
      second
        .latest_transition
        .map(|transition| transition.state_hash)
    );
  }

  #[test]
  fn competitive_durable_checkpoint_recovers_across_store_restart() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-checkpoint-{}.save",
      std::process::id()
    ));
    let mut store = GameSessionStore::with_competitive_persistence(path.clone());
    let session = start(&mut store, "competitive-regional-v1");
    let session_id = session.session_id.clone();
    store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("first month");
    let saved = store
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable save");
    assert_eq!(saved.transition_count, 1);
    assert!(path.is_file());

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let loaded = restarted
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable load");
    assert_eq!(loaded.operation, "loaded");
    assert_eq!(loaded.transition_count, saved.transition_count);
    assert_eq!(loaded.latest_state_hash, saved.latest_state_hash);
    let next_id = start(&mut restarted, "competitive-regional-v1").session_id;
    assert_eq!(next_id, "session-2");

    let original_next = store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("original continuation");
    let restarted_next = restarted
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("restarted continuation");
    assert_eq!(
      restarted_next
        .latest_transition
        .map(|transition| transition.state_hash),
      original_next
        .latest_transition
        .map(|transition| transition.state_hash)
    );

    restarted
      .end_session(EndSessionRequest { session_id })
      .expect("end recovered session");
    assert!(!path.exists());
  }

  #[test]
  fn competitive_durable_checkpoint_covers_full_campaign_continuation() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-full-campaign-{}.save",
      std::process::id()
    ));
    let mut original = GameSessionStore::with_competitive_persistence(path.clone());
    let session = start(&mut original, "competitive-regional-v1");
    let session_id = session.session_id.clone();
    for _ in 0..12 {
      original
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("pre-checkpoint month");
    }
    let saved = original
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("mid-campaign durable save");
    assert_eq!(saved.transition_count, 12);

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let loaded = restarted
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("mid-campaign durable load");
    assert_eq!(loaded.transition_count, saved.transition_count);
    assert_eq!(loaded.latest_state_hash, saved.latest_state_hash);

    for _ in 12..COMPETITIVE_MONTH_LIMIT {
      let original_next = original
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("original continuation month");
      let restarted_next = restarted
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("restored continuation month");
      assert_eq!(
        original_next
          .latest_transition
          .map(|transition| transition.state_hash),
        restarted_next
          .latest_transition
          .map(|transition| transition.state_hash)
      );
    }

    let original_replay = original
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("original terminal replay");
    let restarted_replay = restarted
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("restored terminal replay");
    assert_eq!(original_replay, restarted_replay);
    assert_eq!(
      original_replay.transition_count,
      COMPETITIVE_MONTH_LIMIT as usize
    );
    assert_eq!(
      original_replay.latest_state_hash,
      restarted_replay.latest_state_hash
    );

    let original_world = original
      .get_regional_world(GetRegionalWorldRequest {
        session_id: session_id.clone(),
      })
      .expect("original terminal regional world");
    let restarted_world = restarted
      .get_regional_world(GetRegionalWorldRequest {
        session_id: session_id.clone(),
      })
      .expect("restored terminal regional world");
    assert_eq!(original_world, restarted_world);
    assert!(original_world.session.done);

    let original_coverage = original
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("original terminal campaign coverage");
    let restarted_coverage = restarted
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("restored terminal campaign coverage");
    assert_eq!(original_coverage, restarted_coverage);
    assert!(original_coverage.session.done);

    restarted
      .end_session(EndSessionRequest { session_id })
      .expect("end recovered terminal session");
    assert!(!path.exists());
  }

  #[test]
  fn durable_checkpoint_does_not_overwrite_live_session_with_reused_id() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-collision-{}.save",
      std::process::id()
    ));
    let mut original = GameSessionStore::with_competitive_persistence(path.clone());
    let original_session = start(&mut original, "competitive-regional-v1");
    let original_id = original_session.session_id.clone();
    original
      .submit_turn(SubmitTurnRequest {
        session_id: original_id.clone(),
        command_text: "hold".to_string(),
      })
      .expect("first month");
    original
      .save_session(SaveSessionRequest {
        session_id: original_id.clone(),
      })
      .expect("durable save");

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let live = start(&mut restarted, "competitive-regional-v1");
    assert_eq!(live.session_id, original_id);
    let error = restarted
      .load_session(LoadSessionRequest {
        session_id: live.session_id.clone(),
      })
      .expect_err("a live colliding session must not be overwritten");
    assert_eq!(error.code.as_deref(), Some("checkpoint_missing"));
    let replay = restarted
      .get_replay(GetReplayRequest {
        session_id: live.session_id.clone(),
      })
      .expect("live session remains available");
    assert_eq!(replay.transition_count, 0);
    restarted
      .end_session(EndSessionRequest {
        session_id: live.session_id,
      })
      .expect("end colliding live session");
    assert!(path.is_file(), "unclaimed durable checkpoint must remain");
    let _ = std::fs::remove_file(path);
  }

  #[test]
  fn durable_stabilization_checkpoint_recovers_across_store_restart() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-stabilization-{}.save",
      std::process::id()
    ));
    let mut store = GameSessionStore::with_competitive_persistence(path.clone());
    let session = start(&mut store, "stabilization-v1");
    let session_id = session.session_id.clone();
    let first = store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: String::new(),
      })
      .expect("first stage");
    let saved = store
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable stabilization save");
    assert_eq!(saved.transition_count, 1);
    assert!(path.is_file());

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let loaded = restarted
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable stabilization load");
    assert_eq!(loaded.transition_count, saved.transition_count);
    assert_eq!(loaded.latest_state_hash, saved.latest_state_hash);
    let restored = restarted
      .get_observation(GetObservationRequest {
        session_id: session_id.clone(),
      })
      .expect("restored observation");
    assert_eq!(restored.turn, first.turn);

    let original_next = store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: String::new(),
      })
      .expect("original continuation");
    let restarted_next = restarted
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: String::new(),
      })
      .expect("restarted continuation");
    assert_eq!(
      restarted_next
        .latest_transition
        .map(|transition| transition.state_hash),
      original_next
        .latest_transition
        .map(|transition| transition.state_hash)
    );

    restarted
      .end_session(EndSessionRequest { session_id })
      .expect("end recovered stabilization session");
    assert!(!path.exists());
  }

  #[test]
  fn durable_stabilization_checkpoint_covers_full_campaign_continuation() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-full-stabilization-{}.save",
      std::process::id()
    ));
    let mut original = GameSessionStore::with_competitive_persistence(path.clone());
    let session = start(&mut original, "stabilization-v1");
    let session_id = session.session_id.clone();
    for _ in 0..2 {
      original
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: String::new(),
        })
        .expect("stabilization stage before checkpoint");
    }
    let saved = original
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable stabilization stage-two save");
    assert_eq!(saved.transition_count, 2);
    assert!(path.is_file());

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let loaded = restarted
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable stabilization stage-two load");
    assert_eq!(loaded.transition_count, saved.transition_count);
    assert_eq!(loaded.latest_state_hash, saved.latest_state_hash);

    for _ in 2..INTERACTIVE_TURN_COUNT {
      let original_next = original
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: String::new(),
        })
        .expect("original stabilization continuation");
      let restarted_next = restarted
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: String::new(),
        })
        .expect("restarted stabilization continuation");
      assert_eq!(
        restarted_next
          .latest_transition
          .map(|transition| transition.state_hash),
        original_next
          .latest_transition
          .map(|transition| transition.state_hash)
      );
    }

    let original_history = original
      .get_history(GetHistoryRequest {
        session_id: session_id.clone(),
      })
      .expect("original stabilization history");
    let restarted_history = restarted
      .get_history(GetHistoryRequest {
        session_id: session_id.clone(),
      })
      .expect("restarted stabilization history");
    assert_eq!(restarted_history, original_history);
    assert_eq!(restarted_history.transition_count, 5);

    let original_replay = original
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("original stabilization replay");
    let restarted_replay = restarted
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("restarted stabilization replay");
    assert_eq!(restarted_replay, original_replay);
    assert_eq!(restarted_replay.transition_count, 5);

    let original_coverage = original
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("original stabilization coverage");
    let restarted_coverage = restarted
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("restarted stabilization coverage");
    assert_eq!(restarted_coverage, original_coverage);
    assert!(restarted_coverage.session.done);

    restarted
      .end_session(EndSessionRequest { session_id })
      .expect("end recovered full stabilization session");
    assert!(!path.exists());
  }

  #[test]
  fn durable_stabilization_checkpoint_does_not_overwrite_live_session() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-stabilization-collision-{}.save",
      std::process::id()
    ));
    let mut original = GameSessionStore::with_competitive_persistence(path.clone());
    let original_session = start(&mut original, "stabilization-v1");
    let original_id = original_session.session_id.clone();
    original
      .submit_turn(SubmitTurnRequest {
        session_id: original_id.clone(),
        command_text: String::new(),
      })
      .expect("first stage");
    original
      .save_session(SaveSessionRequest {
        session_id: original_id.clone(),
      })
      .expect("durable save");

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let live = start(&mut restarted, "stabilization-v1");
    assert_eq!(live.session_id, original_id);
    let error = restarted
      .load_session(LoadSessionRequest {
        session_id: live.session_id.clone(),
      })
      .expect_err("a live colliding session must not be overwritten");
    assert_eq!(error.code.as_deref(), Some("checkpoint_missing"));
    let replay = restarted
      .get_replay(GetReplayRequest {
        session_id: live.session_id.clone(),
      })
      .expect("live session remains available");
    assert_eq!(replay.transition_count, 0);
    restarted
      .end_session(EndSessionRequest {
        session_id: live.session_id,
      })
      .expect("end colliding live session");
    assert!(path.is_file(), "unclaimed durable checkpoint must remain");
    let _ = std::fs::remove_file(path);
  }

  #[test]
  fn durable_affiliation_checkpoint_recovers_across_store_restart() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-affiliation-{}.save",
      std::process::id()
    ));
    let mut store = GameSessionStore::with_competitive_persistence(path.clone());
    let session = start(&mut store, "regional-affiliation-v1");
    let session_id = session.session_id.clone();
    let first = store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "assess".to_string(),
      })
      .expect("assessment stage");
    let saved = store
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable affiliation save");
    assert_eq!(saved.transition_count, 1);
    assert!(path.is_file());

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let loaded = restarted
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable affiliation load");
    assert_eq!(loaded.transition_count, saved.transition_count);
    assert_eq!(loaded.latest_state_hash, saved.latest_state_hash);
    let coverage = restarted
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("restored affiliation coverage");
    assert_eq!(coverage.stage.id, "chooseposture");

    let original_next = store
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "posture choice=independent".to_string(),
      })
      .expect("original continuation");
    let restarted_next = restarted
      .submit_turn(SubmitTurnRequest {
        session_id: session_id.clone(),
        command_text: "posture choice=independent".to_string(),
      })
      .expect("restarted continuation");
    assert_eq!(
      restarted_next
        .latest_transition
        .map(|transition| transition.state_hash),
      original_next
        .latest_transition
        .map(|transition| transition.state_hash)
    );

    restarted
      .end_session(EndSessionRequest { session_id })
      .expect("end recovered affiliation session");
    assert!(!path.exists());
    let _ = first;
  }

  #[test]
  fn durable_affiliation_checkpoint_covers_full_campaign_continuation() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-full-affiliation-{}.save",
      std::process::id()
    ));
    let mut original = GameSessionStore::with_competitive_persistence(path.clone());
    let session = start(&mut original, "regional-affiliation-v1");
    let session_id = session.session_id.clone();
    for command_text in ["assess", "posture choice=independent", "hold"] {
      original
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: command_text.to_string(),
        })
        .expect("affiliation stage before checkpoint");
    }
    let saved = original
      .save_session(SaveSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable affiliation stage-three save");
    assert_eq!(saved.transition_count, 3);
    assert!(path.is_file());

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let loaded = restarted
      .load_session(LoadSessionRequest {
        session_id: session_id.clone(),
      })
      .expect("durable affiliation stage-three load");
    assert_eq!(loaded.transition_count, saved.transition_count);
    assert_eq!(loaded.latest_state_hash, saved.latest_state_hash);

    for _ in 3..AFFILIATION_TURN_COUNT {
      let original_next = original
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("original affiliation continuation");
      let restarted_next = restarted
        .submit_turn(SubmitTurnRequest {
          session_id: session_id.clone(),
          command_text: "hold".to_string(),
        })
        .expect("restarted affiliation continuation");
      assert_eq!(
        restarted_next
          .latest_transition
          .map(|transition| transition.state_hash),
        original_next
          .latest_transition
          .map(|transition| transition.state_hash)
      );
    }

    let original_history = original
      .get_history(GetHistoryRequest {
        session_id: session_id.clone(),
      })
      .expect("original affiliation history");
    let restarted_history = restarted
      .get_history(GetHistoryRequest {
        session_id: session_id.clone(),
      })
      .expect("restarted affiliation history");
    assert_eq!(restarted_history, original_history);
    assert_eq!(restarted_history.transition_count, 6);

    let original_replay = original
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("original affiliation replay");
    let restarted_replay = restarted
      .get_replay(GetReplayRequest {
        session_id: session_id.clone(),
      })
      .expect("restarted affiliation replay");
    assert_eq!(restarted_replay, original_replay);
    assert_eq!(restarted_replay.transition_count, 6);

    let original_coverage = original
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("original affiliation coverage");
    let restarted_coverage = restarted
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session_id.clone(),
      })
      .expect("restarted affiliation coverage");
    assert_eq!(restarted_coverage, original_coverage);
    assert!(restarted_coverage.session.done);

    restarted
      .end_session(EndSessionRequest { session_id })
      .expect("end recovered full affiliation session");
    assert!(!path.exists());
  }

  #[test]
  fn durable_checkpoint_replacement_preserves_cross_campaign_identity() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-cross-campaign-{}.save",
      std::process::id()
    ));
    let mut writer = GameSessionStore::with_competitive_persistence(path.clone());
    let competitive = start(&mut writer, "competitive-regional-v1");
    let competitive_id = competitive.session_id.clone();
    writer
      .submit_turn(SubmitTurnRequest {
        session_id: competitive_id.clone(),
        command_text: String::new(),
      })
      .expect("competitive checkpoint transition");
    let competitive_saved = writer
      .save_session(SaveSessionRequest {
        session_id: competitive_id.clone(),
      })
      .expect("competitive checkpoint");
    assert_eq!(competitive_saved.campaign, "competitive-regional-v1");

    let stabilization = start(&mut writer, "stabilization-v1");
    let stabilization_id = stabilization.session_id.clone();
    writer
      .submit_turn(SubmitTurnRequest {
        session_id: stabilization_id.clone(),
        command_text: String::new(),
      })
      .expect("stabilization checkpoint transition");
    let stabilization_saved = writer
      .save_session(SaveSessionRequest {
        session_id: stabilization_id.clone(),
      })
      .expect("stabilization checkpoint replacement");
    assert_eq!(stabilization_saved.campaign, "stabilization-v1");

    let mut stabilization_host = GameSessionStore::with_competitive_persistence(path.clone());
    let competitive_live = start(&mut stabilization_host, "competitive-regional-v1");
    assert_eq!(competitive_live.session_id, competitive_id);
    let replaced_competitive = stabilization_host
      .load_session(LoadSessionRequest {
        session_id: competitive_id.clone(),
      })
      .expect_err("replaced competitive checkpoint must not hydrate");
    assert_eq!(
      replaced_competitive.code.as_deref(),
      Some("checkpoint_missing")
    );
    stabilization_host
      .end_session(EndSessionRequest {
        session_id: competitive_id.clone(),
      })
      .expect("end competitive placeholder");

    let stabilization_live = start(&mut stabilization_host, "stabilization-v1");
    assert_eq!(stabilization_live.session_id, stabilization_id);
    stabilization_host
      .end_session(EndSessionRequest {
        session_id: stabilization_id.clone(),
      })
      .expect("end stabilization placeholder before hydration");
    let loaded_stabilization = stabilization_host
      .load_session(LoadSessionRequest {
        session_id: stabilization_id.clone(),
      })
      .expect("latest stabilization checkpoint must hydrate");
    assert_eq!(loaded_stabilization.campaign, "stabilization-v1");
    assert_eq!(loaded_stabilization.transition_count, 1);

    let affiliation = start(&mut stabilization_host, "regional-affiliation-v1");
    let affiliation_id = affiliation.session_id.clone();
    stabilization_host
      .submit_turn(SubmitTurnRequest {
        session_id: affiliation_id.clone(),
        command_text: "assess".to_string(),
      })
      .expect("affiliation checkpoint transition");
    let affiliation_saved = stabilization_host
      .save_session(SaveSessionRequest {
        session_id: affiliation_id.clone(),
      })
      .expect("affiliation checkpoint replacement");
    assert_eq!(affiliation_saved.campaign, "regional-affiliation-v1");

    let mut affiliation_host = GameSessionStore::with_competitive_persistence(path.clone());
    let competitive_placeholder = start(&mut affiliation_host, "competitive-regional-v1");
    assert_eq!(competitive_placeholder.session_id, competitive_id);
    let stabilization_placeholder = start(&mut affiliation_host, "stabilization-v1");
    assert_eq!(stabilization_placeholder.session_id, stabilization_id);
    let replaced_stabilization = affiliation_host
      .load_session(LoadSessionRequest {
        session_id: stabilization_id.clone(),
      })
      .expect_err("replaced stabilization checkpoint must not hydrate");
    assert_eq!(
      replaced_stabilization.code.as_deref(),
      Some("checkpoint_missing")
    );
    affiliation_host
      .end_session(EndSessionRequest {
        session_id: stabilization_id,
      })
      .expect("end stabilization placeholder");

    let affiliation_placeholder = start(&mut affiliation_host, "regional-affiliation-v1");
    assert_eq!(affiliation_placeholder.session_id, affiliation_id);
    affiliation_host
      .end_session(EndSessionRequest {
        session_id: affiliation_id.clone(),
      })
      .expect("end affiliation placeholder before hydration");
    let loaded_affiliation = affiliation_host
      .load_session(LoadSessionRequest {
        session_id: affiliation_id.clone(),
      })
      .expect("latest affiliation checkpoint must hydrate");
    assert_eq!(loaded_affiliation.campaign, "regional-affiliation-v1");
    assert_eq!(loaded_affiliation.transition_count, 1);

    affiliation_host
      .end_session(EndSessionRequest {
        session_id: affiliation_id,
      })
      .expect("end latest recovered campaign");
    assert!(!path.exists());
  }

  #[test]
  fn durable_affiliation_checkpoint_does_not_overwrite_live_session() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-durable-affiliation-collision-{}.save",
      std::process::id()
    ));
    let mut original = GameSessionStore::with_competitive_persistence(path.clone());
    let original_session = start(&mut original, "regional-affiliation-v1");
    let original_id = original_session.session_id.clone();
    original
      .submit_turn(SubmitTurnRequest {
        session_id: original_id.clone(),
        command_text: "assess".to_string(),
      })
      .expect("assessment stage");
    original
      .save_session(SaveSessionRequest {
        session_id: original_id.clone(),
      })
      .expect("durable save");

    let mut restarted = GameSessionStore::with_competitive_persistence(path.clone());
    let live = start(&mut restarted, "regional-affiliation-v1");
    assert_eq!(live.session_id, original_id);
    let error = restarted
      .load_session(LoadSessionRequest {
        session_id: live.session_id.clone(),
      })
      .expect_err("a live colliding session must not be overwritten");
    assert_eq!(error.code.as_deref(), Some("checkpoint_missing"));
    let replay = restarted
      .get_replay(GetReplayRequest {
        session_id: live.session_id.clone(),
      })
      .expect("live session remains available");
    assert_eq!(replay.transition_count, 0);
    restarted
      .end_session(EndSessionRequest {
        session_id: live.session_id,
      })
      .expect("end colliding live session");
    assert!(path.is_file(), "unclaimed durable checkpoint must remain");
    let _ = std::fs::remove_file(path);
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
  fn competitive_end_session_keeps_history_replay_and_debrief_aligned() {
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
        session_id: session.session_id.clone(),
      })
      .expect("end session");

    assert_eq!(ended.schema_version, END_SESSION_SCHEMA_VERSION);
    assert!(ended.done);
    assert_eq!(ended.history.len(), ended.replay.transition_count);
    assert_eq!(ended.history.len(), 1);
    assert_eq!(
      ended.history.last().map(|entry| &entry.state_hash),
      ended.replay.latest_state_hash.as_ref()
    );
    assert!(!ended.debrief.is_empty());
    assert!(
      store
        .get_history(GetHistoryRequest {
          session_id: session.session_id,
        })
        .is_err()
    );
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
    assert_eq!(
      stabilization_coverage
        .audio
        .as_ref()
        .expect("stabilization campaign audio")
        .music_state_id,
      "stable_operations"
    );
    assert!(
      stabilization_coverage
        .audio
        .as_ref()
        .expect("stabilization campaign audio")
        .audio_cue_ids
        .is_empty()
    );
    assert_eq!(stabilization_before, stabilization_after);

    let stabilization_committed = start(&mut store, "stabilization-v1");
    let stabilization_committed = store
      .submit_turn(SubmitTurnRequest {
        session_id: stabilization_committed.session_id,
        command_text: "8 18 112".to_string(),
      })
      .expect("stabilization transition");
    let stabilization_history = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: stabilization_committed.session_id,
      })
      .expect("stabilization committed coverage")
      .history;
    assert_eq!(stabilization_history.len(), 1);
    assert_eq!(
      stabilization_history[0]
        .observation
        .as_ref()
        .expect("stabilization decision observation")[0],
      "Turn 1"
    );

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
    assert_eq!(
      affiliation_coverage
        .audio
        .as_ref()
        .expect("affiliation campaign audio")
        .music_state_id,
      "affiliation_negotiation"
    );
    assert!(
      affiliation_coverage
        .audio
        .as_ref()
        .expect("affiliation campaign audio")
        .audio_cue_ids
        .is_empty()
    );
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

    let affiliation_committed = start(&mut store, "regional-affiliation-v1");
    let affiliation_committed = store
      .submit_turn(SubmitTurnRequest {
        session_id: affiliation_committed.session_id,
        command_text: "assess".to_string(),
      })
      .expect("affiliation transition");
    let affiliation_history = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: affiliation_committed.session_id,
      })
      .expect("affiliation committed coverage")
      .history;
    assert_eq!(affiliation_history.len(), 1);
    assert!(
      affiliation_history[0]
        .observation
        .as_ref()
        .expect("affiliation decision observation")[0]
        .starts_with("Stage 1:")
    );
    let mut legacy_transition_value =
      serde_json::to_value(&stabilization_history[0]).expect("transition summary value");
    legacy_transition_value
      .as_object_mut()
      .expect("transition summary object")
      .remove("observation");
    let legacy_transition: TransitionSummary =
      serde_json::from_value(legacy_transition_value).expect("legacy transition summary");
    assert!(legacy_transition.observation.is_none());

    let competitive = start(&mut store, "competitive-regional-v1");
    let competitive = store
      .submit_turn(SubmitTurnRequest {
        session_id: competitive.session_id,
        command_text: "hold".to_string(),
      })
      .expect("competitive transition");
    let competitive_json =
      serde_json::to_value(competitive.latest_transition.expect("competitive summary"))
        .expect("competitive summary value");
    assert!(
      !competitive_json
        .as_object()
        .expect("competitive summary object")
        .contains_key("observation")
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

    let mut legacy_value = serde_json::to_value(&stabilization_coverage).expect("coverage value");
    legacy_value
      .as_object_mut()
      .expect("coverage object")
      .remove("audio");
    let legacy: crate::mcp::campaign_coverage::CampaignCoverageEnvelope =
      serde_json::from_value(legacy_value).expect("legacy campaign coverage without audio");
    assert!(legacy.audio.is_none());

    let competitive = start(&mut store, "competitive-regional-v1");
    let competitive_before = store
      .get_observation(GetObservationRequest {
        session_id: competitive.session_id.clone(),
      })
      .expect("competitive before coverage");
    let competitive_coverage = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: competitive.session_id.clone(),
      })
      .expect("competitive coverage");
    assert_eq!(
      competitive_coverage.session.campaign,
      "competitive-regional-v1"
    );
    assert_eq!(
      competitive_coverage.session.max_turns,
      COMPETITIVE_MONTH_LIMIT
    );
    assert_eq!(competitive_coverage.stage.id, "month-1");
    assert_eq!(competitive_coverage.decisions.len(), 7);
    assert_eq!(
      competitive_coverage
        .audio
        .as_ref()
        .expect("competitive campaign audio")
        .music_state_id,
      "competitive_escalation"
    );
    assert!(
      competitive_coverage
        .decisions
        .iter()
        .any(|decision| decision.id == "monitor")
    );
    assert!(
      competitive_coverage
        .actors
        .iter()
        .any(|actor| actor.id == "regional-rivals")
    );
    assert!(
      competitive_coverage
        .processes
        .iter()
        .any(|process| process.id == "information-gaps")
    );
    assert!(
      competitive_coverage
        .metrics
        .iter()
        .any(|metric| metric.label == "Operating margin")
    );
    let competitive_json =
      serde_json::to_string(&competitive_coverage).expect("competitive coverage json");
    for forbidden in [
      "CompetitiveWorldState",
      "WorldState",
      "ResolvedInputs",
      "resolved_inputs",
      "effect_queue",
    ] {
      assert!(!competitive_json.contains(forbidden), "found {forbidden}");
    }
    let competitive_after = store
      .get_observation(GetObservationRequest {
        session_id: competitive.session_id,
      })
      .expect("competitive after coverage");
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
    assert_eq!(coverage.session.turn, 6);
    assert!(coverage.decisions.is_empty());
    assert!(
      coverage
        .debrief
        .iter()
        .any(|line| line.contains("Regional affiliation debrief"))
    );
  }

  #[test]
  fn campaign_coverage_audio_state_covers_all_full_campaign_reads() {
    let allowed_music_states = [
      "menu",
      "stable_operations",
      "pressure",
      "regulatory_scrutiny",
      "competitive_escalation",
      "affiliation_negotiation",
      "debrief",
    ];
    let allowed_audio_cues = [
      "event.project-complete",
      "event.staffing-constraint",
      "event.operating-loss",
      "event.operating-recovery",
      "event.payer-decision",
      "event.regulatory-decision",
      "event.rival-expansion",
      "event.affiliation-milestone",
    ];
    let assert_audio_state = |coverage: crate::mcp::campaign_coverage::CampaignCoverageEnvelope,
                              terminal: bool| {
      assert_eq!(coverage.schema_version, "campaign-coverage-v1");
      let audio = coverage.audio.expect("campaign coverage audio");
      assert!(
        allowed_music_states.contains(&audio.music_state_id.as_str()),
        "unexpected music state {}",
        audio.music_state_id
      );
      for cue_id in &audio.audio_cue_ids {
        assert!(
          allowed_audio_cues.contains(&cue_id.as_str()),
          "unexpected audio cue {cue_id}"
        );
      }
      if terminal {
        assert!(coverage.session.done);
        assert_eq!(audio.music_state_id, "debrief");
        assert!(!coverage.debrief.is_empty());
      } else {
        assert!(!coverage.session.done);
      }
    };

    let mut store = GameSessionStore::default();
    let mut competitive = start(&mut store, "competitive-regional-v1");
    assert_audio_state(
      store
        .get_campaign_coverage(GetCampaignCoverageRequest {
          session_id: competitive.session_id.clone(),
        })
        .expect("competitive genesis coverage"),
      false,
    );
    for month in 0..COMPETITIVE_MONTH_LIMIT {
      competitive = store
        .submit_turn(SubmitTurnRequest {
          session_id: competitive.session_id,
          command_text: String::new(),
        })
        .expect("competitive month");
      assert_audio_state(
        store
          .get_campaign_coverage(GetCampaignCoverageRequest {
            session_id: competitive.session_id.clone(),
          })
          .expect("competitive campaign coverage"),
        month + 1 == COMPETITIVE_MONTH_LIMIT,
      );
    }

    let mut stabilization = start(&mut store, "stabilization-v1");
    assert_audio_state(
      store
        .get_campaign_coverage(GetCampaignCoverageRequest {
          session_id: stabilization.session_id.clone(),
        })
        .expect("stabilization genesis coverage"),
      false,
    );
    for stage in 0..INTERACTIVE_TURN_COUNT {
      stabilization = store
        .submit_turn(SubmitTurnRequest {
          session_id: stabilization.session_id,
          command_text: String::new(),
        })
        .expect("stabilization stage");
      assert_audio_state(
        store
          .get_campaign_coverage(GetCampaignCoverageRequest {
            session_id: stabilization.session_id.clone(),
          })
          .expect("stabilization campaign coverage"),
        stage + 1 == INTERACTIVE_TURN_COUNT,
      );
    }

    let mut affiliation = start(&mut store, "regional-affiliation-v1");
    let affiliation_commands = [
      "assess",
      "posture choice=independent",
      "hold",
      "hold",
      "hold",
      "hold",
    ];
    assert_audio_state(
      store
        .get_campaign_coverage(GetCampaignCoverageRequest {
          session_id: affiliation.session_id.clone(),
        })
        .expect("affiliation genesis coverage"),
      false,
    );
    for (stage, command) in affiliation_commands.into_iter().enumerate() {
      affiliation = store
        .submit_turn(SubmitTurnRequest {
          session_id: affiliation.session_id,
          command_text: command.to_string(),
        })
        .expect("affiliation stage");
      assert_audio_state(
        store
          .get_campaign_coverage(GetCampaignCoverageRequest {
            session_id: affiliation.session_id.clone(),
          })
          .expect("affiliation campaign coverage"),
        stage + 1 == AFFILIATION_TURN_COUNT as usize,
      );
    }
  }

  #[test]
  fn full_campaign_history_and_replay_reads_remain_hash_aligned() {
    let assert_alignment =
      |store: &GameSessionStore, session_id: &str, expected_count: usize, terminal: bool| {
        let before = store
          .get_observation(GetObservationRequest {
            session_id: session_id.to_string(),
          })
          .expect("observation before history/replay read");
        let history = store
          .get_history(GetHistoryRequest {
            session_id: session_id.to_string(),
          })
          .expect("history read");
        let replay = store
          .get_replay(GetReplayRequest {
            session_id: session_id.to_string(),
          })
          .expect("replay read");
        let after = store
          .get_observation(GetObservationRequest {
            session_id: session_id.to_string(),
          })
          .expect("observation after history/replay read");

        assert_eq!(before, after);
        assert_eq!(before.done, terminal);
        assert_eq!(history.schema_version, HISTORY_SCHEMA_VERSION);
        assert_eq!(replay.schema_version, REPLAY_SCHEMA_VERSION);
        assert_eq!(history.session_id, session_id);
        assert_eq!(replay.session_id, session_id);
        assert_eq!(history.transition_count, expected_count);
        assert_eq!(replay.transition_count, expected_count);
        assert_eq!(history.transitions, replay.transitions);
        assert_eq!(
          replay.latest_state_hash,
          history
            .transitions
            .last()
            .map(|transition| transition.state_hash.clone())
        );
      };

    let mut store = GameSessionStore::default();
    let mut competitive = start(&mut store, "competitive-regional-v1");
    assert_alignment(&store, &competitive.session_id, 0, false);
    for month in 0..COMPETITIVE_MONTH_LIMIT {
      competitive = store
        .submit_turn(SubmitTurnRequest {
          session_id: competitive.session_id,
          command_text: String::new(),
        })
        .expect("competitive month");
      assert_alignment(
        &store,
        &competitive.session_id,
        month as usize + 1,
        month + 1 == COMPETITIVE_MONTH_LIMIT,
      );
    }

    let mut stabilization = start(&mut store, "stabilization-v1");
    assert_alignment(&store, &stabilization.session_id, 0, false);
    for stage in 0..INTERACTIVE_TURN_COUNT {
      stabilization = store
        .submit_turn(SubmitTurnRequest {
          session_id: stabilization.session_id,
          command_text: String::new(),
        })
        .expect("stabilization stage");
      assert_alignment(
        &store,
        &stabilization.session_id,
        stage as usize + 1,
        stage + 1 == INTERACTIVE_TURN_COUNT,
      );
    }

    let mut affiliation = start(&mut store, "regional-affiliation-v1");
    assert_alignment(&store, &affiliation.session_id, 0, false);
    let affiliation_commands = [
      "assess",
      "posture choice=independent",
      "hold",
      "hold",
      "hold",
      "hold",
    ];
    for (stage, command) in affiliation_commands.into_iter().enumerate() {
      affiliation = store
        .submit_turn(SubmitTurnRequest {
          session_id: affiliation.session_id,
          command_text: command.to_string(),
        })
        .expect("affiliation stage");
      assert_alignment(
        &store,
        &affiliation.session_id,
        stage + 1,
        stage + 1 == AFFILIATION_TURN_COUNT as usize,
      );
    }
  }

  #[test]
  fn competitive_campaign_coverage_sanitizes_private_rival_actions() {
    let ruleset = default_competitive_ruleset();
    let genesis =
      crate::competitive::genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let month_index = genesis.policy_calendar.month_index;
    let transition = crate::competitive::regenerate_competitive_month(
      &genesis,
      &ruleset,
      42,
      AggregatedMonthlyActions {
        month_index,
        batches: vec![
          SystemMonthlyBatch::new(0, vec![CompetitiveCommand::Hold]),
          SystemMonthlyBatch::new(
            1,
            vec![CompetitiveCommand::Monitor {
              target: crate::model::MonitorTarget::Northlake,
              depth: 2,
            }],
          ),
        ],
      },
      None,
    )
    .expect("private rival transition");

    let raw_summary = summarize_competitive_transition(&transition);
    assert!(
      raw_summary
        .events
        .iter()
        .any(|event| event.contains("Northlake Health: monitoring"))
    );

    let coverage_summary = summarize_competitive_campaign_coverage_transition(&transition);
    assert!(coverage_summary.events.is_empty());
    assert!(coverage_summary.effects.is_empty());
  }

  #[test]
  fn campaign_coverage_terminal_competitive_includes_debrief_without_decisions() {
    let mut store = GameSessionStore::default();
    let mut session = start(&mut store, "competitive-regional-v1");
    for _ in 0..COMPETITIVE_MONTH_LIMIT {
      session = store
        .submit_turn(SubmitTurnRequest {
          session_id: session.session_id,
          command_text: "hold".to_string(),
        })
        .expect("competitive month");
    }
    let coverage = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: session.session_id,
      })
      .expect("terminal competitive coverage");
    assert!(coverage.session.done);
    assert_eq!(coverage.session.turn, COMPETITIVE_MONTH_LIMIT);
    assert!(coverage.decisions.is_empty());
    assert!(coverage.stage.label.contains("complete"));
    let debrief = coverage.debrief.join("\n");
    assert!(debrief.contains("Final player tradeoff:"));
    for forbidden in [
      "INSTRUCTOR RUN SUMMARY",
      "DISTRIBUTIONAL OUTCOME SUMMARY",
      "REVEALED FOR INSTRUCTOR REVIEW",
      "unobserved during play",
      "Rival values",
      "Rival Northlake",
      "Rival Summit",
      "Rival Valley",
      "Rival Metro",
    ] {
      assert!(!debrief.contains(forbidden), "found {forbidden}");
    }
    assert!(
      coverage
        .debrief
        .iter()
        .any(|line| line.contains("Competitive preview completed"))
    );
  }

  #[test]
  fn campaign_coverage_terminal_stabilization_has_debrief_without_decisions() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "stabilization-v1");
    let commands = ["1 1 0", "0 1", "1 1", "1 1", "1 1"];
    let mut current = session;
    for command in commands {
      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id,
          command_text: command.to_string(),
        })
        .expect("stabilization stage");
    }
    let coverage = store
      .get_campaign_coverage(GetCampaignCoverageRequest {
        session_id: current.session_id,
      })
      .expect("terminal stabilization coverage");
    assert!(coverage.session.done);
    assert_eq!(coverage.session.turn, 5);
    assert!(coverage.decisions.is_empty());
    assert!(!coverage.debrief.is_empty());
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
    assert!(
      [
        "debrief",
        "regulatory_scrutiny",
        "affiliation_negotiation",
        "competitive_escalation",
        "pressure",
        "stable_operations",
      ]
      .contains(&resolution.music_state_id.as_str())
    );
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
  fn regional_world_facility_projection_covers_all_competitive_months() {
    let mut store = GameSessionStore::default();
    let session = start(&mut store, "competitive-regional-v1");
    let expected_components = [
      "general-hospital-base",
      "ambulatory-center",
      "emergency-department",
      "specialty-center",
    ];
    let expected_metrics = [
      "Staffed beds",
      "Outpatient capacity",
      "Emergency",
      "ICU",
      "Obstetrics",
      "Psychiatric",
      "Cardiology",
      "Oncology",
      "Infusion",
      "Neurology",
      "ASC",
    ];
    let mut current = session;

    for month in 1..=COMPETITIVE_MONTH_LIMIT {
      let world = store
        .get_regional_world(GetRegionalWorldRequest {
          session_id: current.session_id.clone(),
        })
        .expect("regional world during competitive month");
      assert_eq!(world.session.turn, month);
      assert!(!world.session.done);
      let owned = world
        .entities
        .iter()
        .find(|entity| entity.visibility == "owned")
        .expect("owned facility entity");
      assert_eq!(
        owned
          .facilities
          .iter()
          .map(|facility| facility.component_id.as_str())
          .collect::<Vec<_>>(),
        expected_components
      );
      assert!(
        owned
          .facilities
          .iter()
          .all(|facility| facility.source == "PlayerObservation capacity fields")
      );
      assert_eq!(
        owned
          .facilities
          .iter()
          .flat_map(|facility| facility.metrics.iter())
          .map(|metric| metric.label.as_str())
          .collect::<Vec<_>>(),
        expected_metrics
      );
      assert!(
        world
          .entities
          .iter()
          .filter(|entity| entity.visibility == "public identity")
          .all(|entity| entity.facilities.is_empty())
      );

      current = store
        .submit_turn(SubmitTurnRequest {
          session_id: current.session_id,
          command_text: "hold".to_string(),
        })
        .expect("competitive month");
    }

    let terminal = store
      .get_regional_world(GetRegionalWorldRequest {
        session_id: current.session_id,
      })
      .expect("terminal regional world");
    assert!(terminal.session.done);
    assert_eq!(terminal.session.turn, COMPETITIVE_MONTH_LIMIT);
    assert_eq!(
      terminal.replay.transition_count,
      COMPETITIVE_MONTH_LIMIT as usize
    );
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
