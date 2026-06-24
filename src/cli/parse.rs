use crate::model::{CliError, PlayerCommand};

use super::strategy::default_interactive_commands;

pub fn parse_stabilize_access_command(input: &str) -> Result<PlayerCommand, CliError> {
  let trimmed = input.trim();

  if trimmed.is_empty() {
    return Ok(default_interactive_commands()[0].clone());
  }

  let parts: Vec<&str> = trimmed.split_whitespace().collect();
  if parts.len() != 3 {
    return Err(CliError::InvalidCommandInput(
      "turn 1 expects three integers: staffed_beds capital_spend requested_rate".to_string(),
    ));
  }

  let add_staffed_beds = parts[0]
    .parse::<i32>()
    .map_err(|_| CliError::InvalidCommandInput(format!("invalid staffed beds '{0}'", parts[0])))?;
  let capital_spend = parts[1]
    .parse::<i32>()
    .map_err(|_| CliError::InvalidCommandInput(format!("invalid capital spend '{0}'", parts[1])))?;
  let requested_commercial_rate = parts[2].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid requested commercial rate '{}'", parts[2]))
  })?;

  Ok(PlayerCommand::StabilizeAccess {
    add_staffed_beds,
    capital_spend,
    requested_commercial_rate,
  })
}

pub fn parse_policy_command(input: &str) -> Result<PlayerCommand, CliError> {
  let trimmed = input.trim();

  if trimmed.is_empty() {
    return Ok(default_interactive_commands()[1].clone());
  }

  let parts: Vec<&str> = trimmed.split_whitespace().collect();
  if parts.len() != 2 {
    return Err(CliError::InvalidCommandInput(
      "turn 2 expects two integers: advocacy_spend access_commitment".to_string(),
    ));
  }

  let advocacy_spend = parts[0].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid advocacy spend '{0}'", parts[0]))
  })?;
  let access_commitment = parts[1].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid access commitment '{}'", parts[1]))
  })?;

  Ok(PlayerCommand::RespondToStateAccessMandate {
    advocacy_spend,
    access_commitment,
  })
}

pub fn parse_workforce_command(input: &str) -> Result<PlayerCommand, CliError> {
  let trimmed = input.trim();

  if trimmed.is_empty() {
    return Ok(default_interactive_commands()[2].clone());
  }

  let parts: Vec<&str> = trimmed.split_whitespace().collect();
  if parts.len() != 2 {
    return Err(CliError::InvalidCommandInput(
      "turn 3 expects two integers: retention_spend schedule_relief".to_string(),
    ));
  }

  let retention_spend = parts[0].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid retention spend '{0}'", parts[0]))
  })?;
  let schedule_relief_commitment = parts[1].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid schedule relief '{}'", parts[1]))
  })?;

  Ok(PlayerCommand::RespondToWorkforcePressure {
    retention_spend,
    schedule_relief_commitment,
  })
}

pub fn parse_coalition_command(input: &str) -> Result<PlayerCommand, CliError> {
  let trimmed = input.trim();

  if trimmed.is_empty() {
    return Ok(default_interactive_commands()[3].clone());
  }

  let parts: Vec<&str> = trimmed.split_whitespace().collect();
  if parts.len() != 2 {
    return Err(CliError::InvalidCommandInput(
      "turn 4 expects two integers: coalition_investment shared_access_commitment".to_string(),
    ));
  }

  let coalition_investment = parts[0].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid coalition investment '{}'", parts[0]))
  })?;
  let shared_access_commitment = parts[1].parse::<i32>().map_err(|_| {
    CliError::InvalidCommandInput(format!("invalid shared access commitment '{}'", parts[1]))
  })?;

  Ok(PlayerCommand::JoinRegionalAccessCoalition {
    coalition_investment,
    shared_access_commitment,
  })
}

pub fn describe_command_defaults(command: &PlayerCommand) -> String {
  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate,
    } => {
      format!("Enter for defaults: {add_staffed_beds} {capital_spend} {requested_commercial_rate}")
    }
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => format!("Enter for defaults: {advocacy_spend} {access_commitment}"),
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => format!("Enter for defaults: {retention_spend} {schedule_relief_commitment}"),
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => format!("Enter for defaults: {coalition_investment} {shared_access_commitment}"),
  }
}
