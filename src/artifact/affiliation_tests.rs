use super::{
  deserialize_affiliation_replay, serialize_affiliation_replay, verify_affiliation_replay,
};
use crate::affiliation::resolve_affiliation_turn;
use crate::model::{
  AFFILIATION_REPLAY_ARTIFACT_VERSION, AffiliationCommand, AffiliationHistory, AffiliationPosture,
  AffiliationReplayArtifact, default_affiliation_ruleset,
};
use crate::scenario::default_regional_affiliation_scenario;

fn sample_history() -> AffiliationHistory {
  let ruleset = default_affiliation_ruleset();
  let mut current = default_regional_affiliation_scenario()
    .unwrap()
    .initial_affiliation_world_state()
    .unwrap();
  let genesis = current.clone();
  let commands = [
    AffiliationCommand::AssessPartner,
    AffiliationCommand::ChoosePosture {
      posture: AffiliationPosture::Independent,
    },
    AffiliationCommand::Hold,
    AffiliationCommand::Hold,
    AffiliationCommand::Hold,
    AffiliationCommand::Hold,
  ];
  let mut transitions = Vec::new();
  for command in commands {
    let transition = resolve_affiliation_turn(&current, command, 42, &ruleset).unwrap();
    current = transition.next.clone();
    transitions.push(transition);
  }
  AffiliationHistory {
    genesis,
    transitions,
  }
}

#[test]
fn affiliation_replay_round_trip_verifies() {
  let ruleset = default_affiliation_ruleset();
  let artifact = AffiliationReplayArtifact {
    artifact_version: AFFILIATION_REPLAY_ARTIFACT_VERSION.to_string(),
    seed: 42,
    ruleset_version: ruleset.version.clone(),
    history: sample_history(),
  };
  let serialized = serialize_affiliation_replay(&artifact);
  assert_eq!(
    deserialize_affiliation_replay(&serialized).unwrap(),
    artifact
  );
  assert!(verify_affiliation_replay(&serialized, &ruleset).is_ok());
}

#[test]
fn affiliation_replay_detects_hash_tampering() {
  let ruleset = default_affiliation_ruleset();
  let artifact = AffiliationReplayArtifact {
    artifact_version: AFFILIATION_REPLAY_ARTIFACT_VERSION.to_string(),
    seed: 42,
    ruleset_version: ruleset.version.clone(),
    history: sample_history(),
  };
  let mut value = serde_json::to_value(artifact).unwrap();
  value["history"]["transitions"][0]["state_hash"] =
    serde_json::Value::String("tampered".to_string());
  let serialized = serde_json::to_string(&value).unwrap();
  assert!(verify_affiliation_replay(&serialized, &ruleset).is_err());
}

#[test]
fn affiliation_replay_detects_observation_tampering() {
  let history = sample_history();
  let artifact = AffiliationReplayArtifact {
    artifact_version: AFFILIATION_REPLAY_ARTIFACT_VERSION.to_string(),
    seed: 42,
    ruleset_version: default_affiliation_ruleset().version.clone(),
    history,
  };
  let mut value: serde_json::Value =
    serde_json::from_str(&serialize_affiliation_replay(&artifact)).unwrap();
  value["history"]["transitions"][0]["observation"]["cash"] = serde_json::json!(999);
  let text = serde_json::to_string(&value).unwrap();
  assert!(verify_affiliation_replay(&text, &default_affiliation_ruleset()).is_err());
}
