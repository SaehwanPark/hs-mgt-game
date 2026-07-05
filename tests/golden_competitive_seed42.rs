use hs_mgt_game::competitive::build_month1_resolution_history;
use hs_mgt_game::model::Difficulty;

#[test]
fn competitive_seed42_month1_preset_resolution_is_stable() {
  let history = build_month1_resolution_history(Difficulty::Normal, 42).expect("resolve month 1");
  assert_eq!(history.transitions.len(), 1);

  let transition = &history.transitions[0];
  assert_eq!(transition.prior.turn, 0);
  assert_eq!(transition.next.turn, 1);
  assert_eq!(transition.next.policy_calendar.month_index, 2);
  assert_eq!(
    transition
      .next
      .public_action_log
      .iter()
      .filter(|entry| entry.month_index == 1)
      .count(),
    1
  );
  assert!(
    transition
      .aggregated
      .batches
      .iter()
      .filter(|batch| batch.rationale.is_some())
      .count()
      == 2
  );
  // v3 schema (added obs= field + version string bump, 2026-07-05)
  assert_eq!(transition.state_hash, "e57cc6377e17ea09");
}

#[test]
fn generate_mock_replay_fixture() {
  use hs_mgt_game::competitive::build_multi_month_resolution_history;
  use std::fs;
  use std::path::Path;

  let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 24)
    .expect("build multi month history");

  let json = serde_json::to_string_pretty(&history).expect("serialize history");

  let dir = Path::new("tests/fixtures");
  if !dir.exists() {
    fs::create_dir_all(dir).expect("create fixtures dir");
  }
  fs::write(dir.join("mock_replay.json"), json).expect("write mock replay file");
}
