use std::io;

use crate::model::CliError;

use super::display::{
  PromptContext, global_commands_footer, print_prompt_block, replay_export_prompt_lines,
};

pub fn read_replay_export_path() -> Result<Option<String>, CliError> {
  let mut lines = replay_export_prompt_lines();
  lines.extend(global_commands_footer(PromptContext::ReplayExport));
  print_prompt_block(&lines);

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
