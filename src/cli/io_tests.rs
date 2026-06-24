use crate::cli::io::*;
use crate::model::{CliError, DEFAULT_SEED, PlayMode, StrategyPath};

#[test]
fn empty_play_mode_choice_defaults_to_interactive() {
  assert_eq!(parse_play_mode_choice("\n").unwrap(), PlayMode::Interactive);
}
#[test]
fn interactive_play_mode_alias_is_parsed() {
  assert_eq!(
    parse_play_mode_choice("i\n").unwrap(),
    PlayMode::Interactive
  );
}
#[test]
fn numbered_play_mode_choices_select_preset_paths() {
  assert_eq!(
    parse_play_mode_choice("1\n").unwrap(),
    PlayMode::Preset(StrategyPath::AccessStabilization)
  );
  assert_eq!(
    parse_play_mode_choice("2\n").unwrap(),
    PlayMode::Preset(StrategyPath::FiscalCaution)
  );
  assert_eq!(
    parse_play_mode_choice("3\n").unwrap(),
    PlayMode::Preset(StrategyPath::AggressiveBargaining)
  );
}
#[test]
fn invalid_play_mode_choice_is_error() {
  assert_eq!(
    parse_play_mode_choice("9\n"),
    Err(CliError::InvalidPlayModeChoice("9".to_string()))
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
