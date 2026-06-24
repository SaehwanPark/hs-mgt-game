use crate::artifact::{
  REPLAY_ARTIFACT_VERSION, deserialize_replay_artifact, serialize_replay_artifact,
  verify_replay_artifact,
};
use crate::cli::{
  build_history_for_strategy, build_history_interactive, default_interactive_commands,
};
use crate::model::*;
use crate::test_support::sample_replay_artifact;

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
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
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
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
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
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
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
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
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
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();
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
