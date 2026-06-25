use crate::cli::input::*;
use crate::cli::io::*;
use crate::model::{
  CampaignId, CliError, DEFAULT_SEED, Difficulty, ExperienceMode, PlayMode, StrategyPath,
};

#[test]
fn empty_campaign_choice_defaults_to_stabilization() {
  assert_eq!(
    parse_campaign_choice("").unwrap(),
    CampaignId::StabilizationV1
  );
}

#[test]
fn competitive_campaign_alias_is_parsed() {
  assert_eq!(
    parse_campaign_choice("c").unwrap(),
    CampaignId::CompetitiveRegionalV1
  );
}

#[test]
fn empty_difficulty_choice_defaults_to_normal() {
  assert_eq!(parse_difficulty_choice("").unwrap(), Difficulty::Normal);
}

#[test]
fn numbered_difficulty_choices_are_parsed() {
  assert_eq!(parse_difficulty_choice("1").unwrap(), Difficulty::Easy);
  assert_eq!(parse_difficulty_choice("4").unwrap(), Difficulty::Expert);
}

#[test]
fn empty_play_mode_choice_defaults_to_interactive_standard() {
  let selection = parse_play_mode_choice("\n").unwrap();
  assert_eq!(selection.play_mode, PlayMode::Interactive);
  assert_eq!(selection.experience_mode, ExperienceMode::Standard);
}

#[test]
fn interactive_play_mode_alias_is_parsed() {
  let selection = parse_play_mode_choice("i\n").unwrap();
  assert_eq!(selection.play_mode, PlayMode::Interactive);
  assert_eq!(selection.experience_mode, ExperienceMode::Standard);
}

#[test]
fn beginner_play_mode_alias_is_parsed() {
  let selection = parse_play_mode_choice("b\n").unwrap();
  assert_eq!(selection.play_mode, PlayMode::Interactive);
  assert_eq!(selection.experience_mode, ExperienceMode::Beginner);
}

#[test]
fn numbered_play_mode_choices_select_preset_paths() {
  let one = parse_play_mode_choice("1\n").unwrap();
  assert_eq!(
    one.play_mode,
    PlayMode::Preset(StrategyPath::AccessStabilization)
  );

  let two = parse_play_mode_choice("2\n").unwrap();
  assert_eq!(two.play_mode, PlayMode::Preset(StrategyPath::FiscalCaution));

  let three = parse_play_mode_choice("3\n").unwrap();
  assert_eq!(
    three.play_mode,
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
fn global_quit_is_recognized() {
  assert_eq!(parse_global_input("quit\n"), GlobalInput::Quit);
  assert_eq!(parse_global_input("exit\n"), GlobalInput::Quit);
}

#[test]
fn global_help_is_recognized() {
  assert_eq!(parse_global_input("help\n"), GlobalInput::Help);
  assert_eq!(parse_global_input("?\n"), GlobalInput::Help);
}

#[test]
fn resume_choice_parses() {
  assert!(parse_resume_choice("r\n").unwrap());
  assert!(!parse_resume_choice("n\n").unwrap());
  assert_eq!(
    parse_resume_choice("x\n"),
    Err(CliError::InvalidResumeChoice("x".to_string()))
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

#[test]
fn replay_export_empty_skips() {
  assert_eq!(parse_replay_export_path("\n"), None);
  assert_eq!(
    parse_replay_export_path("artifact.txt\n"),
    Some("artifact.txt".to_string())
  );
}
