use std::collections::{HashMap, HashSet};
use std::fmt;
use std::fs;
use std::path::Path;

use serde::Deserialize;

use crate::model::{INTERACTIVE_TURN_COUNT, Ruleset, WorldState};

pub const SCENARIO_TOML_FORMAT_VERSION: &str = "scenario-toml-0.1.40";
pub const STABILIZATION_SCENARIO_TOML: &str = include_str!("../../scenarios/stabilization-v1.toml");

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
  pub initial_state: ScenarioInitialState,
  pub turn_schedule: Vec<TurnScheduleEntry>,
  pub actor_stubs: Vec<ActorStub>,
  pub evaluation_profile: Option<EvaluationProfile>,
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
    self.initial_state.to_world_state()
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
  if scenario.initial_state.turn != 0 {
    return Err(ScenarioError::InvalidInitialTurn(
      scenario.initial_state.turn,
    ));
  }
  if scenario.learning_objectives.is_empty() {
    return Err(ScenarioError::EmptyLearningObjectives);
  }

  validate_turn_schedule(&scenario.turn_schedule)?;
  validate_actor_stubs(&scenario.actor_stubs, &scenario.turn_schedule)?;

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
    scenario.actor_stubs.pop();

    assert!(matches!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::InvalidActorStub(_))
    ));
  }

  #[test]
  fn actor_stub_turn_mismatch_is_rejected() {
    let mut scenario = default_stabilization_scenario().expect("scenario");
    scenario.actor_stubs[0].turn = 5;

    assert!(matches!(
      validate_stabilization_scenario(&scenario, &default_ruleset()),
      Err(ScenarioError::InvalidActorStub(_))
    ));
  }
}
