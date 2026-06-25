use std::io;

use crate::model::{
  CampaignId, CliError, DEFAULT_SEED, Difficulty, ExperienceMode, PlayMode, StrategyPath,
};

use super::display::{
  PromptContext, campaign_menu_lines, difficulty_menu_lines, global_commands_footer,
  play_mode_menu_lines, print_prompt_block, resume_choice_prompt_lines, seed_prompt_lines, style,
};
use super::guidance::print_context_help;
use super::input::{GlobalInput, ReadLineOutcome, parse_global_input};

pub fn read_line_with_globals(
  prompt_lines: &[String],
  context: PromptContext,
) -> Result<ReadLineOutcome, CliError> {
  loop {
    print_prompt_block(prompt_lines);

    let mut input = String::new();
    io::stdin()
      .read_line(&mut input)
      .map_err(|_| CliError::InputUnavailable)?;

    match parse_global_input(&input) {
      GlobalInput::Quit => return Ok(ReadLineOutcome::Quit),
      GlobalInput::Help => {
        print_context_help(context);
        continue;
      }
      GlobalInput::Payload(payload) => return Ok(ReadLineOutcome::Payload(payload)),
    }
  }
}

pub fn read_resume_choice() -> Result<ReadLineOutcome, CliError> {
  let mut lines = resume_choice_prompt_lines();
  lines.extend(global_commands_footer(PromptContext::ResumeChoice));
  read_line_with_globals(&lines, PromptContext::ResumeChoice)
}

pub fn parse_resume_choice(input: &str) -> Result<bool, CliError> {
  let trimmed = input.trim();
  match trimmed {
    "r" | "R" => Ok(true),
    "n" | "N" => Ok(false),
    other => Err(CliError::InvalidResumeChoice(other.to_string())),
  }
}

pub fn read_campaign_choice() -> Result<ReadLineOutcome, CliError> {
  let mut lines = campaign_menu_lines();
  lines.extend(global_commands_footer(PromptContext::Campaign));
  read_line_with_globals(&lines, PromptContext::Campaign)
}

pub fn parse_campaign_choice(input: &str) -> Result<CampaignId, CliError> {
  let trimmed = input.trim();
  match trimmed {
    "" | "1" => Ok(CampaignId::StabilizationV1),
    "2" | "c" | "C" => Ok(CampaignId::CompetitiveRegionalV1),
    other => Err(CliError::InvalidCampaignChoice(other.to_string())),
  }
}

pub fn read_difficulty_choice() -> Result<ReadLineOutcome, CliError> {
  let mut lines = difficulty_menu_lines();
  lines.extend(global_commands_footer(PromptContext::Difficulty));
  read_line_with_globals(&lines, PromptContext::Difficulty)
}

pub fn parse_difficulty_choice(input: &str) -> Result<Difficulty, CliError> {
  let trimmed = input.trim();
  match trimmed {
    "" | "2" => Ok(Difficulty::Normal),
    "1" => Ok(Difficulty::Easy),
    "3" => Ok(Difficulty::Hard),
    "4" => Ok(Difficulty::Expert),
    other => Err(CliError::InvalidDifficultyChoice(other.to_string())),
  }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PlayModeSelection {
  pub play_mode: PlayMode,
  pub experience_mode: ExperienceMode,
}

pub fn read_play_mode_choice() -> Result<ReadLineOutcome, CliError> {
  let mut lines = play_mode_menu_lines();
  lines.extend(global_commands_footer(PromptContext::PlayMode));
  read_line_with_globals(&lines, PromptContext::PlayMode)
}

pub fn parse_play_mode_choice(input: &str) -> Result<PlayModeSelection, CliError> {
  let trimmed = input.trim();

  match trimmed {
    "" | "i" | "I" => Ok(PlayModeSelection {
      play_mode: PlayMode::Interactive,
      experience_mode: ExperienceMode::Standard,
    }),
    "b" | "B" => Ok(PlayModeSelection {
      play_mode: PlayMode::Interactive,
      experience_mode: ExperienceMode::Beginner,
    }),
    "1" => Ok(PlayModeSelection {
      play_mode: PlayMode::Preset(StrategyPath::AccessStabilization),
      experience_mode: ExperienceMode::Standard,
    }),
    "2" => Ok(PlayModeSelection {
      play_mode: PlayMode::Preset(StrategyPath::FiscalCaution),
      experience_mode: ExperienceMode::Standard,
    }),
    "3" => Ok(PlayModeSelection {
      play_mode: PlayMode::Preset(StrategyPath::AggressiveBargaining),
      experience_mode: ExperienceMode::Standard,
    }),
    other => Err(CliError::InvalidPlayModeChoice(other.to_string())),
  }
}

pub fn read_seed_choice() -> Result<ReadLineOutcome, CliError> {
  let mut lines = seed_prompt_lines();
  lines.extend(global_commands_footer(PromptContext::Seed));
  read_line_with_globals(&lines, PromptContext::Seed)
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

pub fn read_command_line(prompt: &str, turn: u32) -> Result<ReadLineOutcome, CliError> {
  loop {
    super::display::print_line(prompt);
    super::display::print_line("");

    let mut input = String::new();
    io::stdin()
      .read_line(&mut input)
      .map_err(|_| CliError::InputUnavailable)?;

    match parse_global_input(&input) {
      GlobalInput::Quit => return Ok(ReadLineOutcome::Quit),
      GlobalInput::Help => {
        print_context_help(PromptContext::TurnCommand { turn });
        continue;
      }
      GlobalInput::Payload(payload) => return Ok(ReadLineOutcome::Payload(payload)),
    }
  }
}

pub fn read_beginner_choice(menu_lines: &[String], turn: u32) -> Result<ReadLineOutcome, CliError> {
  let mut lines = menu_lines.to_vec();
  lines.extend(global_commands_footer(PromptContext::BeginnerTurn { turn }));
  read_line_with_globals(&lines, PromptContext::BeginnerTurn { turn })
}

pub fn read_replay_export_path() -> Result<ReadLineOutcome, CliError> {
  let mut lines = super::display::replay_export_prompt_lines();
  lines.extend(global_commands_footer(PromptContext::ReplayExport));
  read_line_with_globals(&lines, PromptContext::ReplayExport)
}

pub fn read_validation_demo_choice() -> Result<ReadLineOutcome, CliError> {
  let lines = vec![style::subsection("Validation demo choice")];
  read_line_with_globals(&lines, PromptContext::ValidationDemo)
}

pub fn read_competitive_command_batch() -> Result<ReadLineOutcome, CliError> {
  let lines = vec![style::subsection("Competitive command batch")];
  read_line_with_globals(&lines, PromptContext::CompetitiveCommand)
}

pub fn parse_replay_export_path(input: &str) -> Option<String> {
  let trimmed = input.trim();
  if trimmed.is_empty() {
    None
  } else {
    Some(trimmed.to_string())
  }
}
