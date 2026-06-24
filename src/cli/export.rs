use std::io;

use crate::model::CliError;

pub fn read_replay_export_path() -> Result<Option<String>, CliError> {
  println!("Export replay artifact? Enter path (or Enter to skip):");

  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;

  let trimmed = input.trim();
  if trimmed.is_empty() {
    return Ok(None);
  }

  Ok(Some(trimmed.to_string()))
}
