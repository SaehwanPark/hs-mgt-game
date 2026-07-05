use std::collections::{HashMap, HashSet};
use std::fmt;
use std::fs;
use std::path::Path;

use serde::Deserialize;

use crate::model::{
  AiProfile, AiStyleWeights, CompetitiveRuleset, CompetitiveWorldState, Difficulty,
  HealthSystemState, INTERACTIVE_TURN_COUNT, PlayerController, PlayerResources, PlayerSlot,
  PolicyCalendar, Ruleset, SharedMarketFields, WorldState,
};

pub const SCENARIO_TOML_FORMAT_VERSION: &str = "scenario-toml-0.1.40";
pub const STABILIZATION_SCENARIO_TOML: &str = include_str!("../../scenarios/stabilization-v1.toml");

use std::sync::{Mutex, OnceLock};

static NAME_INTERNER: OnceLock<Mutex<HashSet<&'static str>>> = OnceLock::new();

fn intern_string(s: &str) -> &'static str {
  let cache_mutex = NAME_INTERNER.get_or_init(|| Mutex::new(HashSet::new()));
  let mut cache = cache_mutex.lock().unwrap();
  if let Some(&static_str) = cache.get(s) {
    static_str
  } else {
    let leaked = Box::leak(s.to_string().into_boxed_str());
    cache.insert(leaked);
    leaked
  }
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Scenario {
  pub format_version: String,
  pub campaign_id: String,
  pub scenario_id: String,
  pub scenario_version: String,
  pub turn_unit: String,
  pub ruleset_id: String,
  pub title: String,
  pub default_seed: u64,
  pub learning_objectives: Vec<String>,
  pub initial_state: Option<ScenarioInitialState>,
  pub turn_schedule: Option<Vec<TurnScheduleEntry>>,
  pub actor_stubs: Option<Vec<ActorStub>>,
  pub evaluation_profile: Option<EvaluationProfile>,
  pub initial_market: Option<ScenarioMarketState>,
  pub systems: Option<Vec<ScenarioSystemState>>,
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ScenarioMarketState {
  pub regional_demand_index: i32,
  pub commercial_payer_pressure: i32,
  pub policy_pressure: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ScenarioSystemState {
  pub system_id: u32,
  pub name: String,
  pub staffed_beds: i32,
  pub outpatient_capacity: i32,
  pub emergency_capacity: Option<i32>,
  pub icu_capacity: Option<i32>,
  pub nurses: i32,
  pub physicians: i32,
  pub admins: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub workforce_trust: i32,
  pub community_trust: i32,
  pub market_share_index: i32,
  pub cash: i32,
  pub political_capital: u32,
  pub controller: String,
  pub ai_style: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ScenarioInitialState {
  pub turn: u32,
  pub cash: i32,
  pub staffed_beds: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub workforce_trust: i32,
  pub community_trust: i32,
  pub commercial_rate: i32,
  pub policy_pressure: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TurnScheduleEntry {
  pub turn: u32,
  pub command_kind: String,
  pub briefing_context: String,
  pub actor_stub: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ActorStub {
  pub id: String,
  pub card_ref: String,
  pub turn: u32,
}

#[derive(Clone, Debug, PartialEq, Eq, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct EvaluationProfile {
  pub debrief_prompt: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ScenarioError {
  Io(String),
  Parse(String),
  UnsupportedFormatVersion(String),
  UnsupportedCampaign(String),
  UnsupportedTurnUnit(String),
  RulesetMismatch { expected: String, actual: String },
  InvalidInitialTurn(u32),
  EmptyLearningObjectives,
  InvalidTurnSchedule(String),
  InvalidActorStub(String),
  InvalidSystem(String),
}

impl fmt::Display for ScenarioError {
  fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
    match self {
      ScenarioError::Io(message) => write!(f, "could not read scenario: {message}"),
      ScenarioError::Parse(message) => write!(f, "could not parse scenario TOML: {message}"),
      ScenarioError::UnsupportedFormatVersion(version) => {
        write!(f, "unsupported scenario format '{version}'")
      }
      ScenarioError::UnsupportedCampaign(campaign) => {
        write!(f, "unsupported scenario campaign '{campaign}'")
      }
      ScenarioError::UnsupportedTurnUnit(turn_unit) => {
        write!(f, "unsupported scenario turn unit '{turn_unit}'")
      }
      ScenarioError::RulesetMismatch { expected, actual } => {
        write!(f, "scenario ruleset '{actual}' does not match '{expected}'")
      }
      ScenarioError::InvalidInitialTurn(turn) => {
        write!(f, "stabilization scenario must start at turn 0, got {turn}")
      }
      ScenarioError::EmptyLearningObjectives => {
        write!(f, "scenario must include at least one learning objective")
      }
      ScenarioError::InvalidTurnSchedule(message) => write!(f, "invalid turn schedule: {message}"),
      ScenarioError::InvalidActorStub(message) => write!(f, "invalid actor stub: {message}"),
      ScenarioError::InvalidSystem(message) => write!(f, "invalid system configuration: {message}"),
    }
  }
}

impl std::error::Error for ScenarioError {}

impl ScenarioInitialState {
  pub fn to_world_state(&self) -> WorldState {
    WorldState {
      turn: self.turn,
      cash: self.cash,
      staffed_beds: self.staffed_beds,
      access_index: self.access_index,
      quality_index: self.quality_index,
      workforce_trust: self.workforce_trust,
      community_trust: self.community_trust,
      commercial_rate: self.commercial_rate,
      policy_pressure: self.policy_pressure,
    }
  }
}

impl Scenario {
  pub fn initial_world_state(&self) -> WorldState {
    self
      .initial_state
      .as_ref()
      .expect("initial_state must be present for stabilization")
      .to_world_state()
  }

  pub fn initial_competitive_world_state(
    &self,
    difficulty: Difficulty,
    _ruleset: &CompetitiveRuleset,
  ) -> Result<CompetitiveWorldState, ScenarioError> {
    let market_spec = self.initial_market.as_ref().ok_or_else(|| {
      ScenarioError::Parse("missing initial_market in competitive scenario".to_string())
    })?;

    let systems_spec = self
      .systems
      .as_ref()
      .ok_or_else(|| ScenarioError::Parse("missing systems in competitive scenario".to_string()))?;

    let mut systems = Vec::with_capacity(systems_spec.len());
    let mut players = Vec::with_capacity(systems_spec.len());

    for sys in systems_spec {
      let controller = match sys.controller.to_ascii_lowercase().as_str() {
        "human" => PlayerController::Human,
        "ai" => {
          let style_str = sys.ai_style.as_deref().ok_or_else(|| {
            ScenarioError::Parse(format!("missing ai_style for AI system '{}'", sys.name))
          })?;
          let style = match style_str.to_ascii_lowercase().as_str() {
            "growth" => AiStyleWeights::growth_focused(),
            "margin" => AiStyleWeights::margin_focused(),
            "access" => AiStyleWeights::access_focused(),
            "political" => AiStyleWeights::political_focused(),
            _ => {
              return Err(ScenarioError::Parse(format!(
                "invalid ai_style '{}' for system '{}'",
                style_str, sys.name
              )));
            }
          };
          PlayerController::Ai(AiProfile {
            org_name: intern_string(&sys.name),
            style,
          })
        }
        other => {
          return Err(ScenarioError::Parse(format!(
            "invalid controller '{}' for system '{}'",
            other, sys.name
          )));
        }
      };

      let ap_budget = if let PlayerController::Human = controller {
        difficulty.human_ap_per_month()
      } else {
        difficulty.cpu_ap_per_month()
      };

      let resources = PlayerResources {
        cash: sys.cash,
        political_capital: sys.political_capital,
        ap_budget,
        active_projects: 0,
        active_project_monthly_draws: 0,
      };

      systems.push(HealthSystemState {
        system_id: sys.system_id,
        name: sys.name.clone(),
        staffed_beds: sys.staffed_beds,
        outpatient_capacity: sys.outpatient_capacity,
        emergency_capacity: sys.emergency_capacity.unwrap_or(0),
        icu_capacity: sys.icu_capacity.unwrap_or(0),
        nurses: sys.nurses,
        physicians: sys.physicians,
        admins: sys.admins,
        access_index: sys.access_index,
        quality_index: sys.quality_index,
        workforce_trust: sys.workforce_trust,
        community_trust: sys.community_trust,
        market_share_index: sys.market_share_index,
        resources,
      });

      players.push(PlayerSlot {
        system_id: sys.system_id,
        controller,
      });
    }

    Ok(CompetitiveWorldState {
      difficulty,
      turn: 0,
      market: SharedMarketFields {
        regional_demand_index: market_spec.regional_demand_index,
        commercial_payer_pressure: market_spec.commercial_payer_pressure,
        policy_pressure: market_spec.policy_pressure,
      },
      systems,
      players,
      public_action_log: Vec::new(),
      effect_queue: Vec::new(),
      policy_calendar: PolicyCalendar::new_month(1),
      scenario_id: self.scenario_id.clone(),
      event_metadata: std::collections::HashMap::new(),
    })
  }
}

pub fn parse_scenario_toml(input: &str) -> Result<Scenario, ScenarioError> {
  toml::from_str(input).map_err(|error| ScenarioError::Parse(error.to_string()))
}

pub fn load_scenario_file(path: impl AsRef<Path>) -> Result<Scenario, ScenarioError> {
  let contents = fs::read_to_string(path).map_err(|error| ScenarioError::Io(error.to_string()))?;
  parse_scenario_toml(&contents)
}

pub fn default_stabilization_scenario() -> Result<Scenario, ScenarioError> {
  let scenario = parse_scenario_toml(STABILIZATION_SCENARIO_TOML)?;
  validate_stabilization_scenario(&scenario, &crate::model::default_ruleset())?;
  Ok(scenario)
}

pub fn validate_stabilization_scenario(
  scenario: &Scenario,
  ruleset: &Ruleset,
) -> Result<(), ScenarioError> {
  if scenario.format_version != SCENARIO_TOML_FORMAT_VERSION {
    return Err(ScenarioError::UnsupportedFormatVersion(
      scenario.format_version.clone(),
    ));
  }
  if scenario.campaign_id != "stabilization-v1" {
    return Err(ScenarioError::UnsupportedCampaign(
      scenario.campaign_id.clone(),
    ));
  }
  if scenario.turn_unit != "abstract" {
    return Err(ScenarioError::UnsupportedTurnUnit(
      scenario.turn_unit.clone(),
    ));
  }
  if scenario.ruleset_id != ruleset.version {
    return Err(ScenarioError::RulesetMismatch {
      expected: ruleset.version.to_string(),
      actual: scenario.ruleset_id.clone(),
    });
  }
  let initial = scenario.initial_state.as_ref().ok_or_else(|| {
    ScenarioError::Parse("missing initial_state in stabilization scenario".to_string())
  })?;
  if initial.turn != 0 {
    return Err(ScenarioError::InvalidInitialTurn(initial.turn));
  }
  if scenario.learning_objectives.is_empty() {
    return Err(ScenarioError::EmptyLearningObjectives);
  }

  let schedule = scenario.turn_schedule.as_ref().ok_or_else(|| {
    ScenarioError::Parse("missing turn_schedule in stabilization scenario".to_string())
  })?;
  validate_turn_schedule(schedule)?;

  let stubs = scenario.actor_stubs.as_ref().ok_or_else(|| {
    ScenarioError::Parse("missing actor_stubs in stabilization scenario".to_string())
  })?;
  validate_actor_stubs(stubs, schedule)?;

  Ok(())
}

pub fn validate_competitive_scenario(
  scenario: &Scenario,
  ruleset: &CompetitiveRuleset,
) -> Result<(), ScenarioError> {
  if scenario.format_version != SCENARIO_TOML_FORMAT_VERSION {
    return Err(ScenarioError::UnsupportedFormatVersion(
      scenario.format_version.clone(),
    ));
  }
  if scenario.campaign_id != "competitive-regional-v1" {
    return Err(ScenarioError::UnsupportedCampaign(
      scenario.campaign_id.clone(),
    ));
  }
  if scenario.turn_unit != "month" {
    return Err(ScenarioError::UnsupportedTurnUnit(
      scenario.turn_unit.clone(),
    ));
  }
  if scenario.ruleset_id != ruleset.version {
    return Err(ScenarioError::RulesetMismatch {
      expected: ruleset.version.to_string(),
      actual: scenario.ruleset_id.clone(),
    });
  }
  if scenario.learning_objectives.is_empty() {
    return Err(ScenarioError::EmptyLearningObjectives);
  }

  let _ = scenario.initial_market.as_ref().ok_or_else(|| {
    ScenarioError::InvalidSystem("missing initial_market in competitive scenario".to_string())
  })?;

  let systems = scenario
    .systems
    .as_ref()
    .ok_or_else(|| ScenarioError::Parse("missing systems in competitive scenario".to_string()))?;

  if systems.is_empty() {
    return Err(ScenarioError::InvalidSystem(
      "scenario systems list cannot be empty".to_string(),
    ));
  }

  let mut system_ids: Vec<u32> = systems.iter().map(|sys| sys.system_id).collect();
  system_ids.sort_unstable();
  let expected_ids: Vec<u32> = (0..systems.len() as u32).collect();
  if system_ids != expected_ids {
    return Err(ScenarioError::InvalidSystem(format!(
      "system IDs must be unique, sequential, and start at 0 (expected {:?}, got {:?})",
      expected_ids, system_ids
    )));
  }

  let mut human_count = 0;
  for sys in systems {
    match sys.controller.to_ascii_lowercase().as_str() {
      "human" => human_count += 1,
      "ai" => {
        let style_str = sys.ai_style.as_ref().ok_or_else(|| {
          ScenarioError::InvalidSystem(format!("AI system '{}' must define ai_style", sys.name))
        })?;
        match style_str.to_ascii_lowercase().as_str() {
          "growth" | "margin" | "access" | "political" => {}
          other => {
            return Err(ScenarioError::InvalidSystem(format!(
              "AI system '{}' has invalid ai_style '{}'",
              sys.name, other
            )));
          }
        }
      }
      other => {
        return Err(ScenarioError::InvalidSystem(format!(
          "system '{}' has invalid controller '{}'",
          sys.name, other
        )));
      }
    }
  }

  if human_count != 1 {
    return Err(ScenarioError::InvalidSystem(format!(
      "competitive scenario must have exactly one human player, found {human_count}"
    )));
  }

  Ok(())
}

fn validate_turn_schedule(schedule: &[TurnScheduleEntry]) -> Result<(), ScenarioError> {
  const EXPECTED_COMMANDS: [&str; 5] = [
    "StabilizeAccess",
    "RespondToStateAccessMandate",
    "RespondToWorkforcePressure",
    "JoinRegionalAccessCoalition",
    "RespondToCompetitorCapacityMove",
  ];

  if schedule.len() != INTERACTIVE_TURN_COUNT as usize {
    return Err(ScenarioError::InvalidTurnSchedule(format!(
      "expected {INTERACTIVE_TURN_COUNT} turns, got {}",
      schedule.len()
    )));
  }

  for (index, entry) in schedule.iter().enumerate() {
    let expected_turn = (index + 1) as u32;
    if entry.turn != expected_turn {
      return Err(ScenarioError::InvalidTurnSchedule(format!(
        "expected turn {expected_turn}, got {}",
        entry.turn
      )));
    }
    let expected_command = EXPECTED_COMMANDS[index];
    if entry.command_kind != expected_command {
      return Err(ScenarioError::InvalidTurnSchedule(format!(
        "turn {expected_turn} must use {expected_command}, got {}",
        entry.command_kind
      )));
    }
    if entry.briefing_context.trim().is_empty() {
      return Err(ScenarioError::InvalidTurnSchedule(format!(
        "turn {expected_turn} has an empty briefing context"
      )));
    }
    if entry.actor_stub.trim().is_empty() {
      return Err(ScenarioError::InvalidTurnSchedule(format!(
        "turn {expected_turn} has an empty actor stub"
      )));
    }
  }

  Ok(())
}

fn validate_actor_stubs(
  stubs: &[ActorStub],
  schedule: &[TurnScheduleEntry],
) -> Result<(), ScenarioError> {
  let scheduled_stubs = schedule
    .iter()
    .map(|entry| (entry.actor_stub.as_str(), entry.turn))
    .collect::<HashMap<_, _>>();
  let mut seen = HashSet::new();

  for stub in stubs {
    if stub.id.trim().is_empty() {
      return Err(ScenarioError::InvalidActorStub(
        "actor stub id cannot be empty".to_string(),
      ));
    }
    if !seen.insert(stub.id.as_str()) {
      return Err(ScenarioError::InvalidActorStub(format!(
        "duplicate actor stub '{}'",
        stub.id
      )));
    }
    let Some(scheduled_turn) = scheduled_stubs.get(stub.id.as_str()) else {
      return Err(ScenarioError::InvalidActorStub(format!(
        "actor stub '{}' is not used by the turn schedule",
        stub.id
      )));
    };
    if stub.card_ref.trim().is_empty() {
      return Err(ScenarioError::InvalidActorStub(format!(
        "actor stub '{}' has an empty card_ref",
        stub.id
      )));
    }
    if stub.turn == 0 || stub.turn > INTERACTIVE_TURN_COUNT {
      return Err(ScenarioError::InvalidActorStub(format!(
        "actor stub '{}' has out-of-range turn {}",
        stub.id, stub.turn
      )));
    }
    if stub.turn != *scheduled_turn {
      return Err(ScenarioError::InvalidActorStub(format!(
        "actor stub '{}' declares turn {}, but schedule uses turn {}",
        stub.id, stub.turn, scheduled_turn
      )));
    }
  }

  for scheduled_stub in scheduled_stubs.keys() {
    if !seen.contains(scheduled_stub) {
      return Err(ScenarioError::InvalidActorStub(format!(
        "turn schedule references missing actor stub '{scheduled_stub}'"
      )));
    }
  }

  Ok(())
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{default_ruleset, genesis_state};

  #[test]
  fn bundled_stabilization_scenario_parses_and_validates() {
    let ruleset = default_ruleset();
    let scenario = parse_scenario_toml(STABILIZATION_SCENARIO_TOML).expect("scenario");

    validate_stabilization_scenario(&scenario, &ruleset).expect("valid scenario");

    assert_eq!(scenario.format_version, SCENARIO_TOML_FORMAT_VERSION);
    assert_eq!(scenario.campaign_id, "stabilization-v1");
    assert_eq!(scenario.default_seed, 42);
    assert_eq!(scenario.initial_world_state(), genesis_state());
  }

  #[test]
  fn bundled_turn_schedule_matches_current_stabilization_sequence() {
    let scenario = default_stabilization_scenario().expect("scenario");
    let commands = scenario
      .turn_schedule
      .as_ref()
      .unwrap()
      .iter()
      .map(|entry| entry.command_kind.as_str())
      .collect::<Vec<_>>();

    assert_eq!(
      commands,
      vec![
        "StabilizeAccess",
        "RespondToStateAccessMandate",
        "RespondToWorkforcePressure",
        "JoinRegionalAccessCoalition",
        "RespondToCompetitorCapacityMove",
      ]
    );
  }

  #[test]
  fn ruleset_mismatch_is_rejected() {
    let mut scenario = default_stabilization_scenario().expect("scenario");
    scenario.ruleset_id = "other-ruleset".to_string();

    assert_eq!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::RulesetMismatch {
        expected: "demo-ruleset-0.1.9".to_string(),
        actual: "other-ruleset".to_string(),
      })
    );
  }

  #[test]
  fn unsupported_campaign_is_rejected() {
    let mut scenario = default_stabilization_scenario().expect("scenario");
    scenario.campaign_id = "competitive-regional-v1".to_string();

    assert_eq!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::UnsupportedCampaign(
        "competitive-regional-v1".to_string()
      ))
    );
  }

  #[test]
  fn unsupported_turn_unit_is_rejected() {
    let mut scenario = default_stabilization_scenario().expect("scenario");
    scenario.turn_unit = "month".to_string();

    assert_eq!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::UnsupportedTurnUnit("month".to_string()))
    );
  }

  #[test]
  fn malformed_required_field_is_rejected() {
    let input = STABILIZATION_SCENARIO_TOML.replace("default_seed = 42", "default_seed = \"bad\"");

    assert!(matches!(
      parse_scenario_toml(&input),
      Err(ScenarioError::Parse(_))
    ));
  }

  #[test]
  fn missing_actor_stub_is_rejected() {
    let mut scenario = default_stabilization_scenario().expect("scenario");
    scenario.actor_stubs.as_mut().unwrap().pop();

    assert!(matches!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::InvalidActorStub(_))
    ));
  }

  #[test]
  fn actor_stub_turn_mismatch_is_rejected() {
    let mut scenario = default_stabilization_scenario().expect("scenario");
    scenario.actor_stubs.as_mut().unwrap()[0].turn = 5;

    assert!(matches!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::InvalidActorStub(_))
    ));
  }
}
