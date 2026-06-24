use super::{PlayerCommand, ValidationError};

pub const DEFAULT_SEED: u64 = 42;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PlayMode {
  Interactive,
  Preset(StrategyPath),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum StrategyPath {
  AccessStabilization,
  FiscalCaution,
  AggressiveBargaining,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct StrategyPlan {
  pub name: &'static str,
  pub first_command: PlayerCommand,
  pub second_command: PlayerCommand,
  pub third_command: PlayerCommand,
  pub fourth_command: PlayerCommand,
  pub fifth_command: PlayerCommand,
}

pub struct StrategyCommitments {
  pub staffed_beds: i32,
  pub capital_spend: i32,
  pub requested_commercial_rate: i32,
  pub advocacy_spend: i32,
  pub access_commitment: i32,
  pub retention_spend: i32,
  pub schedule_relief_commitment: i32,
  pub coalition_investment: i32,
  pub shared_access_commitment: i32,
  pub defensive_capital_commitment: i32,
  pub access_posture: i32,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct RunConfig {
  pub seed: u64,
  pub play_mode: PlayMode,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CliError {
  InvalidPlayModeChoice(String),
  InvalidSeed(String),
  InvalidCommandInput(String),
  InvalidStrategyPlan(ValidationError),
  InvalidInteractiveCommand(ValidationError),
  InputUnavailable,
}
