use hs_mgt_game::model::default_ruleset;
use hs_mgt_game::scenario::{load_scenario_file, validate_stabilization_scenario};
use std::fs;

#[test]
fn test_load_non_existent_file() {
  let res = load_scenario_file("this_file_does_not_exist_at_all.toml");
  assert!(res.is_err());
}

#[test]
fn test_load_malformed_toml() {
  let temp_path = "temp_malformed_test.toml";
  fs::write(temp_path, "not_valid_toml = [").unwrap();
  let res = load_scenario_file(temp_path);
  let _ = fs::remove_file(temp_path);
  assert!(res.is_err());
}

#[test]
fn test_load_valid_scenario() {
  let temp_path = "temp_valid_test.toml";
  let content = fs::read_to_string("scenarios/stabilization-v1.toml").expect("read bundled file");
  fs::write(temp_path, content).unwrap();
  let res = load_scenario_file(temp_path);
  let _ = fs::remove_file(temp_path);
  assert!(res.is_ok());

  let scenario = res.unwrap();
  assert_eq!(scenario.campaign_id, "stabilization-v1");
  let ruleset = default_ruleset();
  assert!(validate_stabilization_scenario(&scenario, &ruleset).is_ok());
}
