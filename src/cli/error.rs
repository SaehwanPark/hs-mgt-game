use crate::model::CliError;

pub fn describe_cli_error(error: &CliError) -> String {
  match error {
    CliError::InvalidPlayModeChoice(choice) => {
      format!("play mode '{choice}' is not available; use Enter, i, 1, 2, or 3")
    }
    CliError::InvalidSeed(seed) => {
      format!("seed '{seed}' is not a valid unsigned integer")
    }
    CliError::InvalidCommandInput(message) => message.clone(),
    CliError::InvalidStrategyPlan(error) => {
      format!("selected strategy is internally invalid: {error:?}")
    }
    CliError::InvalidInteractiveCommand(error) => {
      format!("command is invalid for this turn: {error:?}")
    }
    CliError::InputUnavailable => "could not read input from standard input".to_string(),
  }
}
