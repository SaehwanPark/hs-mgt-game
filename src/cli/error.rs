use crate::model::CliError;

pub fn describe_cli_error(error: &CliError) -> String {
  match error {
    CliError::InvalidPlayModeChoice(choice) => {
      format!("play mode '{choice}' is not available; use Enter, i, b, 1, 2, or 3")
    }
    CliError::InvalidSeed(seed) => {
      format!("seed '{seed}' is not a valid unsigned integer")
    }
    CliError::InvalidResumeChoice(choice) => {
      format!("resume choice '{choice}' is not available; use r or n")
    }
    CliError::InvalidCampaignChoice(choice) => {
      format!("campaign '{choice}' is not available; use Enter, 1, or 2")
    }
    CliError::InvalidDifficultyChoice(choice) => {
      format!("difficulty '{choice}' is not available; use Enter, 1, 2, 3, or 4")
    }
    CliError::InvalidCommandInput(message) => message.clone(),
    CliError::InvalidStrategyPlan(error) => {
      format!("selected strategy is internally invalid: {error:?}")
    }
    CliError::InvalidInteractiveCommand(error) => {
      format!("command is invalid for this turn: {error:?}")
    }
    CliError::SessionSaveFailed(message) => format!("session save failed: {message}"),
    CliError::InputUnavailable => "could not read input from standard input".to_string(),
  }
}
