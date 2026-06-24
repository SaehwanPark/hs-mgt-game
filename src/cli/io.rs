use std::io;

use crate::model::{CliError, DEFAULT_SEED, PlayMode, StrategyPath};

pub fn read_play_mode_choice() -> Result<PlayMode, CliError> {
  println!("Choose play mode:");
  println!("  Enter or i. Interactive (enter each turn's command)");
  println!("  1. Preset path: Access stabilization");
  println!("  2. Preset path: Fiscal caution");
  println!("  3. Preset path: Aggressive bargaining");

  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;
  parse_play_mode_choice(&input)
}

pub fn parse_play_mode_choice(input: &str) -> Result<PlayMode, CliError> {
  let trimmed = input.trim();

  match trimmed {
    "" | "i" | "I" => Ok(PlayMode::Interactive),
    "1" => Ok(PlayMode::Preset(StrategyPath::AccessStabilization)),
    "2" => Ok(PlayMode::Preset(StrategyPath::FiscalCaution)),
    "3" => Ok(PlayMode::Preset(StrategyPath::AggressiveBargaining)),
    other => Err(CliError::InvalidPlayModeChoice(other.to_string())),
  }
}

pub fn read_seed_choice() -> Result<u64, CliError> {
  println!("Seed (Enter for default {DEFAULT_SEED}):");

  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;
  parse_seed_choice(&input)
}

pub fn parse_seed_choice(input: &str) -> Result<u64, CliError> {
  let trimmed = input.trim();

  if trimmed.is_empty() {
    return Ok(DEFAULT_SEED);
  }

  trimmed
    .parse::<u64>()
    .map_err(|_| CliError::InvalidSeed(trimmed.to_string()))
}
pub fn read_command_line(prompt: &str) -> Result<String, CliError> {
  println!("{prompt}");
  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;
  Ok(input)
}
